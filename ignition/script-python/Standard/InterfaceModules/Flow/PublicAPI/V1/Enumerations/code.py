#------------------------------------------------GetEnumerationGroups------------------------
def GetEnumerationGroups(ConnectionTagPath):
	endPoint = "v1/config/enumerationgroups"
	response = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetFromConnection(ConnectionTagPath=ConnectionTagPath,EndPoint=endPoint)
	return response['json']['enumerationGroups']
#------------------------------------------------GetEnumerationGroup------------------------
def GetEnumerationGroup(ConnectionTagPath,EnumerationGroupID):
	endPoint = "v1/config/enumerationgroups/" + str(EnumerationGroupID)
	response = Standard.InterfaceModules.Flow.PublicAPI.V1.Common.GetFromConnection(ConnectionTagPath=ConnectionTagPath,EndPoint=endPoint)
	return response['json']['enumerationGroup']
#------------------------------------------------GetOptions------------------------
def GetEnumerationGroupOptions(ConnectionTagPath,EnumerationGroupID,StartColumnIndex=0):
	enumerationGroup = GetEnumerationGroup(ConnectionTagPath=ConnectionTagPath,EnumerationGroupID=EnumerationGroupID)
	#print enumerationGroup
	columns = enumerationGroup['columns']
	rows = enumerationGroup['rows']
	optionsArray = []
	
	def getOptions(columnIndex,matchKey=None,matchOrdinals=None):
		options = {}
		for row in rows:
			rowValues = row['values']
			ordinal = row['ordinal']
			
			if matchOrdinals is not None and ordinal not in matchOrdinals:
				continue
			
			rowValue = rowValues[columnIndex]
			key = rowValue['value']
			if key not in options:
				option = {'ordinals':[],'value':key,'options':[]}
			else:
				option = options[key]
			
			ordinals = option['ordinals']
			ordinals.append(ordinal)
						
			if columnIndex+1 < len(rowValues):
				childOptions = getOptions(columnIndex+1,key,ordinals)
				option['options'] = childOptions
				
			options[key] = option

		return options
	
	columnIndex = StartColumnIndex
	options = getOptions(columnIndex)
	
	
	return options