
#Flow Event Functions
#Data structures
#period = {'periodStart':{'value'},'periodEnd':{'value'},'timestamp':{'value'}}
#eventPeriod = {'eventPeriodID':{'value'},'period':{'value'}}
#eventAttributeValue = {'eventAttributeID','value'}
debug = False

chartTypeRequired = 'tables-eventbased-table'
formTypeRequired = 'tables-eventbased-table'
def getFlowDefinitionFromForm(Connection,FormID):
	url = Connection["Private API"] + '/definition/forms/' + str(FormID)
	response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Get(url)
	return response
	
def GetDefinitionFromForm(Connection,FormID):

	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()

	response = getFlowDefinitionFromForm(Connection,FormID)
	if response['error']:
		return response
	#print response
	json = response['json']
	
	formType = json['formType']
	if formType != formTypeRequired:
		return 'Invalid Form Type'
	
	defFormGroups = []	
	formGroups = json['formGroups']
	defFormGroup = {}
	formGroup = formGroups[0]
	eventScheme = formGroup['eventSchemes'][0]
	defFormGroup['title'] = formGroup['name']
	defEvent = {}
	
	render={'datatype':'date','numberFormat':'0.0','dateFormat':'YYYY-MM-DD HH:mm:ss'}
	#renderEditColumn = {'datatype':'date','numberFormat':'0.0','dateFormat':'YYYY-MM-DD HH:mm:ss'}
	defEvent['baseColInstances'] = [
	getColumnInstance('periodStart','Period Start',True,False,150,render),getColumnInstance('periodEnd','Period End',True,False,150,render)]
	defEvent['name'] = eventScheme['alias']
	defEvent['eventSchemeID'] = eventScheme['eventSchemeID']

	
	
	eventAttributes = eventScheme['eventAttributes']
	defEventAttributes = []
	measures = []
	#Get Enumeration Group from Definition
	#Use Flow Definition in conjunction with an array of the attributes the SINGLE enumeration group on the form is being filtered by
	#Technically does not reference the enumerationGroup anywhere. Uses the filtered on property to determine the options.
	defEnumerationGroup = getEnumGroupFromFlowDefinition(json,[])
		
	#Get Attributes
	for eventAttribute in eventAttributes:
		defEventAttribute = {}
		title = eventAttribute['alias']
		defEventAttribute['title'] = title
		name = eventAttribute['alias']
		defEventAttribute['name'] = name
		defEventAttribute['eventAttributeID'] = eventAttribute['eventAttributeID'] 
		
		readOnly = False
		if 'readOnly' in eventAttribute:
			readOnly = eventAttribute['readOnly']
		defEventAttribute['readOnly'] = readOnly
		
		defEventAttribute['displayOrder'] = eventAttribute['displayOrder']
		
		
		#Setup Table Column
		editable = not readOnly
		visible=True
		name = name.replace(' ','')
		defEventAttribute['colInstance'] = getColumnInstance(name,title,visible,editable)
			
		defEventAttributes.append(defEventAttribute)
	
	defMeasures = []
	measures = eventScheme['measures']
	#Get measures
	for measure in measures:
		#print measure
		defMeasure = {}
		title = measure['alias']
		defMeasure['title'] = title
		name = measure['alias']
		defMeasure['name'] = name
		defMeasure['measureID'] = measure['measureID'] 
		uom = measure['uom']
		defMeasure['uom'] = uom
		readOnly = False
		if 'readOnly' in measure:
			readOnly = measure['readOnly']
		defMeasure['readOnly'] = readOnly

		defMeasure['displayOrder'] = measure['displayOrder']
		
		#Setup Table Column
		editable = not readOnly
		visible=True
		name = name.replace(' ','')
		defMeasure['colInstance'] = getColumnInstance(name,title +' ('+uom +')',visible,editable)
		
		defMeasures.append(defMeasure)
	
	defEvent["enumerationGroup"] = defEnumerationGroup		
	defEvent['eventAttributes'] = defEventAttributes
	defEvent['measures'] = defMeasures
	defFormGroup['event'] = defEvent
	defFormGroups.append(defFormGroup)
	#defFormGroups = system.util.jsonEncode(defFormGroups)
	return defFormGroups
	

