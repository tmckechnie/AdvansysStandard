#===============================================queryStatus===============================================
def queryStatus(priority = [1,2,3,4], state = [0,1,2,3], path = "", source = "", displaypath="", all_properties=[], any_properties=[], defined=[], includeShelved = False):

	alarmQueryResult = system.alarm.queryStatus(priority,state,path,source,displaypath,all_properties,any_properties,defined,includeShelved)
	return alarmQueryResult

#===============================================GetAlarmSummary===============================================
def GetAlarmSummary(DisplayPath,Trigger):
	#print "Create Logger: AlarmScripts"
	#logger = system.util.getLogger("AlarmScripts")
	#logger.info("GetAlarmSummary For: " + DisplayPath)
	alarmQueryResult = queryStatus(displaypath = DisplayPath,state = [0,2,3],includeShelved = True)
	#print "alarmQueryResult:" + str(alarmQueryResult)
	#Alarm Summary Initialisation
	#Get Default PriorityAlarmSummaryObject
	def getPriorityAlarmSummaryObject():
		PriorityAlarmSummaryObject = {
		
		"Total":0,
		"ActiveAckCount":0,
		"ActiveUnackCount":0,
		"ClearUnackCount":0,
		"ShelvedCount":0,
		"Detail":[]
		}
		
		return PriorityAlarmSummaryObject
	
	alarmSummaryObject = {
		"HighestActivePriority":None,
		"HighestActivePriorityName":None,
		"HighestUnackedPriority":None,
		"HighestUnackedPriorityName":None,
		"Overall":getPriorityAlarmSummaryObject(),
		"PriorityDetail": {
			"Critical":getPriorityAlarmSummaryObject(),
			"High":getPriorityAlarmSummaryObject(),
			"Medium":getPriorityAlarmSummaryObject(),
			"Low":getPriorityAlarmSummaryObject()
		}
	}
	highestActivePriorityInteger = 0
	highestUnackedPriorityInteger = 0
	
	highestActivePriorityString = None
	highestUnackedPriorityString = None	
	
	
	for alarmResultObject in alarmQueryResult:
		priorityObject = alarmResultObject.getPriority()
		stateObject = alarmResultObject.getState()
		#print "priorityObject:" + str(priorityObject)
		#print str(alarmResultObject)
		#Alarm Properties
		priorityInteger = priorityObject.getIntValue() # 0 - Diagnostic, 1 - Low, 2 - Medium , 3 - High, 4 - Critical
		priorityString = priorityObject.toString()
		stateIsActive = stateObject.isActive()
		stateIsAck = stateObject.isAcked()
		stateIsShelved = alarmResultObject.isShelved()
		# Update root level Alarm Summary Variables
		if stateIsActive and priorityInteger > highestActivePriorityInteger:
			highestActivePriorityInteger = priorityInteger
			highestActivePriorityString = priorityString
			
		if stateIsAck == False and priorityInteger > highestUnackedPriorityInteger:
			highestUnackedPriorityInteger = priorityInteger
			highestUnackedPriorityString = priorityString
		
		# Update Priority Detail Object

		if stateIsActive and stateIsAck and (stateIsShelved == False):
			alarmSummaryObject["PriorityDetail"][priorityString]["ActiveAckCount"] += 1
			alarmSummaryObject["PriorityDetail"][priorityString]["Total"] += 1
			alarmSummaryObject["Overall"]["ActiveAckCount"] += 1
			alarmSummaryObject["Overall"]["Total"] += 1

		
		elif stateIsActive and (stateIsAck == False) and (stateIsShelved == False):
			alarmSummaryObject["PriorityDetail"][priorityString]["ActiveUnackCount"] += 1
			alarmSummaryObject["PriorityDetail"][priorityString]["Total"] += 1
			alarmSummaryObject["Overall"]["ActiveUnackCount"] += 1
			alarmSummaryObject["Overall"]["Total"] += 1
		
		elif (stateIsActive == False) and (stateIsAck == False) and (stateIsShelved == False):
			alarmSummaryObject["PriorityDetail"][priorityString]["ClearUnackCount"] += 1
			alarmSummaryObject["PriorityDetail"][priorityString]["Total"] += 1
			alarmSummaryObject["Overall"]["ClearUnackCount"] += 1
			alarmSummaryObject["Overall"]["Total"] += 1
		
		if stateIsShelved:
			alarmSummaryObject["PriorityDetail"][priorityString]["ShelvedCount"] += 1
		
		detail = {}
		detail["EventID"] = alarmResultObject["EventId"]
		detail["Label"] = alarmResultObject.getLabel()
		detail["State"] = stateObject.toString() 
		alarmSummaryObject["PriorityDetail"][priorityString]["Detail"].append(detail)
	
	# Update root level Alarm Summary
	alarmSummaryObject["HighestActivePriority"] = highestActivePriorityInteger
	alarmSummaryObject["HighestActivePriorityName"] = highestActivePriorityString
	alarmSummaryObject["HighestUnackedPriority"] = highestUnackedPriorityInteger
	alarmSummaryObject["HighestUnackedPriorityName"] = highestUnackedPriorityString
	
	alarmSummaryObjectJsonEncoded = system.util.jsonEncode(alarmSummaryObject)
	#Update Parent Model Item Alarm Summary Information	
	#TriggerParentModelItemAlarmSummaryInformation()
	return alarmSummaryObjectJsonEncoded
	
