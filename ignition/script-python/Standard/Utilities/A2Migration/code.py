#Series of Scripts used to convert an Archestra Export into Ignition Standard UDTs
#Exports come from the A2 Migration tool which posts via the webdev module to a tag

#====================================== GetTagParametersFromA2Object ==============================	
#Function that finds values for all attributes and object information that map to a parameter on the 
#Ignition UDT
def GetTagParametersFromA2Object(Params,A2Object,UDTMappingObject):
	a2Object = A2Object
	uDTMappingObject = UDTMappingObject
	params = Params
	#Map A2 ObjectInfo to UDT Params	
	if "ObjectInfo" in uDTMappingObject:
		objectInfo = uDTMappingObject["ObjectInfo"]
		for objectInfoKey in objectInfo:
			objectInfoObject = objectInfo[objectInfoKey]
			objectInfoPath = objectInfoObject["Path"]
			if "Params" in objectInfoPath:
				parameterName = objectInfoPath.replace("Params.","")
				params[parameterName] = a2Object[objectInfoKey]	
				
	#Map A2 Attributes to UDT Params
	
	
	return params
#====================================== GetUDTInstanceTagDefinition ====================================
# Returns UDT tag object required for system.tag.configure
def GetUDTInstanceTagDefinition(tagName = "", typeID = "", params = {}, tags = []):
	tagObject = {
		            "name": tagName, 
		            "tagType" : "UdtInstance",              
		            "typeId" : typeID,	#UDT Tag path	            
		            "parameters" : params,
		            "tags":tags
		        }	
	if params is None:
		del tagObject['parameters']
	return tagObject
#====================================== GetFolderTagDefinition ====================================	
# Returns Folder object used in tag definitions for system.tag.configure
def GetFolderTagDefinition(folderName):
	# Tag Folder Object
	folderDefinition =  {
              "name": folderName,
              "tagType": "Folder",
              "tags": [	]
              }
	return folderDefinition

	
#====================================== GetAtomicTagDefinition ====================================	
#Returns default object required for an atomic tag
def GetAtomicTagDefinition(tagName = "",valueSource = ""):	
	tagObject = {
				  "name": tagName,
				  "tagType": "AtomicTag",
				  "valueSource":valueSource,
						}	
	return tagObject
#====================================== GetTagDefinition ====================================	
# Returns tag instance object used in tag definitions for system.tag.configure
# Will be main function that calls inner functions for different types of tags
# Types of tags include OPC, memory, expression etc.
def GetTagDefinition(tagName,valueSource,a2AttributeObject,attributeValueParameters):
	# tagObject used for Tags required on UDT level
	if valueSource is None:
		tagObject = None
	else:
		tagObject = GetAtomicTagDefinition(tagName,valueSource)
	#Base Tag Object Creation				
	if valueSource == "udtInstance":		
		#If a UDT then check which udt and create the definition accordingly
		udtTypeID = attributeValueParameters["TypeID"]
		typeID = udtTypeID
		tagObject = GetUDTInstanceTagDefinition(tagName = tagName, typeID = typeID, params = None, tags = [])
		#Interlock Definition
		if "Standard/Primitives/Interlock Primitive" in udtTypeID:
			interlockName = tagName
			tagObject = getInterlockPrimitiveDefinition(interlockName,typeID,a2AttributeObject)	
		elif "Standard/Alarms/Alarm Primitive" == udtTypeID:
			alarmName = tagName
			tagObject = getAlarmPrimitiveDefinition(alarmName,typeID,a2AttributeObject,attributeValueParameters)
		#Primitive Parameter Definition
		elif "Primitives/Parameter" in udtTypeID:
			tagObject["tagType"] = "UdtInstance"
			tagObject["typeId"] = typeID
			tagObject = getImplementationModulePrimitiveParameterDefinition(tagObject,a2AttributeObject,attributeValueParameters)	
			
	else:			
		valueSource, valueSourceParameters = getValueSourceParameters(valueSource,a2AttributeObject)
		if valueSource == "opc":
			tagObject = getOPCTagDefinition(tagObject,valueSourceParameters,attributeValueParameters)
			
		elif valueSource == "memory":
			#First check if that value is not a default value. If it is the default then do not create the tag
			createTag = True
			requiredDataTypeName = a2AttributeObject["DataTypeName"]
			valueSourceParameters["value"] = getA2ConvertedDataType(valueSourceParameters["value"],requiredDataTypeName)
			requiredValue = valueSourceParameters["value"]
			if "DefaultValue" in attributeValueParameters:
				defaultValue = attributeValueParameters["DefaultValue"]
				if requiredDataTypeName == "Bool":		
					if "reverse" in attributeValueParameters:
						requiredValue = not requiredValue
				elif requiredDataTypeName == "Integer":
					defaultValue = int(defaultValue)
				elif requiredDataTypeName == "Double":
					defaultValue = float(defaultValue)					
					
				if defaultValue == requiredValue:
					createTag = False
					
			if createTag:
				tagObject = getMemoryTagDefinition(tagObject,valueSourceParameters)
			else:
				tagObject = None

		
	return tagObject
