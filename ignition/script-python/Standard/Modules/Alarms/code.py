#=====================================================================AlarmActiveChangeScript=====================================================================
def AlarmActiveChangeScript(State):
	logger = system.util.getLogger("Alarm Active Change Script")
	#If New Event is Active and Unacked then reset SCADA Acknowledge boolean
	isAcked = State.isAcked()
	isActive = State.isActive()	
	if isAcked == False and isActive:
		ackTagPath = "[.]AcknowledgeSCADA"
		#Check if SCADA Ack Tag is already 1
		currentAckValue = system.tag.readBlocking([ackTagPath])[0].value
		if currentAckValue == False:
			return
		else:
			tagwrite = system.tag.writeBlocking([ackTagPath],[False])	
	return
	
#=====================================================================AlarmAcknowledgeChangeScript=====================================================================
def AlarmAcknowledgeChangeScript(State,AckedBy):
	#Standard.Tag.acknowledgeAlarmCmd(ackedBy)
	#Acknowledge SCADA Acknowledge Tag
	logger = system.util.getLogger("Alarm Acknowledge Change Script")
	isAcked = State.isAcked()#alarmEvent["acked"]	
	#logger.info("State: " + str(state) + str(isAcked) + str(ackedBy))
	if isAcked == True and AckedBy is not None:
		#Write to SCADA Ack Tag
		ackTagPath = "[.]../Cmd/Acknowledge"
		tagwrite = system.tag.writeBlocking([ackTagPath],[True])
		#logger.info("TagWrite Response on SCADA Acknowledge: " + str(tagwrite[0]))	
		if tagwrite[0].isGood() == False:
			logger.info("TagWrite Response on SCADA Acknowledge: " + str(tagwrite))
	return
#===============================================GetAlarmStyle===============================================
def GetAlarmStyle(AlarmSummary,ComponentPart = 'Border'):
	style = {}
	classes = ""
	baseStylePath = 'Standard/Alarms'
	highestUnackedPriorityName = AlarmSummary['HighestUnackedPriorityName']
	highestActivePriorityName = AlarmSummary['HighestActivePriorityName']
	
	#No Alarms = Don't return a Style
	if highestUnackedPriorityName is None and highestActivePriorityName is None:
#		style["classes"] = baseStylePath + "/Text"
		style["classes"] = ""
		return style
		
	if highestUnackedPriorityName is not None:	
		alarmCounts = AlarmSummary["PriorityDetail"][highestUnackedPriorityName]
		highestPriorityName = highestUnackedPriorityName
	else:
		alarmCounts = AlarmSummary["PriorityDetail"][highestActivePriorityName]
		highestPriorityName = highestActivePriorityName
		
	overall = AlarmSummary["Overall"]
	
	#Set Base Alarms Styles
	#Only if ComponentPart = Border the apply text
	if  ComponentPart == "Border":
		classes += baseStylePath + "/" + highestPriorityName + "/Text "
	classes += baseStylePath + "/" + highestPriorityName + "/"+ComponentPart+" "
	#Any Unacked Alarms enables Border Animation
	if overall["ActiveUnackCount"]>0 or overall["ClearUnackCount"]>0:
		classes += "Standard/Alarms/"+ComponentPart+"Animation "

	#This Changes the Border Style
	if alarmCounts["ActiveUnackCount"]>0:
		classes += baseStylePath + "/" + highestPriorityName + "/ActiveUnacked/"+ComponentPart
	elif alarmCounts["ActiveAckCount"]>0:
		classes += baseStylePath + "/" + highestPriorityName + "/ActiveAcked/"+ComponentPart
	elif alarmCounts["ClearUnackCount"]>0:
		classes += baseStylePath + "/" + highestPriorityName + "/ClearUnacked/"+ComponentPart

	style["classes"] = classes

	return style