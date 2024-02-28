#======================================================= GetTimePeriodMeasureID =======================================================

def GetTimePeriodMeasureID(PublicAPI,PublicKey,interval):
	timePeriodMeasureID = None
	#First get calendar metric ID
	metricURL = getIgnitionCalendarTimePeriodsMetricURL(PublicAPI)
	metricID = 	getIgnitionCalendarTimePeriodsMetricID(metricURL,PublicKey)
	if metricID is not None:		
		timePeriodMeasureIDUrl = getIgnitionCalendarTimePeriodsMetricMeasuresURL(PublicAPI,metricID,interval)
		#Use Metric ID to get all Calendar Measures
		timePeriodMeasureID = getIgnitionCalendarTimePeriodsMetricMeasureID(timePeriodMeasureIDUrl,PublicKey,interval)

	return timePeriodMeasureID

#======================================================= getIgnitionCalendarTimePeriodsMetricURL =======================================================

def getIgnitionCalendarTimePeriodsMetricURL(PublicAPI):
	url = PublicAPI + "/v1/search?query=Ignition%20445%20Calendar%20Time%20Periods&type=metric&match=name&limit=1000&page=1"	
	return url
	
#======================================================= getIgnitionCalendarTimePeriodsMetricID =======================================================

def getIgnitionCalendarTimePeriodsMetricID(MetricURL,PublicKey):
	headerValues = {"Authorization":"Bearer " + PublicKey}
	metricIDResponse = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.Get(MetricURL,HeaderValues=headerValues)	
	metricID = None
	if metricIDResponse["error"] == False:
		metricID = Standard.InterfaceModules.Flow.PublicAPI.V1.Data.queryAPIMatchNameID(metricIDResponse["json"])
	return metricID
	
#======================================================= getIgnitionCalendarTimePeriodsMetricMeasuresURL =======================================================

def getIgnitionCalendarTimePeriodsMetricMeasuresURL(PublicAPI,TimePeriodMetricID,interval):
	url = PublicAPI + "/v1/model/metrics/%s/measures?retrieval=manual&interval=%s&fields=false"%(TimePeriodMetricID,interval)
	return url
#======================================================= getIgnitionCalendarTimePeriodsMetricMeasureID =======================================================

def getIgnitionCalendarTimePeriodsMetricMeasureID(MeasureURL,PublicKey,interval):
	headerValues = {"Authorization":"Bearer " + PublicKey}
	measureResponse = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.Get(MeasureURL,HeaderValues=headerValues)	
	measureID = None
	if measureResponse["error"] == False:
		#Find measure id with correct interval
		measureResponsejson = measureResponse["json"]
		measures = measureResponsejson["measures"]
		for measure in measures:
			measureInterval = measure["interval"]
			if measureInterval == interval:
				measureID = measure["id"]
				break
				
	return measureID


	
	
	
	
