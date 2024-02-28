#API Info
version='v1'
#General Exceptions
import java.lang.Exception as Exception 
import java.io.IOException as IOException
#import java.io.InterruptedIOException as InterruptedIOException

#httpClient High Level Exceptions
import java.net.http.HttpTimeoutException as Timeout
import java.net.http.HttpConnectTimeoutException as ConnectTimeout
import java.net.http.WebSocketHandshakeException as WebSocketHandshakeException

#General Socket Timeout
import java.net.SocketTimeoutException as SocketTimeout

#client = system.net.httpClient()
client = None
#===============================================GetClient===============================================
def GetClient():
	global client
	if client is None:
		#return None
		client = system.net.httpClient()
	return client

connectionTagPath = '[default]Flow/CCBZA10/Connection'
usersDetailTagPath = '[default]Flow/CCBZA10/UsersDetail'
#===============================================GetDefaultConnectionPath===============================================-
def GetDefaultConnectionPath():
	return connectionTagPath

#===============================================GetConnection===============================================
def GetConnection(ConnectionTagPath=None,Connection=None):
	if Connection is not None:
		return Connection
	if ConnectionTagPath is None:
		ConnectionTagPath = connectionTagPath
	Connection = system.tag.readBlocking([ConnectionTagPath])[0].value
	Connection = system.util.jsonDecode(str(Connection))
	return Connection

#===============================================JsonArrayLookup===============================================
def JsonArrayLookup(JsonArray,LookupKey,LookupValue,ValueKey):
		jsonArray = system.util.jsonDecode(str(JsonArray))
		for item in jsonArray:
			print type(item)
			lookupValue = item[LookupKey]
			if lookupValue == LookupValue:
				if ValueKey == "*": #return item
					return system.util.jsonEncode(item)
				else:
					return system.util.jsonEncode({ValueKey:item[ValueKey]})
				#print token
	
		return system.util.jsonEncode({'error':'Item Not Found for :' + str(LookupValue)})

#===============================================GetUserDetails===============================================
def GetUserDetails(Connection,Username=None,Token=None):
		connection = GetConnection(ConnectionTagPath=None,Connection=Connection)
		token = Token
			
		#Get User Details
		api = connection['Public API']
		url = api+ "/token"
		headers = {
		  'Content-Type': 'application/json',
		  'Cookie': 'token=' + token
		}
		response = Get(url,headers)
		json = response['json']
		if 'n' in json and 'id' in json and 'p' in json: #check if valid response
			username = json['n'].lower().replace('\\','')		
			properties = json['p']
			props = {}
			for prop in properties:
				propName = prop['n']
				value = None
				if 'v' in prop:
					value = prop['v']
				props[propName] = value
			return {'username':username,'properties':props}
		else:
			return {'error':'Connot get user details:' + str(json)}
#===============================================GetTokenForUser===============================================		
def GetTokenForUser(Connection,UserInformation,Username,Validate=True,ConnectionTagPath = None):
	connection = GetConnection(ConnectionTagPath=None,Connection=Connection)
	userDetail = UserInformation
	username = Username.lower().replace('\\','')		
	logger = system.util.getLogger("GetTokenForUser")
	if userDetail is not None:
		#check expiry
		dateExpiry = system.date.parse(userDetail["Interfaces"]["Flow"]["Expires"])
		now = system.date.now()
		expired = system.date.isAfter(now,dateExpiry)
		logger.info("expired:  " + str(expired) + " expired date:  " +str(dateExpiry))
		if expired :
			userDetail["Interfaces"]["Flow"]['Valid'] = False
			return userDetail
		
		if Validate: #See if token is still valid
			api = connection['Private API']
			url = api+ "/token"
			headers = {
			  'Content-Type': 'application/json',
			  'Cookie': 'token='+userDetail["Interfaces"]["Flow"]['Token']
			}
			response = Get(url,headers)
			json = response['json']
			userDetail["Interfaces"]["Flow"]['Valid'] = not (json=={})
			logger.info("Validate json:  " + str(json))
			return userDetail
		else:	
			userDetail["Interfaces"]["Flow"]['Valid'] = True
			return userDetail

	return {'error':'Token not Found for Username:' + username,'Valid':False}	

