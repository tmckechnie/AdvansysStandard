def dtfromiso(strIsoDateTime):
	"""Converts ISO8601 string to dt

    Accounts for time zone suffix if separated by + sign

    Args:
        strIsoDateTime: ISO datetime string

    Returns:
        dt object

    Raises:
        Exception: returns default dt of 1970 01 01
	"""
	from datetime import datetime
	from datetime import timedelta
	
	#Check for timestamp separator
	if int(strIsoDateTime.find("+")) > 0:
		strTimeStamp = strIsoDateTime[:strIsoDateTime.find("+")]
		strOffset = strIsoDateTime[strIsoDateTime.find("+"):strIsoDateTime.find("+")+3]
	else:
		strTimeStamp = strIsoDateTime
		strOffset = "0"
	try:
		dt = datetime.strptime(strTimeStamp,"%Y-%m-%dT%H:%M:%S")
		#Correct timestamp against local timezone. Assuming gateway is in the same timezone as ESP
		dt = dt - timedelta(hours=system.date.getTimezoneOffset())
	except Exception as e:
		logger = system.util.getLogger("dtfromiso")
		logger.error(str(e))
		dt = datetime(1970,1,1)
	return dt
	
def timeStringFromSecs(seconds, granularity=2):
	"""
	Converts seconds to descriptive string 
	Credit: StackOverflow
	"""
	intervals = (
	    ('weeks', 604800),  # 60 * 60 * 24 * 7
	    ('days', 86400),    # 60 * 60 * 24
	    ('hours', 3600),    # 60 * 60
	    ('minutes', 60),
	    ('seconds', 1),
	)
	result = []

	for name, count in intervals:
		value = seconds // count
		if value:
			seconds -= value * count
			#Change description to singular if quantity is 1
			if value == 1:
				name = name.rstrip('s')
			
			result.append("{} {}".format(value, name))
	return ', '.join(result[:granularity])
	
def getTimeToPowerOff(strTagpath):
	from datetime import datetime
	from datetime import timedelta
	strTagpath += "/AreaInformation/Data"
	
	dictEventData = system.tag.readBlocking([strTagpath])[0].value
	
	strStartDT = dictEventData["events"][0]["start"]

	dt = EskomSePush.dtfromiso(strStartDT)
	
	delta = datetime.now() - dt
	
	UTCOffset = system.date.getTimezoneOffset() * 3600
	
	return (delta.total_seconds() - UTCOffset)/60.0