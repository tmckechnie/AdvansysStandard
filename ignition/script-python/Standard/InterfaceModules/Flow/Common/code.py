def GetProjectRoles(username,password,ConnectionTagPath,UsersDetailTagPath,ADRoles = None, UserSource = "CCBAD",summaryObject = None):
	if ADRoles is None:
		ADRoles = GetADRoles(username,password,ConnectionTagPath,UserSource =UserSource,summaryObject = summaryObject)
		if "error" in ADRoles:
			return ADRoles	
		else:
			ADRoles = ADRoles["roles"]
	print ADRoles
	#Get User Role Mapping Document Tag to map AD Roles to equivalent Project Roles Configured
	roles = []
	projectUserRoleMapping = Standard.Model.Common.GetUserRoleMapping(UsersDetailTagPath)
	userADRolesSet = set(ADRoles)
	print userADRolesSet
	for projectRoleKey in projectUserRoleMapping:
		validADRolesSet = set(projectUserRoleMapping[projectRoleKey]["ADRoles"])
		print validADRolesSet
		print len(validADRolesSet)
		commonRolesSet =  validADRolesSet.intersection(userADRolesSet)
		print len(commonRolesSet)
		if len(commonRolesSet) > 0:
			roles.append(projectRoleKey)
	roles = {"roles":roles}		
	return roles
#=============================================================== GetADRoles ===============================================================
def GetADRoles(username,password,ConnectionTagPath,UserSource = "CCBAD",summaryObject = None):
	logger = system.util.getLogger("GetADRoles")	
	
	if summaryObject is None:
		summaryObject = Standard.InterfaceModules.Flow.Common.GetSummaryObject(username = username,line = ConnectionTagPath)
		
	roles = system.security.getUserRoles(username,password,UserSource) #system.user.getUser("CCBAD",userNameFinal).getRoles()#
	if roles is None:
		statusCode = 401
		message = "Exception thrown when getting User Roles."
		detail = {"message":message}
		Standard.InterfaceModules.Flow.Common.ThrownException(Detail= detail)
		#SaveChangesSummary
		# {'error':True,'json':{},'statusCode':statusCode,'message':message}
		summaryObject["error"]["value"] = True
		summaryObject["error"]["label"] = statusCode
		summaryObject["error"]["reason"] = reason
		return {'error':'Roles not Found for Username:' + username,'Valid':False,"SummaryObject":summaryObject}	
		
	logger.info("Current User Roles: " + str(roles))
	return {"roles":roles}	
	
#=============================================================== HasRequiredRole ===============================================================
def HasRequiredRole(userRoles,requiredRoles = []):
	userRolesSet = set(userRoles)
	for requireRole in requiredRoles:
		if requireRole in userRolesSet:
			return True
	return False

#-------------------------------------------------------------------Logmessage-------------------------------------------------------------
def Logmessage(LoggerName,Message,DebugLevel=10):
	logger = system.util.getLogger(LoggerName)
	logger.info(Message)

	return

def LogAudit(summaryObject,username,auditProfile = "SaveChangesSummary",summaryLogger = True):	
	summaryObjectJsonString = system.util.jsonEncode(summaryObject)
	system.util.audit(actionValue =  summaryObjectJsonString, auditProfile = auditProfile ,actor = username)	
	#Also log to summary gateway logger if true
	if summaryLogger:
		logger = system.util.getLogger(auditProfile)
		logger.info("summaryObject for username %s : "%username + str(summaryObjectJsonString))
		
	return
#=============================================================== GetSummaryObject ===============================================================
def GetSummaryObject(UserInformation=None,username = "",line = None,ChartName = None,ChartID = None):
	if UserInformation is not None:
		username = UserInformation["FullName"]
	summaryLoggerStartDate = system.date.toMillis(system.date.now())
	summaryObject = {			
			"username":username,
			"line":line,
			"startDate":summaryLoggerStartDate	,
			"allocations":{
							},
			"info":{"ChartName":ChartName,"ChartID":ChartID},
			"error":{
					"value":False,
					"label":"", 
					"reason":""	,
					"failedRequests":{} #midKey/mvidKey : {'statusCode':statusCode,'message':message}						
						}
				}
	return summaryObject

#-------------------------------------------------------------------GetListFromDataset-------------------------------------------------------------
def GetListFromDataset(Dataset):
		getColumnHeaders = system.dataset.getColumnHeaders(Dataset)
		dataset = system.dataset.toPyDataSet(Dataset)
		list = []
		for row in dataset:
			dictRow = {}
			for col in getColumnHeaders:	
				dictRow[col] = row[col]
			list.append(dictRow)
		return list
