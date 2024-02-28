# Event Based Table
#requiredMeasureItemType = "tables-eventbased-measureitem"
#requiredAttributeItemType = "tables-eventbased-attributeitem"
#requiredFolderNameType = "tables-eventbased-eventschemecomponent"

# Time Based Tables
#requiredMeasureItemType = "tables-timebased-measureitem"
#requiredAttributeItemType = "tables-timebased-attributeitem"
#requiredFolderNameType = "tables-timebased-sectioncomponent"

#==============================================GetDefinition==============================================
def GetDefinition(ChartID,Username=None,Connection=None,UserInformation=None,ConnectionTagPath=None,UsersDetailTagPath=None):	
	#logger = system.util.getLogger("getDefinition")
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection(ConnectionTagPath)

	if UserInformation is None:
		UsersInformationTagPath = UsersDetailTagPath + "/Information"
		UserInformation = Standard.Model.Common.GetUserInformation(Username,UsersInformationTagPath)
		
	headerValues = {'Cookie':'token=' + UserInformation["Interfaces"]["Flow"]['Token']}
	url = Connection["Private API"] + '/definition/charts/' + str(ChartID) 
	#logger.info("url: " + str(url))
	chartDefinition = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Get(url,HeaderValues = headerValues)	
	return chartDefinition	
	
#==============================================GetData==============================================
def GetData(ChartID,Username=None,Connection=None,UserInformation=None,StartUTC=None,EndUTC=None,TimeStampUTC=None,ConnectionTagPath = None):	
	#logger = system.util.getLogger("getDefinition")
	if Connection is None:
		Connection = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.GetConnection(ConnectionTagPath)

	if UserInformation is None:
		UsersInformationTagPath = UsersDetailTagPath + "/Information"
		UserInformation = Standard.Model.Common.GetUserInformation(Username,UsersInformationTagPath)
		
	headerValues = {'Cookie':'token=' + UserInformation["Interfaces"]["Flow"]['Token']}		
	url = Connection["Private API"] + '/data/charts/' + str(ChartID)
	if StartUTC is not None and EndUTC is not None:
		url += "?periodStart="+ str(StartUTC) + "&periodEnd=" + str(EndUTC)
	elif TimeStampUTC is not None:
		url += "?timestamp=" + str(TimeStampUTC)
	else:
		url = url
		
	chartData = Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.Get(url,HeaderValues = headerValues)	
	return chartData	

	
#==============================================GetChartPeriodInfo=========================================
def GetChartPeriodInfo(Components,GeneralComponentType = "tables-timebased-general",PeriodComponentType = "common-components-period"):
	for component in Components:
		componentType = component["componentType"]
		if componentType == GeneralComponentType:
			generalComponents = component['components']
			for generalComponent in generalComponents:
					generalComponentType = generalComponent["componentType"]
					if generalComponentType == 	PeriodComponentType:
						return generalComponent	
	return None	
#==============================================GetChartMeasureInfo=========================================
def GetChartMeasureInfo(Components,measureInfo = {},requiredItemType = "tables-timebased-measureitem",requiredFolderNameType = "tables-timebased-sectioncomponent"):
	sectionIndex = 0
	for component in Components:
		items = component["items"] 
		componentType = component["componentType"]
		if componentType == requiredFolderNameType:
			if component.has_key("title"):
				sectionName = component["title"]
				for item in items:
					if item["itemType"] == 	requiredItemType:
						measure = {}
						for row in item["measure"]:
							measure[row] = item["measure"][row]
						measure["SectionName"] = sectionName
						measure["SectionIndex"] = sectionIndex
						if item.has_key("title"):
							measure["MeasureTitle"] = item["title"]
						readOnly = False
						if item.has_key("readOnly"):
							readOnly = True
						measure["readOnly"] = readOnly
						measure["displayOrder"] = item["displayOrder"]
						measure["visibility"] = item["visibility"]
						mid = measure["measureID"]
						midKey = "mid" + str(mid)
						measureInfo[midKey] = measure
						
						sectionIndex += 1
		measureInfo = GetChartMeasureInfo(component["components"],measureInfo,requiredItemType,requiredFolderNameType)		
	return measureInfo

#==============================================GetRawData===========================================
#Get MeasureValueData
def GetRawDataPortrait(Data,attributesObject={},attributeValues={}):	
	data = []
	timePeriods = Data["timePeriods"]
	measureValues = Data["measureValues"]
	for tp in timePeriods:
		tpid = tp["id"]
		
	for mv in measureValues:
		if "v" in mv:
			pass
		else:
			continue
		tpid = mv["pid"]
		tpidKey = "pid" + str(tpid)
		if tpidKey in data:
			pass
		else:
			data[tpidKey] = {}	
				
		mid = mv["mid"]
		midKey = "mid" + str(mid)
		if midKey in data[tpidKey]:
			pass
		else:
			data[tpidKey][midKey] = {}
			
		avid = None
		if "avid" in mv:
			avid = mv["avid"]
			
		if avid is None:	
			eaKey = "NoContext"	
			if data[tpidKey][midKey].has_key(eaKey):
				data[tpidKey][midKey][eaKey].append(mv)
			else:
				data[tpidKey][midKey][eaKey] = []
				data[tpidKey][midKey][eaKey].append(mv)		
		else:
			avKey = "av" + str(avid)
			if attributeValues.has_key(avKey):
				eaKey = "ea" +  str(attributeValues[avKey]["eaid"])
				if attributesObject.has_key(eaKey):
					if data[tpidKey][midKey].has_key(eaKey):
						data[tpidKey][midKey][eaKey][avKey] = mv
					else:
						data[tpidKey][midKey][eaKey] = {}
						data[tpidKey][midKey][eaKey][avKey] = mv
		
	return data

