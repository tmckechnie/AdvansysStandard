client = None
version = 'v1'
#------------------------------------------------------------------------GetClient-----------------------------------------------
def GetClient():
	global client
	if client is None:
		#return None
		client = system.net.httpClient()
	return client

##------------------------------------------------------------------------GetAPIBaseUrl-----------------------------------------------
#def GetAPIBaseUrl(type='data'):
#	url = 'http://pscv01001vs1:8079/api/v1/'+type+'/'
#	return url

##------------------------------------------------------------------------GetToken-----------------------------------------------
#def GetToken():
#	bearerToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBMkMwNjA2Ni03MDA1LTQzMEYtOEFCQS00MkYzOUUwNjc1QzQiLCJleHAiOjE5NjUwMzY4NTIsImlzcyI6Imh0dHBzOi8vUFNDVjAxMDAxVlMxL2Zsb3ctc29mdHdhcmUvZmxvdy9pbnN0YW5jZXMvQjY2RUNFQTQtRkEyQy00M0Q4LUE3NTAtQzU4RDQzNDA2OUQ1L3NlcnZlci8iLCJhdWQiOiJCNjZFQ0VBNC1GQTJDLTQzRDgtQTc1MC1DNThENDM0MDY5RDUifQ.51Yh6rBnSU0Se_KQyavYQrzCOH5a8agbvKN0I47aq24'
#	return bearerToken

def GetUTCTime(TimestampLocal):
	timezoneOffset = int(-1*system.date.getTimezoneOffset(TimestampLocal))
	return system.date.addHours(TimestampLocal, timezoneOffset)

def GetLocalTime(TimestampUTC):
	timezoneOffset = int(system.date.getTimezoneOffset(TimestampUTC))
	return system.date.addHours(TimestampUTC, timezoneOffset)
#------------------------------------------------------------------------GetDateTimeFormat-----------------------------------------------
def GetDateTimeFormat(Timestamp,UTC=True):
	if UTC:
		return system.date.format(Timestamp,"yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
	return system.date.format(Timestamp,"yyyy-MM-dd'T'HH:mm:ss.SSS")

#------------------------------------------------------------------------GetLocalDateTimeFromFlowFormat-----------------------------------------------	
def GetLocalDateTimeFromFlowFormat(DateTime,Format = 'yyyy-MM-dd HH:mm:ss'):
	dateTime = system.date.parse(dateTime,Format)
	return dateTime
#------------------------------------------------------------------------GetLocalDateTimeFromFlowFormat-----------------------------------------------	
def GetLocalDateTimeFromFlow(DateTimeUTC,Format = 'yyyy-MM-dd HH:mm:ss'):
	dateTimeUTC = DateTimeUTC.replace('T',' ').replace('Z','')
	format = Format
	dateTimeUTC = system.date.parse(dateTimeUTC,format)
	dateTime = GetLocalTime(dateTimeUTC)
	
	return dateTime
#------------------------------------------------------------------------interfaceResponse-----------------------------------------------
def interfaceResponse(response):
	if response.good:
		try:
			json = response.json
			return {'error':False,'json':json,'headers':response.headers}
		except ValueError:	
			if '<!doctype html>' in str(response.text):
				message = 'Not A Valid Response for url'
				return {'error':True,'json':{},'message':message}
			else:
				message = 'Not A Valid Response'
				message = message + ' -- Response:' + str(response.text)
				return {'error':True,'json':{},'message':message}
	#return system.util.jsonEncode(response.json)
	else:
		statusCode = response.getStatusCode()
		message = str(statusCode) + ':Unknown'
		if statusCode == 401:
			message = '401:Unauthorized'
		if statusCode == 404:
			message = '404:Not Found'
			
		text = response.getText()

		if text != '':
			text = system.util.jsonDecode(text)
			#print text
			if 'text' in str(text):
				message = message + " - Text:" + str(text)
		return {'error':True,'json':{},'statusCode':statusCode,'message':message}
#------------------------------------------------------------------------Get-----------------------------------------------	
def Get(url,HeaderValues={}):
	global client
	if client is None:
		GetClient()
	try:
		response = client.get(url,headers = HeaderValues)
	except:
		return {'error':True,'json':{},'statusCode':404,'message':'Not Found'}
	
	return interfaceResponse(response)
#------------------------------------------------------------------------GetFromConnection-----------------------------------------------	
def GetFromConnection(ConnectionTagPath,EndPoint,HeaderValues=None):
	global client
	if client is None:
		GetClient()
	try:
		connection = GetConnection(ConnectionTagPath=ConnectionTagPath)
		publicAPI = connection['Public API']
		headers = HeaderValues
		if headers is None:
			headers = GetPublicHeader(Connection=connection)
		url = publicAPI + '/' + EndPoint
		response = client.get(url,headers = headers)
	except:
		return {'error':True,'json':{},'statusCode':404,'message':'Not Found'}
	
	return interfaceResponse(response)
#------------------------------------------------------------------------GetDefaultPublicHeader-----------------------------------------------
def GetPublicHeader(Connection):
	publicKey = Connection['PublicKey']
	headers = {"Authorization": "Bearer " + publicKey}
	return headers

#===============================================GetConnection===============================================
def GetConnection(ConnectionTagPath):
	Connection = system.tag.readBlocking([ConnectionTagPath])[0].value
	Connection = system.util.jsonDecode(str(Connection))
	return Connection
#------------------------------------------------------------------------GetConnectionStatus------------------------------------------------------------
def GetConnectionStatus(ConnectionPath):
	client = GetClient()
	connection = GetConnection(ConnectionTagPath=ConnectionPath)
	publicAPI = connection['Public API']
	publicKey = connection['PublicKey']
	url = publicAPI + '/'+version+'/config/calendars'
	headerValues = {"Authorization": "Bearer " + publicKey}
	print url
	result = Get(url=url,HeaderValues=headerValues)
	if result['error']:
		return result
	else:
		return 'Connected'