def GetRawDataFromForm(Connection,Username,UserInformation,FormID,DefinitionFormGroup=None,Period=None):
		loggerName = "Flow Event GetRawDataFromForm"
		logMessage = 'Starting...'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=logMessage,Debug=debug)
		if Connection is None:
			Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()

		period = ""
		if Period is not None:
			if 'timeStamp' in Period:
				timestampUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(LocalTimestamp=Period['timeStamp'])
				timeStamp = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(TimestampUTC=timestampUTC)
				period = '?timeStamp=' + timeStamp
			else:
				periodStartUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(LocalTimestamp=Period['periodStart'])
				periodStart = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(TimestampUTC=periodStartUTC)
				
				periodEndUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(LocalTimestamp=Period['periodEnd'])
				periodEnd = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(TimestampUTC=periodEndUTC)
				
				period = '?periodStart=' + periodStart + '&periodEnd=' + periodEnd
		
		
		user = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,UserInformation,Username)
		headerValues = {'Cookie':'token=' + userDetail["Interfaces"]["Flow"]['Token']}	
		url = Connection["Private API"] + '/data/forms/' + str(FormID) + period
		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Get(url,HeaderValues=headerValues)
		if response['error']:
			return response
		json = response['json']
		return json
		
def GetDataFromForm(Connection,Username,UserInformation,FormID,DefinitionFormGroup=None,Period=None):
	loggerName = "Flow Event GetDataFromForm"
	logMessage = 'Starting...'
	
	Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=logMessage,Debug=debug)
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
	if DefinitionFormGroup is None:
		DefinitionFormGroup = GetDefinitionFromForm(Connection,FormID)
	
	definition = DefinitionFormGroup
	
	rawData = GetRawDataFromForm(Connection=Connection,Username=Username,UserInformation=UserInformation,FormID=FormID,DefinitionFormGroup=None,Period=Period)
	if 'eventPeriods' not in rawData:
		return rawData
		
	eventPeriods = rawData['eventPeriods']
	attributeValues = rawData['attributeValues']
	measureValues= []
	if 'measureValues' in rawData:
		measureValues = rawData['measureValues']
	
	data = []
	
	for formGroup in definition:
		
		event = formGroup['event']
		eventSchemeID = event['eventSchemeID']
		eventAttributes = event['eventAttributes']
		measures = event['measures']
		#Get Event Periods
		for eventPeriod in eventPeriods:
			if eventPeriod['esid'] == eventSchemeID:
				ep = Standard.InterfaceModules.Flow.PrivateAPI.V1.Event.GetDataFromFlowEventPeriod(FlowEventPeriod=eventPeriod,AttributeValues=attributeValues,EventAttributes=eventAttributes,Measures=measures)
				ep['formGroup'] = {'value':formGroup['title']}
				data.append(ep)
				
	logMessage = 'Done!'
	Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=logMessage,Debug=True)
	return data
	
def GetDataFromFlowEventPeriod(FlowEventPeriod,AttributeValues,EventAttributes=None,Measures=None):
	loggerName = 'GetDataFromFlowEventPeriod'
	ep = {}
	#Event Period ID
	eventPeriodID = FlowEventPeriod['id']
	index = FlowEventPeriod['idx']
	ep["edit"] = {"value":True}
	ep["index"] = {"value":index}
	ep['eventSchemeID'] = {'value':FlowEventPeriod['esid']}
	ep['eventPeriodID'] = {'value':eventPeriodID}
	#Period Start
	periodStart = FlowEventPeriod['s']
	ep['periodStart'] = {'value':FlowEventPeriod['s']}
	ep['periodStartLocal'] = {'value':Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalDateTimeFromFlowFormat(FlowEventPeriod['fs'],Format = 'yyyy-MM-dd HH:mm:ss')}
	ep['periodStartFormated'] = {'title':'Period Start','name':'Period Start','value':FlowEventPeriod['fs'],'displayOrder':-1}
	
	#Period End
	if 'e' in FlowEventPeriod:
		periodEnd = FlowEventPeriod['e']
		periodEndFormated = FlowEventPeriod['fe']
		periodEndLocal = {'value':Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalDateTimeFromFlowFormat(FlowEventPeriod['fs'],Format = 'yyyy-MM-dd HH:mm:ss')}
	else:
