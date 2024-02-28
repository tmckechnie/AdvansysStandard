#======================================================= GetTagDataURL =======================================================
#Create measureDataAPI url
def GetTagDataURL(PublicAPI,StartUTC="",EndUTC="",MeasureIds = [],TemplateIds=[],TagIds=[],Limit=1000):

	url = PublicAPI + "/v1/data/tags?"
	tagDataAPIParameters = getTagDataParameters(StartUTC,EndUTC,MeasureIds,TemplateIds,TagIds,Limit)
	for parameter in tagDataAPIParameters:
		if tagDataAPIParameters[parameter] == "":
			continue
		elif parameter == "id" or parameter == "templateid" or parameter == "tagid":
			for id in tagDataAPIParameters[parameter]:			
				url += "%s=%s&"%(parameter,id)
		else:
			
			paramterValue = tagDataAPIParameters[parameter]
			url += "%s=%s&"%(parameter,paramterValue)
	
	url = url[0:-1]
	return url
#======================================================= getTagDataParameters =======================================================
#Used to get all tagdataAPI paramters into usable dictionary
def getTagDataParameters(StartUTC,EndUTC,measureIds,templateids,tagIds,limit):
	
		tagDataAPIParameters = {
									  "start": StartUTC,
									  "end":EndUTC ,
									  "id":measureIds,
									  "templateid": templateids,
									  "tagid": tagIds,						  
									  "limit": limit								  
									}
		return tagDataAPIParameters
#======================================================= GetMeasureDataURL =======================================================
#Create measureDataAPI url
def GetMeasureDataURL(PublicAPI,StartUTC="",EndUTC="",id = [],templateid=[],preferred = True,eventPeriods = False,eventid="",calendarid = "",comments = False,exceptions=False,attributes=False,users=True,limit=1000,MeasureDataAPIParameters = None):

	url = PublicAPI + "/v1/data/measures?"
	if MeasureDataAPIParameters is None:
		MeasureDataAPIParameters = getMeasureDataParameters(StartUTC,EndUTC,id,templateid,preferred,eventPeriods,eventid,calendarid,comments,exceptions,attributes,users,limit)
	for parameter in MeasureDataAPIParameters:
		if MeasureDataAPIParameters[parameter] == "":
			continue
		elif parameter == "id" or parameter == "templateid" or parameter == "tagid":
			for id in MeasureDataAPIParameters[parameter]:
				#print id				
				url += "%s=%s&"%(parameter,id)
		else:
			paramterValue = MeasureDataAPIParameters[parameter]
			url += "%s=%s&"%(parameter,paramterValue)
	
	url = url[0:-1]
	return url	
#======================================================= getMeasureDataParameters =======================================================
#Used to get all measuredataAPI paramters into usable dictionary
def getMeasureDataParameters(StartUTC,EndUTC,id,templateid,preferred,eventPeriods,eventid,calendarid,comments,exceptions,attributes,users,limit):
	
		measureDataAPIParameters = {
									  "start": StartUTC,
									  "end":EndUTC ,
									  "id":id,
									  "templateid": templateid,
									  "preferred": preferred,
									  "eventPeriods": eventPeriods,
									  "eventid": eventid,
									  "calendarid": calendarid,
									  "comments": comments,
									  "exceptions": exceptions,
									  "attributes": attributes,
									  "users": users,								  
									  "limit": limit								  
									}
		return measureDataAPIParameters
#======================================================= queryAPIMatchID =======================================================
#Used to find exact match on query response objects on the object name.
#Returns the ID associated with exact match	
def queryAPIMatchNameID(QueryResponse):	
	id = None
	queries = QueryResponse["queries"]
	objects = QueryResponse["objects"]
	errors = QueryResponse["errors"]	
	queriesSet = set(queries)
	if len(errors) != 0:
		return None
	
	for object in objects:
		name = object["name"]
		if name in queriesSet:
			id = object["id"]
			break
	return id

#=======================================================GetLastEvent=======================================================
def GetLastEvent(EventID,Connection=None,ConnectionTagPath=None):
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetConnection(ConnectionTagPath)
	publicAPI = Connection['Public API']
	url = publicAPI + "/v1/data/events?id=" + str(EventID) + "&preferred=true&attributes=true"
	print url
	headerValues = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetPublicHeader(Connection)
	response =  Standard.InterfaceModules.Flow.PublicAPI.V1.Common.Get(url=url,HeaderValues=headerValues)
	print response
	if response['error']:
		return response['message']
	else:
#		event = {}
#		event
#		eventPeriod = {}
		
		return response['json']
