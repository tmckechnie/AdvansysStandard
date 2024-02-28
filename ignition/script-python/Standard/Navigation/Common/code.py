#======================================================== SetLogoImage ======================================================== 
def SetLogoImage(TagPath,Image):
	system.tag.writeBlocking([TagPath],[Image])
	return
#======================================================== GetModelItems ================================================	
def GetModelItems(ModelItem):
	modelItem = ModelItem
	tagProvider = modelItem['TagProvider']
	pathToParentFolder = modelItem['PathToParentFolder']
	modelItemTagPath = "[" + tagProvider + "]"+ pathToParentFolder + "/Model Item"

	
	modelItem = {"data": 
						{"Name": modelItem["Name"],
						"Path": "0",
						"ViewPaths": modelItem["ViewPaths"]["ViewPathArray"],
						"BaseViewPath":modelItem["BaseViewPath"],
						"TagFolderName": modelItem["Name"],
						"ModelItemTagPath": modelItemTagPath,
						"Order":0
						
						},
				"modelItems": modelItem["Children"]
				}  
	return [modelItem]
#===================================================== GetPopupMenuItem ================================================================						
def GetPopupMenuItem(ModelItemTagPath,Path,ContentType = "",Label = "",InstanceStyleClass = ""):
	if Label=="":
		Label = ContentType
	menuItem = {
				  "instanceStyle": {
					"classes": InstanceStyleClass
				  },
				  "instancePosition": {
					"grow": 1
				  },
				  "ModelItemTagPath": ModelItemTagPath,
				  "Path":Path,
				  "ContentType":ContentType,
				  "Label":Label
				}
	return menuItem
#======================================================== GetContentTypes ========================================================	
def GetContentTypes(ViewPaths,GetOnlyConfiguredContentTypes=False,AllowedContentTypes=[]):		
	viewPaths = ViewPaths
	contentTypes={}
	def checkAllowedContentType(contentType):
		if len(AllowedContentTypes)==0:
			return True
		allowed=False
		for allowedContentType in AllowedContentTypes:
			if contentType == allowedContentType:
				return True
		return False
		

	for viewPathItem in viewPaths:
		viewPath = viewPathItem["ViewPath"]
		label = viewPathItem["Label"]
		order = int(str(viewPathItem["Order"]))
		
		if not GetOnlyConfiguredContentTypes or (GetOnlyConfiguredContentTypes and len(viewPath)>0):
			contentTypeArray = viewPathItem["ContentType"]
			for contentType in contentTypeArray:
				if checkAllowedContentType(contentType):
					contentTypes[contentType] = {'contentType':contentType,'label':label,'order':order}
	contentTypesList = contentTypes.values()
	contentTypesSorted = sorted(contentTypesList, key=lambda d: (d['order'],d['contentType']))
	return contentTypesSorted
#======================================================== GetModelItemByTagPath ======================================================== 
#Script used to find a specific modelItem within ModelItems
#Returns a ModelItem object of the correct ModelItemTagPath
def GetModelItemByTagPath(ModelItems,ModelItemTagPath):
	modelItems = ModelItems
	for modelItem in modelItems:
		modelItemTagPath = str(modelItem['data']['ModelItemTagPath'])
		if modelItemTagPath == str(ModelItemTagPath):
			return modelItem
		else:
			modelItem = SearchModelItem(modelItem['modelItems'],ModelItemTagPath)
			if modelItem is not None:
				return modelItem
	return None	
#======================================================== GetModelItemByPath ======================================================== 
#Script used to find a specific modelItem within ModelItems
#Returns a ModelItem object of the correct Path '0/1/0'
def GetModelItemByPath(ModelItems,Path):
	modelItems = ModelItems
	path = Path
	pathArray = path.split('/')	
	for i in pathArray:
		index=int(i)
		if len(modelItems)>index:
			modelItem = modelItems[index]
			modelItems = modelItem['modelItems']
			
	return 	modelItem	
	

#======================================================== GetModelItemsUpTo--------------------------
#Script to get full list of ModelItems that lead to specified ModelItem
def GetModelItemsUpTo(ModelItems,Path):
	modelItems = ModelItems
	#modelItem = SearchModelItem(modelItems,ModelItemTagPath)
	#If Model Item is not found the return None