#===============================================Connect===============================================	
def Connect(ConnectionTagPath,UsersDetailTagPath,Username,Password,Debug=True,Reconnect=False,RolesUserSource = None):
		usernameKey = Username.lower().replace('\\','')				
			
		loggerName = "Flow Connect"
		connection = GetConnection(ConnectionTagPath=ConnectionTagPath)
		UsersInformationTagPath = UsersDetailTagPath + "/Information"
		userinformation = Standard.Model.Common.GetUserInformation(Username,UsersInformationTagPath)
		#LogMessage(LoggerName=loggerName,message=str(userinformation),Debug=Debug)
		LogMessage(LoggerName=loggerName,message="Reconnect: " + str(Reconnect) +  str(not Reconnect),Debug=Debug)
		#Get token if exist and not Expired
		if not Reconnect: #Try using same Token
			LogMessage(LoggerName=loggerName,message="Checking Token is Valid",Debug=Debug)
			userDetail = GetTokenForUser(Connection=connection,UserInformation = userinformation,Username=Username,Validate=True)
			if ("error" in userDetail) == False:
				flowUserTokenValid = userDetail["Interfaces"]["Flow"]["Valid"]
				if flowUserTokenValid:
					message = 'Token still valid'
					LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
					print message
					return usernameKey
		
		#Token either expired or was not Found
		message = 'Token Invalid:Token either expired or was not Found'
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		
		#SaveChanges Summary
		summaryLoggerName = "Flow Connect SaveChangesSummary"
		summaryLoggerLine = ConnectionTagPath	
		summaryLoggerAllocationsLogin= 0
		summaryUsername = usernameKey
		#summaryLoggerEndDate = system.date.toMillis(system.date.now())	
		summaryLoggerStartDate = system.date.toMillis(system.date.now())
		summaryObject = {			
					"username":summaryUsername,
					"line":summaryLoggerLine,
					"allocations":{
							"login":summaryLoggerAllocationsLogin,
									},
					"startDate":summaryLoggerStartDate	,
					"error":{
							"value":False,
							"label":"",
							"reason":""							
								}
						}	
		
		
		message = "Starting Login Process for user: " + str(Username)
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		#logger.info("Connect.....Username:" + Username + " --- Password:" + Password)
		Password = Password.replace("\\","\\\\") # This just makes sure if their password has any "\" that they are made correctly in python
		
		#Python Libraries
		import rsa
		import base64
		#Java Classes

		import javax.crypto.Cipher
		#Creating RSA key with java securities
		import java.security.spec
		import java.math
		import java.security.PublicKey
		import java.security.spec.RSAPublicKeySpec
		import java.security.interfaces.RSAPublicKey
		import java.security.KeyFactory
		import javax.crypto.Cipher
		#Used to save Token to document tag
		from com.inductiveautomation.ignition.common import TypeUtilities
		
		client = GetClient()#requests.session()
		
		#Getting the Public Key
		api = connection['Private API']
		url = api+ "/token/PublicKey"  
		payload = {}
		headers= {}
		
		LogMessage(LoggerName=loggerName,message=str(url),Debug=Debug)
		response = Get(url,headers)
		message = 'Getting the Public Key:' + str(response)
		print message
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		if response['error']:
			message = response['message']
			statusCode = response["statusCode"]
			error = {"Message":message,"Reason":str(statusCode)}
			LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
			#Add Audit Log Summary
			# {'error':True,'json':{},'statusCode':statusCode,'message':message}
			summaryObject["error"]["value"] = True
			summaryObject["error"]["label"] = statusCode
			summaryObject["error"]["reason"] = message
			Standard.InterfaceModules.Flow.Common.LogAudit(summaryObject,usernameKey,auditProfile = "SaveChangesSummary",summaryLogger = False)
			return {'error':error}
		
		
		json = response['json']
		modulus = json["m"] #This is the moduls recieved after using the public key api
		headers = response['headers']
		cookieHeader = headers["Set-Cookie"]#.split(";")
		message = 'PublicKey Recieved with Cookie Header:' + str(cookieHeader)
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		cookie = ""
		#This for loop just strips the cookie with a 1 min expiration for the authentication
		for element in cookieHeader:
			innerelement = element.split(",")	
			for subelement in innerelement:
				innersubelement = subelement.replace(" ","")
				if ("request=" in innersubelement) and (len(innersubelement) > len("request=")):
					cookie = innersubelement
							
		message = 'PublicKey Recieved with Json:' + str(json)
		print message
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		exponent = json["e"]#"AQAB" #This is the exponent recieved after using the public key api
		
		#The following lines are using the modulus and exponent to create the RSA key for encryption of the user password
		
		decoded_modulus = int(base64.b64decode(modulus).encode('hex'), 16)
		decoded_exponent = int(base64.b64decode(exponent).encode('hex'), 16)
		bigInt_modulus = java.math.BigInteger(str(decoded_modulus))
		bigInt_exponent = java.math.BigInteger(str(decoded_exponent))
		#Creating Key with Java securities
		java_securities_publicInfo = java.security.spec.RSAPublicKeySpec(bigInt_modulus,bigInt_exponent)
		kf = java.security.KeyFactory.getInstance("RSA")
		java_securities_publicKey = kf.generatePublic(java_securities_publicInfo)
		java_securitiesencodedKey = java_securities_publicKey.getEncoded()
		java_base64_string = base64.b64encode(java_securitiesencodedKey)
		#Encrypting Password using Public Key
		cipher = javax.crypto.Cipher.getInstance("RSA/ECB/OAEPWithSHA-1AndMGF1Padding")
		cipher.init(1, java_securities_publicKey)
		byte_array_pw = bytearray(str(Password))
		final_encryption = cipher.doFinal(byte_array_pw)
		#print final_encryption
		base64_string = base64.b64encode(final_encryption)
		#print base64_string
		request_cookie = cookie
		url = api + "/token"
		
		# Submit the username and encrypted password (along with stripped cookie in the header) to flow using token api
		payload = "{\r\n    \"username\":\""+Username+"\",\r\n    \"password\":\"%s\"\r\n}"%base64_string
			
		headers = {
		  'Content-Type': 'application/json',
		  'Cookie': request_cookie
		}
		message = 'Requesting Token...'
		print message
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		response = Post(url,headers,payload)
		if response['error']:
			message = response['message']
			statusCode = response["statusCode"]
			error = {"Message":message,"Reason":str(statusCode)}
			LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
			#Add Audit Log Summary
			# {'error':True,'json':{},'statusCode':statusCode,'message':message}
			summaryObject["error"]["value"] = True
			summaryObject["error"]["label"] = statusCode
			summaryObject["error"]["reason"] = message
			#Standard.InterfaceModules.Flow.Common.LogAudit(summaryObject,usernameKey,auditProfile = "SaveChangesSummary",summaryLogger = False)
			return {'error':error}

		#Get Token
		#If authentication successfull then store token in document tag. This token is then used when this user submits any changes to forms/charts
		#The rest of the code is all ignition side and is used to add the token to the document tag.
		
		headers = response['headers']
		cookieHeader = headers["Set-Cookie"]
		message = "Get Token Headers: " + str(headers)
		print message
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		#print cookieHeader
		#This for loop just strips the expires time
		for element in cookieHeader:
			innerelement = element.split("expires=")
			#print element
			for subelement in innerelement:
				#print subelement
				date = ""
				strDate = subelement.split(";")[0]
				try:
					#date = system.date.parse(strDate,'')
					date = system.date.parse(strDate,'E, dd MMM yyyy HH:mm:ss zzz')
				except:
					pass
					#print sys.exc_info()
					
				
				innersubelement = subelement.replace(" ","")
				if ("request=" in innersubelement) and (len(innersubelement) > len("request=")):
					cookie = innersubelement
		
		
		#print "Date:" + str(date)
		json = response['json']
		token = json["token"]
	
		
		#Get tag with Tokens
		newUser = False
		#message = "Existing tokens: " + str(userinformation)
		#LogMessage(LoggerName=loggerName,message=message,Debug=Debug)

		if userinformation is None:
			userinformation = Standard.Model.Common.GetUserInformationObject()
			newUser = True
			
		#Get User Detail		
		flowuserDetails = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetUserDetails(Connection=connection,Username=Username,Token=token)
		properties = None
		if 'error' in flowuserDetails:
			properties = flowuserDetails
		else:
			properties = flowuserDetails['properties']	
			if "Name" in properties:
				userinformation["FullName"] = properties["Name"]
						
		#Save User Details	
		userinformation["Username"] = Username
		userinformation["Interfaces"]["Flow"]["Token"] = token
		userinformation["Interfaces"]["Flow"]["Expires"] = system.date.format(date,'yyyy-MM-dd HH:mm:ss')
		userinformation["Interfaces"]["Flow"]["Valid"] = True
		userinformation["Interfaces"]["Flow"]["Properties"] = properties
		#Get AD Roles and Add to User Details	
		if RolesUserSource is not None:
			userRoles = Standard.InterfaceModules.Flow.Common.GetProjectRoles(Username,Password,ConnectionTagPath,UsersDetailTagPath,ADRoles = None, UserSource = RolesUserSource,summaryObject = summaryObject)
			if "error" in userRoles:
				summaryObject = userRoles["SummaryObject"]
				message = userRoles["error"]
				LogMessage(LoggerName=summaryLoggerName,message=message,Debug=Debug)	
				Standard.InterfaceModules.Flow.Common.LogAudit(summaryObject,usernameKey,auditProfile = "SaveChangesSummary",summaryLogger = True)
				error = {"Message":message,"Reason":""}
				return {'error':error}
			else:
				userRoles = userRoles["roles"]			
				userinformation["Interfaces"]["Flow"]["UserRoles"] = userRoles
		
		updateUserInformation = Standard.Model.Common.UpdateUserInformation(usernameKey,userinformation,UsersInformationTagPath)
		message = "Login Successful: " +str(Username)
		LogMessage(LoggerName=loggerName,message=message,Debug=Debug)
		#Logger Summary	
		summaryObject["allocations"]["login"] += 1		
		#SaveChangesSummary Logger
		message = system.util.jsonEncode(summaryObject)
		LogMessage(LoggerName=summaryLoggerName,message=message,Debug=Debug)	
		#Standard.InterfaceModules.Flow.Common.LogAudit(summaryObject,usernameKey,auditProfile = "SaveChangesSummary",summaryLogger = True)
		return usernameKey
		
