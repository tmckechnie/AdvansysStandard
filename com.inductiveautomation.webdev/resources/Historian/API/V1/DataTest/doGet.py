def doGet(request, session):
	loggerName = "WebDev: Historian/API/V1/DataTest (GET)"

	
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Request:' + str(request))
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Parameters:' + str(request['params']))
	params = request['params']
	periodStart = params['PeriodStart'].replace('T',' ')
	periodEnd = params['PeriodEnd'].replace('T',' ')
	periodStart = system.date.parse(periodStart)
	periodEnd = system.date.parse(periodEnd)

	data = []
	for i in range(0,5):
		#print i
		ts = system.date.addMinutes(periodStart,i*10)
		#ts = system.date.addHours(ts,-2) #UTC
		ts = system.date.format(ts,'yyyy-MM-dd HH:mm:ss.SSS')
		point = {"t_stamp":ts,"Value":i*10.00}
		data.append(point)

	
	return {'json': {'data':data}}