#==============================================GetDataFromChart==============================================
#Get Formatted Data from Raw Data
#Includes all id's required to write back
#Includes all meta data required for Reporting
#rowDataStructure:
def GetDataFromTimePeriodChart(Definition,Data):
	
	return


def GetDataFromTimePeriod(FlowTimePeriod,Measures=None):
	return

def GetColumnInstance(field,header,visible,editable = False,StrictWidth = False,Width = "",justify = "auto",render={'datatype':'auto','numberFormat':'0.0','dateFormat':'YYYY/MM/DD HH:mm:ss'},viewPath = "",viewParams={}):
	
	columnInstance = {
				  "field": field,
				  "visible": visible,
				  "editable": editable,
				  "render": render['datatype'],
				  "justify": justify,
				  "align": "center",
				  "resizable": True,
				  "sortable": False,
				  "sort": "none",
				  "viewPath": viewPath,
				  "viewParams": viewParams,
				  "boolean": "checkbox",
				  "number": "value",
				  "progressBar": {
					"max": 100,
					"min": 0,
					"bar": {
					  "color": "",
					  "style": {
						"classes": ""
					  }
					},
					"track": {
					  "color": "",
					  "style": {
						"classes": ""
					  }
					},
					"value": {
					  "enabled": True,
					  "format": "0,0.##",
					  "justify": "center",
					  "style": {
						"classes": ""
					  }
					}
				  },
				  "toggleSwitch": {
					"color": {
					  "selected": "",
					  "unselected": ""
					}
				  },
				  "numberFormat": render['numberFormat'],
				  "dateFormat": render['dateFormat'],
				  "width": Width,
				  "strictWidth": StrictWidth,
				  "header": {
					"title": header,
					"justify": justify,
					"align": "center",
					"style": {
					  "classes": ""
					}
				  },
				  "footer": {
					"title": "",
					"justify": "left",
					"align": "center",
					"style": {
					  "classes": ""
					}
				  },
				  "style": {
					"classes": ""
				  }
				}
	return columnInstance

def GetColumnsfromMeasureandAttributeInfo(MeasureInfo,AttributeInfo,RequiredColumns,UseUOM = False):
	#If UseUOM then UOM used as part of unique field key
	#Get Measure Columns
	measuresColumnsObject = {}
	for midKey in MeasureInfo:
		measureTitle = MeasureInfo[midKey]["MeasureTitle"] 
		measureUom = MeasureInfo[midKey]["uom"]
		displayOrder = MeasureInfo[midKey]["displayOrder"]
		description = ""
		if "description" in MeasureInfo[midKey]:
			description = MeasureInfo[midKey]["description"]
		visibility = "alwaysVisible"
		if "visibility" in MeasureInfo[midKey]:
			visibility = MeasureInfo[midKey]["visibility"]
		
		readOnly = MeasureInfo[midKey]["readOnly"]
		if UseUOM:
			field = (measureTitle + measureUom).replace(" ","").replace(":","").replace("/","")
		else:
			field = measureTitle.replace(" ","").replace(":","").replace("/","")
			
		if field in measuresColumnsObject:			
			currentDisplayOrder = measuresColumnsObject[field]["displayOrder"]			
			if displayOrder > currentDisplayOrder:
				measuresColumnsObject[field]["displayOrder"] = displayOrder
			if (measureUom in measuresColumnsObject[field]["uom"]) == False:
				measuresColumnsObject[field]["uom"] += ("/" + measureUom)
		else:	
			requiredColumnObject = {
									"field":field,
									"header":"",
									"uom":measureUom,
									"displayOrder":displayOrder,
									"measureTitle":measureTitle,
									"description":description,
									"readOnly":readOnly,
									"visibility":visibility
										}
			measuresColumnsObject[field] = requiredColumnObject
			
	for field in measuresColumnsObject:
		displayOrder = measuresColumnsObject[field]["displayOrder"]
		measureTitle = measuresColumnsObject[field]["measureTitle"]
		uom =  measuresColumnsObject[field]["uom"]
		description = measuresColumnsObject[field]["description"]
		readOnly = measuresColumnsObject[field]["readOnly"]
		visibility = measuresColumnsObject[field]["visibility"]
		if uom != "":
			header = measureTitle + " (" + uom + ")"
		else:
			header = measureTitle
		requiredColumnObject = {
							"field":field,
							"header":header,
							"displayOrder":displayOrder,
							"description":description,
							"readOnly":readOnly,
							"visibility":visibility
								}		
		RequiredColumns.append(requiredColumnObject)
		
	#Get Attribute Columns
	attributesUsed = set()
	for eaKey in AttributeInfo:
		header = AttributeInfo[eaKey]["title"] 
		displayOrder = AttributeInfo[eaKey]["displayOrder"]
		field = header.replace(" ","").replace(":","").replace("/","")
		if field in attributesUsed:	
			continue
		else:
			attributesUsed.add(field)
		requiredColumnObject = {
								"field":field,
								"header":header,
								"displayOrder":displayOrder
									}
		RequiredColumns.append(requiredColumnObject)
		
	RequiredColumnsSorted = sorted(RequiredColumns, key = lambda row:row["displayOrder"])	
	return RequiredColumnsSorted
