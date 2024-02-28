#
#usersDetailTagPath = '[default]Flow/CCBZA10/UsersDetail'
##=========================================================GetUsersDetail=========================================================
#def GetUsersInformation(UsersInformationTagPath):
#	usersInformation = system.tag.readBlocking([UsersInformationTagPath])[0].value
#	#Standard.InterfaceModules.Flow.Common.Logmessage("GetUsersInformation",str(usersInformation) + str(type(usersInformation)),DebugLevel=10)
#	usersInformation = usersInformation.toDict()
#	return usersInformation
#=========================================================getUserDetailTagPath=========================================================
def getUserInformationTagPath(username,UsersInformationTagPath = None):
	username = username.lower().replace('\\','')
	if UsersInformationTagPath is None:
		global usersDetailTagPath
		userInformationTagPath = usersDetailTagPath + "/Information" + "['%s']"%(username)
	else:		
		userInformationTagPath = UsersInformationTagPath + "['%s']"%(username)	
	
	return userInformationTagPath
#=========================================================GetUserRoleMapping=========================================================
def GetUserRoleMapping(UsersDetailTagPath):
	UserRoleMappingTagPath = getUserRoleMappingTagPath(UsersDetailTagPath)
	userRoleMapping = Standard.Model.Common.TagRead(UserRoleMappingTagPath)
	if userRoleMapping is not None:
		userRoleMapping = userRoleMapping.toDict()
	return userRoleMapping
	
#=========================================================getUserRoleMappingTagPath=========================================================	
def getUserRoleMappingTagPath(UsersDetailTagPath):
	UserRoleMappingTagPath = UsersDetailTagPath + "/User Role Mapping"
	return UserRoleMappingTagPath

	
#=========================================================GetUserDetail=========================================================
#Get User Detail from UsersDetail Information Object on UsersDetail UDT
def GetUserInformation(Username,UsersInformationTagPath):
	#logger = system.util.getLogger("GetUserInformation")
	username = Username.lower().replace('\\','')
	usersInformationObject = GetUsersInformation(UsersInformationTagPath)
	if username in usersInformationObject:
		userInformation = usersInformationObject[username]
	else:
		userInformation = None
	return userInformation
	
#=========================================================UpdateUserDetail=========================================================
def UpdateUserInformation(Username,UserInfomationObject,UsersInformationTagPath):
	
	userInformationTagPath = getUserInformationTagPath(Username,UsersInformationTagPath)
	currentUserInformation = GetUserInformation(Username,UsersInformationTagPath)
	if currentUserInformation is not None:
		UserInformationObject = system.util.jsonEncode(UserInfomationObject)
		UserInformationWrite = system.tag.writeBlocking([userInformationTagPath],[UserInformationObject])			
	else:
		usernameKey = Username.lower().replace('\\','')		
		UsersInformation = GetUsersInformation(UsersInformationTagPath)
		UsersInformation[usernameKey] = UserInfomationObject
		Standard.InterfaceModules.Flow.PrivateAPI.V1.Common.LogMessage("UpdateUserInformation",str(UsersInformation),Debug=True)
		UsersInformation = system.util.jsonEncode(UsersInformation)
		UserInformationWrite = system.tag.writeBlocking([UsersInformationTagPath],[UsersInformation])	
		
	return True
	
	
#=========================================================GetUserDetailObject=========================================================
def GetUserInformationObject():
	
	userDetailObject = {
						  "FullName": "",
						  "Image": "",
						  "Username":"",
						  "Interfaces": {
							"Flow": {
							  "Token": "",
							  "UserRoles": [],
							  "Expires": "",
							  "Valid":True
							}
						  }
						}
	return userDetailObject
	
#=========================================================UpdateUserImage=========================================================

def UpdateUserImage(UserDetailTagPath,Username,Image):
	usersInformationTagPath = UserDetailTagPath + "/Information"
	imageConvertorTagPath = UserDetailTagPath + "/ImageConverter"
	
	#Get Current User Information
	userInformation = GetUserInformation(Username,usersInformationTagPath)
	
	#Convert Bytes to String by writing to String Tag
	system.tag.writeBlocking([imageConvertorTagPath],[Image])
	#Read String Converted Image back from tag
	imageConverted = system.tag.readBlocking([imageConvertorTagPath])
	imageConvertedString = imageConverted[0].value
	
	if userInformation is None:
		return

	#Get User
	usernameKey = Username.lower().replace('\\','')	
	#Get image
	userInformationTagPath = usersInformationTagPath + "['%s']"%(usernameKey)
	userInformation['Image'] = 'data:imagef;base64,%s'%(imageConvertedString)
	
	userInformation = system.util.jsonEncode(userInformation)
	system.tag.writeBlocking([userInformationTagPath],[userInformation])	
	return 	



	
#=========================================================TagWrite=========================================================
	
def TagWrite(TagPath,TagValue,retries = 3):	
	#If Tag Quality is bad then retry 3 times
	for retry in range(retries):
		tagQualityObject = system.tag.writeBlocking([TagPath],[TagValue])[0]
		tagQuality = tagQualityObject.isGood()
		if tagQuality:
			break
	
	return tagQuality
	
#=========================================================TagRead=========================================================	
def TagRead(TagPath):	
	tagRead = system.tag.readBlocking([TagPath])[0]
	tagQuality = tagRead.quality
	if tagQuality.isGood():
		tagValue = tagRead.value	
	else:
		tagValue = None	
	return tagValue
