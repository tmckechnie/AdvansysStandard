#================================================GetSiteCurrentPowerFlow================================================
def GetSiteCurrentPowerFlow(SiteRequestDetails,Period):
	endpoint ='currentPowerFlow'
	
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']

	url = url + '/site/' + str(siteID) + '/'+endpoint+'?&api_key='+apiKey
	return TPFMS.SolarEdge.Common.get(url)	
#================================================GetSitePower================================================
def GetSiteEnergy(SiteRequestDetails,Period):
	endpoint ='energy'
	
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
#================================================GetSitePowerDetails================================================
def GetSiteEnergyDetails(SiteRequestDetails,Period):
	endpoint ='energyDetails'
	
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


#================================================GetSiteTimeFrameEnergy================================================
def GetSiteTimeFrameEnergy(SiteRequestDetails,Period):
	endpoint ='timeFrameEnergy'
	
	#Site Details
	url = SiteRequestDetails['BaseUrl']
	siteID = SiteRequestDetails['SiteID']
	apiKey = SiteRequestDetails ['APIKey']
		
	#Period Part
	period = Period
	periodUrl = period['UrlPart']
	url = url + '/site/' + str(siteID) + '/'+endpoint+'?'+ periodUrl+'&api_key='+apiKey
	return TPFMS.SolarEdge.Common.get(url)