#	if modelItem is None:
#		return []
	modelItemsList = []
	path = Path
	pathArray = path.split('/')
	for i in pathArray:
		index=int(i)
		if len(modelItems)>index:
			modelItem = modelItems[index]
			modelItemsList.append(modelItem)
			modelItems = modelItem['modelItems']	

	return modelItemsList

#======================================================== GetModelItemChildren ======================================================== 
#Script to get full list of ModelItems Children for Specified ModelItem Path
def GetModelItemChildren(ModelItems,Path):
#	modelItems = ModelItems
#	path = Path
#	pathArray = path.split('/')
#	#return path
#	for i in pathArray:
#		index=int(i)
#		if len(modelItems)>index:
#			modelItem = modelItems[index]
#			modelItems = modelItem['modelItems']
	modelItem = GetModelItemByPath(ModelItems=ModelItems,Path=Path)
	modelItems = modelItem['modelItems']
	childModelItems = []
	for modelItem in modelItems:
		childModelItem = {'data':modelItem['data'],
						   'childrenCount':len(modelItem['modelItems'])
						   }
		childModelItems.append(childModelItem)
		
	return childModelItems
#======================================================== SearchModelItem ======================================================== 
#Script used to find a specific modelItem within ModelItems
#Returns a ModelItem object of the correct ModelItem
def SearchModelItem(ModelItems,ModelItemTagPath):
	modelItems = ModelItems
	for modelItem in modelItems:
		modelItemTagPath = str(modelItem['data']['ModelItemTagPath'])
		if modelItemTagPath == str(ModelItemTagPath):
			return modelItem
		else:
			modelItem = SearchModelItem(modelItem['modelItems'],ModelItemTagPath)
			if modelItem is not None:
				return modelItem
	return None

#======================================================== GetCurrentModelItemPath ================================================
#Function to get the CurrentModelItemPath for this page
def GetCurrentModelItem(CurrentModelItem,UseSession = True,PerspectivePageID = None):
	currentModelItem = None
	
	#Standard.Utilities.Common.LogMessage(LoggerName="GetCurrentModelItem 1:", Message = 'CurrentModelItem: ' + str(CurrentModelItem))
	#==getModelItemTagPathsKey ================================================	
	def getModelItemKey(UseSession = True,PerspectivePageID = None):
		key = None
		#If using SessionModelItemTagPath then modelItemKey is sessionKey else use perspectivePageID key
		if UseSession:
			key = "Session"	
		elif PerspectivePageID is not None:
			key = "pid" + str(PerspectivePageID)
		return key
	
	#Get required ModelItemTagPathsKey
	currentModelItemKey = getModelItemKey(UseSession,PerspectivePageID)
	if currentModelItemKey in CurrentModelItem:
		currentModelItem = CurrentModelItem[currentModelItemKey]			
	else:
		currentModelItem = CurrentModelItem["Session"]
	#Standard.Utilities.Common.LogMessage(LoggerName="GetCurrentModelItem 2:", Message = 'CurrentModelItem: ' + str(currentModelItem))
	#Ensure that Path is specisfied for CurrentModelItem
	currentModelItem = currentModelItem.toDict()
	path = currentModelItem['Path']
	if path == "" or path is None:
		currentModelItem['Path'] = '0'
	return currentModelItem

#======================================================== UpdateCurrentModelItemTagPaths ================================================	
#Function to update the CurrentModelItemPaths object for this session
def UpdateCurrentModelItem(Path,CurrentModelItem,UseSession = True,PerspectivePageID = None,ContentType="",SearchModule=""):
	#Get required ModelItemTagPathsKey
	if CurrentModelItem is None:
		CurrentModelItem = {'Session':{"ContentType":"Overview","Path": "0","SearchModule": ""}}
	updatedModeltItemKey = getModelItemTagPathsKey(UseSession,PerspectivePageID)
	#Re-create the UpdateCurrentModelItemTagPaths object as session property is PropertyTreeScriptWrapper$ObjectWrapper 
	#and cannot be written to like a python object
	def getCurrentModelItem(CurrentModelItem):
		pyCurrentModelItem = {}
		for modelItemKey in CurrentModelItem:
			pyCurrentModelItem[modelItemKey] = CurrentModelItem[modelItemKey]
		return pyCurrentModelItem
		
	CurrentModelItem = getCurrentModelItem(CurrentModelItem)
	contentType = ContentType
	path = Path
	#modelItemData = ModelItemData
	if updatedModeltItemKey in CurrentModelItem:
		if contentType == "":
			contentType = CurrentModelItem[updatedModeltItemKey]['ContentType']