#					periodEnd = system.date.now()
		periodEnd = ''
		periodEndFormated = ''
		periodEndLocal = None
		
	ep['periodEnd'] = {'value':periodEnd}
	ep['periodEndFormated'] = {'value':periodEndFormated}
	ep['periodEndLocal'] = {'value':periodEndLocal}
	eventAttributes = EventAttributes
	#Get Event Attributes
	if eventAttributes is not None:
		eventAttributeValues = FlowEventPeriod['eav']
		for eventAttribute in eventAttributes:
			name = eventAttribute['name']
			name = name.replace(' ','')
			ea = {}
			eventAttributeID = eventAttribute['eventAttributeID']
			ea['displayOrder'] = eventAttribute['displayOrder']
			ea['title'] = eventAttribute['title']
			ea['name'] = eventAttribute['title']
			ea['eventAttributeID'] = eventAttributeID
			ea['readOnly'] = eventAttribute['readOnly']
			ea['value'] = None
			#Get Value
			for eventAttributeValue in eventAttributeValues:
				if eventAttributeID == eventAttributeValue['eaid']:


					
					#pending
					pending = False
					if 'pending' in eventAttributeValue:
						pending = eventAttributeValue['pending']
					ea['pending'] = pending
					
					#preferred
					preferred = True
					if 'p' in eventAttributeValue:
						preferred = eventAttributeValue['p']
					ea['preferred'] = preferred
					
					#versionType
					versionType = ''
					if 'vt' in eventAttributeValue:
						versionType = eventAttributeValue['vt']
					ea['versionType'] = versionType

					logMessage = 'preferred:' + str(preferred) + '------vt:' + str(versionType)
					Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName='',message=logMessage,Debug=debug)
					if not preferred and versionType != 'manualRequest':
						logMessage = 'skip!'
						Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=logMessage,Debug=debug)
						continue

					#version
					version = 1
					if 'ver' in eventAttributeValue:
						version = eventAttributeValue['ver']
					ea['version'] = version
					
					#value
					attributeValueID=None
					if 'avid' in eventAttributeValue:
						attributeValueID = eventAttributeValue['avid']
					
										
					for attributeValue in AttributeValues:
						if attributeValue['id'] == attributeValueID:
							if 'v' in attributeValue:
								ea['value'] = attributeValue['v']
							
					#quality
					ea['quality'] = eventAttributeValue['q']
					
			ep[name] = ea
	#Get Measures
	measures = Measures
	if measures is not None:
		measureValues = FlowEventPeriod['mv']
		for measure in measures:
			name = measure['name']
			name = name.replace(' ','')
			m = {}
			measureID = measure['measureID']
			m['title'] = measure['title']
			m['name'] = measure['title']
			m['measureID'] = measureID
			m['readOnly'] = measure['readOnly']
			m['value'] = None
			m['displayOrder'] = measure['displayOrder']
			m['measureValueID'] = None
			#Get Value
			pending = False
			for measureValue in measureValues:
				#Get Pending
				if not pending and 'pending' in measureValue:
					pending = measureValue['pending']
					
				#Get preferred
				preferred = True
				if 'preferred' in measureValue:
					preferred = measureValue['preferred']
				
				if preferred:
					m['value'] = measureValue['fv']
					m['valueFull'] = measureValue['v']
					m['quality'] = measureValue['q']
					m['measureValueID'] =  measureValue['id']
			m['pending'] = pending		
					
					
			ep[name] = m

	return ep

def getEnumGroupFromFlowDefinition(FlowDefinition,EnumerationArray):
#	#Example Array to be used for now during testing
#	EnumerationArray = [
#						  {"name": "Duration Type","type": "label"},
#						  {"name": "Mode","type": "Dropdown"},
#						  {"name": "State","type": "Dropdown"},
#						  {"name": "Equipment","type": "Dropdown"},
#						  {"name": "Reason","type": "Dropdown"},
#						  {"name": "Reason Code","type": "Dropdown"},
#						  {"name": "Allowed Duration","type": "Dropdown"},
#						  {"name": "Classification","type": "Dropdown"},
#						  {"name": "Raw Reason","type": "Label"}
#						]
#	
	#return 	FlowDefinition				
	eventAttributes = FlowDefinition["formGroups"][0]["eventSchemes"][0]["eventAttributes"]
	EnumerationFilterOrderObject = getEnumerationFilterOrderFromFlowDefinition(eventAttributes)
	eventAttributeIDMapping = {}	
	for eventAttributeObject in eventAttributes:
		eventAttributeObjectAlias =  eventAttributeObject["alias"].replace(" ","")
		filteredAttributeID = eventAttributeObject["formGroupEventSchemeEventAttributeID"]					
		
		filteredAttributeIDKey = "fid"  + str(filteredAttributeID)
		eventAttributeIDMapping[filteredAttributeIDKey] = eventAttributeObjectAlias
	
	enumerationGroupsObject = {}
	enumerationOrdinals = FlowDefinition["enumerationOrdinals"]
	for EnumerationFilterOrderKey in EnumerationFilterOrderObject:
		EnumerationFilterOrder = EnumerationFilterOrderObject[EnumerationFilterOrderKey]
		optionPathsObject = {}
		for eventAttributeAlias in EnumerationFilterOrder:
			for eventAttributeObject in eventAttributes:
				eventAttributeObjectAlias =  eventAttributeObject["alias"]
				if eventAttributeAlias == eventAttributeObjectAlias:
					if ("filterAttributeID" in eventAttributeObject) == False:
						#Parent Attribute just uses enumerationValues
						if "enumerationValues" in eventAttributeObject:
							enumerationValues = eventAttributeObject["enumerationValues"]	
							eventAttributeAliasKey = eventAttributeAlias.replace(" ","")						
							for enumValue in enumerationValues:	
								optionPathObject = {}
								validOptionKey = "oid" + str(enumValue)
								optionPathObject[eventAttributeAliasKey] = enumerationOrdinals[str(enumValue)]									
								optionPathsObject[validOptionKey] = optionPathObject					

						break				
						
					filteredAttributeID = eventAttributeObject["filterAttributeID"]
					filterAttributeAlias = eventAttributeIDMapping["fid" + str(filteredAttributeID)]
					filteredOptions = eventAttributeObject["filteredOptions"]
					for filteredOption in filteredOptions:						
						for eventAttributeEnum in filteredOptions[filteredOption]:
							validOptions = filteredOptions[filteredOption][eventAttributeEnum] 
							for validOption in validOptions:
								validOptionKey = "oid" + str(validOption)
								
								if validOptionKey in optionPathsObject:
									optionPathsObject[validOptionKey][eventAttributeObjectAlias.replace(" ","")] = enumerationOrdinals[eventAttributeEnum]
									optionPathsObject[validOptionKey][filterAttributeAlias] = 	enumerationOrdinals[filteredOption]	
								else:
									optionPathObject = {}
									for alias in EnumerationFilterOrder:
										enumValue = ""
										if alias == eventAttributeAlias:
											enumValue = enumerationOrdinals[eventAttributeEnum]
										elif alias.replace(" ","") == filterAttributeAlias:
											enumValue = enumerationOrdinals[filteredOption]
											
										optionPathObject[alias.replace(" ","")] = enumValue
									optionPathsObject[validOptionKey] = optionPathObject
		optionPathsObject = optionPathsObject.values()
		enumerationGroupsObject[EnumerationFilterOrderKey] = {"enumerationGroup":optionPathsObject,"enumerationFilterOrder":EnumerationFilterOrder}
	return enumerationGroupsObject

