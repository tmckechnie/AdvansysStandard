HttpClient = None

#----------------------------------------GetClient----------------------------------------
def GetClient(Timeout = 120000):
	#Create an http Client to be used for all requests within a script
	#Timeout refers to the Connect Timeout
	global HttpClient
	HttpClient = system.net.httpClient(timeout = Timeout)
	return
#----------------------------------------GetHttpBasicAuthenticationValue----------------------------------------
def GetHttpBasicAuthenticationValue(Username,Password):
	username = Username
	password = Password
	
	import base64
	authString = username+":"+password
	authStringBytes = authString.encode("ascii")
	base64Bytes = base64.b64encode(authStringBytes)
	return base64Bytes

#----------------------------------------ClientGet-------------------------------------------------
def ClientGet(Url,Headers,Timeout = 120000):	
	if HttpClient is None:
		GetClient(Timeout=Timeout)	
	response = HttpClient.get(url=Url,headers = headers,timeout = Timeout)	
	return response
#----------------------------------------ClientPost-------------------------------------------------	
def ClientPost(Url,Data,Headers,Timeout = 120000):	
	if HttpClient is None:
		print 'Create new Client...'
		GetClient(Timeout=Timeout)
	response = HttpClient.post(url=Url,data=Data,headers=Headers,timeout = Timeout)	
	return response
#----------------------------------------ClientPut-------------------------------------------------	
def ClientPut(Url,Data,Headers,Timeout = 120000):	
	if HttpClient is None:
		print 'Create new Client...'
		GetClient(Timeout=Timeout)
		#print str(HttpClient)
	print 'ClientPut Payload:' + str(Data)
	response = HttpClient.put(url=Url,data = Data,headers=Headers,Timeout = Timeout)	
	return response
#----------------------------------------ClientDelete-------------------------------------------------		
def ClientDelete(Url,Data,Headers,Timeout = 120000):	
	if HttpClient is None:
		print 'Create new Client...'
		GetClient(Timeout=Timeout)
	response = HttpClient.delete(url,data = Data,headers=headers,timeout = timeout)	
	return response



	
	
	
	