#		if path is None:
#			path = CurrentModelItemTagPaths[updatedModeltItemKey]['Path']
#		if modelItemData is None:
#			modelItemData = CurrentModelItemTagPaths[updatedModeltItemTagPathKey]['ModelItemData']
	#Update ModelItemTagPaths key with new value
	CurrentModelItem[updatedModeltItemKey] = {'Path':path,'ContentType':contentType,'SearchModule':SearchModule}
	return CurrentModelItem
#======================================================== GetCurrentModelItemPath ================================================
#Function to get the CurrentModelItemPath for this page
def GetCurrentModelItemTagPath(CurrentModelItemTagPaths,UseSessionModelItemTagPath = True,PerspectivePageID = None):
	currentModelItemTagPath = None
	#Get required ModelItemTagPathsKey
	currentModelItemTagPathsKey = getModelItemTagPathsKey(UseSessionModelItemTagPath,PerspectivePageID)
	if currentModelItemTagPathsKey in CurrentModelItemTagPaths:
		currentModelItemTagPath = CurrentModelItemTagPaths[currentModelItemTagPathsKey]			
	else:
		currentModelItemTagPath = CurrentModelItemTagPaths["Session"]
	return currentModelItemTagPath

#======================================================== UpdateCurrentModelItemTagPaths ================================================	
#Function to update the CurrentModelItemPaths object for this session
def UpdateCurrentModelItemTagPaths(UpdatedModelItemTagPath,CurrentModelItemTagPaths,UseSessionModelItemTagPath = True,PerspectivePageID = None,ContentType="",SearchModule="",Path=None,ModelItemData=None):
	#Get required ModelItemTagPathsKey
	updatedModeltItemTagPathKey = getModelItemTagPathsKey(UseSessionModelItemTagPath,PerspectivePageID)
	#Re-create the UpdateCurrentModelItemTagPaths object as session property is PropertyTreeScriptWrapper$ObjectWrapper 
	#and cannot be written to like a python object
	def getCurrentModelItemTagPaths(CurrentModelItemTagPaths):
		pyCurrentModelItemTagPaths = {}
		for modelItemTagPathsKey in CurrentModelItemTagPaths:
			pyCurrentModelItemTagPaths[modelItemTagPathsKey] = CurrentModelItemTagPaths[modelItemTagPathsKey]
		return pyCurrentModelItemTagPaths
		
	CurrentModelItemTagPaths = getCurrentModelItemTagPaths(CurrentModelItemTagPaths)
	contentType = ContentType
	path = Path
	modelItemData = ModelItemData
	if updatedModeltItemTagPathKey in CurrentModelItemTagPaths:
		if contentType == "":
			contentType = CurrentModelItemTagPaths[updatedModeltItemTagPathKey]['ContentType']
		if path is None:
			path = CurrentModelItemTagPaths[updatedModeltItemTagPathKey]['Path']
#		if modelItemData is None:
#			modelItemData = CurrentModelItemTagPaths[updatedModeltItemTagPathKey]['ModelItemData']
	#Update ModelItemTagPaths key with new value
	CurrentModelItemTagPaths[updatedModeltItemTagPathKey] = {'ModelItemTagPath':UpdatedModelItemTagPath,'ContentType':contentType,'SearchModule':SearchModule,'Path':path}
	return CurrentModelItemTagPaths

#======================================================== getModelItemTagPathsKey ================================================	
def getModelItemTagPathsKey(UseSessionModelItemTagPath = True,PerspectivePageID = None):
	modelItemTagPathsKey = None
	#If using SessionModelItemTagPath then modelItemKey is sessionKey else use perspectivePageID key
	if UseSessionModelItemTagPath:
		modelItemTagPathsKey = "Session"	
	elif PerspectivePageID is not None:
		modelItemTagPathsKey = "pid" + str(PerspectivePageID)
	return modelItemTagPathsKey
	