#=========================================================ThrownException=========================================================
def ThrownException(Detail={}):
	if "message" in Detail:
		message = Detail["message"]
	else:
		message = "Unknown Error."		
	if "heading" in Detail:
		heading = Detail["heading"]
	else:
		heading = "An Error Occurred"
	system.perspective.openPopup("ThrownException","Application Standard/Components/ThrownException",{"Message":message,"Heading":heading},resizable = True,showCloseIcon = False)
	
	return 
	
#=========================================================SaveChangesWarning=========================================================	
def SaveChangesWarning(message,payload = {},id = "SaveChangesWarning",popupViewPath = "Application Standard/Components/Confirm Changes/Save Changes Warning",pagePath = None, navigationCurrentPathArray = None, scope = "page"):
	
		params = {
				"Message":message,
				"Scope":scope,
				"PagePath":pagePath,
				"NavigationCurrentPathArray":navigationCurrentPathArray,
				"SaveChangesPayload":payload
					}
	
		system.perspective.openPopup(id = id,view = popupViewPath,params = params ,resizable = True,showCloseIcon = False)
	
		return	
#=========================================================UpdateNavigationTree=========================================================	
def UpdateNavigationTree(LoseChangesWarning,pagePath,currentPathArray):
	#Update Navigation LoseChangesWarningProperty - Disable/Enables popup warning when navigating away from a page with changes
	system.perspective.sendMessage("LoseChangesWarning",payload = {"LoseChangesWarning":LoseChangesWarning},scope = "page")
	#Close Current Popup
	system.perspective.closePopup("")
	#Navigate to selected page
	pagePath =  pagePath
	system.perspective.navigate(page = pagePath)
	#Update Selected Menu Tree Items
	currentPathArray = currentPathArray
	payload = {
		"currentPath":	currentPathArray
			}	
	system.perspective.sendMessage("selectedItem",payload = payload, scope = "page")	
	return 	
#=========================================================UpdateChartParameterMeasureData=========================================================
def UpdateChartParameterMeasureData(Username,Connection,UserInformation,UtilitiesTagPath,ChartName,ChartID,RequiredInterval,MeasureID,TimeSchemeID,SectionIndex,MeasureIndex,DataIndex,DataObject,Audit = True,summaryObject = None):
	logger = system.util.getLogger("UpdateChartParameterMeasureData")
	#Initialise summary object for audit log
	if summaryObject is None:
		summaryObject = GetSummaryObject(username = Username,ChartID = ChartID,ChartName = ChartName)