#=======================================================GetLatestTags=======================================================
#connectionTagPath='[AdvansysStandard]Standard/Interface Modules/Flow/Connection'
#Standard.InterfaceModules.Flow.PublicAPI.V1.Data.GetLatestTags(ConnectionTagPath=connectionTagPath,MeasureIds=[],TemplateIds=[],TagIds=[19])
def GetLatestTags(ConnectionTagPath,MeasureIds=[],TemplateIds=[],TagIds=[]):
	connection = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetConnection(ConnectionTagPath=ConnectionTagPath)
	publicAPI = connection['Public API']
	headers = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetPublicHeader(Connection=connection)
	url = GetTagDataURL(
						PublicAPI=publicAPI,
						StartUTC="",
						EndUTC="",
						MeasureIds = MeasureIds,
						TemplateIds=TemplateIds,
						TagIds=TagIds,
						Limit=1000
						)
	print url
	response = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.Get(url=url,HeaderValues=headers)
	#return response
	#print response['json']['values']
	values = response['json']['values']
	tagData = {}
	for tag in values:
		#print [measure['name'],measure['data'][0]['value']]
		key = tag['name']
		value = tag['data'][0]['value']
		timestamp = tag['data'][0]['start']
		quality = tag['data'][0]['quality']['value']
		tagData[key] = {'value':value,'quality':quality,'timestamp':timestamp}
	return tagData
#=======================================================GetTags=======================================================
#connectionTagPath='[AdvansysStandard]Standard/Interface Modules/Flow/Connection'
#Standard.InterfaceModules.Flow.PublicAPI.V1.Data.GetLatestTags(ConnectionTagPath=connectionTagPath,MeasureIds=[],TemplateIds=[],TagIds=[19])
def GetTags(ConnectionTagPath,PeriodStart,PeriodEnd=None,MeasureIds=[],TemplateIds=[],TagIds=[],Limit=1000):
	if PeriodEnd is None:
		PeriodEnd = system.date.now()
		
	#Period in UTC
	timezoneOffset = int(-1*system.date.getTimezoneOffset(PeriodStart))
	periodStartUTC = system.date.addHours(PeriodStart, timezoneOffset)
	periodEndUTC = system.date.addHours(PeriodEnd, timezoneOffset)
	
	periodStartUTC = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetDateTimeFormat(periodStartUTC,UTC=True)
	periodEndUTC = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetDateTimeFormat(periodEndUTC,UTC=True)
		
	connection = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetConnection(ConnectionTagPath=ConnectionTagPath)
	publicAPI = connection['Public API']
	headers = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetPublicHeader(Connection=connection)
	url = GetTagDataURL(
						PublicAPI=publicAPI,
						StartUTC=periodStartUTC,
						EndUTC=periodEndUTC,
						MeasureIds = MeasureIds,
						TemplateIds=TemplateIds,
						TagIds=TagIds,
						Limit=Limit
						)
	#print url
	response = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.Get(url=url,HeaderValues=headers)
	#return response
	#print response['json']['values']
	values = response['json']['values']
	tagData = {}
	for tag in values:
		#print [measure['name'],measure['data'][0]['value']]
		key = tag['name']
		data = tag['data']
		dataList = []
		for dataPoint in data:
			value = dataPoint['value']
			timestamp = dataPoint['start']
			quality = dataPoint['quality']['value']
			tvq = {'value':value,'quality':quality,'timestamp':timestamp}
			dataList.append(tvq)
		tagData[key] = dataList
	return tagData
#=======================================================GetLatestMeasures=======================================================
#connectionTagPath='[AdvansysStandard]Standard/Interface Modules/Flow/Connection'
#Standard.InterfaceModules.Flow.PublicAPI.V1.Data.GetLatestMeasures(ConnectionTagPath=connectionTagPath,MeasureIds=[],TemplateIDs=[2])
def GetLatestMeasures(ConnectionTagPath,MeasureIds=[],TemplateIDs=[]):
	connection = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetConnection(ConnectionTagPath=ConnectionTagPath)
	publicAPI = connection['Public API']
	headers = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetPublicHeader(Connection=connection)
	url = GetMeasureDataURL(
							PublicAPI=publicAPI,
							StartUTC="",
							EndUTC="",
							id = MeasureIds,
							templateid=TemplateIDs,
							preferred = True,
							eventPeriods = False,
							eventid="",
							calendarid = "1",
							comments = False,
							exceptions=False,
							attributes=False,
							users=True,
							limit=1000,
							MeasureDataAPIParameters = None
							)
	#print url
	response = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.Get(url=url,HeaderValues=headers)
	#print response['json']['values']
	values = response['json']['values']
	measureData = {}
	for measure in values:
		#print [measure['name'],measure['data'][0]['value']]
		key = measure['name']
		value = measure['data'][0]['value']
		measureData[key] = value
	return measureData

	
	

	
	
