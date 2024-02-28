#================================================get================================================
def get(url):
	client = system.net.httpClient()
	response = client.get(url)
	results = response.getText()
	decodedDict = system.util.jsonDecode(results)
	return decodedDict
#================================================getGetSite================================================
def GetSiteRequestDetails(BaseUrl,SiteID,APIKey):
	return {'BaseUrl':BaseUrl,'SiteID':SiteID,'APIKey':APIKey}
#================================================getPeriod================================================
def GetPeriod(PeriodStart,PeriodEnd,TimeUnit=None,FormatType='Time',FormatKey='Time'):

	format = 'yyyy-MM-dd%20HH:mm:00'
	if FormatType == 'Date':
		format = 'yyyy-MM-dd'

	period = {}
	#PeriodStart
	periodStart = system.date.format(PeriodStart,format)
	period['StartTime'] = periodStart
	#PeriodEnd
	periodEnd = system.date.format(PeriodEnd,format)
	period['EndTime'] = periodStart
	#PeriodUrl
	periodUrl = 'start'+FormatKey+'='+str(periodStart) + '&end'+FormatKey+'='+str(periodEnd)

	if TimeUnit is not None:
		periodUrl = periodUrl+ '&timeUnit='+str(timeUnit)
	
	period['UrlPart'] = periodUrl

	return period

#================================================GetSiteDataPeriod================================================
def GetSiteDataPeriod(SiteRequestDetails):
	endpoint ='dataPeriod'
	
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']
		
	url = url + '/site/' + str(siteID) + '/'+endpoint+'?api_key='+apiKey
	print url
	return get(url)	

#================================================GetSiteOverview================================================
def GetSiteOverview(SiteRequestDetails):
	endpoint ='overview'
	
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']
		
	url = url + '/site/' + str(siteID) + '/'+endpoint+'?api_key='+apiKey
	print url
	return get(url)	

#================================================GetSiteDetails================================================
def GetSiteDetails(SiteRequestDetails):
	endpoint ='details'
	
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']
		
	url = url + '/site/' + str(siteID) + '/'+endpoint+'?api_key='+apiKey
	print url
	return get(url)
#================================================GGetSiteDetailsForTag================================================
def GetSiteDetailsForTag(BaseUrl,SiteID,APIKey):
	Standard.Utilities.Common.LogMessage("GetSiteDetailsForTag", "Start...:")
	siteRequestDetails = TPFMS.SolarEdge.Common.GetSiteRequestDetails(BaseUrl=BaseUrl,SiteID=SiteID,APIKey=APIKey)
	data = GetSiteDetails(siteRequestDetails)
	strData = system.util.jsonEncode(data)
	Standard.Utilities.Common.LogMessage("GetSiteDetailsForTag", "Data: " + str(data))
	return strData

