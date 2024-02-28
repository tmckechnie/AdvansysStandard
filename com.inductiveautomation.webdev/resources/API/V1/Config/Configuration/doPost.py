def doPost(request, session):
	logConfiguration = system.util.getLogger("API/V1/Config/Configuration-Post")
	data = request["data"]
	logConfiguration.info("Request Data Datatype:" + str(type(data)))
	#data = system.util.jsonDecode(strData)
	for key in data:
		logConfiguration.info("Request Data Key:" + str(key))

	tagProvider = data["TagProvider"]
	tagPath = data["TagPath"]
	a2Object = data["A2Object"]

	
	def getChildren(children):
		for child in children:
			tagname = child["Tagname"]
			description = child["Description"]
			derivedTemplate = child["DerivedTemplate"]
			baseDerivedTemplate = child["BaseDerivedTemplate"]
			objectBaseType = child["ObjectBaseType"]
			typeid = baseDerivedTemplate
			if objectBaseType == "$Area":
				typeid = "Folder"
			area = child["Area"]
			container = child["Container"]
			containedName = child["ContainedName"]
			logConfiguration.info(str([tagname,description,derivedTemplate,area,container,containedName,typeid]))
			getChildren(child["Children"])

	#logConfiguration.info("Data Datatype:" + str(type(data)))
	baseAreaName = a2Object["Tagname"]
	logConfiguration.info(str([tagProvider,tagPath,baseAreaName]))
	children = a2Object["Children"]
	getChildren(children)
	#Add ExportDate Property to A2Object
	a2Object["ExportDate"] = system.date.format(system.date.now(),"yyyy-MM-dd HH:mm:ss")
	basePath = "["+tagProvider+"]" + tagPath
	modelTag = {
	  "valueSource": "memory",
	  "dataType": "Document",
	  "name": "A2Model",
	  "value": a2Object,
	  "tagType": "AtomicTag"
	}
	system.tag.configure(basePath, [modelTag])

		
	
	return {'json': 'OK'}