
def getUTCTime(TimestampLocal):
	timezoneOffset = int(-1*system.date.getTimezoneOffset(TimestampLocal))
	return system.date.addHours(TimestampLocal, timezoneOffset)
#-----------------------------------------------------------------------getListFromDataset-----------------------------------------------------		
def getListFromDataset(Dataset):
	getColumnHeaders = system.dataset.getColumnHeaders(Dataset)
	dataset = system.dataset.toPyDataSet(Dataset)
	list = []
	for row in dataset:
		dictRow = {}
		for col in getColumnHeaders:	
			dictRow[col] = row[col]
		list.append(dictRow)
	return list
#-----------------------------------------------------------------------execute-----------------------------------------------------	
def execute(path,parameters={},getKey=False,transactionID=''):
	try:
		result = system.db.runNamedQuery(path=path,parameters = parameters,getKey=getKey,tx=transactionID)
		#print result
		return {'error':False,'result':result}
	except:
		message = sys.exc_info()
		return {'error':True,'message':message}
#-----------------------------------------------------------------------GetTag-----------------------------------------------------
#This will create the tag if it does not exists
def GetTag(Name,Description=None,EngUnit=None):
	params = {}
	params['Name'] = Name
	if Description is not None:
		params['Description'] = Description
	if EngUnit is not None:
		params['EngUnit'] = EngUnit
	response = execute(path='FlowTraining/GetTag',parameters=params)
	if response['error']:
		return  response
	data = getListFromDataset(response['result'])
	return data[0]['TagID']
#-----------------------------------------------------------------------CreateTagValue-----------------------------------------------------
#This will create the tag if it does not exists
def CreateTagValue(TagID,TimestampLocal,Value,Quality=192):
	timestampUTC = FlowTraining.DB.getUTCTime(TimestampLocal=TimestampLocal)
	params = {}
	params['TagID'] = TagID
	params['Timestamp'] = timestampUTC
	params['Quality'] = Quality
	if Value is not None:
		params['Value'] = Value

	response = execute(path='FlowTraining/CreateTagValue',parameters=params)
	if response['error']:
		return  response
	return 'Ok'
#-----------------------------------------------------------------------LogTags-----------------------------------------------------	
def LogTags(ConnectionTagPath,TagIDs,PeriodStart,FirstValue,Limit,Deadband=1.5):
	print 'Get Tags...'
	tags = Standard.InterfaceModules.Flow.PublicAPI.V1.Data.GetTags(ConnectionTagPath=ConnectionTagPath,PeriodStart=PeriodStart,TagIds=TagIDs,Limit=Limit)
	for tag in tags:
		name = tag
		print name
		tagID = FlowTraining.DB.GetTag(Name=name)
		print tagID
		
		data = tags[tag]
		if len(data) == 1:
			return None
		if not FirstValue:
			data = data[1:]
		valuePre = None
		for tvq in data: #Ignore first value
			timestampUTC = tvq['timestamp']
			value = tvq['value']
			if valuePre is not None and abs(valuePre-value) < Deadband: #Skip if not in deadband deviation
				continue
			valuePre = value
			quality = tvq['quality']
			timestampLocal = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetLocalDateTimeFromFlow(DateTimeUTC=timestampUTC)
			response = FlowTraining.DB.CreateTagValue(TagID=tagID,TimestampLocal=timestampLocal,Value=value,Quality=quality)
			if response != 'Ok':
				print response
	return timestampLocal #return last Timestamp
	