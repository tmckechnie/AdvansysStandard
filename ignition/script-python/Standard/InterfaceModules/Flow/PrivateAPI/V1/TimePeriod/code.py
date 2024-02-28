
#==============================================UpdateMeasureTimePeriodValues==============================================
def UpdateChartTimePeriodMeasureValues(Username,Connection,UserInformation,ChartID,TimeSchemeID,Comments = [],MeasureValues = [],ChartName = None,Audit = True,summaryObject = None):
	logger = system.util.getLogger("UpdateChartTimePeriodMeasureValues")
	logger.info("Started")
	#PayloadObject
	#PayloadObject = {"Comments":{"mvidKey":{"id":mvid,"v":comment}},"Measures":{"midKey":{"Changes":[],"MeasureID":MeasureID}}}
	#MeasureValues = [{MeasureID:[{id:mvid,v:value}..]}]	
	#Comments = [{id:mvid,v:comment}...]
	#Intitial Loggers
	logger.info("ChartID: " + str(ChartID))
	logger.info("TimeSchemeID: " + str(TimeSchemeID))
	logger.info("Comments: " + str(Comments))
	logger.info("MeasureValues: " + str(MeasureValues))
	#Initialise failed requests Object for thrown exception popup and to update current changes object on Ignition time period table
	failedRequests = {"Comments":[],"Measures":[]}
	successfulRequests = {"Comments":[],"Measures":[]}
	#Initialise summary object for audit log
	if summaryObject is None:
		summaryObject = Standard.InterfaceModules.Flow.Common.GetSummaryObject(username = Username,ChartID = ChartID,ChartName = ChartName)
	
	#Do Measures
	#Loop through Measure Value Objects - Create payload array - Send to Flow - updatefailed requests object
	for measureObject in MeasureValues:
		MeasureID = measureObject["MeasureID"]
		measureIDKey = "mid" + str(MeasureID)
		Changes = measureObject["Changes"]
		payloadArray = []
		for change in Changes:
			changePyObject = {}
			changePyObject["v"] = change["v"]
			changePyObject["id"] = change["id"]
			payloadArray.append(changePyObject)
			#Add payload to summary object
			summaryObject["allocations"][measureIDKey] = payloadArray
			
		#Write change to Flow
		measureValueResponse = UpdateTimePeriodMeasureValues(Connection,UserInformation,ChartID,TimeSchemeID,MeasureID,payloadArray)
		#if error: {'error':True,'json':{},'statusCode':statusCode,'message':message}
		if measureValueResponse["error"]:
			failedRequests["Measures"].append(measureIDKey)
		elif "measureValues" in measureValueResponse["json"]:
			successfulRequests["Measures"]+= measureValueResponse["json"]["measureValues"]
				
	#Do Comments
	#Loop through Comment Objects - Create payload - Send to Flow - updatefailed requests object
	for commentObject in Comments:
		MeasureValueID = commentObject["id"]
		comment = commentObject["v"]
		#Add payload to summary object
		summaryObject["allocations"]["mvid" + str(MeasureValueID)] = comment
		commentResponse = UpdateMeasureValueComment(Connection,UserInformation,MeasureValueID,comment)
		if commentResponse["error"]:
			failedRequests["Comments"].append("mvid" + str(MeasureValueID))		
		elif "measureValueComment" in commentResponse["json"]:
			successfulRequests["Comments"].append(commentResponse["json"]["measureValueComment"])
			
	#Update summary object with failed requests	
	summaryObject["error"][	"failedRequests"] = failedRequests
	#If failed requests is not empty then throw popup
	if len(failedRequests["Comments"]) > 0 or len(failedRequests["Measures"]) > 0:
		message = "Failed to submit 1 or more "
		if len(failedRequests["Comments"]) > 0:
			#Use last error message to measure/comment
			message += "Comments (%s)"%commentResponse["statusCode"]
		if len(failedRequests["Measures"]) > 0 and len(failedRequests["Comments"]) > 0: 
			message += " and Measure Values (%s)"%measureValueResponse["statusCode"]
		elif len(failedRequests["Measures"]) > 0:
			message += "Measure Values (%s)"%measureValueResponse["statusCode"]
		else:
			message += ""	
						
		message += " to Flow."
		
		detail = {"message":message}
		Standard.InterfaceModules.Flow.Common.ThrownException(Detail=detail)
		#If there were errors then update summaryObject and logger info
		summaryObject["error"][	"value"] = True
		summaryObject["error"][	"label"] = ChartName
		summaryObject["error"][	"reason"] = message
		logger.info("failedRequests for %s on Chart: %s for CalendarID: %s "%(Username,ChartID,TimeSchemeID) + str(failedRequests))
	
	#Log to Audit profile if auditing enabled	
	if Audit:
		Standard.InterfaceModules.Flow.Common.LogAudit(summaryObject,Username,auditProfile = "SaveChangesSummary")
	#Use failed requests object to update changes object of all tables that have had changes succesfully made
	resultObject = {"SuccessfulRequests":successfulRequests,"FailedRequests":failedRequests,"SummaryObject":summaryObject}
	return resultObject
	