def getEnumerationFilterOrderFromFlowDefinition(eventAttributes):
	eventAttributeObjects = {}
		
	def getChildAttribute(filterID,eventAttributes,eventAttributeArray):
		for eventAttribute in eventAttributes:
			if "filterAttributeID" in eventAttribute:
				parentFilterID = eventAttribute["filterAttributeID"]
				selfID = eventAttribute["formGroupEventSchemeEventAttributeID"]				
				if parentFilterID == filterID:
					alias = eventAttribute["alias"]
					eventAttributeArray.append(alias)				
					eventAttributeArray = getChildAttribute(selfID,eventAttributes,eventAttributeArray)
					#break
		return eventAttributeArray
			
	#Find EnumerationFilter Order for all attributes in Form
	for eventAttribute in eventAttributes:
		if ("filterAttributeID" in eventAttribute) == False:
			#Attribute is Parent Attribute
			eventAttributeArray = [eventAttribute["alias"]]
			filterID = eventAttribute["formGroupEventSchemeEventAttributeID"]
			filterIDKey = "pid" + str(filterID)
			
			eventAttributeArray = getChildAttribute(filterID,eventAttributes,eventAttributeArray)
			eventAttributeObjects[filterIDKey] = eventAttributeArray		
	
	return eventAttributeObjects	

	
def getColumnInstance(field,header,visible,editable = False,Width = "",render={'datatype':'auto','numberFormat':'0.0','dateFormat':'YYYY/MM/DD HH:mm:ss'}):

	columnInstance = {
				  "field": field,
				  "visible": visible,
				  "editable": editable,
				  "render": render['datatype'],
				  "justify": "auto",
				  "align": "center",
				  "resizable": True,
				  "sortable": False,
				  "sort": "none",
				  "viewPath": "",
				  "viewParams": {},
				  "boolean": "checkbox",
				  "number": "value",
				  "progressBar": {
					"max": 100,
					"min": 0,
					"bar": {
					  "color": "",
					  "style": {
						"classes": ""
					  }
					},
					"track": {
					  "color": "",
					  "style": {
						"classes": ""
					  }
					},
					"value": {
					  "enabled": True,
					  "format": "0,0.##",
					  "justify": "center",
					  "style": {
						"classes": ""
					  }
					}
				  },
				  "toggleSwitch": {
					"color": {
					  "selected": "",
					  "unselected": ""
					}
				  },
				  "numberFormat": render['numberFormat'],
				  "dateFormat": render['dateFormat'],
				  "width": Width,
				  "strictWidth": False,
				  "header": {
					"title": header,
					"justify": "left",
					"align": "center",
					"style": {
					  "classes": ""
					}
				  },
				  "footer": {
					"title": "",
					"justify": "left",
					"align": "center",
					"style": {
					  "classes": ""
					}
				  },
				  "style": {
					"classes": ""
				  }
				}
	return columnInstance

