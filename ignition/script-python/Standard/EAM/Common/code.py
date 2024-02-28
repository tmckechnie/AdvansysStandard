#-----------------------------------------------RunTask-----------------------------
def RunTask(Task):
	def printResponse(responseList):
	    if len(responseList) > 0:
	        for response in responseList:
	            print "", response
	    else:
	        print " None"
	        
	print "Task:" + Task
	response = system.eam.runTask(Task)

	# Print out the returned Info (if any).
	infos = response.getInfos()
	print "Infos are:"
	printResponse(infos)
	
	# Print out the returned Warnings (if any).
	warnings = response.getWarns()
	print "Warnings are:"
	printResponse(warnings)
	 
	# Print out the returned Errors (if any).
	errors = response.getErrors()
	print "Errors are:"
	printResponse(errors)
	 
	
	return response
	
#task = 'Send Standard Tags To TPSite'
#response = Standard.EAM.Common.RunTask(Task=task)
#task = 'Send Standard Tags To TPPlant1'
#response = Standard.EAM.Common.RunTask(Task=task)
#task = 'Send Standard Tags To TPPlant2'
#response = Standard.EAM.Common.RunTask(Task=task)
#task = 'Send Project Resources from Plant 1 To Site'
#response = Standard.EAM.Common.RunTask(Task=task)
#task = 'Send Project Resources from Plant 2 To Site'
#response = Standard.EAM.Common.RunTask(Task=task)