#==============================================UpdateMeasureValueComment==============================================

def UpdateMeasureValueComment(Connection,UserInformation,MeasureValueID,comment):
	logger = system.util.getLogger("UpdateMeasureValueComment")
	logger.info("Update Started")
	logger.info("MeasureValueID" + str(MeasureValueID))
	logger.info("comment" + str(comment))
	token = "token=" + UserInformation["Interfaces"]["Flow"]["Token"]
	HeaderValues = {"Cookie":token,"Content-Type":"text/plain"}	
	url = Connection["Private API"] + "/data/timePeriodValues/%s/comments"%(MeasureValueID)
	payload = comment #[{"v":num,"id":measureValueID},....]			
	updateMeasureValueCommentResponse = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Post(url,HeaderValues=HeaderValues,PostData=payload)	
	logger.info("updateMeasureValueCommentResponse" + str(updateMeasureValueCommentResponse))
	return updateMeasureValueCommentResponse

#==============================================UpdateMeasureTimePeriodValues#==============================================
def UpdateTimePeriodMeasureValues(Connection,UserInformation,ChartID,TimeSchemeID,MeasureID,PayloadArray = []):
	logger = system.util.getLogger("UpdateTimePeriodMeasureValues")
	logger.info("Update Started")
	logger.info("ChartID" + str(ChartID))
	logger.info("TimeSchemeID" + str(TimeSchemeID))
	logger.info("MeasureID" + str(MeasureID))
	logger.info("PayloadArray" + str(PayloadArray))
	
	url = Connection["Private API"] + "/data/measures/%s/timeSchemes/%s/timePeriodValues"%(MeasureID,TimeSchemeID)
	token = "token=" + UserInformation["Interfaces"]["Flow"]["Token"]
	HeaderValues = {"Cookie":token,"Content-Type":"application/json"}
	
	payload = {"v":PayloadArray} #[{"v":num,"id":measureValueID},....]

	updateMeasureValuesResponse = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Put(url,HeaderValues=HeaderValues,Data=payload)	
	#if error: {'error':True,'json':{},'statusCode':statusCode,'message':message}
	logger.info("updateMeasureValuesResponse: " + str(updateMeasureValuesResponse))
	return updateMeasureValuesResponse

#==============================================UpdateTimePeriodMeasureValue==============================================
def UpdateTimePeriodMeasureValue(Connection,UserInformation,MeasureValueID,TimeSchemeID,MeasureID,Value,Username=None,ChartID=None,RequiredInterval=None,TimeStampUTC=None,ChartName = None,Audit = False,summaryObject = None):
#	logger = system.util.getLogger("UpdateTimePeriodMeasureValue")
#	logger.info("Update Started")
#	logger.info("Username" + str(Username))
#	#logger.info("Connection" + str(Connection))
#	#logger.info("UserInformation" + str(UserInformation))
#	logger.info("ChartID" + str(ChartID))
#	logger.info("MeasureID" + str(MeasureID))
#	logger.info("TimeSchemeID" + str(TimeSchemeID))
#	logger.info("MeasureValueID" + str(MeasureValueID))
#	logger.info("Value" + str(Value))
#	logger.info("TimeStampUTC" + str(TimeStampUTC))	
	#Initialise summary object for audit log
	if summaryObject is None:
		summaryObject = Standard.InterfaceModules.Flow.Common.GetSummaryObject(UserInformation=UserInformation,username = Username,ChartID = ChartID,ChartName = ChartName)
		
	if MeasureValueID is None:
		measureValueResultObject  = getMeasureValueID(Username,Connection,UserInformation,ChartID,TimeSchemeID,MeasureID,RequiredInterval,TimeStampUTC)
		MeasureValueID = measureValueResultObject["MeasureValueID"]
		TimeStampUTC = measureValueResultObject["TimePeriodStartUTC"]
		