def UpdateEventAttributeValues(Connection,Username,EventPeriod,EventAttributeValues):
	logger = system.util.getLogger("UpdateEventAttribute")
	#Get Connection if None
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
	token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
	API = Connection["Private API"] #http://Localhost:4501/flow-software/flow/instances/CFB7C6FD-ADE3-4617-BE09-929561277339/server/api
	
	eventSchemeID = EventPeriod['eventSchemeID']['value']
	eventPeriodID = EventPeriod['eventPeriodID']['value']
	token = "token=" + token
	responses = []
	

	for eventAttributeValue in EventAttributeValues:
		
		if 'eventAttributeID' in eventAttributeValue:
			eventAttributeID = eventAttributeValue['eventAttributeID']
		else:
			eventAttributeName = eventAttributeValue['name']
			eventAttributeNameKey = eventAttributeName.replace(' ','')
			eventAttribute = EventPeriod[eventAttributeNameKey]	
			eventAttributeID = eventAttribute['eventAttributeID']
		value = eventAttributeValue['value']
		url = API + "/data/eventSchemes/"+ str(eventSchemeID) + "/eventPeriods/"+ str(eventPeriodID) +"/eventAttributes/"+ str(eventAttributeID) + "/eventAttributeValues"
		payload = {"eaid":eventAttributeID,
				  "av":{"v":value},
				  "q":192}
		  
		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Post(url,HeaderValues={"Cookie":token},PostData = payload)
		responses.append(response)
		
	return responses


def Update(BIData,FlowData,Username,Connection=None):
	logger = system.util.getLogger("Flow Event Update")
	#Get Connection if Blank
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
	
	print Connection
	api = Connection["Private API"]
	token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
	if not token['valid']:
		return 'Invalid for Username:' + Username
	token = token['token']
	
	header = {'Cookie':'token='+token}
	print header
	mappingDefinition = BusinessInterface.ShopOrder.getFlowMappingDefinition()

	message = 'Event Update....'
	print message
	logger.info(message)
	#print mappingDefinition
	
	#Use This only for Test
#	bIData = system.util.jsonEncode(BIData)
#	flowData = system.util.jsonEncode(FlowData)
#	result = system.tag.writeBlocking(['[CVP]CVP03 Filmatic 1 5L Line/BIData','[CVP]CVP03 Filmatic 1 5L Line/FlowData'],[str(bIData),str(flowData)])
#	logger.info('Event Update....' + str(result))	
	
	
	eventPeriodID = FlowData['eventPeriodID']['value']
	eventSchemeID = FlowData['eventSchemeID']['value']
	#Get Mapping Fields
	posts = []
	
	for map in mappingDefinition:
		if 'flow' in mappingDefinition[map]:
			print map
			#Get BIData
			value = BIData[map]
			print value
			#Get Flow Info
			
			flowKey = mappingDefinition[map]['flow'].replace(' ','')
			detail = FlowData[flowKey]
			#Check if 'Manual or Retrieved'
			readOnly = detail['readOnly']
			if not readOnly:
				#print detail
				eventAttributeID = detail['eventAttributeID']
				url = api + "/data/eventSchemes/"+ str(eventSchemeID) + "/eventPeriods/"+ str(eventPeriodID) +"/eventAttributes/"+ str(eventAttributeID) + "/eventAttributeValues"
				payload = {'eaid':eventAttributeID,'av':{'v':str(value)},'q':192}
				print payload
				post = {'url':url,'payload':payload,'header':header}
				posts.append(post)
			
	
	print posts
	for post in posts:
		url = post['url']
		print url
		headerValues = header
		payload = post['payload']
		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Post(url,HeaderValues=headerValues,PostData=payload)
		print response
		logger.info(str(response))
	
	
	message = 'Event Update....Done!'
	print message
	logger.info(message)
	status = 'Ok'
	data = GetDataFromForm(Connection,6,Username)
	logger.info(str(data))
	return status