#====================================== GetValueSource ========================================
#Function to get actual value source of an Attribute. Used to check if an OPC tag has a valid address or must just default
#to a value
def GetValueSource(ValueSource,A2AttributeObject):
	valueSource = ValueSource
	a2AttributeObject = A2AttributeObject
	if valueSource in ["memory","opc"]:
		#Not All Attributes have an Address associated with them
		if "Address" in A2AttributeObject:
			attributeValueFullyQualifiedAddress = a2AttributeObject["Address"]
			#================================== Memory Tag Check ==========================================
			#Done for tags that were configured as OPC in the A2 UDT but do not have a valid address
			#If Always true in an address then it should be a Memory Tag with default value of true
			if (attributeValueFullyQualifiedAddress is None)or ("Alwaysfalse" in attributeValueFullyQualifiedAddress) or ("Alwaystrue" in attributeValueFullyQualifiedAddress) or ("AlwaysTrue" in attributeValueFullyQualifiedAddress) or ("AlwaysFalse" in attributeValueFullyQualifiedAddress) or ("---" in attributeValueFullyQualifiedAddress):
				valueSource = "memory"	
				
	return valueSource	
#====================================== getA2ConvertedDataType ========================================
def getA2ConvertedDataType(value,datatype):
	requiredValue = value
	requiredDataTypeName = datatype
	if requiredDataTypeName == "Bool":
		if requiredValue == "false":
			requiredValue = False
		elif requiredValue == "true":
			requiredValue = True
	elif requiredDataTypeName == "Integer":
		requiredValue = int(requiredValue)
	elif requiredDataTypeName == "Double":
		requiredValue = float(requiredValue.replace(",","."))		
	return	requiredValue
			
#====================================== GetValueSourceParameters ===============================
#Function to extract required data (eg: addresses or attribute values) from an A2 Attribute object
#For a tagUDTInstance
def getValueSourceParameters(ValueSource,A2AttributeObject):
	valueSource = ValueSource
	a2AttributeObject = A2AttributeObject
	valueSourceParameters = {}

	valueSource = 	GetValueSource(valueSource,a2AttributeObject)
	
	if "Address" in A2AttributeObject:
		attributeValueFullyQualifiedAddress = a2AttributeObject["Address"]
		#================================== OPC Tags =================================================	
		if valueSource == "opc":
			attributeValueAddress = attributeValueFullyQualifiedAddress.split(".")[-1]
			valueSourceParameters["opcItemPath"] = "{OPCPath}%s"%(attributeValueAddress)
			#Check for Scaling
			if "Scaling" in A2AttributeObject:
				if A2AttributeObject["Scaling"] is not None:
					scalingObject = A2AttributeObject["Scaling"]
					valueSourceParameters["Scaling"] = scalingObject			
			
		#================================== Memory Tags ==============================================
		elif valueSource == "memory":
			valueSourceParameterValue = None
			if attributeValueFullyQualifiedAddress is None:
				valueSourceParameterValue = a2AttributeObject["Value"] 
			elif "alwaystrue" in attributeValueFullyQualifiedAddress.lower():
				 valueSourceParameterValue = True
			elif "alwaysfalse" in attributeValueFullyQualifiedAddress.lower():
				valueSourceParameterValue = False
			else:
				valueSourceParameterValue = a2AttributeObject["Value"] 
			
			valueSourceParameters["value"] = valueSourceParameterValue
	else:
		valueSourceParameters["value"] = a2AttributeObject["Value"] 
	
	return valueSource,valueSourceParameters

#====================================== getOPCTagDefinition ====================================	
# Inner function to get OPCTagDefinition for GetTagDefinition
def getOPCTagDefinition(tagObject,valueSourceParameters,attributeValueParameters):
	opcItemPath =  valueSourceParameters["opcItemPath"]
	# Add OPC ItemPath configuration
	tagObject["opcItemPath"] = {
							    "bindType": "parameter",
							    "binding": opcItemPath
							  }
