def doGet(request, session):
	loggerName = "WebDev: Example/API/V1/HelloWorld (GET)"
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Request:' + str(request))
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Parameters:' + str(request['params']))
	params = request['params']
	returnType = ''
	if 'ReturnType' in params:
		returnType = params['ReturnType']

	
	if returnType == 'html':
		return {'html': '<html><body>Hello World Send Me Somethng</body></html>'}
	elif returnType == 'json':
		return {'json': {'value':'Hello World Send Me Somethng'}}
	else:
		return {'html': "<html><body>Need ReturnType in url Parameters eg: '?ReturnType=html' or ?ReturnType=json'</body></html>"}