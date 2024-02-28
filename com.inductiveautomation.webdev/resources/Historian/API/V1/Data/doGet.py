def doGet(request, session):
	loggerName = "WebDev: Historian/API/V1/Data (GET)"

	
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Request:' + str(request))
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Parameters:' + str(request['params']))
	params = request['params']
	tagPath = params['TagPath'] #[TPROM]ROM/CV01/100WT001/Sts/Value
	periodStart = params['PeriodStart'].replace('T',' ')
	periodEnd = params['PeriodEnd'].replace('T',' ')
	isBool =  bool(params['IsBool'])
	
	
	historyTagPath = system.tag.readBlocking([tagPath+'.History Path'])[0].value
	message = str([tagPath,historyTagPath,periodStart,periodEnd])
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message=message)	
	rawData=system.tag.queryTagHistory(paths=[historyTagPath],columnNames=['Value'],startDate=periodStart,endDate=periodEnd,returnSize=-1,includeBoundingValues=True,noInterpolation=True,returnFormat='Wide')
	
	data = Standard.Utilities.Common.GetListFromDataset(Dataset=rawData)
	#data[0]['t_stamp'] = periodStart
	Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message='Period Type:' + str(type(data[0]['t_stamp'])))	
	returnData = {}
	returnData['data'] = data
	return {'json': returnData}