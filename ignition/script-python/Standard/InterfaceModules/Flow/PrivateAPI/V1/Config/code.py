debug = False
def GetEnums(Connection,Username):
	logggerName = "Flow.Config.GetEnums"
	api = Connection['Private API']
	url = api + '/v1/config/enumerations'
	token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
	token = token['token']
	headerValues = {'Cookie':'token=' + token}	
	response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Get(url=url,HeaderValues=headerValues)
	if response['error']:
		message = 'GetEnums...Error!'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=debug)
		return response
	json = response['json']
	print json
	return json['enumerations']
	
def getEnum(Connection,Username,Id):
	logggerName = "Flow.Config.getEnum"
	api = Connection['Private API']
	url = api + '/v1/config/enumerations/'+str(Id)
	#print url
	token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
	headerValues = {'Cookie':'token=' + token['token']}
	response = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Get(url=url,HeaderValues=headerValues)
	if response['error']:
		message = 'getEnum...Error!'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		return response
	json = response['json']
	return json['enumeration']
		
def GetEnum(Connection,Username,Name):
	if Connection == None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection()
	enums = GetEnums(Connection=Connection,Username=Username)
	id = -1
	for enum in enums:
		#print enum['name']
		if enum['name'] == Name:
			return getEnum(Connection,Username,enum['id'])
	
	return 'Not Found'


def GetEnumGroups(Connection,Username):
	logggerName = "Flow.Config.GetEnums"
	api = Connection['Private API']
	url = api + '/v1/config/enumerationgroups'
	token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
	headerValues = {'Cookie':'token=' + token['token']}	
	response = Standard.InterfaceModules.Flow.Common.Get(url=url,HeaderValues=headerValues)
	if response['error']:
		message = 'GetEnums...Error!'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		return response
	json = response['json']
	return json['enumerationGroups']
	
def getEnumGroup(Connection,Username,Id):
	logggerName = "Flow.Config.getEnum"
	api = Connection['Private API']
	url = api + '/v1/config/enumerationgroups/'+str(Id)
	#print url
	token = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetTokenForUser(Connection,Username)
	headerValues = {'Cookie':'token=' + token['token']}
	response = Standard.InterfaceModules.Flow.Common.Get(url=url,HeaderValues=headerValues)
	if response['error']:
		message = 'getEnumGroup...Error!'
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage(LoggerName=loggerName,message=message,Debug=True)
		return response
	json = response['json']
	return json['enumerationGroup']
		
def GetEnumGroup(Connection,Username,Name):
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection(ConnectionTagPath=None)
	enumGroups = GetEnumGroups(Connection,Username)
	id = -1
	for enum in enumGroups:
		#print enum['name']
		if enum['name'] == Name:
			return getEnumGroup(Connection,Username,enum['id'])
	
	return 'Not Found'