def getFormOptions(Connection,FormID):
	if Connection is None:
		Connection	= Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection(ConnectionTagPath=None)
		
	definition = GetFlowDefinitionFromForm(Connection,FormID)
	#print definition[]
	value = definition['formGroups'][0]['eventSchemes'][0]['eventAttributes']
	enumerationOrdinals = definition['enumerationOrdinals']
	def getEnumValue(ordinal):
		enumValue = {}
		for id in enumerationOrdinals:			
			if str(id) == str(ordinal):
				#return type(ev)
				enumValue = {'id':id,'value':enumerationOrdinals[id]}
		return enumValue
	
	def getFilteredOptions(filteredOptions):
		options = {}
		for filterOption in filteredOptions:
			option = getEnumValue(filterOption)
			optionkey = option['value']
			optionkey = optionkey.replace(' ','')
			childOptions = getOptions(filteredOptions[filterOption])
			option['options'] = childOptions
			options[optionkey] = option
		return options
		
	def getOptions(filteredOptions):
		options = []
		for filterOption in filteredOptions:
			childOption = getEnumValue(filterOption)
			optionkey = childOption['value']
			optionkey = optionkey.replace(' ','')
			#selections = filteredOptions[filterOption]
	#			enumValues = []
	#			for selection in selections:
	#				enumValue = getEnumValue(selection)
	#				enumValues.append(enumValue)
	#				
	#			childOption['enumValues'] = enumValues
			options.append(childOption['value'])	
			#childOptions[optionkey] = childOption
		return options
	
	eventAttributesObject = {}
	for eventAttribute in value:
		if 'enumerationValues' in eventAttribute:
			eventAttributeObject = {}
			#formGroupEventSchemeEventAttributeID
			#Get Filtered Column
			if 'filterAttributeID' in eventAttribute:
				filterAttributeID = eventAttribute['filterAttributeID']
				
				for  filteredEventAttribute in value:
					#return 'koos' 
					if filterAttributeID == filteredEventAttribute['formGroupEventSchemeEventAttributeID']:
						eventAttributeObject['filteredOn'] = filteredEventAttribute['alias']
						#return 'koos' 
			
			#Get Filtered Option
			filteredOptions = eventAttribute['filteredOptions']
			eventAttributeObject['filteredOptions'] = getFilteredOptions(filteredOptions)
		
			
			enumerationValues = eventAttribute['enumerationValues']
			#AllOptions
			allOptions = []
			name = eventAttribute['alias']
			key = name.replace(' ','')
			for ev in enumerationValues:
					option = getEnumValue(ev)
					allOptions.append(option)
							
			eventAttributeObject['name'] = name
			eventAttributeObject['allOptions'] = allOptions
			
			#Filtered Options:
			
			filteredOptions = eventAttribute['filteredOptions']
			
			eventAttributesObject[key] = eventAttributeObject		
	

	return eventAttributesObject

def CreateEvent(periodStart, periodEnd, esid, ep, Connection, Username):
#		periodStart = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(Timestamp=None)
#		periodStart = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(periodStart)
#		print periodStart
#		esid = 1
#		ep = {}
#		
#		ep["epid"] = 15468
#		ep["idx"] = 1
#		ep["s"] = "2021-10-25T14:47:55.839Z"
#		Username = "advansys"
#		
#		Flow.Event.CreateEvent(periodStart=periodStart, periodEnd=None, 
#		esid=esid, ep=ep, Connection=None, Username=Username)
		logger = system.util.getLogger("Flow Event Update")
		#Get Connection if Blank
		if Connection is None:
			Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
		
		print Connection
		api = Connection["Private API"]
		token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)		
		if not token['valid']:
			return 'Invalid for Username:' + Username
		token = token['token']
		header = {'Cookie':'token='+token}
		print header
	
		message = 'Create Event....'
		print message
		logger.info(message)
		
		eventSchemeID = esid
		eventPeriodID = ep["epid"]
		eventIndex = ep["idx"]
		epPeriodStart = ep["s"]
	
		url = api + "/data/eventSchemes/"+ str(eventSchemeID) + "/eventPeriods"
		payload = {'idx':eventIndex,'esid':eventSchemeID,'s':periodStart, 'e': periodEnd}

		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Post(url,HeaderValues=header,PostData=payload)
		
	
		message = 'Create Event...Done!'
		print message
		logger.info(message)
	
		return response
#----------------------------------------------------------------------SplitEvent----------------------------------------------------------------------
def SplitEvent(Connection,Username, EventPeriod ,SplitTimeStamp):
#		periodStart = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(Timestamp=None)
#		periodStart = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(periodStart)
#		print periodStart
#		esid = 1
#		ep = {}
#		
#		ep["epid"] = 15468
#		ep["idx"] = 1
#		ep["s"] = "2021-10-25T14:47:55.839Z"
#		Username = "advansys"
#		
#		Flow.Event.SplitEvent(periodStart=periodStart, periodEnd=None, 
#		esid=esid, ep=ep, Connection=None, Username=Username)
		loggerName = "Flow Event Split"
		#Get Connection if Blank
		if Connection is None:
			Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
		
		api = Connection["Private API"]
		token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
		if not token['valid']:
			return 'Invalid for Username:' + Username
		token = token['token']
		
		header = {'Cookie':'token='+token}
	
		message = 'Split Event....'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		
		eventSchemeID = EventPeriod['eventSchemeID']['value']
		eventPeriodID = EventPeriod["eventPeriodID"]['value']
		eventIndex = EventPeriod["index"]['value']
		epPeriodStart = EventPeriod["periodStart"]['value']
		epPeriodEnd = EventPeriod["periodEnd"]['value']
		if epPeriodEnd != '':
			epPeriodEnd = EventPeriod["periodEnd"]['value']
		
	
		url = api + "/data/eventSchemes/"+ str(eventSchemeID) + "/eventPeriods/"+ str(eventPeriodID) + "/split"
		
		splitTimeStampUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(SplitTimeStamp)
		splitTimeStampUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(splitTimeStampUTC)
		payload = [
		{'idx':eventIndex,'esid':eventSchemeID,'s':epPeriodStart, 'e': splitTimeStampUTC}, 
		{'idx':eventIndex+1,'esid':eventSchemeID,'s':splitTimeStampUTC}]
		if epPeriodEnd is not None:
			payload[1]['e'] = epPeriodEnd
		
		print payload
		postData = payload
		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Post(url,HeaderValues=header,PostData=postData)
		if response['error']:
			message = 'Split Event...Done With Error!'
			Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
			return response
			
		message = 'Split Event...Done!'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		eventPeriods = []
		json = response['json']
		for flowEventPeriod in json:
			print flowEventPeriod
			eventPeriod = GetDataFromFlowEventPeriod(FlowEventPeriod=flowEventPeriod)
			#print eventPeriod
			eventPeriods.append(eventPeriod)
		return eventPeriods