#Is there by default and therefore do not want to override on Instance Level
#	# Add OPC Server configuration						  
#	tagObject["opcServer"] = {
#							    "bindType": "parameter",
#							    "binding": "{OPCServerName}"
#							  }
	# Add Scaling if available
	if "Scaling" in valueSourceParameters:
		scalingParameters = valueSourceParameters["Scaling"]
		scalingDefaults = None
		if "ScalingDefaultValues" in attributeValueParameters:
			scalingDefaults = attributeValueParameters["ScalingDefaultValues"]
			
		if 	scalingDefaults is not None:
			#Check if default value is different from required value
			#Do not want to override defaults if they are the same
			#If defaults, then also dont need to override scale mode
			defaultRawHigh = scalingDefaults["rawHigh"]
			defaultRawLow = scalingDefaults["rawLow"]
			defaultScaledLow = scalingDefaults["scaledLow"]
			defaultScaledHigh = scalingDefaults["scaledHigh"]
			defaultEngHigh= scalingDefaults["engHigh"]
			defaultEngLow = scalingDefaults["engLow"]
			if float(str(scalingParameters["RawMax"])) != float(defaultRawHigh):
				tagObject["rawHigh"] = scalingParameters["RawMax"]
			if float(str(scalingParameters["RawMin"])) != float(defaultRawLow):
				tagObject["rawLow"] = scalingParameters["RawMin"]
			if float(str(scalingParameters["EngMin"])) != float(defaultScaledLow):
				tagObject["scaledLow"] = scalingParameters["EngMin"]
			if float(str(scalingParameters["EngMax"])) != float(defaultScaledHigh):
				tagObject["scaledHigh"] = scalingParameters["EngMax"]
			
			if "EngRangeMax" in scalingParameters:
				if float(str(scalingParameters["EngRangeMax"])) != float(defaultEngHigh):
					tagObject["engHigh"] = scalingParameters["EngRangeMax"]
			if "EngRangeMin" in scalingParameters:
				if float(str(scalingParameters["EngRangeMin"])) != float(defaultEngLow):
					tagObject["engLow"] = scalingParameters["EngRangeMin"] 
					
		else:
			tagObject["scaleMode"] = "Linear"
			tagObject["rawHigh"] = scalingParameters["RawMax"]
			tagObject["rawLow"] = scalingParameters["RawMin"]
			tagObject["scaledLow"] = scalingParameters["EngMin"]
			tagObject["scaledHigh"] = scalingParameters["EngMax"]
			if "EngRangeMax" in scalingParameters:
				tagObject["engHigh "] = scalingParameters["EngRangeMax"]
			if "EngRangeMin" in scalingParameters:
				tagObject["engLow "] = scalingParameters["EngRangeMin"] 
		

	return tagObject
#====================================== getMemoryTagDefinition ====================================	
# Inner function to get OPCTagDefinition for GetTagDefinition		
def getMemoryTagDefinition(tagObject,valueSourceParameters):	
	if "value" in valueSourceParameters:
		memoryValue = valueSourceParameters["value"]	
		tagObject["value"] = memoryValue
				
	return tagObject
