DateTimeLocalformat = 'yyyy-MM-dd HH:mm:ss'
#---------------------------------------------------GetCalendar----------------------------------------
def GetCalendar(Connection,Name):
#	logger = system.util.getLogger("GetCalendar")
#	logger.info(str(Connection))
#	Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName="GetCalendar",Message=str(Connection),DebugLevel=10)
#	
	publicKey = Connection['PublicKey']
	publicAPI = Connection['Public API']
#	logger.info("publicAPI: " + str(publicAPI))
	url = publicAPI + '/v1/config/calendars'
	headerValues = {'Authorization':'Bearer '+publicKey}
	response = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.Get(url,HeaderValues=headerValues)
	if 'error' in str(response):
		if response['error']:
			return response['message']
#	logger.info("response: " + str(response))
	calendars = response['json']
	for calendar in calendars['calendars']:
		name = calendar['name']
		if name.upper() == Name.upper():
			return calendar['id']
	
	return '-1'

#---------------------------------------------------Get445CalendarPattern-----------------------------
def Get445CalendarPattern(Year=None,StartOfDay=None):
	
	#default Year
	year = Year
	if year == None:
		year = system.date.getYear(system.date.now())

	#default Year
	startOfDay = StartOfDay
	if startOfDay == None:
		startOfDay = 0
	
	def getWeekDayCount(periodStart,periodEnd):
		totaldays = system.date.daysBetween(periodStart,periodEnd)
		cnt = 0
		for i in range(0,totaldays):
			period = system.date.addDays(periodStart,i)
			dayOfWeek = system.date.getDayOfWeek(period)
			if dayOfWeek<7 and dayOfWeek>1:
				cnt +=1		
		return cnt


	startOfYear = system.date.getDate(year,0,1)
	startOfYear = system.date.addHours(startOfYear,startOfDay)
	#return startOfYear
	months = []
	monthEnd = startOfYear
	pattern = [4,4,5]
	patternIndex = 0
	futureIntervalInMonthsCount=0
	for i in range(1,13):
		month = {}
		periodStart = monthEnd
		if i<12:
			monthEnd = system.date.addWeeks(monthEnd,pattern[patternIndex])
			patternIndex = patternIndex+1
			if patternIndex==3:
				patternIndex = 0
			
			dayOfMonthEnd = system.date.getDayOfWeek(monthEnd)
			if dayOfMonthEnd!=6: #should Always Ends On Friday(6)
				if dayOfMonthEnd>6:
					monthEnd = system.date.addDays(monthEnd,6-dayOfMonthEnd)
				else:
					monthEnd = system.date.addDays(monthEnd,6-(7+dayOfMonthEnd))
			monthEnd = system.date.addDays(monthEnd,1)
		else:
			monthEnd = system.date.addYears(startOfYear,1)
		
		periodEnd = monthEnd
		
		periodEndMidnight = system.date.addDays(periodEnd,1)
		periodEndMidnight = system.date.midnight(periodEndMidnight)
		
		#system.perspective.print('Debug 3------------------' + system.date.format(periodStart,' MM-dd HH:'))
		month['PeriodStart'] = system.date.format(periodStart,DateTimeLocalformat)
		month['PeriodEnd'] = system.date.format(periodEnd,DateTimeLocalformat)
		month['WeekDaysInPeriod'] = getWeekDayCount(periodStart,periodEnd)
		month['TotalDaysInPeriod'] = system.date.daysBetween(periodStart,periodEnd)
		month['PeriodEndMidnight'] = system.date.format(periodEndMidnight,DateTimeLocalformat)
		month['LastDayInMonth'] = system.date.getDayOfMonth(system.date.addDays(periodEnd,-1))
		month['DayOfWeekMonthEnd'] = system.date.getDayOfWeek(periodEnd)-1 #should Always be 6
		
		months.append(month)
	
	return months
