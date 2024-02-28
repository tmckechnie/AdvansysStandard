def doGet(request, session):
	periodStart = '2023-01-23 11:00:00'
	periodStart = system.date.parse(periodStart)
	periodStartSeconds = system.date.toMillis(periodStart)/1000.0
	
	
	data = []
	for i in range(0,5):
		#print i
		ts = system.date.addMinutes(periodStart,i*10)
		#ts = system.date.addHours(ts,-2) #UTC
		ts = system.date.format(ts,'yyyy-MM-dd HH:mm:ss.SSS')
		point = {"t_stamp":ts,"Value":i*10.00}
		data.append(point)
#	
#	ts = system.date.format(tsStart,'yyyy-MM-dd HH:mm:ss.SSS')
#	point = {"t_stamp":tsStart,"Value":ts}
#	print point
	returnData = {}
	returnData['data'] = data
	return {'json': returnData}