def getTypes(strProvider):
	
	strPath = strProvider + "_types_"
	results = TagManagement.getType(strPath)
	return results

def getType(strPath):
	"""
	Recursively browses list of tag types without structure
	Arguments:
		strPath: Full path to tag
	Returns:
		List of types
    """
	results = system.tag.browse(strPath, filter={"recursive":False})
	listTypes = []
	for item in results:
		#print item
		if str(item['tagType']) == "Folder":
			#print "found folder: " + str(item['fullPath'])
			items = getType(item['fullPath'])
		if str(item['tagType']) == "UdtType":
			#print "found tag: " + str(item['fullPath'])
			items = [item]
		listTypes = listTypes + items
	return listTypes

def SyncType(strSrcPath,strDestProvider):
	"""
	Writes UDT at strSrcPath assuming it is in the [Standard] provider to strDestProvider
	Arguments:
		strSrcPath: Path to tag
		strDestProvider: Name of destination provider
	Returns:
		List of types
    """
	if system.tag.exists(strSrcPath) and system.tag.exists(strDestProvider):
		#Get tag object from source provider
		tag = system.tag.getConfiguration(strSrcPath, recursive=True)
		#Remove instance name from path	
		strDestPath = strDestProvider + "_types_/" + '/'.join(strSrcPath.split('/')[1:-1])
		#Write to destination
		result = system.tag.configure(strDestPath,tags=tag)
	else:
		result = -1
	return result
	
