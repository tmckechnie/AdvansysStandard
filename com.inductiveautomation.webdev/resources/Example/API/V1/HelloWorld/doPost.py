def doPost(request, session):
	loggerName = "WebDev: Example/API/V1/HelloWorld (POST)"
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Request:' + str(request))
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Parameters:' + str(request['params']))
	data = request['data']
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Data:' + str(data))
	return {'json': data}