#=================================================================TriggerParentModelItemAlarmSummaryInformation#=================================================================	
def TriggerParentModelItemAlarmSummaryInformation():
	loggerName = "TriggerParentModelItemAlarmSummaryInformation"
	parentModelItemUpdateTriggerPath = "[.]../../../Model Item/Alarm Summary/Update Trigger"
	#[.]../../../Model Item/Alarm Summary/Update Trigger
	
	currentTriggerQualifiedValue = system.tag.readBlocking([parentModelItemUpdateTriggerPath])[0]
	
	#Standard.Utilities.Common.LogMessage(LoggerName=loggerName,Message=message,DebugLevel = 1)
	currentTriggerValue = currentTriggerQualifiedValue.value
	currentTriggerQualityCode = currentTriggerQualifiedValue.quality.getCode()
	
	message = "currentParentTriggerValue: " + str(currentTriggerValue) + " currentParentTriggerQuality: " + str(currentTriggerQualityCode)
		
#	Standard.Utilities.Common.LogMessage(LoggerName=loggerName,Message=message,DebugLevel = 1)

	if currentTriggerQualityCode == -2147483129:#Should be 519 according to documentation
		message = "Parent Not Found"
		#Standard.Utilities.Common.LogMessage(LoggerName=loggerName,Message=message,DebugLevel = 1)
		return message
	
	updateModelItemAlarmTrigger = system.tag.writeBlocking([parentModelItemUpdateTriggerPath],[not currentTriggerValue])
	message = "Parent Found:" + " UpdateModelItemAlarmTrigger: " + str(updateModelItemAlarmTrigger)
	#Standard.Utilities.Common.LogMessage(LoggerName=loggerName,Message=message,DebugLevel = 1)
	return updateModelItemAlarmTrigger	
	
#=================================================================TriggerParentModelItemAlarmSummaryInformation#=================================================================	
def TriggerParentAlarmSummaryInformation(ParentAlarmSummaryTagPath):
	loggerName = "TriggerParentAlarmSummaryInformation"
	#Script to trigger an Alarm Summaries ParentAlarmSummary
	parentModelItemUpdateTriggerPath = ParentAlarmSummaryTagPath
	
	currentTriggerQualifiedValue = system.tag.readBlocking([parentModelItemUpdateTriggerPath])[0]
	currentTriggerValue = currentTriggerQualifiedValue.value
	currentTriggerQualityCode = currentTriggerQualifiedValue.quality.getCode()
	
	message = "currentParentTriggerValue: " + str(currentTriggerValue) + " currentParentTriggerQuality: " + str(currentTriggerQualityCode)
		
#	Standard.Utilities.Common.LogMessage(LoggerName=loggerName,Message=message,DebugLevel = 1)

	if currentTriggerQualityCode == -2147483129:#Should be 519 according to documentation
		message = "Parent Not Found"
#		Standard.Utilities.Common.LogMessage(LoggerName=loggerName,Message=message,DebugLevel = 1)
		return message
	
	updateModelItemAlarmTrigger = system.tag.writeBlocking([parentModelItemUpdateTriggerPath],[not currentTriggerValue])
	message = "Parent Found:" + " UpdateModelItemAlarmTrigger: " + str(updateModelItemAlarmTrigger)
#	Standard.Utilities.Common.LogMessage(LoggerName=loggerName,Message=message,DebugLevel = 1)
	return updateModelItemAlarmTrigger	
	
#=================================================================GetParentAlarmSummaryTagPath=================================================================	
#Function to find ParentAlarmSummaryTagPath
#def GetParentAlarmSummaryTagPath(

