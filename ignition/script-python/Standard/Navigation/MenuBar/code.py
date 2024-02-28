import Standard.Navigation.Common as Common

stylePopupMenuItemChildren = "Standard/Popups/Navigation/MenuItem/Children"
stylePopupMenuItemContentType = "Standard/Popups/Navigation/MenuItem/ContentType"
#===================================================== GetMenuBarMenuItem ================================================================	
def GetMenuBarMenuItems(ModelItems,InstanceStyleClass = "Standard/Popups/Navigation/MenuItem/Item", GetOnlyConfiguredContentTypes=False, AllowedContentTypes = []):
	modelItems = ModelItems	
	getOnlyConfiguredContentTypes = GetOnlyConfiguredContentTypes
	allowedContentTypes = AllowedContentTypes

	instances = []
	index = 0
	totalItems = len(modelItems)
	for modelItem in modelItems:
		modeltItemData = modelItem["data"]
		modelItemTagPath = modeltItemData["ModelItemTagPath"]
		#Keep Current Popup Position in each menu item view
		menuItemPosition = {
							  "top": 60,
							  "left": 0,
							  "height": None,
							  "width": 180
							}
		if index > 0:
			menuItemPosition["left"] = menuItemPosition["width"] * index #- 20			

		instanceObject = getMenuBarMenuItem(modelItem,menuItemPosition,InstanceStyleClass = InstanceStyleClass, GetOnlyConfiguredContentTypes=getOnlyConfiguredContentTypes, AllowedContentTypes = allowedContentTypes)
		instances.append(instanceObject)
		index += 1
	return instances

#===================================================== getMenuBarMenuItem ================================================================	
def getMenuBarMenuItem(ModelItem,MenuItemPosition,InstanceStyleClass = "Standard/Popups/Navigation/Background", GetOnlyConfiguredContentTypes=False, AllowedContentTypes = []):
	
	viewPaths = ModelItem['data']['ViewPaths']
	contentTypes = Common.GetContentTypes(ViewPaths=viewPaths,GetOnlyConfiguredContentTypes=GetOnlyConfiguredContentTypes,AllowedContentTypes=AllowedContentTypes)	
	menuItem = {
			  "instanceStyle": {
				"classes": InstanceStyleClass
			  },
			  "instancePosition": {
				"grow": 1
			  },
			  "ModelItem":ModelItem['data'],
			  "MenuItemPosition":MenuItemPosition,
			  "Label": ModelItem['data']['Name'],
			  "ChildrenCount": len(ModelItem['modelItems']),
			  "ContentTypes":contentTypes,
			  "AllowedContentTypes":AllowedContentTypes,
			  "ShowOnlyConfiguredContentTypes":GetOnlyConfiguredContentTypes,
			  "OpenPopups":[]
			}
	return menuItem	

#===================================================== GetChildMenuBarItems ================================================================	
def GetPopupMenuBarItems(ModelItems,MenuItemPosition,Path,ContentTypes,AllowedContentTypes = [],ShowOnlyConfiguredContentTypes = False,OpenPopups = []):
	getOnlyConfiguredContentTypes = ShowOnlyConfiguredContentTypes
	allowedContentTypes = AllowedContentTypes
	menuItemPosition = MenuItemPosition
	openPopups = OpenPopups
	#The Menu Item instance postition must also take content types above it into account
	#Therefore starting menu position is equal to quantity of contentTypes + 1		
	menuInstanceItemPosition = len(ContentTypes) + 1		
	childModelItems = Common.GetModelItemChildren(ModelItems=ModelItems,Path=Path)
	instances = []
	
	for modelItem in childModelItems:
		viewPaths = modelItem['data']['ViewPaths']
		modelItemTagPath = modelItem['data']['ModelItemTagPath']
		path = modelItem['data']['Path']
		label = modelItem['data']['Name']
		childModelItemCount = modelItem['childrenCount']
		
		childModelContentTypes = Common.GetContentTypes(ViewPaths=viewPaths,GetOnlyConfiguredContentTypes=getOnlyConfiguredContentTypes,AllowedContentTypes=allowedContentTypes)	

		instance = Common.GetPopupMenuItem(ModelItemTagPath=modelItemTagPath,Path = path,ContentType = "",Label = label,InstanceStyleClass = stylePopupMenuItemChildren)	
		instance["ModelItem"] = modelItem["data"]
		instance["ShowOnlyConfiguredContentTypes"] = getOnlyConfiguredContentTypes
		instance["AllowedContentTypes"] = allowedContentTypes
		instance["ContentTypes"] = childModelContentTypes
		instance["MenuItemPosition"] = menuItemPosition
		instance["OpenPopups"] = openPopups		
		instance["MenuInstanceItemPosition"] = menuInstanceItemPosition	
		instance["ChildrenCount"] = childModelItemCount
		instances.append(instance)	
		menuInstanceItemPosition += 1	
		
	return instances			
			
#===================================================== GetPopupContentTypeMenuItems ================================================================			
def GetPopupContentTypeMenuItems(ModelItem,ContentTypes,OpenPopups = []):
	contentTypes = ContentTypes
	openPopups = OpenPopups
	modelItem = ModelItem
	instances = []
	for contentType in contentTypes:
		modelItemTagPath = modelItem["ModelItemTagPath"]
		path = modelItem["Path"]
		contentTypeValue = contentType['contentType']
		label = contentType['label']	
		instance = Common.GetPopupMenuItem(ModelItemTagPath=modelItemTagPath,Path = path,ContentType=contentTypeValue,Label = label,InstanceStyleClass = stylePopupMenuItemContentType)	
		instance["OpenPopups"] = openPopups
		instance["ModelItem"] = modelItem
		instances.append(instance)	
	return instances		
	
	
#===================================================== getMenuBarPopupMenuItem ================================================================								
def getMenuBarPopupMenuItem(ModelItem,MenuItemPosition, InstanceStyleClass = "Standard/Popups/Navigation/Background",ContentTypes = [], GetOnlyConfiguredContentTypes=False, AllowedContentTypes = [],OpenPopups = []):

	contentTypes = ContentTypes

	menuItem = {
			  "instanceStyle": {
				"classes": InstanceStyleClass
			  },
			  "instancePosition": {
				"grow": 1
			  },
			  "ModelItem":ModelItem['data'],
			  "MenuItemPosition":MenuItemPosition,
			  "Label": ModelItem['data']['Name'],
			  "ChildrenCount": len(ModelItem['modelItems']),
			  "ContentTypes":contentTypes,
			  "OpenPopups":[]
			}
	return menuItem		