#----------------------------------------------------------------------SplitCurrentEvent----------------------------------------------------------------------	
def SplitCurrentEvent(Connection, Username,FormID,SplitTimeStamps,Period=None):
	#Get Current Event Detail
	data = GetDataFromForm(Connection,Username,FormID,DefinitionFormGroup=None,Period=Period)
	if 'error' in data:
		return data
	#print data
	for eventPeriod in data:
		periodEnd = eventPeriod['periodEnd']['value']
		#print periodEnd
		if periodEnd == '':
			#eventPeriods = SplitEvent(Connection=Connection,Username=Username, EventPeriod=eventPeriod ,SplitTimeStamp=SplitTimeStamp)
			eventPeriods = SplitEventInMultipleEvents(Connection=Connection,Username=Username, EventPeriod=eventPeriod ,SplitTimeStamps=SplitTimeStamps)
			return eventPeriods
			
	return 'No Current Event Found!'

#----------------------------------------------------------------------SplitEventInMultipleEvents----------------------------------------------------------------------
def SplitEventInMultipleEvents(Connection,Username, EventPeriod ,SplitTimeStamps):
		loggerName = "Flow Split Event In Multiple Events"
		message = 'EventPeriod:' + str(EventPeriod)
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		#Get Connection if Blank
		if Connection is None:
			Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
		
		api = Connection["Private API"]
		token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
		if not token['valid']:
			return 'Invalid for Username:' + Username
		token = token['token']
		
		header = {'Cookie':'token='+token}
	
		message = 'Starting....'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=debug)
		
		eventSchemeID = EventPeriod['eventSchemeID']['value']
		eventPeriodID = EventPeriod["eventPeriodID"]['value']
		eventIndex = EventPeriod["index"]['value']
		epPeriodStart = EventPeriod["periodStart"]['value']
		epPeriodEnd = EventPeriod["periodEnd"]['value']
		if epPeriodEnd == '':
			epPeriodEnd = None
		
	
		url = api + "/data/eventSchemes/"+ str(eventSchemeID) + "/eventPeriods/"+ str(eventPeriodID) + "/split"
		newEvents = []
		i=0
		numberOfSplits = len(SplitTimeStamps)
		epNewPeriodStart = epPeriodStart
		for splitTimeStamp in SplitTimeStamps:
			splitTimeStampUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(splitTimeStamp)
			splitTimeStampUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(splitTimeStampUTC)
			epNewPeriodEnd = splitTimeStampUTC
			newEvent = {'idx':eventIndex+i,'esid':eventSchemeID,'s':epNewPeriodStart,'e':splitTimeStampUTC}
			newEvents.append(newEvent)
			numberOfSplits = numberOfSplits-1
			epNewPeriodStart = epNewPeriodEnd
			#Process Last Spilt
			if numberOfSplits==0:
				lastEvent = {'idx':eventIndex+i+1,'esid':eventSchemeID,'s':epNewPeriodStart}
				if epPeriodEnd is not None:
					lastEvent['e'] = epPeriodEnd
				newEvents.append(lastEvent)
			
			i=i+1
			
		payload = newEvents
		#return newEvents
		print payload
		postData = payload
		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Post(url,HeaderValues=header,PostData=postData)
		if response['error']:
			message = 'Split Event...Done With Error!' + str(response)
			Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
			message = 'Split Event...Done With Error: PostData:' + str(postData)
			Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
			return response
			
		message = 'Split Event...Done!'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=debug)
		eventPeriods = []
		json = response['json']

		for flowEventPeriod in json:
			print flowEventPeriod
			eventPeriod = GetDataFromFlowEventPeriod(FlowEventPeriod=flowEventPeriod,AttributeValues=[])
			#print eventPeriod
			eventPeriods.append(eventPeriod)
		return eventPeriods