#	logger.info("MeasureValueID" + str(MeasureValueID))
#	logger.info("TimeStampUTC" + str(TimeStampUTC))
	#If TimePeriodID could not be found for given TimeStamp of given chart
	if MeasureValueID is None:
		updateTimePeriodResponse = {'error':True,'json':{},'message':"Time Period not found for selected Date Time for measure with measureID: %s."%(MeasureID)}
	else:
		updateTimePeriodResponse = updateTimePeriodMeasureValue(Connection,UserInformation,MeasureID,TimeSchemeID,MeasureValueID,Value)
	
	if updateTimePeriodResponse["error"]:
		logger.info("updateTimePeriodResponse: " + str(updateTimePeriodResponse))
		Standard.InterfaceModules.Flow.Common.ThrownException(updateTimePeriodResponse)		
		#If there were errors then update summaryObject and logger info
		message = updateTimePeriodResponse["message"]
		summaryObject["error"][	"value"] = True
		summaryObject["error"][	"label"] = ChartName
		summaryObject["error"][	"reason"] = message		
	else:
		measureValueIDKey = "mvid" + str(MeasureValueID)
		summaryObject["allocations"][measureValueIDKey] = 1
		
	#Log to Audit profile if auditing enabled	
	if Audit:
		Standard.InterfaceModules.Flow.Common.LogAudit(summaryObject,Username,auditProfile = "SaveChangesSummary")
		
	resultObject = {"TimePeriodResponse":updateTimePeriodResponse,"PeriodStartUTC":TimeStampUTC,"SummaryObject":summaryObject}
	return resultObject
	
#==============================================updateTimePeriodMeasureValue==============================================
def updateTimePeriodMeasureValue(Connection,UserInformation,MeasureID,TimeSchemeID,MeasureValueID,Value):
	logger = system.util.getLogger("updateTimePeriodMeasureValue")
	#Put Request to Flow
	url = Connection["Private API"] + "/data/measures/%s/timeSchemes/%s/timePeriodValues"%(MeasureID,TimeSchemeID)
	token = "token=" + UserInformation["Interfaces"]["Flow"]["Token"]
	HeaderValues = {"Cookie":token,"Content-Type":"application/json"}
	payload = {"v":[{"id":MeasureValueID,"v":Value}]}
	#payload = system.util.jsonEncode(payload)
#	logger.info("url:  " +str(url))
#	logger.info("HeaderValues:  " +str(HeaderValues))
#	logger.info("payload:  " +str(payload))
	putRequest = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Put(url,HeaderValues=HeaderValues,Data=payload)
	
	return putRequest
#===================================================getTimePeriodID=====================================================	
def getMeasureValueID(Username,Connection,UserInformation,ChartID,TimeSchemeID,MeasureID,RequiredInterval,TimeStampUTC=None):
	logger = system.util.getLogger("getTimePeriodID")
	logger.info("getTimePeriodID Started")
	requiredInterval = RequiredInterval
	requiredTimeScheme = TimeSchemeID
	requiredMeasureID = MeasureID
	requiredTimeStampUTC = TimeStampUTC	
	#logger.info("Connection: " + str(Connection))
	logger.info("ChartID: " + str(ChartID))
	chartData = Standard.InterfaceModules.Flow.PrivateAPI.V1.Chart.GetData(ChartID,Username,Connection,UserInformation,TimeStampUTC=TimeStampUTC)
	data = chartData["json"]
	#logger.info("chartData: " + str(chartData))
	#Loop through measure values to find current TimePeriodID with PeriodStartUTC <= TimeStampUTC <= PeriodEndUTC
	timePeriodID = None
	requiredTimeStampLocalDateTime = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(requiredTimeStampUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'")
	timePeriods = data["timePeriods"]
	timePeriodStartUTC = None
	for timePeriod in timePeriods:
		timePeriodTimeScheme = timePeriod["tsid"]
		timePeriodInterval = timePeriod["it"]
		if timePeriodTimeScheme == requiredTimeScheme and timePeriodInterval == requiredInterval:
			timePeriodStartUTC = timePeriod["s"]
			timePeriodEndUTC = timePeriod["e"]			
			#timePeriod as Local Datetimes to compare dates to each other
			timePeriodStartLocalDateTime = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(timePeriodStartUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'")
			timePeriodEndLocalDateTime = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(timePeriodEndUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'")
			
			#If  timePeriodStartLocalDateTime <= requiredTimeStampLocalDateTime <= timePeriodEndLocalDateTime
			isBetween = system.date.isBetween(requiredTimeStampLocalDateTime,timePeriodStartLocalDateTime,timePeriodEndLocalDateTime)
			if isBetween and requiredTimeStampUTC != timePeriodEndUTC:
				logger.info("isBetween PeriodStart: " + str(timePeriodStartUTC))
				logger.info("isBetween PeriodEnd: " + str(timePeriodEndUTC))
				logger.info("isBetween requiredTimeStampUTC: " + str(requiredTimeStampUTC))				
				timePeriodID = timePeriod["id"]	
				break	
					
	#Find MeasureValueID
	measureValues = data["measureValues"]	
	measureValueID = None	
	for measureValue in measureValues:		
		measureValueTimePeriodID = measureValue["pid"]
		measureID = measureValue["mid"]
		if measureValueTimePeriodID == timePeriodID and measureID == requiredMeasureID:
			measureValueID = int(measureValue["id"])
			break
			
	resultObject = {
				"MeasureValueID":measureValueID,
				"TimePeriodStartUTC":timePeriodStartUTC #Actual PeriodStartUTC associated with TimePeriodID
	
				}		
	return resultObject

	