##------------------------------------------------------------------------------------GetContentTypes----------------------------------------------------------------------	
#def _GetContentTypes(ModelItemTagPath,GetOnlyConfiguredContentTypes=False,AllowedContentTypes=[]):		
#	#logger = system.util.getLogger("Navigation [Common]")
#	#logger.info("GetContentTypes:" + ModelItemTagPath)
#	ViewPathsTagPath = ModelItemTagPath + "/ViewPaths"
#	viewPaths = system.tag.readBlocking([ViewPathsTagPath])[0].value
#	contentTypes={}
#	def checkAllowedContentType(contentType):
#		if len(AllowedContentTypes)==0:
#			return True
#		allowed=False
#		for allowedContentType in AllowedContentTypes:
#			if contentType == allowedContentType:
#				return True
#		return False
#		
#	viewPathArray = viewPaths['ViewPathArray']
#
#	for viewPathItem in viewPathArray:
#		viewPath = viewPathItem["ViewPath"]
#		label = viewPathItem["Label"]
#		order = int(str(viewPathItem["Order"]))
#		
#		if not GetOnlyConfiguredContentTypes or (GetOnlyConfiguredContentTypes and len(viewPath)>0):
#			contentTypeArray = viewPathItem["ContentType"]
#			for contentType in contentTypeArray:
#				if checkAllowedContentType(contentType):
#					contentTypes[contentType] = {'contentType':contentType,'label':label,'order':order}
#	contentTypesList = contentTypes.values()
#	contentTypesSorted = sorted(contentTypesList, key=lambda d: (d['order'],d['contentType']))
#	return contentTypesSorted

#
##------------------------------------------------------------------------------------showChild-------------------------------------------------------------------------
#def showChild(modelTagPath):
#	#logger = system.util.getLogger("Navigation [Common]")
#	#logger.info("showChild:" + modelTagPath)
#	visiblePath = modelTagPath + "/Visible"
#	orderPath = modelTagPath + "/Order"
#	childTagPath = modelTagPath + "/ChildrenTagProviderFolderPath"
#	values = system.tag.readBlocking([visiblePath,orderPath,childTagPath])
#	showChild = values[0].value
#	order = values[1].value
#	childTagPath = values[2].value
#	return {"showChild":showChild,"childTagPath":childTagPath,"order":order}
##------------------------------------------------------------------------------------GetChildrenCount-------------------------------------------------------------------					
#def GetChildrenCount(PathToParentFolder):
#	pathToParentFolder = PathToParentFolder
#	#logger = system.util.getLogger("Navigation [Common]")
#	#logger.info("getChildrenCount:" + pathToParentFolder)	
#	childrenCount = 0
#	children = system.tag.browse(path = pathToParentFolder, filter = {"tagType":"Folder","recursive":False})
#	#print children
#	for child in children:
#		childModelTagPath = child["fullPath"].toString()  + "/Model Item"
#		showChildItem = showChild(childModelTagPath)
#		#print showChildItem
#		if showChildItem["showChild"]:
#			childrenCount += 1		
#	return childrenCount
#------------------------------------------------------------------------------------getChildAreaName-------------------------------------------------------------------			
#def getChildAreaName(modelTagPath):
#	#logger = system.util.getLogger("Navigation [Common]")
#	#logger.info("getChildAreaName:" + modelTagPath)	
#	childAreaName = system.tag.readBlocking([modelTagPath + "/Name"])[0].value
#	return childAreaName	


