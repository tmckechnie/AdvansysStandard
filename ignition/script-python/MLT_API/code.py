def getAllWorkOrders():
	"""Gets work order information

    Parameters:
    	ping (int): pong

    Returns:
    	jsonResponse: String response cast to JSON

	"""
	strUrl = "https://ais-oci-pd.multotec-connect.com/jderest/orchestrator/ORCH_55_IGN_GetWorkOrderInformation"
	
	dictHeader = {"Authorization":"Basic QURWQU5TWVM6UzBsRG9ucmFjMW5n"} 
	
	httpClient = system.net.httpClient()
	jsonResponse = httpClient.get(url=strUrl, headers = dictHeader)
	#jsonResponse = system.util.jsonDecode(strResponse)
	return jsonResponse.json

def getWorkOrderInfo(strWorkOrderID):
	WorkOrders = getAllWorkOrders()
	return WorkOrders.get(strWorkOrderID,None)

def UpdateWO(strWOID):
	
	return

def PopulateTag():
	jsonWorkOrders = getAllWorkOrders()
	system.tag.writeBlocking("[default]Multotec/MM_PU_WorkOrders/AllWorkOrders", jsonWorkOrders)
	return