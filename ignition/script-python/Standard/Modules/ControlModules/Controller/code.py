#==================================================== Control Module UDT Scripting ===========================================================================
#Scripting functions used in Standard/Valve UDT tags
#These scripts are used to account for a project that requires the SCADA standard to do some of the control logic.
#The logic is based on the original A2 Standard done for Impala

#================================================== GetMode ==============================================
#Gets required Mode value and uses that to determine what Mode the Analog Output should be
def GetMode(Mode,AOTagPath):

	#SCRIPTDisableManualMode
	#If DisablManualMode is set to true
	#Set Mode to Auto (i.e. auto mode, true)
	
	mode = Mode
	aoTagPath = AOTagPath
	
	if mode is not None:
		mode = 1
		#aoTagPath = system.tag.readBlocking("[.]../Metadata/AnalogOutputTagPath")[0].value

		#Change Analog Output InternalExternalSelect
		if mode==2:
				system.tag.writeBlocking([aoTagPath+"/Cfg/InternalExternalSelect"],[True])
		else:
				system.tag.writeBlocking([aoTagPath+"/Cfg/InternalExternalSelect"],[False])