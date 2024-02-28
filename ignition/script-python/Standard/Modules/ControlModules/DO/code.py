#==================================================== Control Module UDT Scripting ===========================================================================
#Scripting functions used in Standard/Valve UDT tags
#These scripts are used to account for a project that requires the SCADA standard to do some of the control logic.
#The logic is based on the original A2 Standard done for Impala

#================================================== GetRequestOn ==============================================
#Gets required Request On value and uses that to determine what outputs to write to Out.Output
#Only writes to outputs in Manual mode
def GetRequestOn(Mode,AutoOn,ManualOn,ManualOff,Interlocked,RequestOn,DOTagPath):
	#logger = system.util.getLogger("DO - GetRequestOn")
	#logger.info("DO - GetrequestOn Evaluating")
	mode = Mode
	doTagPath = DOTagPath
	updatedRequestOn = RequestOn
	#If in Auto Mode, simply return AutoOn value
	#SCRIPTAutomaticMode
	if mode == 2:
			updatedRequestOn = AutoOn
			#SCRIPTBumplessTransfer when in auto
			#'Whenever the device is placed into Automatic Mode, the CommandOperator is continually
			#' updated to reflect the CommandProgram. This is to ensure that the device does not
			#'change state should the device be placed in Manual Mode, 
			#'unless the operator requests it to.
			#manualOnTagPath = doTagPath + "/Cmd/ManualOn"
			#manualOffTagPath = doTagPath + "/Cmd/ManualOff"
			#manualOnUpdateValue = updatedRequestOn
			#manualOffUpdateValue = not updatedRequestOn
			#system.tag.writeBlocking([manualOnTagPath,manualOffTagPath], [manualOnUpdateValue,manualOffUpdateValue])
			
			return updatedRequestOn

	#SCRIPTManualMode	
	#Else if in Manual Mode, evaluate updatedRequestOpen and write to Outputs if required
	requestOn = RequestOn
	#logger.info("requestOn: " + str(requestOn) + str(type(requestOn)))
	manualOn = ManualOn
	#logger.info("manualOpen: " + str(manualOpen) + str(type(manualOpen)))
	manualOff = ManualOff
	#logger.info("manualClose: " + str(manualClose) + str(type(manualClose)))
	interlocked = Interlocked
	#logger.info("interlocked: " + str(interlocked) + str(type(interlocked)))
	
	#If the Mode is Manual Mode and CommandOperator is set from the 
	#face plate, then the internal RequestOpen is latched.	

	#If the Mode is reset (i.e. Manual Mode) and CommandOperator is reset from the
	#face plate, then the internal RequestOpen is unlatched.
	#If the CM has generated an AlarmFailure or an Interlock, then the 
	#RequestOpen is unlatched without delay.
	
	#Evaluate Request On
	if manualOn and (interlocked == False) and requestOn == False:		
		updatedRequestOn = True
	if manualOff or interlocked:
		updatedRequestOn = False
	
	if requestOn is None:
		updatedRequestOn = False
		
	#logger.info("updatedRequestOn: "+ str(updatedRequestOn))	
	#Evaluate Output if updatedRequestOn has changed since last evaluation
	if updatedRequestOn != requestOn:
		outputOn = None
		if updatedRequestOn and interlocked == False:
			outputOn = True
				
		if updatedRequestOn == False or interlocked:
			outputOn = False
				
		if outputOn is not None:
			outputOnTagPath = doTagPath + "/Out/Output"
			tagWrite = system.tag.writeBlocking([outputOnTagPath,], [outputOn,])	
			#logger.info("outputTagWrites: "+ str(tagWrite))		

	#If Manual On is true then reset Manual On
	if manualOn:	
		manualOnTagPath = doTagPath + "/Cmd/ManualOn"
		tagWrite = system.tag.writeBlocking([manualOnTagPath], [False])	
		
	#If Manual Off is true then reset Manual Off	
	if manualOff:
		manualOffTagPath = doTagPath + "/Cmd/ManualOff"
		tagWrite = system.tag.writeBlocking([manualOffTagPath], [False])	
	
	return updatedRequestOn