#	DataObject = {
#			"PeriodStartUTC":"",
#			"Version":"",
#			"DateTimeUTC":"",
#			"Username":"",
#			"Value":"",
#			"MeasureValueID":""
#					}
	#If Data Index is None then add new entry
	logger.info("DataIndex: " + str(DataIndex))	
	updatedValue = DataObject["Value"]
	if DataIndex is None:
		ChartParameterMeasureDataTagPath = getChartParameterMeasureDataTagPath(UtilitiesTagPath,ChartName,SectionIndex,MeasureIndex)
		logger.info("ChartParameterMeasureDataTagPath: " + str(ChartParameterMeasureDataTagPath))
		currentMeasureData = getChartParameterMeasureData(ChartParameterMeasureDataTagPath)
		dataObjectIndex = getNewDataObjectInsertIndex(currentMeasureData,DataObject)
		logger.info("dataObjectIndex: " + str(dataObjectIndex))
		if dataObjectIndex is None:
			currentMeasureData.append(DataObject)
		else:
			currentMeasureData.insert(dataObjectIndex,DataObject)
		currentMeasureData = system.util.jsonEncode(currentMeasureData)		
		logger.info("currentMeasureData: " + str(currentMeasureData))		
		tagWrite = Standard.Model.Common.TagWrite(ChartParameterMeasureDataTagPath,currentMeasureData)		
		
		#Update Summary Object with path that was updated
		summaryObject["allocations"]["IgnitionDocumentPath"] = ChartParameterMeasureDataTagPath
		
	#If Value is null then remove entry
	elif updatedValue is None:
		ChartParameterMeasureDataTagPath = getChartParameterMeasureDataTagPath(UtilitiesTagPath,ChartName,SectionIndex,MeasureIndex)
		currentMeasureData = getChartParameterMeasureData(ChartParameterMeasureDataTagPath)
		#Remove entry from current data with index equal to DataIndex
		logger.info("Removing measure data at index: " + str(DataIndex))
		currentMeasureData.pop(DataIndex)
		currentMeasureData = system.util.jsonEncode(currentMeasureData)		
		logger.info("currentMeasureData: " + str(currentMeasureData))		
		tagWrite = Standard.Model.Common.TagWrite(ChartParameterMeasureDataTagPath,currentMeasureData)				
		#Update Summary Object with path that was updated
		summaryObject["allocations"]["IgnitionDocumentPath"] = ChartParameterMeasureDataTagPath		
				
	#Else Update Current Entry
	#If updating current Entry - Check if Datetime has changed. If so then write null to original datetime in Flow.
	else:
		ChartParameterMeasureDataIndexTagPath = getChartParameterMeasureDataIndexTagPath(UtilitiesTagPath,ChartName,SectionIndex,MeasureIndex,DataIndex)
		#Current Data Object
		CurrentDataHashMap = Standard.Model.Common.TagRead(ChartParameterMeasureDataIndexTagPath) #Hashmap
		CurrentDataObject = Standard.Model.Common.HashMapToPyObject(CurrentDataHashMap)
		logger.info("CurrentDataObject: " + str(CurrentDataObject))
		#Compare Current Object StartUTC to New Object StartUTC
		currentDataObjectPeriodStartUTC = CurrentDataObject["PeriodStartUTC"]
		newDataObjectPeriodStartUTC = DataObject["PeriodStartUTC"]		
		logger.info("currentDataObjectPeriodStartUTC: " + str(currentDataObjectPeriodStartUTC))
		logger.info("newDataObjectPeriodStartUTC: " + str(newDataObjectPeriodStartUTC))
		isEqual = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.isFlowUTCFormattedEqual(currentDataObjectPeriodStartUTC,newDataObjectPeriodStartUTC)
		logger.info("isEqual: " + str(isEqual))
		if isEqual:
			#Do Nothing
			pass
		else:
			#Update Current Object's timestamp to None
			TimeStampUTC = currentDataObjectPeriodStartUTC
			Value = None
			MeasureValueID = CurrentDataObject["MeasureValueID"]			
			updateTimePeriodMeasureValue = Standard.InterfaceModules.Flow.PrivateAPI.V1.TimePeriod.UpdateTimePeriodMeasureValue(Username,Connection,UserInformation,ChartID,MeasureID,TimeSchemeID,MeasureValueID,Value,RequiredInterval,TimeStampUTC=None)
		
		#Check if Version is None - 
		#If true then Flow Response was an empty array. No changes were made and use current data
		if DataObject["Version"] is None:
			DataObject["Version"] = CurrentDataObject["Version"]
		
		logger.info("DataObject: " + str(DataObject))	
		logger.info("ChartParameterMeasureDataIndexTagPath: " + str(ChartParameterMeasureDataIndexTagPath))		
		#Once current object is not needed anymore, write new value to tag	
		DataObject = system.util.jsonEncode(DataObject)	
		tagWrite = Standard.Model.Common.TagWrite(ChartParameterMeasureDataIndexTagPath,DataObject)	
		#Update Summary Object with path that was updated
		summaryObject["allocations"]["IgnitionDocumentPath"] = ChartParameterMeasureDataIndexTagPath
		
	#If tag write is True then good quality else error
	if tagWrite:
		pass
	else:		
		summaryObject["error"][	"value"] = True
		summaryObject["error"][	"label"] = ChartName
		summaryObject["error"][	"reason"] = "Ignition Document Tag Failed to Update"
		#failedRequests Object
		summaryObject["error"]["failedRequests"]["SectionIndex"] = SectionIndex
		summaryObject["error"]["failedRequests"]["MeasureIndex"] = MeasureIndex
		summaryObject["error"]["failedRequests"]["DataIndex"] = DataIndex	
		#Error Response Operator Popup
		errorResponseObject = {'error':True,'json':{},'message':"Failed to update Ignition Chart Parameter Data for Chart: %s with Start Date: %s."%(ChartName,PeriodStartUTC)}
		Standard.InterfaceModules.Flow.Common.ThrownException(errorResponseObject)		
			
	#Log to Audit profile if auditing enabled	
	if Audit:
		Standard.InterfaceModules.Flow.Common.LogAudit(summaryObject,Username,auditProfile = "SaveChangesSummary")		
		
	resultObject = {"TagWrite":tagWrite,"SummaryObject":summaryObject}	
	return resultObject
#=========================================================getChartParameterMeasureDataTagPath=========================================================

def getChartParameterMeasureDataTagPath(UtilitiesTagPath,ChartName,SectionIndex,MeasureIndex):
	tagPath = UtilitiesTagPath + "/Flow Parameters/Chart Parameters['%s.Sections[%s].Measures[%s].Data']"%(ChartName,SectionIndex,MeasureIndex)
	return tagPath
