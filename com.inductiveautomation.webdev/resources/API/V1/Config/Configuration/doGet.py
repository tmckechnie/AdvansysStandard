def doGet(request, session):
	logConfiguration = system.util.getLogger("API/V1/Config/Configuration-Get")
	logConfiguration.info("Configuration-Get Called from:" + request["remoteAddr"])
	
	return {'json': 'Send Some Config Object'}