##------------------------------------------------------------------------------------GetChildModelItems--------------------------
##Script to get immediate children of a model item. Used to get the ModelItem Menu items for breadcrumb and menu bar popups
#def GetChildModelItemTagPaths(ModelItems,ModelItemTagPath):
#	childModelItemTagPaths = []
#	modelItem = SearchModelItem(ModelItems,ModelItemTagPath)
#	#If Model Item is not found then return an empty array
#	if modelItem is None:
#		return childModelItemTagPaths
#	childModelItems = modelItem["modelItems"]
#	for childModelItem in childModelItems:
#		childModelItemTagPath = childModelItem["data"]["ModelItemTagPath"]
#		childModelItemTagPaths.append(childModelItemTagPath)
#	
#	return childModelItemTagPaths
##------------------------------------------------------------------------------------GetModelItemsTagPathList--------------------------
##Script to get full list of ModelItemTagPaths that lead to specified ModelItem
#def GetModelItemsTagPathList(ModelItems,ModelItemTagPath):
#	modelItems = ModelItems
#	modelItem = SearchModelItem(modelItems,ModelItemTagPath)
#	#If Model Item is not found the return None
#	if modelItem is None:
#		return []
#	modelItemTagPathList = []
#	path = modelItem['data']['Path']
#	pathArray = path.split('/')
#	for i in pathArray:
#		index=int(i)
#		if len(modelItems)>index:
#			modelItem = modelItems[index]
#			modelItemTagPath= modelItem['data']['ModelItemTagPath']
#			modelItemTagPathList.append(modelItemTagPath)
#			modelItems = modelItem['modelItems']	
#
#	return modelItemTagPathList

#---------------------------------------------------SearchModule--------------------------
#This will query tag values within Metadata/InstanceName and Metadata/Description
def SearchModule(Provider,SearchString,Limit=1000):
	
	query = {
		"options": {"includeUdtMembers": True,"includeUdtDefinitions": False},
		"condition": {"path": "*Metadata*","tagType": "AtomicTag","attributes": {"values": [],"requireAll": True},
			"valueSource": "memory","properties": {
		      "op": "Or",
		      "conditions": [
		        {"op": "And","conditions": [{"prop": "name","comp":"Equal","value": "Description"}]},
		        {"op": "And","conditions": [{"prop": "name","comp":"Equal","value": "InstanceName"}]}
		      ]
		    }
		},
		"returnProperties": ["name","tagType","quality"]
		}
	
	results = system.tag.query(provider=Provider, query=query, limit=Limit)
	
	searchString = SearchString
	modules = []
	wildCard = '*'
	searchType = 'a' #Default is to search any
	searchStr = searchString.replace(wildCard,"")
	searchStringLen = len(searchStr)
	if searchString[0]==wildCard:
		searchType = 'r' #match Left
	elif searchString[-1]==wildCard:
		searchType = 'l' #match Right
	#print [searchType,searchStr]
	for result in results:
		name = result['name']
		resultValue = str(result['value'].value)
		searchContinue = False
		
#		searchStr = searchString.replace(wildCard,"")
#		searchStringLen = len(searchString)
		#any
		if searchType == 'a' and searchStr in resultValue:
			searchContinue = True
		#match Left
		elif searchType == 'l' and searchStr == resultValue[:searchStringLen]:
			searchContinue = True
		#match Right
		elif searchType == 'r' and searchStr == resultValue[-searchStringLen:]:
			searchContinue = True
		
		#print [searchContinue,resultValue,resultValue[:searchStringLen],resultValue[-searchStringLen:]]
		if searchContinue:
			#return result
			#Search For ModelItem
			fullPath = result['fullPath']
			#paths = fullPath.split('/')
			paths = fullPath.getParentPath()
			pathLength = fullPath.getPathLength()
			checkPath = fullPath.getParentPath()
			modelItemPaths = []
			for i in range(pathLength-1):
				checkPath = checkPath.getParentPath()
				
				modelItemPath = str(checkPath) + '/Model Item'
				modelItemVisiblePath = str(modelItemPath) + '/Visible'
				strCheckPath = str(modelItemVisiblePath)
				checked={'path':strCheckPath}
				exists = system.tag.exists(strCheckPath)
				if exists:
					checked['exists'] = exists
					visible = system.tag.readBlocking(tagPaths=[strCheckPath])[0].value
					checked['visible'] = visible
					if visible:
						modelItemPaths.append(checked)
						modelItemTagPath = modelItemPath
						instancePath = result['fullPath'].getParentPath().getParentPath()
						instanceName = instancePath.getLastPathComponent()
						searchResult = {'tag':result['name'],'value':resultValue}
						module = {'modelItemTagPath':modelItemTagPath,'instance':{'fullPath':instancePath,'name':instanceName},'SearchResult':searchResult}
						modules.append(module)
						break
	return modules


























