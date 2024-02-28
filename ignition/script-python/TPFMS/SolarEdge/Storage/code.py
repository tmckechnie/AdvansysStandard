#================================================GetSiteStorageData================================================
def GetSiteStorageData(SiteRequestDetails,Period):
	endpoint ='storageData'
		
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']
		
	#Period Part
	period = Period
	periodUrl = period['UrlPart']
	
	url = url + '/site/' + str(siteID) + '/'+endpoint+'?'+ periodUrl+'&api_key='+apiKey
	print url
	return TPFMS.SolarEdge.Common.get(url)