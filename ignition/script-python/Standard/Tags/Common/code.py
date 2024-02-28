#----------------------------------------------------WriteTagsTVQ------------------------------------------------------
#Example:
#tagPathBase = "[AdvansysStandard]Standard/Interface Modules/WebDev/RX001/"
#paths = [tagPathBase+"TestNumber",tagPathBase+"TestNumber 1",tagPathBase+"TestNumber 2"]
#tvqs = [{'ts':timestamp,'v':63.0,'q':'GOOD_DATA'},{'ts':timestamp1,'v':6.0,'q':'GOOD_DATA'},{'ts':timestamp2,'v':7.0,'q':'GOOD_DATA'}]
#result = Standard.Tags.Common.WriteTagsTVQ(TagPaths=paths,TVQs=tvqs)
#print result

def WriteTagsTVQ(TagPaths,TVQs):
	from com.inductiveautomation.ignition.common.model.values import BasicQualifiedValue
	tvqs = TVQs
	basicQualifiedValues = []
	for tvq in tvqs:
		v= tvq['v']
		q= tvq['q']
		ts= tvq['ts']
		basicQualifiedValue = BasicQualifiedValue(v)
		basicQualifiedValue.timestamp = ts
		#basicQualifiedValue.quality = q --Not Sure How to do this?
		basicQualifiedValues.append(basicQualifiedValue)
	result = system.tag.writeBlocking(TagPaths, basicQualifiedValues)
	return result
	
#------------------------------------------------------GetTrendData------------------------------------------------------
def GetTrendData(HistoryConfig,PeriodEnd,HistoryDuration,TimestampFormat=None):
	#return None 
	periodStart = system.date.addMinutes(PeriodEnd, -HistoryDuration)
	periodStartMillis = system.date.toMillis(periodStart)
	series = {}
	for seriesConfig in HistoryConfig:
		paths = []
		columnNames = []
		seriesName = seriesConfig['seriesName']
		series[seriesName] = {}
		tags = seriesConfig['tags']
		for tag in tags:
			path = tag['path']
			columnName = tag['alias']
			paths.append(path)
			columnNames.append(columnName)
		#break
		#return columnNames
		rawData=system.tag.queryTagHistory(paths=paths,columnNames=columnNames,startDate=periodStart,endDate=PeriodEnd,returnSize=-1,includeBoundingValues=True,noInterpolation=True,returnFormat='Wide')
		#return rawData
		data = Standard.Utilities.Common.GetListFromDataset(Dataset=rawData)
		
		#Add 'dateTime' key in data
		addDateTime = TimestampFormat is not None
		
		#Convert 't_stamp' to millis time
		for dataPoint in data:
			t_stamp = dataPoint.pop('t_stamp')
			
			timeMillis = system.date.toMillis(t_stamp)
			#Set Boundry Timestamp if 
			if timeMillis < periodStartMillis:
				timeMillis = periodStartMillis
				t_stamp = periodStart
				dataPoint['boundryType'] = 'Boundry'
			else:
				dataPoint['boundryType'] = 'Between'
				
			dataPoint['time'] = timeMillis
			if addDateTime:
				dataPoint['timestamp'] = system.date.format(t_stamp,TimestampFormat)
			
			for tag in tags:
				isBool = tag['isBool']
				if tag['isBool']:
					alias = tag['alias']
					dataPoint[alias]= 1 if dataPoint[alias] else 0
		
		#Create Period Start Trend Data Point if no Data
		if len(data)==0:
			periodStartDataPoint = {"time": system.date.toMillis(periodStart),'boundryType': 'No Records'}
			if addDateTime:
				periodStartDataPoint['timestamp'] = system.date.format(periodStart,TimestampFormat)
			for tag in tags:
				alias = tag['alias']
				isBool = tag['isBool']
				currentValue = tag['currentValue']
				if tag['isBool']:
					currentValue = 1 if currentValue else 0
				periodStartDataPoint[alias]=currentValue
			data.append(periodStartDataPoint)
		#Check if Boundry Value
		else:
			fisrtDataPoint = data[0]
			timeMillis = fisrtDataPoint['time']
			if timeMillis < periodStartMillis:
				fisrtDataPoint['boundryType'] = 'Boundry'	
				
				
		#Create End Trend Data Point
		periodEndDataPoint = {"time": system.date.toMillis(PeriodEnd),'boundryType': 'Current'}
		if addDateTime:
			periodEndDataPoint['timestamp'] = system.date.format(PeriodEnd,TimestampFormat)
		for tag in tags:
			alias = tag['alias']
			currentValue = tag['currentValue']
			if tag['isBool']:
				currentValue = 1 if currentValue else 0
			periodEndDataPoint[alias]=currentValue
		data.append(periodEndDataPoint)
		
		series[seriesName]['data'] = data
		series[seriesName]['name'] = seriesName
#		series[seriesName]['periodStart'] = periodStart
#		series[seriesName]['periodEnd'] = PeriodEnd
	return series.values()
