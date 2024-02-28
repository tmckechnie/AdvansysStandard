#=========================================================getUserDetailTagPath=========================================================	
def GetTreeItems(ModelItems = []):
	treeItems = []
	modelItems = ModelItems
	#getTreeItem-----------------------------------------------------------------------------------------------------
	def getTreeItem(label,modelItemTagPath,tagFolderName,expanded = False,path=None,modelItemData=None):	
		#logger = system.util.getLogger("Navigation [TreeView]")
		#logger.info("GetTreeItem:" + label)		
		menuItem = {
					  "label": label,
					  "expanded": expanded,
					  "dataV0": {"ModelItemTagPath":modelItemTagPath,"TagFolderName":tagFolderName},
					  "data": modelItemData,
					  "items": []
					}
	
		return menuItem
	
	#Iterate through all the model items in a session to build the default Tree Menu Items for the ModelItems
	for modelItem in modelItems:
		label = modelItem["data"]["Name"]
		path = modelItem["data"]["Path"]
		expanded = False
		dataModelItemTagPath = modelItem["data"]["ModelItemTagPath"]
		dataTagFolderName = modelItem["data"]["TagFolderName"]
		modelItemData = modelItem["data"]
		
		treeMenuItem = getTreeItem(label=label,modelItemTagPath = dataModelItemTagPath,tagFolderName= dataTagFolderName,expanded=expanded,modelItemData=modelItemData)
		childModelItems = modelItem["modelItems"]
		childTreeItems = GetTreeItems(childModelItems)
		treeMenuItem["items"] = childTreeItems	
		treeItems.append(treeMenuItem)
											
	return	treeItems

	

	