#=========================================================getChartParameterMeasureData=========================================================
	
def getChartParameterMeasureData(ChartParameterMeasureDataTagPath):

	chartDataArrayList = Standard.Model.Common.TagRead(ChartParameterMeasureDataTagPath)
	currentData = []
	for hashMap in chartDataArrayList:
		objectFromHashMap = Standard.Model.Common.HashMapToPyObject(hashMap)
		currentData.append(objectFromHashMap)
		
	return currentData
#=========================================================getNewDataObjectInsertIndex=========================================================

def getNewDataObjectInsertIndex(CurrentMeasureData,DataObject):
	dataObjectPeriodStartUTC = DataObject["PeriodStartUTC"]
	dataObjectPeriodStartLocal = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(dataObjectPeriodStartUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'") 
	requiredIndex = None
	print "dataObjectPeriodStartLocal" + str(dataObjectPeriodStartLocal)
	for i in range(1,len(CurrentMeasureData)):
		print i
		currentMeasureObject = CurrentMeasureData[-i]
		print currentMeasureObject
		previousMeasureObject = CurrentMeasureData[-i-1]
		print previousMeasureObject
		#PeriodStartUTC Strings
		currentMeasureObjectPeriodStartUTC = currentMeasureObject["PeriodStartUTC"]
		previousMeasureObjectPeriodStartUTC = previousMeasureObject["PeriodStartUTC"]		
		#PeriodStart Local Datetime
		currentMeasureObjectPeriodStartLocal = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(currentMeasureObjectPeriodStartUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'") 
		previousMeasureObjectPeriodStartLocal = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(previousMeasureObjectPeriodStartUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'") 
		print currentMeasureObjectPeriodStartLocal
		print previousMeasureObjectPeriodStartLocal
		isBetween = system.date.isBetween(dataObjectPeriodStartLocal,previousMeasureObjectPeriodStartLocal,currentMeasureObjectPeriodStartLocal)
		if isBetween and dataObjectPeriodStartUTC!=currentMeasureObjectPeriodStartUTC:
			requiredIndex = -i
			break
	print "requiredIndex: " + str(requiredIndex)		
	#If requiredIndex is none then it is either in the beginning or the end
	#Return None to append to end and return 0 to insert in the beginning
	if requiredIndex is None:
		if len(CurrentMeasureData) > 0:
			dataPeriodStartUTCBegin = CurrentMeasureData[0]["PeriodStartUTC"] 
			dataPeriodStartBeginLocal = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(dataPeriodStartUTCBegin,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'") 
			isAfter = system.date.isAfter(dataObjectPeriodStartLocal,dataPeriodStartBeginLocal)
			if isAfter:
				requiredIndex = None
			else:
				requiredIndex = 0
		else:
			requiredIndex = None
			
	return requiredIndex

#=========================================================getChartParameterMeasureDataIndexTagPath=========================================================
def getChartParameterMeasureDataIndexTagPath(UtilitiesTagPath,ChartName,SectionIndex,MeasureIndex,DataIndex):
	#{ConnectionTagPath}/Flow Parameters/Chart Parameters['{ChartName}.Sections[{SectionIndex}].Measures[{MeasureIndex}].Data[{DataIndex}]']
	tagPath = UtilitiesTagPath + "/Flow Parameters/Chart Parameters['%s.Sections[%s].Measures[%s].Data[%s]']"%(ChartName,SectionIndex,MeasureIndex,DataIndex)
	return tagPath

#===============================================GetDateTimeFormat================================================
#Format Datetime to a string	
def GetDateTimeFormat(TimestampUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'" ):
	return system.date.format(TimestampUTC,Format)
#=========================================================GetUTCFormattedTime=============================================================================	
def GetUTCFormattedTime(LocalTimestamp=None,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'"):
	#Gets UTC as a date time
	utcUnformattedTime = GetUTCTime(LocalTimestamp)
	#Converts date time to a string to send back to Flow
	utcFormattedTime = GetDateTimeFormat(utcUnformattedTime,Format)
	return utcFormattedTime	
#===============================================GetUTCTime=======================================================
#Get UTC Date Time from Local Datetime
def GetUTCTime(LocalTimestamp=None):
	offset = int(system.date.getTimezoneRawOffset())*-1
	if LocalTimestamp is None:
		LocalTimestamp = system.date.now()
	#return utcNow
	utcTime = system.date.addHours(LocalTimestamp,offset)
	return utcTime

	