#====================================== getAlarmPrimitiveDefinition ====================================	
# Inner function to get Alarm Primitive for GetTagDefinition		
def getAlarmPrimitiveDefinition(AlarmName,TypeID,A2AttributeObject,AttributeValueParameters):
	
	def getAlarmPrimitiveInfo(A2AlarmAttributeInfo):
		a2AlarmAttributeName = A2AlarmAttributeInfo["Name"]
		alarmPrimitiveFolderName = "Cfg"
		alarmPrimitiveTagName = None
		alarmPrimitiveTagPath = None
		if "Enable" in a2AlarmAttributeName:
			alarmPrimitiveTagName = "Enable"
		elif "Limit" in a2AlarmAttributeName or "Tolerance" in a2AlarmAttributeName or "Threshold" in a2AlarmAttributeName or a2AlarmAttributeName == "AlarmPositionAction":
			alarmPrimitiveTagName = "ConditionSetpoint"
		elif "Delay" in a2AlarmAttributeName:
			alarmPrimitiveTagName = "Delay"
		
		alarmName = a2AlarmAttributeName.replace("Enable","").replace("Alarm","")
		getAlarmPrimitiveInfo = {"InstanceName":alarmName,"AlarmPrimitiveFolderName":alarmPrimitiveFolderName,"AlarmPrimitiveTagName":alarmPrimitiveTagName}
		return getAlarmPrimitiveInfo
		
	alarmTagName = AlarmName
	typeID = TypeID
	a2AttributeObject = A2AttributeObject	
	attributeValueParameters = AttributeValueParameters
	
	alarmPrimitiveInfo = getAlarmPrimitiveInfo(a2AttributeObject)
	alarmPrimitiveInstanceName = alarmPrimitiveInfo["InstanceName"]
	alarmPrimitiveFolderName = alarmPrimitiveInfo["AlarmPrimitiveFolderName"]
	alarmPrimitiveTagName = alarmPrimitiveInfo["AlarmPrimitiveTagName"]
	alarmPrimitiveAtomicTagValue = type(getA2ConvertedDataType(A2AttributeObject["Value"],["DataTypeName"]))
	
	alarmPrimitiveTags = []
	#Add Config Folder to tags
	alarmPrimitiveTagFolder = GetFolderTagDefinition(alarmPrimitiveFolderName)
	alarmPrimitiveTags.append(alarmPrimitiveTagFolder)
	#Add required memory tags to config folder in tags
	valueSource = "memory"
	valueSourceParameters = {"value":alarmPrimitiveAtomicTagValue}
	#memoryTagDefintion = GetAtomicTagDefinition(tagName = alarmPrimitiveTagName,valueSource = valueSource)
	#memoryTagDefintion = getMemoryTagDefinition(memoryTagDefintion,valueSourceParameters)
	memoryTagDefintion = GetTagDefinition(alarmPrimitiveTagName,"memory",a2AttributeObject,attributeValueParameters)
	if memoryTagDefintion is not None:
		alarmPrimitiveTags[0]["tags"].append(memoryTagDefintion)

	tagObject = GetUDTInstanceTagDefinition(tagName = AlarmName, typeID = typeID, params = None, tags = alarmPrimitiveTags)
	return tagObject

#====================================== getInterlockPrimitiveDefinition ============================
# Inner function to get Interlock Primitive for GetTagDefinition	
def getInterlockPrimitiveDefinition(InterlockName,TypeID,A2AttributeObject):
	interlockName = InterlockName
	typeID = TypeID
	attributeObject = A2AttributeObject
	interlockTags = []
	#Get Address or Value of Interlock State Tag based on Attribute Object Info
	address = attributeObject["Address"]
	if ("AlwaysTrue" in address) or "--" in address:
		interlockValue = True
		stateTagObject = {
					      "valueSource": "memory",
					      "name": "State",
					      "value": interlockValue,
					      "tagType": "AtomicTag"
					    }	
	elif ("AlwaysFalse" in address):
		interlockValue = False
		stateTagObject = {
					      "valueSource": "memory",
					      "name": "State",
					      "value": interlockValue,
					      "tagType": "AtomicTag"
					    }		
	else:
		attributeValueAddress = address.split(".")[-1]
		stateTagObject = {
					      "valueSource": "opc",
					      "name": "State",
					      "tagType": "AtomicTag"
					    }	
		stateTagObject["opcItemPath"] = {
									    "bindType": "parameter",
									    "binding": "{OPCPath}%s"%(attributeValueAddress)
									  }
#Is there by default and therefore do not want to override on Instance Level
#		stateTagObject["opcServer"] = {
#									    "bindType": "parameter",
#									    "binding": "{OPCServerName}"
#									  }
	#Create Interlock Tag Object
	interlockTags.append(stateTagObject)
	tagObject = GetUDTInstanceTagDefinition(tagName = interlockName, typeID = typeID, params = {}, tags = interlockTags)
				
	return tagObject


#====================================== getImplementationModulePrimitiveParameterDefinition ============================
def getImplementationModulePrimitiveParameterDefinition(TagObject,A2AttributeObject,AttributeValueParameters):
	tagObject = TagObject 	
	attributeObject = A2AttributeObject
	attributeValueParameters = AttributeValueParameters
	#Create Parameter/Value Tag Object based on A2AttributeObject
	valueSource, valueSourceParameters = getValueSourceParameters("opc",attributeObject)
	valueTagObject = GetAtomicTagDefinition(tagName = "Value",valueSource = valueSource)
	if valueSource == "opc":
		valueTagObject = getOPCTagDefinition(valueTagObject,valueSourceParameters,attributeValueParameters)
		
	elif valueSource == "memory":
		valueTagObject = getMemoryTagDefinition(valueTagObject,valueSourceParameters)	
		
	tagObject["tags"].append(valueTagObject)			
	return tagObject

	