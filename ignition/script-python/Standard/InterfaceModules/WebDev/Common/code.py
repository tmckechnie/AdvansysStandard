#---------------------------------------------------------GetPacket--------------------------------------------------
#Standard.InterfaceModules.WebDev.Common.GetData(TagPath='[AdvansysStandard]Standard/Interface Modules/WebDev/RX001')
def GetData(TagPath):
	tagPath = TagPath + '/Data'
	data = system.tag.readBlocking([tagPath])
	data = data[0].value
	data = system.util.jsonDecode(str(data))
	return data

#---------------------------------------------------------PostData--------------------------------------------------
#Standard.InterfaceModules.WebDev.Common.PostData(TagPath='[AdvansysStandard]Standard/Interface Modules/WebDev/RX001',Data)
def PostData(TagPath,Data):
	tagPath = TagPath + '/Data'
	data = Data
	data = system.util.jsonEncode(data)
	system.tag.writeBlocking([tagPath], [data])
	return data