#=========================================================HashMapToPyObject=========================================================		
def HashMapToPyObject(hashMap):
	object = {}
	for key in hashMap.keySet():
		value = hashMap.get(key)
		object[key] = value
	
	return object

#=========================================================GetChildModelItems=========================================================		
def GetChildModelItems(FolderTagPath):
	modelItems = getChildModelItems(FolderTagPath=FolderTagPath,path="0",modelItems=[])
	return system.util.jsonEncode(modelItems)
	
#=========================================================getChildModelItems=========================================================			
def getChildModelItems(FolderTagPath,path,modelItems=[]):
	folderTagPath = FolderTagPath
	childAreas = system.tag.browse(folderTagPath, filter = {"tagType":"Folder","recursive":False})
	index = 0
	rootPath = path
	for childArea in childAreas:		
		childTagPath = childArea["fullPath"].toString()
		modelItemTagPath = childTagPath + "/Model Item"
		childItem = getChildModelItem(ModelItemTagPath = modelItemTagPath)
		showChildItem = childItem["showChild"]
		if showChildItem:
			#Check if Child is on Different Tag Provider
			childTagPathItem = childItem["childTagPath"]
			if childTagPathItem != "":
				childTagPath = childTagPathItem
				modelItemTagPath = childTagPath + "/Model Item"
				childItem = getChildModelItem(ModelItemTagPath = modelItemTagPath)
				
			viewPaths = childItem["viewPaths"]	
			baseViewPath = childItem["baseViewPath"]
			childModelItemOrder = childItem["order"]
			childItemName = childItem["name"]
			tagFolderName = childArea["name"]
			if childItemName is None:
				childItemName = tagFolderName
				
			if rootPath =="":
				path = "%s"%index
			else:
				path = rootPath + "/%s"%index
			modelItem = getModelItem(Name = childItemName, ModelItemTagPath = modelItemTagPath, tagFolderName = tagFolderName,path = path,order = childModelItemOrder,viewPaths=viewPaths,baseViewPath = baseViewPath)
			
			childItems = getChildModelItems(childTagPath,path,modelItem["modelItems"])
			index += 1	
			modelItems.append(modelItem)
				
	modelItemsSorted = sorted(modelItems, key=lambda d: d['data']['Order'])				
	return modelItemsSorted
#=========================================================getChildModelItem=========================================================
def getChildModelItem(ModelItemTagPath):
	modelItemTagPath= ModelItemTagPath

	visiblePath = modelItemTagPath + "/Visible"
	namePath = modelItemTagPath + "/Name"
	orderPath = modelItemTagPath + "/Order"
	childTagPath = modelItemTagPath + "/ChildrenTagProviderFolderPath"
	viewPathsTagPath = modelItemTagPath + "/ViewPaths"
	baseViewPath = modelItemTagPath + "/BaseViewPath"
	values = system.tag.readBlocking([namePath,visiblePath,orderPath,childTagPath,viewPathsTagPath,baseViewPath])
	name = values[0].value
	showChild = values[1].value
	order = values[2].value
	childTagPath = values[3].value
	viewPaths = values[4].value
	baseViewPath = values[5].value
	if viewPaths is not None:
		viewPaths = viewPaths.toDict()['ViewPathArray']
	childModelItem =  {'showChild':showChild,'childTagPath':childTagPath,'order':order,'baseViewPath':baseViewPath,'viewPaths':viewPaths,'name':name}

	return childModelItem

#=========================================================getChildModelItemAreaName=========================================================			
def getChildModelItemAreaName(ModelItemTagPath):
	#logger = system.util.getLogger("Navigation [Common]")
	#logger.info("getChildAreaName:" + modelTagPath)	
	childAreaName = system.tag.readBlocking([ModelItemTagPath + "/Name"])[0].value
	return childAreaName		
#=========================================================getModelItem=========================================================							
def getModelItem(Name,ModelItemTagPath,tagFolderName,path,order,viewPaths,baseViewPath):	
#	logger = system.util.getLogger("Navigation [TreeView]")
#	logger.info("GetTreeItem:" + label)		
	menuItem = {
				  "data": {
				  		"Name":Name,
				  		"ModelItemTagPath":ModelItemTagPath,
				  		"TagFolderName":tagFolderName,
				  		"Path":path,
				  		"Order":order,
				  		"ViewPaths":viewPaths,  
				  		"BaseViewPath":baseViewPath
				  				},
				  "modelItems": []
				}

	return menuItem
#=========================================================GetTagProvidersList=========================================================
def GetTagProvidersList(StartModelItemTagPath,ModelItems=None):
	modelItems = ModelItems
	tagProviders = {}
	
	def getTagProviderFromPath(Path):
		return Path.split(']')[0][1:]
		
	if modelItems is None:
		startModelItem = system.tag.readBlocking(tagPaths=[StartModelItemTagPath])[0].value
		modelItems = startModelItem['Children']
	
	tp = getTagProviderFromPath(Path=StartModelItemTagPath)
	tagProviders[tp] = {}

	
	def getTagProvider(ModelItem):
		#print ModelItemChild
		modelItemTagPath = ModelItem['data']['ModelItemTagPath']
		#print modelItemTagPath
		path = ModelItem['data']['ModelItemTagPath']
		tp = getTagProviderFromPath(path)
		#print ModelItemChild
		tagProviders[tp] = {}
		#tagProviders.append(tp)
		modelItemChildren = ModelItem['modelItems']
		for childModelItem in modelItemChildren:
			getTagProvider(ModelItem = childModelItem)
		return
		
	for modelItem in modelItems:
		getTagProvider(ModelItem = modelItem)
	return tagProviders.keys()

	
	
