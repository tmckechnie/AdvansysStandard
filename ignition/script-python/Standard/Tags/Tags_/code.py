#
#def OwnerID(tagPath,previousValue,currentValue):	
#	#If Owner Changes - add Self ID to new Owner and remove from Old Owner
#	logger = system.util.getLogger("Group Owner Changed Script")
#	if currentValue.quality.isGood() == False:
#		#logger.info("currentValue is bad Quality: " + str(currentValue))
#		return
#	else:
#		pass
#		
#	#Check if Current Owner Exists - If so add selfID to currentOwner, else create owner in Group Document
#	currentOwner = currentValue.value #"Group 1"
#	if currentOwner is None or currentOwner == "" or currentOwner == " ":
#		return
#	else:
#		currentOwner = currentOwner.strip("\x22")
#		
#	#logger.info("currentOwner " + str(currentOwner))
#	#Check if currentOwner value is a valid one
#	selfID = system.tag.readBlocking(["[.]Self"])[0].value #"Control Module 1" 
#	selfID = selfID.strip("\x22")
#
#	tagPathFinalElement = tagPath.rfind("/")
#	tagPathToSelected = tagPath[0:tagPathFinalElement] + "/Selected"	
#	#Current Group Doc for this Area
#	groupDocument = system.tag.readBlocking(["[.]../../../Group Document"])[0].value	
#	groupDocument = system.util.jsonDecode(str(groupDocument))
#	if groupDocument is None:
#		groupDocument = {}
#		
#	#logger.info("Current Group Document json Decoded" + str(groupDocument) + str(type(groupDocument)))
#	#Check if Previous Owner Exists - If so remove selfID from previous owner
#	previousOwner = previousValue.value
#	if previousOwner is not None:
#		previousOwner = previousOwner.strip("\x22")
#		
#	if currentOwner == previousOwner and groupDocument.has_key(currentOwner):
#		#logger.info("currentOwner == previousOwner and groupDocument.has_key(currentOwner)")
#		if groupDocument[currentOwner].has_key(selfID):
#			return
#		else:
#			pass	
#	#logger.info("previousOwner : " + str(previousOwner))
#	previousOwnerExists = groupDocument.has_key(str(previousOwner))		
#	#logger.info("previousOwnerExists: " + str(previousOwnerExists))
#	popped = False
#	if previousOwnerExists and groupDocument[previousOwner].has_key(selfID):
#		try:
#			groupDocument[previousOwner].pop(selfID)
#			popped = True
#			logger.info("Previous Owner does Exist")
#		except:
#			pass
#	currentOwnerExists = groupDocument.has_key(str(currentOwner))
#	#logger.info("Current Owner is Valid")
#	
#	#Trying not to write back an entire doc tag if avoidable
#	if previousOwnerExists and popped:
#		#Remove selfID from previous Owner Group Object
#		previousGroupObject = system.util.jsonEncode(groupDocument[previousOwner])
#		previousGroupRelativeTagPath = "[.]../../../Group Document['%s']"%(previousOwner)
#		previousOwnerTagWrite = system.tag.writeBlocking([previousGroupRelativeTagPath],[previousGroupObject])
#		#logger.info("previousOwnerTagWrite: " + str(previousOwnerTagWrite))
#		
#	
#	#Write new key back or add new value to current key
#	if currentOwnerExists:
#		currentOwnerExistsDocTagPath = "[.]../../../Group Document['%s.%s']"%(currentOwner,selfID)
#		currentOwnerExistsTagWrite = system.tag.writeBlocking([currentOwnerExistsDocTagPath],[tagPathToSelected])
#		#logger.info("currentOwnerExistsTagWrite: " + str(currentOwnerExistsTagWrite))
#		
#	else:
#		#logger.info("CurrentOwner: " + str(currentOwner))
#		newOwnerObjectDocTagPath = "[.]../../../Group Document['%s']"%(currentOwner)
#		newOwnerObject = system.util.jsonEncode({selfID:tagPathToSelected})
#		#logger.info("newOwnerObject: " + str(newOwnerObject))
#		newOwnerObjectTagWrite = system.tag.writeBlocking([newOwnerObjectDocTagPath],[newOwnerObject])
#		#logger.info("newOwnerObjectTagWrite: " + str(newOwnerObjectTagWrite))	
#		
#		
#	return
#
#def SelfID(tagPath,previousValue,currentValue):
#	#Check if Self ID has Changed
#	#If So check if OwnerID != None or blank
#	logger = system.util.getLogger("Self ID Changed Script")
#	currentSelfID = currentValue.value
#	previousSelfID = previousValue.value
#	#logger.info("CurrentSelfID: " + str(currentSelfID) + "PreviousSelfID: " + str(previousSelfID))
#	#Check if Valid CurrentSelfID
#	if currentSelfID == previousSelfID or currentSelfID == " " or currentSelfID is None or currentSelfID == "":
#		return
#	#Check if Valid PreviousSelfID
#	elif previousSelfID == " " or previousSelfID is None or previousSelfID == "":
#		return	
#	#If So check if Group Document OwnerID key exists
#	previousSelfID = previousSelfID.strip("\x22")
#	currentSelfID = currentSelfID.strip("\x22")
#	currentOwnerID = system.tag.readBlocking(["[.]Owner"])[0].value #"Control Module 1" 
#	currentOwnerID = currentOwnerID.strip("\x22")
#	#logger.info("currentOwnerID: "  + str(currentOwnerID)) 
#	if currentOwnerID is None or currentOwnerID == "" or currentOwnerID == " ":
#		return
#	#Current Group Doc for this Area
#	groupDocument = system.tag.readBlocking(["[.]../../../Group Document"])[0].value	
#	groupDocument = system.util.jsonDecode(str(groupDocument))
#	if groupDocument is None or groupDocument == {}:
#		return
#		
#	#If So update SelfID key within OwnerID if previous SelfID exists
#	if groupDocument.has_key(currentOwnerID):
#		if groupDocument[currentOwnerID].has_key(previousSelfID):
#			#logger.info("currentGroupDocument Owner Object: " + str(groupDocument[currentOwnerID]))
#			try:
#				groupDocument[currentOwnerID].pop(previousSelfID)
#				#logger.info("poppedGroupDocument Owner Object: " + str(groupDocument[currentOwnerID]))
#				#Selected Tag Path	
#				tagPathFinalElement = tagPath.rfind("/")
#				tagPathToSelected = tagPath[0:tagPathFinalElement] + "/Selected"
#				groupDocument[currentOwnerID][currentSelfID] = tagPathToSelected
#				#logger.info("newGroupDocument Owner Object: " + str(groupDocument[currentOwnerID]))
#			except:			
#				pass		
#				
#			newGroupObject = system.util.jsonEncode(groupDocument[currentOwnerID])			
#			newGroupRelativeTagPath = "[.]../../../Group Document['%s']"%(currentOwnerID)
#			newGroupTagWrite = system.tag.writeBlocking([newGroupRelativeTagPath],[newGroupObject])		
#			#logger.info("newGroupTagWrite: " + str(newGroupTagWrite))
#	return 
#
#def ThrownException(message,reason):
#	system.perspective.openPopup("ThrownException","Common Components/Error Handling/ThrownException",{"Message":message,"Reason":reason})
#	return