#===============================================ClearTokens===============================================
def ClearTokens(ConnectionTagPath):
		tokens = {}
		strtokens = system.util.jsonEncode(tokens)
		tagPath = ConnectionTagPath + "/Tokens"
		system.tag.writeBlocking([tagPath],[strtokens])
		return
#===============================================ClearUsers===============================================		
def ClearUsers(ConnectionTagPath):
		users = {}
		strUsers = system.util.jsonEncode(users)
		tagPath = ConnectionTagPath + "/Users"
		system.tag.writeBlocking([tagPath],[strUsers])
		return
#===============================================interfaceResponse===============================================
def interfaceResponse(response,url):
	if response.good:
		try:
			json = response.json
			return {'error':False,'json':json,'headers':response.headers}
		except ValueError:	
			if '<!doctype html>' in str(response.text):
				message = 'Not A Valid Response for url:' + str(url)
				return {'error':True,'json':{},'message':message}
			else:
				message = 'Not A Valid Response for url:' + str(url)
				message = message + ' -- Response:' + str(response.text)
				return {'error':True,'json':{},'message':message}
	#return system.util.jsonEncode(response.json)
	else:
		statusCode = response.getStatusCode()
		message = str(statusCode) + ': Unknown'
		if statusCode == 401:
			message = '401: Unauthorized'
		elif statusCode == 404:
			message = '404: Not Found'
		elif statusCode == 400:
			message = '400: Bad Request'
		text = response.getText()

		if text != '':
			text = system.util.jsonDecode(text)
			#print text
			if 'text' in str(text):
				message = message + " - Text:" + str(text)
		return {'error':True,'json':{},'statusCode':statusCode,'message':message}

