#====================================================================GetEvents===============================================================
def GetEvents(HistorianTagPath,PeriodStart,PeriodEnd,MacroDuration=180,CurrentValue=None,Trigger='Onchange'):
	begin=system.date.now() 
	#Get Data
	tag = {}
	tag['alias'] = 'Bit'
	tag['isBool']= True
	tag['path']= HistorianTagPath
	tag['currentValue']= HistorianTagPath
	config = [{"seriesName": "Value","tags": [tag]}]
	
	#Get Raw Data For Evensts===============================================================
	#duration = system.date.minutesBetween(PeriodStart, PeriodEnd)
	periodStart = PeriodStart
	periodEnd = PeriodEnd
	returnRawData=False
	#returnFormat = 'Wide'
	returnFormat = 'Tall' 
	timestampFormat = 'yyyy-MM-dd HH:mm:ss.SSS'
	data = Standard.Tags.Common.GetTrendData(HistoryConfig=config,PeriodStart=periodStart,PeriodEnd=periodEnd,ReturnRawData=returnRawData,TimestampFormat=timestampFormat,ReturnFormat=returnFormat) 
	data = data[0]['data'] 
	#return data[0]['data'] 
			
	PeriodEnd = periodEnd
	PeriodEndMillis = system.date.toMillis(PeriodEnd)
	macroDurationSetpointSeconds = MacroDuration
	macroDurationMillis = macroDurationSetpointSeconds*1000
	#return macroDurationMillis
	
	#Get Evensts===============================================================
	events = []
	producingPre = -1
	timeStampMillisPre = 0 
	start=False
	end = False
	
	for row in data:
		timeStampMillis = row['time']
		if timeStampMillis>PeriodEndMillis:
			timeStampMillis = PeriodEndMillis
		if 'value' not in row:
			return row
		rowValue = row['value'] 
		rowPath = row['path']
		timeStamp = system.date.fromMillis(timeStampMillis)
		
		timeStampFormat = system.date.format(timeStamp,'yyyy-MM-dd HH:mm:ss.SSS')
		if rowPath == "FillerProducing":
			producing = rowValue
			if start==True and end==False:
				end = True #New Event End
				
				periodEnd = timeStamp
				periodEndMillis = timeStampMillis
				periodEndFormat = timeStampFormat
			if start==False:
				start = True #New Event Start
				periodStart = timeStamp
				stateValue = producing
				periodStartMillis = timeStampMillis
				periodStartFormat = timeStampFormat
			if start==True and end==True:
				event = {}
				event['PeriodStart'] = periodStart
				event['PeriodStartMillis'] = periodStartMillis
				event['PeriodStartFormated'] = periodStartFormat
				event['PeriodEnd'] = periodEnd
				event['PeriodEndMillis'] = periodEndMillis
				event['PeriodEndFormated'] = periodEndFormat
				
				event['State'] = stateValue
#				event['Production'] = totalCount
#				event['ProductionCounts'] = counts
				#Calculate Duration
				duration = periodEndMillis-periodStartMillis
				event['Duration'] = duration/60000.0
				#Calculate Duration Type
				durationType = None
				if stateValue==False:
					if duration>macroDurationMillis:
						durationType = "Stopped-Macro"
					elif periodEnd is not None:
						durationType = "Stopped-Micro"
				else:
					durationType = "Running"
				event['DurationType'] = durationType
				totalCount = 0
				counts = []
				
				event['AreaCause'] = 'Unallocated'
				event['Catogary'] = 'Unallocated'
				event['Timegroup'] = 'Unallocated'
				
				#This row also is the start for next Event
				start=True
				stateValue = producing
				periodStart = timeStamp
				periodStartMillis = timeStampMillis
				periodStartFormat = timeStampFormat
				end=False
				events.append(event)		
	end=system.date.now()
	performanceDuration = system.date.millisBetween(begin, end)
	return {'events':events,'performanceDuration':performanceDuration}