#------------------------------------------------------GetCurrentCalendarMonths----------------------------------------
def GetCurrentCalendarMonths(Database,CalendarID,PeriodStartUTC,Refresh=False):
	logger = system.util.getLogger("GetCurrentCalendarMonths")
	logger.info("Database: " + str(Database))
	if PeriodStartUTC is None:
		PeriodStartUTC = system.date.addYears(system.date.now(),-2)
	params = {}
	params['database'] = Database
	params['IntervalTypeID'] = 6
	params['CalendarID'] = CalendarID
	params['PeriodStartUTC'] = PeriodStartUTC
	logger.info("PeriodStartUTC: " + str(PeriodStartUTC))
	manualPeriods = system.db.runNamedQuery('Flow/GetManualPeriods',parameters = params)
	logger.info("manualPeriods: " + str(manualPeriods))
	manualPeriods = Standard.InterfaceModules.Flow.Common.GetListFromDataset(Dataset=manualPeriods)
	periods = []
	period={}
	if len(manualPeriods)>0:
		for periodUTC in manualPeriods:
			period={}
			periodStartUTC = periodUTC['PeriodStart'] 
			periodEndUTC = periodUTC['PeriodEnd']
			#UTC
			period['PeriodStartUTC'] = system.date.format(periodStartUTC,DateTimeLocalformat)
			period['PeriodEndUTC'] = system.date.format(periodEndUTC,DateTimeLocalformat)
			
			periodStart = system.date.addHours(periodStartUTC,int(system.date.getTimezoneOffset(periodStartUTC)))
			period['PeriodStart'] = system.date.format(periodStart,DateTimeLocalformat)
			
			
			periodEnd = system.date.addHours(periodEndUTC,int(system.date.getTimezoneOffset(periodEndUTC)))
			period['PeriodEnd'] = system.date.format(periodEnd,DateTimeLocalformat)
			
			periods.append(period)
	
	return {'periods':periods,'lastPeriod':period}
#-----------------------------------------------------------------------------------------------
def GetMergeCurrentWithConfig(CurrentPeriods,ConfigurationPeriods,FutureIntervalsInMonths):
	Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='Start....',DebugLevel=10)
	currentPeriods = CurrentPeriods['periods'] #Current Configured Periods
	currentLastPeriod = CurrentPeriods['lastPeriod'] #Current Last Configured Periods
	futureIntervalsInMonths = FutureIntervalsInMonths
	configurationPeriods = ConfigurationPeriods #New Planned Configured Periods

	#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='Start....1' + str(CurrentPeriods),DebugLevel=10)
	#--------------------------------------------------------------getFlowPeriod------------------------------
	def getCurrentPeriod(periodStart,periodEnd):
			if currentPeriods is None or len(currentPeriods) == 0:
				return None
			lastCurrentDate = system.date.parse(currentLastPeriod['PeriodEnd'],DateTimeLocalformat)
			#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='getCurrentPeriod....1:' +str(type(lastCurrentDate)),DebugLevel=10)
			midnightOfPeriodStart = system.date.midnight(periodStart)
			midnightOfPeriodEnd = system.date.midnight(periodEnd)
			midnightOfLastCurrentDate = system.date.midnight(lastCurrentDate)
			if midnightOfPeriodStart <= midnightOfLastCurrentDate:
				#get the relevant period
				for period in currentPeriods:
					currentPeriodStart = system.date.parse(period['PeriodStart'],DateTimeLocalformat)
					#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='getCurrentPeriod....2:' +str(type(currentPeriodStart)),DebugLevel=10)
					currentPeriodEnd = system.date.parse(period['PeriodEnd'],DateTimeLocalformat)
					#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='getCurrentPeriod....3:' +str(type(currentPeriodEnd)),DebugLevel=10)
					midnightOfCurrentPeriodStart = system.date.midnight(currentPeriodStart)
					midnightOfCurrentPeriodEnd = system.date.midnight(currentPeriodEnd)
				
					if midnightOfPeriodStart==midnightOfCurrentPeriodStart and midnightOfPeriodEnd<=midnightOfCurrentPeriodEnd:
						return {'PeriodStart':currentPeriodStart,'PeriodEnd':currentPeriodEnd}

					if lastCurrentDate == currentPeriodEnd and midnightOfPeriodStart==midnightOfCurrentPeriodEnd:
						return {'PeriodStart':currentPeriodEnd}

				return {'PeriodStart':periodStart,'PeriodEnd':periodEnd}
			return None
	
	
	periods = []
	futureIntervalsInMonthsCount=0
	for configurationPeriod in configurationPeriods:
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='ConfigurationPeriod....'+str(configurationPeriod),DebugLevel=10)
		month = {}
		periodStart = system.date.parse(configurationPeriod['PeriodStart'],DateTimeLocalformat)
		periodEnd = system.date.parse(configurationPeriod['PeriodEnd'],DateTimeLocalformat)
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='ConfigurationPeriod....1:' +str(type(periodEnd)),DebugLevel=10)
		
		periodEndMidnight = system.date.addDays(periodEnd,1)
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='ConfigurationPeriod....2',DebugLevel=10)
		periodEndMidnight = system.date.midnight(periodEndMidnight)
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='ConfigurationPeriod....3',DebugLevel=10)
		
		#Check if in Flow
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='getCurrentPeriod....Start',DebugLevel=10)
		currentPeriod = getCurrentPeriod(periodStart,periodEnd)
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='getCurrentPeriod....Done!',DebugLevel=10)
		isConfigured = False
		skip = True
		skip = False
		if currentPeriod is not None:
			periodStart = currentPeriod['PeriodStart']
			#system.perspective.print('Debug 2------------------' + system.date.format(periodStart,' MM-dd HH:'))
			if 'PeriodEnd' in currentPeriod:
				periodEnd = currentPeriod['PeriodEnd']
				isConfigured = True
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='Month....1:' + str(type(periodStart)),DebugLevel=10)		
		month['PeriodStart'] = system.date.format(periodStart,DateTimeLocalformat)
		month['PeriodEnd'] = system.date.format(periodEnd,DateTimeLocalformat)
		month['WeekDaysInPeriod'] = configurationPeriod['WeekDaysInPeriod']
		month['TotalDaysInPeriod'] = configurationPeriod['TotalDaysInPeriod']
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='Month....2',DebugLevel=10)	
		month['PeriodEndMidnight'] = system.date.format(periodEndMidnight,DateTimeLocalformat)
		month['LastDayInMonth'] = configurationPeriod['LastDayInMonth']
		month['DayOfWeekMonthEnd'] = configurationPeriod['DayOfWeekMonthEnd']
		month['IsConfigured'] = isConfigured
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='Month....3',DebugLevel=10)	
		create = not isConfigured
		if not isConfigured:
			create = False #default to Fasle
			futureIntervalsInMonthsCount +=1
			if futureIntervalsInMonthsCount<=futureIntervalsInMonths:
				create = True
		month['Create'] = create
		#Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='Month....'+str(month),DebugLevel=10)
		
		periods.append(month)
	Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='GetMergeCurrentWithConfig',Message='End!',DebugLevel=10)
	return periods