#===============================================Get===============================================
def Get(url,HeaderValues={}):
	global client
	if client is None:
		GetClient()
	response = client.get(url,headers = HeaderValues)

	return interfaceResponse(response,url)

#===============================================Post===============================================
def Post(url,HeaderValues={},PostData={}):
	global client
	if client is None:
		GetClient()
	response = client.post(url,headers = HeaderValues,data = PostData)
	return interfaceResponse(response,url)

#===============================================Put===============================================
def Put(url,HeaderValues={},Data={}):
	global client
	if client is None:
		GetClient()
	response = client.put(url,headers = HeaderValues,data = Data)
	return interfaceResponse(response,url)

#===============================================GetClient===============================================
def Delete(url,HeaderValues={},PostData={}):
	global client
	if client is None:
		GetClient()
	response = client.delete(url,headers = HeaderValues,data = PostData)
	return interfaceResponse(response,url)

#===============================================GetDefaultHeader===============================================
def GetDefaultHeader(Connection,Username):
	token = GetTokenForUser(Connection,Username)		
	if not token['valid']:
		return 'Invalid for Username:' + Username
	token = token['token']
	return {'Cookie':'token='+token}

#===============================================isFlowUTCFormattedEqual==================================
def isFlowUTCFormattedEqual(TimestampUTC1,TimestampUTC2):
	Timestamp1Local = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(TimestampUTC1,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'")		
	Timestamp2Local = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetLocalTimeFromFlowUTCFormatted(TimestampUTC2,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'")	
	isEqual = Timestamp1Local.equals(Timestamp2Local)	
	return	isEqual
	
#===============================================GetLocalTimeFromUTCFormattedTime==================================
#Get Local Timestamp from FlowUTC String
def GetLocalTimeFromFlowUTCFormatted(TimestampUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'"):
	timeStampUTCDateTime = GetLocalDateTimeFromFlowFormat(TimestampUTC,Format)
	offset = int(system.date.getTimezoneRawOffset())
	timeStampLocalDateTime = system.date.addHours(timeStampUTCDateTime,offset)
	return timeStampLocalDateTime
#===============================================GetUTCFormattedTime===============================================
#Get FlowUTC String from Local TimeStamp Datetime
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
#===============================================GetDateTimeFormat================================================
#Format Datetime to a string	
def GetDateTimeFormat(TimestampUTC,Format = "yyyy-MM-dd'T'HH:mm:ss'Z'" ):
	return system.date.format(TimestampUTC,Format)
#===============================================GetLocalDateTimeFromFlowFormat===================================
#Get Datetime using parsing format provided	
def GetLocalDateTimeFromFlowFormat(DateTime,Format = 'yyyy-MM-dd HH:mm:ss'):
	dateTime = system.date.parse(DateTime,Format)
	return dateTime
	
#===============================================LogMessage===================================
	
def LogMessage(LoggerName,message,Debug=True):
	Logger = system.util.getLogger(LoggerName)
	if Debug:
		print message
		Logger.info(message)
	return
#===============================================GetConnectionStatus===============================================
def GetConnectionStatus(ConnectionPath,UsersDetailTagPath=''):
	client = GetClient()
	connection = system.tag.readBlocking([ConnectionPath])[0].value
	connection = system.util.jsonDecode(str(connection))
	privateAPI = connection['Private API']
	username = connection['Username']
	password = connection['Password']
	url = privateAPI + '/token/PublicKey'  
	headerValues = {}
	print url
	result = Get(url=url,HeaderValues=headerValues)
	print result
	if result['error']:
		return result
	else:
		if UsersDetailTagPath != '':
			print 'Check Service User'
			result = Connect(ConnectionTagPath=ConnectionPath,UsersDetailTagPath=UsersDetailTagPath,Username=username,Password=password)
			if 'error' in result:
				return result['error']

		return 'Connected'


	
