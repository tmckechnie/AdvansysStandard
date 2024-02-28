#==========================================================LogMessage==========================================================		
def LogMessage(LoggerName,Message,DebugLevel = 1):
	if DebugLevel>0:
		logger = system.util.getLogger(LoggerName)
		logger.info(Message)
	return
#==========================================================PrintPerspectiveMessage==========================================================		
def PrintPerspectiveMessage(Message,DebugLevel = 1):
	if DebugLevel>0:
		system.perspective.print(Message)
	return
	
#==========================================================LogMessage==========================================================		
def GetListFromDataset(Dataset):
	getColumnHeaders = system.dataset.getColumnHeaders(Dataset)
	dataset = system.dataset.toPyDataSet(Dataset)
	list = []
	for row in dataset:
		dictRow = {}
		for col in getColumnHeaders:	
			dictRow[col] = row[col]
		list.append(dictRow)
	return list

#==========================================================GetObjectFromList==========================================================	
def GetObjectFromList(List,KeyName):
	object = {}
	for item in List:
		key = item[KeyName]
		object[key] = item

	return object

#==========================================================GetDate==========================================================
def GetDate(DateTime=None):
	if DateTime is None:
		DateTime = system.date.now()
	return system.date.midnight(DateTime)
	