#---------------------------------Get Allowed TimePeriods To Created
def GetAllowedTimePeriodsToCreated(MergedCalendarData,FutureIntervalsInMonths):
	data=MergedCalendarData
	futureIntervalsInMonths = FutureIntervalsInMonths

	cnt = 0
	for period in data:
		isConfigured = period['IsConfigured']
		if not isConfigured:
			cnt += futureIntervalsInMonths
			break
		cnt +=1
	
	periodEnd = data[cnt-1]['PeriodEnd']
	return {'PeriodStart':period['PeriodStart'],'PeriodEnd':periodEnd}

#---------------------------------
def GetTimePeriodsToCreated(MergedCalendarData,CalendarName,FutureIntervalsInMonths=1,MinuteInterval=30):
	#('Minutely', 'Hourly', 'Shiftly', 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly') 
	calendarData = MergedCalendarData
	calendarName = CalendarName
	allowedConfigurationPeriod = GetAllowedTimePeriodsToCreated(MergedCalendarData,FutureIntervalsInMonths)
	periodStart = system.date.parse(allowedConfigurationPeriod['PeriodStart'],DateTimeLocalformat)
	periodEnd = system.date.parse(allowedConfigurationPeriod['PeriodEnd'],DateTimeLocalformat)
	minuteInterval = MinuteInterval
	
	def getIntervals(periodStart,periodEnd,intervalDuration,appendIntervals,intervalType): #base in minutes
		#create Minutes
		totalMinutesIntervals = system.date.minutesBetween(periodStart,periodEnd) / intervalDuration
		#return totalMinutesIntervals
		ps = periodStart
		intervals = []
		for interval in appendIntervals:
			intervals.append(interval)
	
		for i in range(0,totalMinutesIntervals):
			params = {}
			params['CalendarName'] = calendarName
			params['PeriodStart'] = system.date.format(ps,DateTimeLocalformat)
			params['IntervalType'] = intervalType
			pe = system.date.addMinutes(ps,intervalDuration)
			peFormatted = system.date.format(pe,DateTimeLocalformat)
			params['PeriodEnd'] = peFormatted
			intervals.append(params)
			ps=pe
		return {'intervals':intervals,'count':len(intervals),'ps':intervals[0]['PeriodStart'],'pe':peFormatted}
	
	#create Minutes
	minutesIntervals = getIntervals(periodStart,periodEnd,minuteInterval,[],'Minutely')
	
	#create Hours
	hoursIntervals = getIntervals(periodStart,periodEnd,60,[],'Hourly')
	
	#days
	days = []
	periodStartDay = periodStart
	daysIntervals = []
	startMonthIndex = 0
	for month in calendarData:
		isConfigured = month['IsConfigured']
		if isConfigured: #Skip id already configured
			startMonthIndex +=1
			continue
		startMonthIndex +=1
		periodStartDay = system.date.parse(month['PeriodStart'],DateTimeLocalformat)
		periodEndDay =  system.date.parse(month['PeriodEnd'],DateTimeLocalformat)
		periodStartDayMidnight = system.date.midnight(periodStartDay)
	
		#create first day
		params = {}
		params['CalendarName'] = calendarName
		params['PeriodStart'] = system.date.format(periodStartDay,DateTimeLocalformat)
		params['IntervalType'] = 'Daily'
		periodStartDayHour = system.date.getHour24(periodEndDay)
		defaultStartDay = system.date.addHours(periodStartDayMidnight,periodStartDayHour)
		periodStartDayNexDay = system.date.addDays(defaultStartDay,1)
		params['PeriodEnd'] = system.date.format(periodStartDayNexDay,DateTimeLocalformat)
		daysIntervals.append(params)
		break #Only process First Day
	
	daysIntervals = getIntervals(periodStartDayNexDay,periodEnd,(60*24),daysIntervals,'Daily')
	
	#Months
	months = []
	for i in range(startMonthIndex-1,len(calendarData)):
		month = calendarData[i]
		monthPeriodStart = system.date.parse(month['PeriodStart'],DateTimeLocalformat)
		monthPeriodEnd = system.date.parse(month['PeriodEnd'],DateTimeLocalformat)
		params = {}
		params['CalendarName'] = calendarName
		params['PeriodStart'] = system.date.format(monthPeriodStart,DateTimeLocalformat)
		monthPeriodEndFormetted = system.date.format(monthPeriodEnd,DateTimeLocalformat)
		params['PeriodEnd'] = monthPeriodEndFormetted
		params['IntervalType'] = 'Monthly'
		months.append(params)
		if periodEnd==monthPeriodEnd:
			break
			
	monthsIntervals = {'intervals':months,'count':len(months),'ps':months[0]['PeriodStart'],'pe':monthPeriodEndFormetted}
	intervals = {'minutes':minutesIntervals,'hours':hoursIntervals,'days':daysIntervals,'months':monthsIntervals}
	return intervals

