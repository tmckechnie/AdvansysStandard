#==================================================== Control Module UDT Scripting ===========================================================================
#Scripting functions used in Standard/Valve UDT tags
#These scripts are used to account for a project that requires the SCADA standard to do some of the control logic.
#The logic is based on the original A2 Standard done for Impala

#================================================== GetRequestOpen ==============================================
#Gets required Request Open value and uses that to determine what outputs to write to Out.Open and Out.Close
#Only writes to outputs in Manual mode
def GetRequestOpen(Mode,AutoOpen,ManualOpen,ManualClose,AlarmFailure,Interlocked,RequestOpen,ValveTagPath):
	#logger = system.util.getLogger("GetRequestOpen")
	#logger.info("GetRequestOpen Evaluating")
	mode = Mode
	updatedRequestOpen = RequestOpen	
	#logger.info("mode: " + str(mode) + str(type(mode)))
	#If in Auto Mode, simply return AutoOpen value
	#SCRIPTAutomaticMode
	if mode == 2:
		updatedRequestOpen = AutoOpen
		valveTagPath = ValveTagPath	
		#SCRIPTBumplessTransfer when in auto
		#'Whenever the device is placed into Automatic Mode, the CommandOperator is continually
		#' updated to reflect the CommandProgram. This is to ensure that the device does not
		#'change state should the device be placed in Manual Mode, 
		#'unless the operator requests it to.
		manualOpenTagPath = valveTagPath + "/Cmd/ManualOpen"
		manualCloseTagPath = valveTagPath + "/Cmd/ManualClose"
		manualOpenUpdateValue = updatedRequestOpen
		manualCloseUpdateValue = not updatedRequestOpen
		system.tag.writeBlocking([manualOpenTagPath,manualCloseTagPath], [manualOpenUpdateValue,manualCloseUpdateValue])			
		
		return updatedRequestOpen
		
	#SCRIPTManualMode	
	#Else if in Manual Mode, evaluate updatedRequestOpen and write to Outputs if required
	requestOpen = RequestOpen
	#logger.info("requestOpen: " + str(requestOpen) + str(type(requestOpen)))
	manualOpen = ManualOpen
	#logger.info("manualOpen: " + str(manualOpen) + str(type(manualOpen)))
	manualClose = ManualClose
	#logger.info("manualClose: " + str(manualClose) + str(type(manualClose)))
	alarmFailure = AlarmFailure
	#logger.info("alarmFailure: " + str(alarmFailure) + str(type(alarmFailure)))
	interlocked = Interlocked
	#logger.info("interlocked: " + str(interlocked) + str(type(interlocked)))
	valveTagPath = ValveTagPath	
	#logger.info("valveTagPath: " + str(valveTagPath) + str(type(valveTagPath)))
	#If the Mode is Manual Mode and CommandOperator is set from the 
	#face plate, then the internal RequestOpen is latched.	
	
	#If the Mode is reset (i.e. Manual Mode) and CommandOperator is reset from the
	#face plate, then the internal RequestOpen is unlatched.
	#If the CM has generated an AlarmFailure or an Interlock, then the 
	#RequestOpen is unlatched without delay.	
		
	#Evaluate Request Open
	if manualOpen and (interlocked == False) and requestOpen == False:
		updatedRequestOpen = True
	if manualClose or alarmFailure or interlocked:
		updatedRequestOpen = False
	
	if requestOpen is None:
		updatedRequestOpen = False
		
	#logger.info("updatedRequestOpen: "+ str(updatedRequestOpen))	
	#Evaluate Output Open and Output Close if updatedRequestOpen has changed since last evaluation
	if updatedRequestOpen != requestOpen:
		outputOpen = None
		if updatedRequestOpen and interlocked == False:
			outputOpen = True
			outputClose = False
			
		if updatedRequestOpen == False or interlocked:
			outputOpen = False
			outputClose = True
			
		if outputOpen is not None:
			outputOpenTagPath = valveTagPath + "/Out/Open"
			outputCloseTagPath = valveTagPath + "/Out/Close"
			tagWrite = system.tag.writeBlocking([outputOpenTagPath,outputCloseTagPath], [outputOpen,outputClose])	
			#logger.info("outputTagWrites: "+ str(tagWrite))	
		
		
	#If Manual Open is true then reset Manual Open	
	if manualOpen:	
		manualOpenTagPath = valveTagPath + "/Cmd/ManualOpen"
		tagWrite = system.tag.writeBlocking([manualOpenTagPath], [False])	
		
	#If Manual Close is true then reset Manual Close	
	if manualClose:
		manualCloseTagPath = valveTagPath + "/Cmd/ManualClose"
		tagWrite = system.tag.writeBlocking([manualCloseTagPath], [False])	
	
	return updatedRequestOpen


