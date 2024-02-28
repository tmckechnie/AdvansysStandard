#================================================GetSiteCurrentPowerFlow================================================
def GetSiteCurrentPowerFlow(SiteRequestDetails):
	endpoint ='currentPowerFlow'
	
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']

	url = url + '/site/' + str(siteID) + '/'+endpoint+'?&api_key='+apiKey
	return TPFMS.SolarEdge.Common.get(url)	
#================================================GetSitePower================================================
def GetSitePower(SiteRequestDetails,Period):
	endpoint ='power'
	
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']
		
	#Period Part
	period = Period
	periodUrl = period['UrlPart']
	
	url = url + '/site/' + str(siteID) + '/'+endpoint+'?'+ periodUrl+'&api_key='+apiKey
	return TPFMS.SolarEdge.Common.get(url)
#================================================GetSitePowerDetails================================================
def GetSitePowerDetails(SiteRequestDetails,Period):
	endpoint ='powerDetails'
	
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

#================================================GetSiteCurrentPowerFlowForTag================================================
def GetSiteCurrentPowerFlowForTag(BaseUrl,SiteID,APIKey):
	Standard.Utilities.Common.LogMessage("GetSiteCurrentPowerFlowForTag", "Start...:")
	siteRequestDetails = TPFMS.SolarEdge.Common.GetSiteRequestDetails(BaseUrl=BaseUrl,SiteID=SiteID,APIKey=APIKey)
	data = GetSiteCurrentPowerFlow(siteRequestDetails)
	strData = system.util.jsonEncode(data)
	Standard.Utilities.Common.LogMessage("GetSiteCurrentPowerFlowForTag", "Data: " + str(data))
	return strData