#---------------------------------Create TimePeriods#---------------------------------
def CreateTimePeriods(TimePeriodsToCreated):
	Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='CreateTimePeriods',Message='Start....',DebugLevel=10)
	toBeCreated = TimePeriodsToCreated
	minutes = toBeCreated['minutes']['intervals']
	hours = toBeCreated['hours']['intervals']
	days = toBeCreated['days']['intervals']
	months = toBeCreated['months']['intervals']
	def create(intervals):
		results = []
		result = None
		for period in intervals:
			#return params
			params = {}
			params["IntervalType"] = period["IntervalType"]
			params["PeriodStart"] = period["PeriodStart"]
			params["CalendarName"] = period["CalendarName"]
			params["PeriodEnd"] =period["PeriodEnd"]
			result = system.db.runNamedQuery(path='Flow/CreateManualPeriod',parameters=params)
			if result != -1:
				results.append(result)

		return results
	
	results = {}
	results['minutes'] = create(minutes)
	results['hours'] = create(hours)
	results['days'] = create(days)
	results['months'] = create(months)
	Standard.InterfaceModules.Flow.Common.Logmessage(LoggerName='CreateTimePeriods',Message='End!',DebugLevel=10)
	return results
#====================================================== 	GetStartofDay  ====================================================
def GetStartofDay(SiteTagPath):
	#[default]Flow/CCBZA10/
	startOfDayTagPath = SiteTagPath + "/Calendar Manager/StartOfDay"
	startOfDay = Standard.Model.Common.TagRead(startOfDayTagPath)
	if startOfDay is None:
		startOfDay = 0 # Midnight 
	return startOfDay

	
	
