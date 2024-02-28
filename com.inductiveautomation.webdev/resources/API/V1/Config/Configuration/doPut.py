def doPut(request, session):
	logConfiguration = system.util.getLogger("API/V1/Config/Configuration-Put")
	
	logConfiguration.info("Hello")
	return {'json': 'Put Some Config Object'}