#----------------------------------------------------------------------DeleteEventPeriods----------------------------------------------------------------------
def DeleteEventPeriods(Connection,Username, EventPeriods):
	loggerName = 'DeleteEventPeriods'
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
	
	api = Connection["Private API"]
	headerValues = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDefaultHeader(Connection,Username)
	responses = []
	for eventPeriod in EventPeriods:
		eventSchemeID = eventPeriod['eventSchemeID']['value']
		eventPeriodID = eventPeriod["eventPeriodID"]['value']
		url = api + "/data/eventSchemes/"+ str(eventSchemeID) + "/eventPeriods/"+ str(eventPeriodID)
		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Delete(url,HeaderValues=headerValues,PostData={})
		if response['error']:
			message = 'Delete Event...Error!'
			Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		responses.append(response)
	return responses

#----------------------------------------------------------------------DeleteEventPeriods----------------------------------------------------------------------
def UpdateEventPeriods(Connection,Username, EventPeriods):
	loggerName = 'UpdateEventPeriods'
	Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(loggerName,'Starting...',Debug=True)
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
	
	api = Connection["Private API"]
	headerValues = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDefaultHeader(Connection,Username)
	responses = []
	for eventPeriod in EventPeriods:
		eventSchemeID = eventPeriod['eventSchemeID']['value']
		eventPeriodID = eventPeriod["eventPeriodID"]['value']
		index = eventPeriod["index"]["value"]
		eventPeriodStart = eventPeriod["periodStart"]['value']
		eventPeriodEnd = eventPeriod["periodEnd"]['value']
		if eventPeriodEnd == '':
			eventPeriodEnd = None
		
		url = api + "/data/eventSchemes/"+ str(eventSchemeID) + "/eventPeriods/"+ str(eventPeriodID)
		data = {'id': eventPeriodID, 'idx': index, 's': eventPeriodStart, 'e': eventPeriodEnd}
		message = 'postData:' + str(data)
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Put(url,HeaderValues=headerValues,Data=data)
		if response['error']:
			message = 'Update EventPeriods...Error!'
			Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		responses.append(response)
	Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(loggerName,'Done!')
	return responses



################################################Examples#################################################################################

################################################Connect################################################################################
#connection = None
#username = "braam"
##Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Connect(ConnectionTagPath=None,Username=username,Password='')
#
#
################################################GetUTCTime##############################################################################
#periodStartUTC = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUTCTime(LocalTimestamp=None)
#print periodStartUTC
#
################################################GetDateTimeFormat#######################################################################
#periodStartUTCFormated = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetDateTimeFormat(periodStartUTC)
#print periodStartUTCFormated
#
#
	################################################GetDataFromForm#########################################################################
	#formID = 9
	#formGroupData = Flow.Event.GetDataFromForm(Connection=connection,Username=username,FormID=formID, DefinitionFormGroup=None,Period=None)
	#print formGroupData
	#
################################################SplitEvent##############################################################################
#eventPeriod = formGroupData[0]
#splitTimeStamp = system.date.addHours(system.date.now(),-6)
#print splitTimeStamp
#eventPeriods = Flow.Event.SplitEvent(Connection=connection,Username=username, EventPeriod=eventPeriod ,SplitTimeStamp=splitTimeStamp)
#print eventPeriods
################################################SplitCurrentEvent#######################################################################
#splitTimeStamp = system.date.now()
#eventPeriods = Flow.Event.SplitCurrentEvent(Connection=connection,Username=username, FormID = formID,SplitTimeStamp=splitTimeStamp)
#print eventPeriods

###############################################UpdateEventAttributeValues###############################################################
#formID = 9
#eventAttributeName = 'Work Order'
#attributeValue = 'WO563'
#formGroupData = Flow.Event.GetDataFromForm(Connection=connection,Username=username,FormID=formID, DefinitionFormGroup=None,Period=None)
#eventPeriod = formGroupData[0]
#eventAttributeName = 'Work Order'
#eventAttributeNameKey = name.replace(' ','')
#eventAttribute = eventPeriod[eventAttributeNameKey]
#eventAttributeID = eventAttribute['eventAttributeID']
#print eventAttributeID
#eventAttributeValues = []
#eventAttributeValue = {}
#eventAttributeValue['eventAttributeID'] = eventAttributeID
#eventAttributeValue['value'] = attributeValue
#eventAttributeValues.append(eventAttributeValue)
#response = Flow.Event.UpdateEventAttributeValues(Connection=connection,Username=username,EventPeriod=eventPeriod,EventAttributeValues=eventAttributeValues)
#print response
		 



