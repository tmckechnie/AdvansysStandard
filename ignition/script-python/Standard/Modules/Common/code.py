
#=======================================================getModuleTagname=====================================================
def getModuleTagname(ModuleTagname,ModuleIdentifiers='DB,#'):
	moduleTagname = ModuleTagname.replace('"',"").split('.')[0]
	for moduleIdentifier in ModuleIdentifiers.split(','):
		lenght = len(moduleIdentifier)
		if moduleTagname[0:lenght] == moduleIdentifier:
			moduleTagname = moduleTagname[lenght:]
			break
	return moduleTagname
#=======================================================GetModuleTagPath=====================================================
#This returns the Module Instance TagPath by providing and tagname in the Module
def GetModuleTagPath(TagProvider,ModuleTagname,ModuleIdentifiers='DB,#'):
		
	moduleTagname = getModuleTagname(ModuleTagname=ModuleTagname,ModuleIdentifiers=ModuleIdentifiers)
	provider = TagProvider
	limit = 1
	
	query = {"options": {"includeUdtMembers": True, "includeUdtDefinitions": False},
	  "condition": {"path": "*"+moduleTagname,"tagType": "UdtInstance","attributes": { "values": [],"requireAll": True}},
	  "returnProperties": ["tagType","quality"]
	}
	

	results = system.tag.query(provider, query, limit)
	for result in results:
		fullPath = str(result['fullPath'])
		return fullPath
	return None
	
	
#=======================================================OpenFaceplate=====================================================
def OpenFaceplate(ParamsObject,Title,FaceplatePath,Position={"right":5,"width":455,"height":600,"bottom":45}):
	paramsObject = ParamsObject
	titleString = Title
	id = titleString.replace(" ","")
	viewString = FaceplatePath
	
	positionObject = Position
	
	showCloseIconBool = True
	draggableBool = True
	resizableBool = True
	modalBool = False
	overlayDismissBool = False	
	viewportBoundBool = True
	
	system.perspective.openPopup(id = id,
	view = viewString,
	params = paramsObject,
	title = titleString,
	position = positionObject,
	showCloseIcon = showCloseIconBool,
	draggable = draggableBool,
	resizable = resizableBool,
	modal=modalBool,
	overlayDismiss=overlayDismissBool,
	viewportBound = viewportBoundBool)
		
	return 

def ThrownException(message,reason):
	system.perspective.openPopup("ThrownException","Standard/Components/Error Handling/ThrownException",{"Message":message,"Reason":reason})
	return
#------------------------------------------------------getModuleInfoFromInterlockReason---------------------------------------------
def getModuleInfoFromInterlockReason(Reason,BrowsePath,ModuleIdentifiers = 'DB,#',Version=0):
	module = {'instanceExists':False}
	if Reason is None or len(Reason)==0:
		return module

	moduleTagname = getModuleTagname(ModuleTagname=Reason,ModuleIdentifiers=ModuleIdentifiers)
	if Version==2:
		loggerName="GetModuleInfoFromInterlockReasonV2"
		Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message=moduleTagname)
#	cleanReason = Reason.replace('"','')
#	cleanObjectIdentifier = ObjectIdentifier.replace('"','')
#	#print cleanReason + " " + cleanObjectIdentifier
#	if cleanReason[0:len(cleanObjectIdentifier)] == cleanObjectIdentifier:
#		#replaceString = ObjectIdentifier.replace(ObjectNameDelimiter,"")
#		#tagName = Reason.split(ObjectNameDelimiter)[1].replace(replaceString,"")
#		replaceString = ObjectIdentifier.strip(ObjectNameDelimiter)
#		tagName = cleanReason.strip(cleanObjectIdentifier).split('.')[0]
#		#print tagName
#		#Browse
	browseTagPath = BrowsePath.split('/')[0]
	print browseTagPath
	filter = {"name":"*"+moduleTagname+"*","recursive":True}
	tags = system.tag.browse(path=browseTagPath, filter=filter)
	#return tags
	if len(tags)>0:
		tag = tags[0]
		print tag
		fullPath = str(tag["fullPath"])
		print fullPath
		tagValue = system.tag.readBlocking([fullPath])[0].value
		print tagValue
		description = tagValue['Metadata']['Description']
		instanceName = tagValue['Metadata']['InstanceName']
		standardViewPath = tagValue['Metadata']['StandardViewPath']
		fullPath = str(tag["fullPath"])
		module ={'instanceExists':True}
		module['typeId'] = tag["typeId"]
		module['fullPath'] = fullPath
		module['description'] = description
		module['instanceName'] = instanceName
		module['standardViewPath'] = standardViewPath

		return module

	return module
#------------------------------------------------------GetModuleInfoFromInterlockReason---------------------------------------------
def GetModuleInfoFromInterlockReason(Reason,BrowsePath,ModuleIdentifiers = 'DB,#'):
	#loggerName="GetModuleInfoFromInterlockReason"
	#Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message=str([Reason,BrowsePath]))
	#module = getModuleInfoFromInterlockReason(Reason=Reason,BrowsePath=BrowsePath,ObjectNameDelimiter=ObjectNameDelimiter,ModuleIdentifiers = ModuleIdentifiers)
	module = getModuleInfoFromInterlockReason(Reason=Reason,BrowsePath=BrowsePath,ModuleIdentifiers = ModuleIdentifiers,Version=0)		
	module = system.util.jsonEncode(module)
	#Standard.Utilities.Common.LogMessage(LoggerName=loggerName, Message=str(module))
	return module
	



	
