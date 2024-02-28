stylePopupMenuItemChildren = "Standard/Popups/Navigation/MenuItem/Children"
stylePopupMenuItemContentType = "Standard/Popups/Navigation/MenuItem/ContentType"
styleBreadCrumbMenuItem = "Standard/Docked/Navigation/Background"

import Standard.Navigation.Common as Common

#===================================================== GetBreadCrumbMenuItems================================================================			
#This Gets all the BreadCrumbs Instances up to current navigation
def GetBreadCrumbMenuItems(ModelItems,CurrentPath,LimitItemCount=0,InstanceStyleClass = "",GetOnlyConfiguredContentTypes=False,AllowedContentTypes=[]):
	#getBreadCrumbMenuItem ---------------------------------------------------------------------------------------------------------------------------
	def getBreadCrumbMenuItem(ModelItem,BreadcrumbPosition=1,TotalCrumbs=1,InstanceStyleClass = "Standard/Docked/Navigation/Background", GetOnlyConfiguredContentTypes=False,AllowedContentTypes=[]):
		
		viewPaths = ModelItem['data']['ViewPaths']
		contentTypes = Common.GetContentTypes(ViewPaths=viewPaths,GetOnlyConfiguredContentTypes=GetOnlyConfiguredContentTypes,AllowedContentTypes=AllowedContentTypes)
		menuItem = {
				  "instanceStyle": {
					"classes": InstanceStyleClass
				  },
				  "instancePosition": {
					"grow": 1
				  },
				  #"ModelItemTagPath": ModelItem['data']['ModelItemTagPath'],
				  "ModelItem": ModelItem['data'],
				  "Label": ModelItem['data']['Name'],
				  "ChildrenCount": len(ModelItem['modelItems']),
				  "ContentTypes":contentTypes
				}
		return menuItem	
	#getColourPaletteHex ---------------------------------------------------------------------------------------------------------------------------
	from math import floor						
	def getColourPaletteClasses(position):
		if position == 0:
			position = 1
		colours = ["Standard/Popups/Navigation/BreadCrumb/Palette01",
		"Standard/Popups/Navigation/BreadCrumb/Palette02",
		"Standard/Popups/Navigation/BreadCrumb/Palette03",
		"Standard/Popups/Navigation/BreadCrumb/Palette04",
		"Standard/Popups/Navigation/BreadCrumb/Palette05"]
		
		colourLength = len(colours)
		index = position - int(floor(position/colourLength)*colourLength) -1
		return colours[index]
	
	if InstanceStyleClass == "":
		InstanceStyleClass = styleBreadCrumbMenuItem
		
	modelItemsList = Common.GetModelItemsUpTo(ModelItems=ModelItems,Path=CurrentPath)
	instances = []
	for modelItem in modelItemsList:
		modelItemTagPath = modelItem['data']['ModelItemTagPath']
		label = modelItem['data']['Name']
		instance = getBreadCrumbMenuItem(ModelItem=modelItem,GetOnlyConfiguredContentTypes=GetOnlyConfiguredContentTypes,AllowedContentTypes=AllowedContentTypes)
		instances.append(instance)
		
	breadCrumbPosition = 1
	totalCrumbs = len(instances) 
	
	for instance in instances:
		#instance["TotalCrumbs"] = totalCrumbs
		instance["BreadcrumbPosition"] = breadCrumbPosition
		#Get breadCrump Styles
		baseCrumbStyleClasses = getColourPaletteClasses(breadCrumbPosition-1)
		currentCrumbStyleClasses = getColourPaletteClasses(breadCrumbPosition)
		nextCrumbStyleClasses = ""
		if breadCrumbPosition < totalCrumbs:
			nextCrumbStyleClasses = getColourPaletteClasses(breadCrumbPosition)
		
		
		instance['StyleClasses'] = {
		  "Base": baseCrumbStyleClasses,
		  "Current": currentCrumbStyleClasses,
		  "Next": nextCrumbStyleClasses
			}
		breadCrumbPosition +=1
	
	#Limit Item Count
	if LimitItemCount>0:
			instances = instances[-1*LimitItemCount:]
	return instances

#===================================================== GetBreadCrumbMenuItems================================================================			
#This Gets all the Popup MenuItem Instances for current navigation
def GetPopupModelItemMenuItems(ModelItems,BreadcrumbPosition,Path,InstanceStyleClass = ""):
	if InstanceStyleClass == "":
		InstanceStyleClass = stylePopupMenuItemChildren
		
	modelItems = Common.GetModelItemChildren(ModelItems=ModelItems,Path=Path)
	instances = []
	for modelItem in modelItems:
		modelItemTagPath = modelItem['data']['ModelItemTagPath']
		label = modelItem['data']['Name']
		path = modelItem['data']['Path']
		instance = Common.GetPopupMenuItem(ModelItemTagPath=modelItemTagPath,Path=path,ContentType = "",Label = label,InstanceStyleClass = InstanceStyleClass)
		instance["BreadcrumbPosition"] = BreadcrumbPosition
		instances.append(instance)
	
	return instances

#===================================================== GetPopupContentTypeMenuItems ================================================================			
def GetPopupContentTypeMenuItems(ModelItemTagPath,Path,BreadcrumbPosition,ContentTypes):
	contentTypes = ContentTypes
	instances = []
	for contentType in contentTypes:
		contentTypeValue = contentType['contentType']
		label = contentType['label']
		instance = Common.GetPopupMenuItem(ModelItemTagPath=ModelItemTagPath,Path=Path,ContentType=contentTypeValue,Label = label,InstanceStyleClass = stylePopupMenuItemContentType)	
		instance["BreadcrumbPosition"] = BreadcrumbPosition
		instances.append(instance)	
	return instances	


	

		
		
		
		
		
		
		
		
		