#====================================================================GetMeasureValues===============================================================
def GetMeasureValues(HistorianTagPath,PeriodStart,PeriodEnd,Events=None,CurrentValue=None,RetrievalType='Counter'):
	begin=system.date.now() 
	#Get Data
	tag = {}
	tag['alias'] = 'Bit'
	tag['isBool']= True
	tag['path']= HistorianTagPath
	tag['currentValue']= HistorianTagPath
	config = [{"seriesName": "Value","tags": [tag]}]
	
	#Get Raw Data For Evensts===============================================================
	#duration = system.date.minutesBetween(PeriodStart, PeriodEnd)
	periodStart = PeriodStart
	periodEnd = PeriodEnd
	returnRawData=False
	#returnFormat = 'Wide'
	returnFormat = 'Tall' 
	timestampFormat = 'yyyy-MM-dd HH:mm:ss.SSS'
	data = Standard.Tags.Common.GetTrendData(HistoryConfig=config,PeriodStart=periodStart,PeriodEnd=periodEnd,ReturnRawData=returnRawData,TimestampFormat=timestampFormat,ReturnFormat=returnFormat) 
	data = data[0]['data']
	#return data[0]
	events = Events			
	#return [timeStampMillis,timeStampFormat,rowValue,rowPath]
	countPre = None
	totalCount = 0
	counts = []
	if events is not None:
		#Get Counts
		lastCountIndex = 0
		countMax = len(data)
		i=0
		for event in events:
			periodStartMillis = event['PeriodStartMillis']
			periodEndMillis = event['PeriodEndMillis']
			for i in range(lastCountIndex,countMax):
				row = data[i]
				timeStampMillis = row['time']
				rowPath = row['path']
				rowValue = row['value']
				if rowPath == "FillerCount":
					if timeStampMillis>=periodStartMillis and timeStampMillis<=periodEndMillis:
						lastCountIndex = i
						count = rowValue
						if countPre is None:
							countPre = count
						if count is None:
							count = countPre
						delta = count-countPre
						totalCount = totalCount + delta
						countPre = count
						#row['delta'] = delta
						
						r={'delta':delta,'totalCount':totalCount}
						#lastCountTime = timeStampMillis
						counts.append(r)
					else:
						#return row
						lastCountIndex = i
						event['Production'] = totalCount
						event['ProductionCounts'] = counts
						totalCount = 0
						counts = []
						break
	end=system.date.now()
	performanceDuration = system.date.millisBetween(begin, end)
	return {'events':events,'performanceDuration':performanceDuration}

#====================================================================GetInitialEvents===============================================================
def GetInitialEvents(StateHistorianTagPath,TotalCountHistorianTagPath,PeriodStart,PeriodEnd,Debug=False):
	debug = Debug
	if debug:
		Standard.Utilities.Common.LogMessage("GetInitialEvents", "Starting...")
	historianTagPath = StateHistorianTagPath
	periodStart = PeriodStart
	periodEnd = PeriodEnd
	if periodStart is None or periodEnd is None:
		return {'error':"PeriodStart or PeriodEnd cannot be None!"}
	
	if debug:
		Standard.Utilities.Common.LogMessage("GetInitialEvents", "GetEvents...")
	
	events = Standard.Equipment.Performance.GetEvents(HistorianTagPath=historianTagPath,PeriodStart=periodStart,PeriodEnd=periodEnd,Trigger='Onchange')
	performanceDurationTotal = events['performanceDuration']
	print events['performanceDuration']
	#print events
	events = events['events']
	historianTagPath = TotalCountHistorianTagPath
	if debug:
		Standard.Utilities.Common.LogMessage("GetInitialEvents", "GetMeasureValues...")
	events = Standard.Equipment.Performance.GetMeasureValues(HistorianTagPath=historianTagPath,PeriodStart=periodStart,PeriodEnd=periodEnd,Events=events,CurrentValue=None,RetrievalType='Counter')
	print events['performanceDuration']
	performanceDurationTotal = performanceDurationTotal + events['performanceDuration']
	events['performanceDuration'] = performanceDurationTotal
	if debug:
		Standard.Utilities.Common.LogMessage("GetInitialEvents", "Done!")
	return events
	
#====================================================================GetInitialEventsForTag===============================================================
def GetInitialEventsForTag(StateHistorianTagPath,TotalCountHistorianTagPath,PeriodStart,PeriodEnd,Debug=False):
	debug = Debug
	if debug:
		Standard.Utilities.Common.LogMessage("GetInitialEventsForTag", "Starting...")
		
	events = GetInitialEvents(StateHistorianTagPath,TotalCountHistorianTagPath,PeriodStart,PeriodEnd,Debug)
	events = system.util.jsonEncode(events)
	if debug:
		Standard.Utilities.Common.LogMessage("GetInitialEventsForTag", "Done!")
	return events





