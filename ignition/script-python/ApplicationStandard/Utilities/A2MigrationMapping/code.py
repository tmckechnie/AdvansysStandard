#Set of scripts to bring back all the mapping objects required to Migrate the A2 Impala Object into Standard Ignition UDTs
#============================================================================================
#=================================== Mapping Objects ========================================
#============================================================================================


#==================================== GetControlModuleAttributeMappingObject ==========================
def GetControlModuleAttributeMappingObject():
	
	return 	controlModuleAttributes			
#==================================== GetImplementationModuleA2IgnObject ==============================
def GetImplementationModuleA2IgnObject():
	return implementationModuleA2Ign
#==================================== GetImplementationModuleAttributeMappingObject ===================
def GetImplementationModuleAttributeMappingObject():
	return implementationModuleAttributes



#Impala A2 Unit Implementation Module Mapping
implementationModuleA2Ign = {
				
				#===================== Opnim ==========================
				#Opnim_Barr_GLV
				"b_Opnim_Barr_GLV.HMI_GLV_Status":{"IgnTypeIDKey":"Opnim_Barr_GLV","TagName":"Unit"},
				"b_Opnim_Barr_GLV.HMI_Parameters":{"IgnTypeIDKey":"Opnim_Barr_GLV","TagName":"Unit"},
				#Opnim_GLV
				"b_Opnim_GLV.HMI_GLV_Status":{"IgnTypeIDKey":"Opnim_GLV","TagName":"Unit"},
				"b_Opnim_GLV.HMI_Parameters":{"IgnTypeIDKey":"Opnim_GLV","TagName":"Unit"},
				#Opnim_Ir_Glovebox_8103_8703
				"b_Opnim_Ir_Glovebox_8103_8703.Addition_Control":{"IgnTypeIDKey":"Opnim_Ir_Glovebox_8103_8703","TagName":"Unit"},					
				#Opnim_Ir_Glovebox_8303_8503
				"b_Opnim_Ir_Glovebox_8303_8503.Valve_Control":	{"IgnTypeIDKey":"Opnim_Ir_Glovebox_8303_8503","TagName":"Unit"},	
				#Opnim_IR_GLV
				"b_Opnim_IR_GLV.HMI_GLV_Status": {"IgnTypeIDKey":"Opnim_IR_GLV","TagName":"Unit"},
				"b_Opnim_IR_GLV.HMI_Parameters": {"IgnTypeIDKey":"Opnim_IR_GLV","TagName":"Unit"},
				#Opnim_Ir_GLV_2
				"b_Opnim_Ir_GLV_2.Hand_Switch": {"IgnTypeIDKey":"Opnim_Ir_GLV_2","TagName":"Unit"},
				#Opnim_IX_GLV
				"b_Opnim_IX_GLV.HMI_GLV_Status":{"IgnTypeIDKey":"Opnim_IX_GLV","TagName":"Unit"},
				"b_Opnim_IX_GLV.HMI_Parameters":{"IgnTypeIDKey":"Opnim_IX_GLV","TagName":"Unit"},
				#Opnim_PPT_GLV
				"b_Opnim_PPT_GLV.Bromate_Addition":{"IgnTypeIDKey":"Opnim_PPT_GLV","TagName":"Unit"},
				"b_Opnim_PPT_GLV.DetaVolControl":{"IgnTypeIDKey":"Opnim_PPT_GLV","TagName":"Unit"},
				#Opnim_IX_Column
				"Opnim_IX_Column.Rh_Ix_Column_Flow_Param":{"IgnTypeIDKey":"Opnim_IX_Column","TagName":"Unit"},
				"Opnim_IX_Column.Rh_Ix_Column_Status":{"IgnTypeIDKey":"Opnim_IX_Column","TagName":"Unit"},
				"Opnim_IX_Column.Rh_Ix_Column_Volume_Param":{"IgnTypeIDKey":"Opnim_IX_Column","TagName":"Unit"},
				"Opnim_IX_Column.Rh_Ix_Manual_Steps":{"IgnTypeIDKey":"Opnim_IX_Column","TagName":"Unit"},
				"Opnim_IX_Column.Rh_Ix_Parameters":{"IgnTypeIDKey":"Opnim_IX_Column","TagName":"Unit"},			
				#Rh_7210_30_A_B
				"Rh_7210_30_A_B.Rh_Bromate_Addition":{"IgnTypeIDKey":"Rh_7210_30_A_B","TagName":"Unit"},	
				#Rh_6003C
				"Rh_6003C_Status":	{"IgnTypeIDKey":"Rh_6003C","TagName":"Unit"},
				"Rh_6003C_Control":	{"IgnTypeIDKey":"Rh_6003C","TagName":"Unit"},
				#Rh_6670
				"Rh_6670_Controls":	{"IgnTypeIDKey":"Rh_6670","TagName":"Unit"},
				#Rh_6000
				"Rh_6000_Controls":	{"IgnTypeIDKey":"Rh_6000","TagName":"Unit"},		
				"Rh_GLV6000_HMI_Control":	{"IgnTypeIDKey":"Rh_6000","TagName":"Unit"},		
				#Rh_7100A
				"Rh_7100A_EmergencyStop":	{"IgnTypeIDKey":"Rh_7100A","TagName":"Unit"},
				#Rh_IX_Columns
				"Rh_IX_Global_Param":{"IgnTypeIDKey":"Rh_IX_Columns","TagName":"Unit"},		
				#Rh_GLV_7310
				"Rh_7310_HMI_Parameters":{"IgnTypeIDKey":"Rh_GLV_7310","TagName":"Unit"},
				#Rh_Reset_Brom
				"Rh_Reset_Brom":{"IgnTypeIDKey":"Rh_Reset_Brom","TagName":"Unit"},
				#Rh_7060
				"Rh_7060StripMakeup_Param":{"IgnTypeIDKey":"Rh_7060","TagName":"Unit"},
				"Rh_7060StripMakeup_Status":{"IgnTypeIDKey":"Rh_7060","TagName":"Unit"},
				#Rh_7090_HCL
				"Rh_7090_HCL_Addition":{"IgnTypeIDKey":"Rh_7090_HCL","TagName":"Unit"},
				#Rh_7090
				"Rh_7090_Param":{"IgnTypeIDKey":"Rh_7090","TagName":"Unit"},
				"Rh_7090_Status":{"IgnTypeIDKey":"Rh_7090","TagName":"Unit"},
				#Rh_DeminMakeUp_7080
				"Rh_DeminMakeUp_Param":{"IgnTypeIDKey":"Rh_DeminMakeUp_7080","TagName":"Unit"},
				#Rh_6030
				"Rh_Deta_Makeup_Param":{"IgnTypeIDKey":"Rh_6030","TagName":"Unit"},
				#Rh_7043_5_Organic_Make_up
				#"Rh_DetaDestruct_Vol_7043_5":{"IgnTypeIDKey":"Rh_7043_5_Organic_Make_up","TagName":"Unit"},
				"Rh_Makeup_Param_7043_5":{"IgnTypeIDKey":"Rh_7043_5_Organic_Make_up","TagName":"Unit"},
				"Rh_MakeUP_Vol_7043_5":{"IgnTypeIDKey":"Rh_7043_5_Organic_Make_up","TagName":"Unit"},
				#Rh_7981
				"Rh_7981_Status":{"IgnTypeIDKey":"Rh_7981","TagName":"Unit"},
				#Rh_7096_Chlorine_Supply
				"Rh_Cl2_EmergencyStop_Status":{"IgnTypeIDKey":"Rh_7096_Chlorine_Supply","TagName":"Unit"},				
				#Rh_HCL_Supply_Header
				"Rh_HCL_Supply_Param":{"IgnTypeIDKey":"Rh_HCL_Supply_Header","TagName":"Unit"},
				#Rh_NitricAddition_7030_8030
				"Rh_NitricAddition_7030_8030":{"IgnTypeIDKey":"Rh_NitricAddition_7030_8030","TagName":"Unit"}
							}

#Impala Unit Implementation Module TypeID Mapping
implementationModuleTypeID = {


				#===================== Opnim Unit ==========================
				"Opnim_Barr_GLV":"Instances/Units/Opnim/Units/Opnim_Barr_GLV",
				"Opnim_GLV":"Instances/Units/Opnim/Units/Opnim_GLV",
				"Opnim_Ir_Glovebox_8103_8703":"Instances/Units/Opnim/Units/Opnim_Ir_Glovebox_8103_8703",
				"Opnim_Ir_Glovebox_8303_8503":"Instances/Units/Opnim/Units/Opnim_Ir_Glovebox_8303_8503",
				"Opnim_IR_GLV":"Instances/Units/Opnim/Units/Opnim_IR_GLV",
				"Opnim_Ir_GLV_2":"Instances/Units/Opnim/Units/Opnim_Ir_GLV_2",
				"Opnim_IX_GLV":"Instances/Units/Opnim/Units/Opnim_IX_GLV",			
				"Opnim_PPT_GLV":"Instances/Units/Opnim/Units/Opnim_PPT_GLV",
				"Opnim_IX_Column":"Instances/Units/Opnim/Units/Opnim_IX_Column",	
				"Rh_7210_30_A_B":"Instances/Units/Opnim/Units/Rh_7210_30_A_B",
				"Rh_6003C":"Instances/Units/Opnim/Units/Rh_6003C",
				"Rh_6670":"Instances/Units/Opnim/Units/Rh_6670",
				"Rh_6000":"Instances/Units/Opnim/Units/Rh_6000",
				"Rh_7100A":"Instances/Units/Opnim/Units/Rh_7100A",
				"Rh_IX_Columns":"Instances/Units/Opnim/Units/Rh_IX_Columns",
				"Rh_GLV_7310":"Instances/Units/Opnim/Units/Rh_GLV_7310",
				"Rh_Reset_Brom":"Instances/Units/Opnim/Units/Rh_Reset_Brom",
				"Rh_7060":"Instances/Units/Opnim/Units/Rh_7060",
				"Rh_7090_HCL":"Instances/Units/Opnim/Units/Rh_7090_HCL",
				"Rh_7090":"Instances/Units/Opnim/Units/Rh_7090",
				"Rh_DeminMakeUp_7080":"Instances/Units/Opnim/Units/Rh_DeminMakeUp_7080",				
				"Rh_6030":"Instances/Units/Opnim/Units/Rh_6030",
				"Rh_7043_5_Organic_Make_up":"Instances/Units/Opnim/Units/Rh_7043_5_Organic_Make_up",
				"Rh_7981":"Instances/Units/Opnim/Units/Rh_7981",
				"Rh_7096_Chlorine_Supply":"Instances/Units/Opnim/Units/Rh_7096_Chlorine_Supply",
				"Rh_HCL_Supply_Header":"Instances/Units/Opnim/Units/Rh_HCL_Supply_Header",
				"Rh_NitricAddition_7030_8030":"Instances/Units/Opnim/Units/Rh_NitricAddition_7030_8030"
							}
		
#Impala Unit Implementation Attribute Mapping
opnimUnitParametersObject = {"ValueSource":"udtInstance","TypeID":"CTI505/Implementation Modules/Primitives/Parameter"}

implementationModuleAttributes = {


				#===================== Opnim Unit ==========================
				"Opnim_Barr_GLV":{
							#Parameters
							"Acc_Boildown":{"Path":"Sts/Acc_Boildown","Parameters":opnimUnitParametersObject},
							"Accept_Boildown":{"Path":"Cmd/Accept_Boildown","Parameters":opnimUnitParametersObject},
							"Accept_Heatup_Reflux":{"Path":"Cmd/Accept_Heatup_Reflux","Parameters":opnimUnitParametersObject},					
							"Add_Boildown_Time":{"Path":"Cfg/Add_Boildown_Time","Parameters":opnimUnitParametersObject},												
							"Calced_Boildown_Time":{"Path":"Sts/Calced_Boildown_Time","Parameters":opnimUnitParametersObject},																			
							"Continue":{"Path":"Cmd/Continue","Parameters":opnimUnitParametersObject},																			
							"Final_Volume":{"Path":"Cfg/Final_Volume","Parameters":opnimUnitParametersObject},																										
							"Final_Volume_Entered":{"Path":"Cmd/Final_Volume_Entered","Parameters":opnimUnitParametersObject},																																	
							"Heatup_Current":{"Path":"Sts/Heatup_Current","Parameters":opnimUnitParametersObject},
							"Heatup_Duration":{"Path":"Cfg/Heatup_Duration","Parameters":opnimUnitParametersObject},
							"Initial_Volume":{"Path":"Sts/Initial_Volume","Parameters":opnimUnitParametersObject},							
							"Max_Boildown_Duration":{"Path":"Cfg/Max_Boildown_Duration","Parameters":opnimUnitParametersObject},
							"Max_Boildown_Remaining":{"Path":"Sts/Max_Boildown_Remaining","Parameters":opnimUnitParametersObject},							
							"Reflux_Current":{"Path":"Sts/Reflux_Current","Parameters":opnimUnitParametersObject},
							"Reflux_Duration":{"Path":"Cfg/Reflux_Duration","Parameters":opnimUnitParametersObject},
							"Remaining_Add_Time":{"Path":"Sts/Remaining_Add_Time","Parameters":opnimUnitParametersObject},							
							"Remaining_Time_Final_Volume":{"Path":"Sts/Remaining_Time_Final_Volume","Parameters":opnimUnitParametersObject},							
							"Select_Additional_Boildown":{"Path":"Cmd/Select_Additional_Boildown","Parameters":opnimUnitParametersObject},							
							"Select_Boildown":{"Path":"Cmd/Select_Boildown","Parameters":opnimUnitParametersObject},							
							"Select_Complete":{"Path":"Cmd/Select_Complete","Parameters":opnimUnitParametersObject},							
																																			
							#Status
							"AddBoilCool":{"Path":"Sts/AddBoilCool","Parameters":opnimUnitParametersObject},
							"BoildownComplete":{"Path":"Sts/BoildownComplete","Parameters":opnimUnitParametersObject},
							"BoildownInProgress":{"Path":"Sts/BoildownInProgress","Parameters":opnimUnitParametersObject},																		
							"FinalVolume":{"Path":"Sts/FinalVolume","Parameters":opnimUnitParametersObject},																																				
							"HeatUp":{"Path":"Sts/HeatUp","Parameters":opnimUnitParametersObject},																																																						
							"RefluxComplete":{"Path":"Sts/RefluxComplete","Parameters":opnimUnitParametersObject},																																																					
							"RefluxInProgress":{"Path":"Sts/RefluxInProgress","Parameters":opnimUnitParametersObject},
							"WaypointReached":{"Path":"Sts/WaypointReached","Parameters":opnimUnitParametersObject}																		
								},
				"Opnim_GLV":{
							#Parameters
							"Acc_Boildown":{"Path":"Sts/Acc_Boildown","Parameters":opnimUnitParametersObject},
							"Accept_Boildown":{"Path":"Cmd/Accept_Boildown","Parameters":opnimUnitParametersObject},
							"Accept_Heatup_Reflux":{"Path":"Cmd/Accept_Heatup_Reflux","Parameters":opnimUnitParametersObject},					
							"Add_Boildown_Time":{"Path":"Cfg/Add_Boildown_Time","Parameters":opnimUnitParametersObject},												
							"Calced_Boildown_Time":{"Path":"Sts/Calced_Boildown_Time","Parameters":opnimUnitParametersObject},																			
							"Continue":{"Path":"Cmd/Continue","Parameters":opnimUnitParametersObject},																			
							"Final_Volume":{"Path":"Cfg/Final_Volume","Parameters":opnimUnitParametersObject},																										
							"Final_Volume_Entered":{"Path":"Cmd/Final_Volume_Entered","Parameters":opnimUnitParametersObject},																																	
							"Heatup_Current":{"Path":"Sts/Heatup_Current","Parameters":opnimUnitParametersObject},
							"Heatup_Duration":{"Path":"Cfg/Heatup_Duration","Parameters":opnimUnitParametersObject},
							"Initial_Volume":{"Path":"Sts/Initial_Volume","Parameters":opnimUnitParametersObject},							
							"Max_Boildown_Duration":{"Path":"Cfg/Max_Boildown_Duration","Parameters":opnimUnitParametersObject},
							"Max_Boildown_Remaining":{"Path":"Sts/Max_Boildown_Remaining","Parameters":opnimUnitParametersObject},							
							"Reflux_Current":{"Path":"Sts/Reflux_Current","Parameters":opnimUnitParametersObject},
							"Reflux_Duration":{"Path":"Cfg/Reflux_Duration","Parameters":opnimUnitParametersObject},
							"Remaining_Add_Time":{"Path":"Sts/Remaining_Add_Time","Parameters":opnimUnitParametersObject},							
							"Remaining_Time_Final_Volume":{"Path":"Sts/Remaining_Time_Final_Volume","Parameters":opnimUnitParametersObject},							
							"Select_Additional_Boildown":{"Path":"Cmd/Select_Additional_Boildown","Parameters":opnimUnitParametersObject},							
							"Select_Boildown":{"Path":"Cmd/Select_Boildown","Parameters":opnimUnitParametersObject},							
							"Select_Complete":{"Path":"Cmd/Select_Complete","Parameters":opnimUnitParametersObject},							
																																			
							#Status
							"AddBoilCool":{"Path":"Sts/AddBoilCool","Parameters":opnimUnitParametersObject},
							"BoildownComplete":{"Path":"Sts/BoildownComplete","Parameters":opnimUnitParametersObject},
							"BoildownInProgress":{"Path":"Sts/BoildownInProgress","Parameters":opnimUnitParametersObject},																		
							"FinalVolume":{"Path":"Sts/FinalVolume","Parameters":opnimUnitParametersObject},																																				
							"HeatUp":{"Path":"Sts/HeatUp","Parameters":opnimUnitParametersObject},																																																						
							"RefluxComplete":{"Path":"Sts/RefluxComplete","Parameters":opnimUnitParametersObject},																																																					
							"RefluxInProgress":{"Path":"Sts/RefluxInProgress","Parameters":opnimUnitParametersObject},
							"WaypointReached":{"Path":"Sts/WaypointReached","Parameters":opnimUnitParametersObject}																		
								},
				"Opnim_Ir_Glovebox_8103_8703":{
							#Addition Control
							"Addition_Vol":{"Path":"Cmd/Addition_Vol","Parameters":opnimUnitParametersObject},
							"Start_Addition":{"Path":"Cmd/Start_Addition","Parameters":opnimUnitParametersObject},				
							"Stop_Addition":{"Path":"Cmd/Stop_Addition","Parameters":opnimUnitParametersObject}				
								},
				"Opnim_Ir_Glovebox_8303_8503":{
							#Valve Control
							"Close":{"Path":"Cmd/Close","Parameters":opnimUnitParametersObject},
							"Open":{"Path":"Cmd/Open","Parameters":opnimUnitParametersObject}
								},
				"Opnim_IR_GLV":{
							#Parameters
							"Acc_Boildown":{"Path":"Sts/Acc_Boildown","Parameters":opnimUnitParametersObject},
							"Accept":{"Path":"Cmd/Accept","Parameters":opnimUnitParametersObject},
							"Boildown":{"Path":"Cmd/Boildown","Parameters":opnimUnitParametersObject},
							"Heatup_Current":{"Path":"Sts/Heatup_Current","Parameters":opnimUnitParametersObject},
							"Heatup_Duration":{"Path":"Cfg/Heatup_Duration","Parameters":opnimUnitParametersObject},
							"Max_Boildown_Duration":{"Path":"Cfg/Max_Boildown_Duration","Parameters":opnimUnitParametersObject},
							"Reflux_Current":{"Path":"Sts/Reflux_Current","Parameters":opnimUnitParametersObject},
							"Reflux_Duration":{"Path":"Cfg/Reflux_Duration","Parameters":opnimUnitParametersObject},
							#Status
							"BoildownComplete":{"Path":"Sts/BoildownComplete","Parameters":opnimUnitParametersObject},
							"BoildownInProgress":{"Path":"Sts/BoildownInProgress","Parameters":opnimUnitParametersObject},
							"HeatUp":{"Path":"Sts/HeatUp","Parameters":opnimUnitParametersObject},
							"RefluxComplete":{"Path":"Sts/RefluxComplete","Parameters":opnimUnitParametersObject},
							"RefluxInProgress":{"Path":"Sts/RefluxInProgress","Parameters":opnimUnitParametersObject}							
							},
				"Opnim_Ir_GLV_2":{
							#Hand Switch
							"SteamHandSwitch":{"Path":"Cmd/SteamHandSwitch","Parameters":opnimUnitParametersObject}		
							},
				"Opnim_IX_GLV":{
							#Parameters
							"Acc_Boildown":{"Path":"Sts/Acc_Boildown","Parameters":opnimUnitParametersObject},
							"Accept":{"Path":"Cmd/Accept","Parameters":opnimUnitParametersObject},
							"Boildown":{"Path":"Cmd/Boildown","Parameters":opnimUnitParametersObject},
							"Heatup_Current":{"Path":"Sts/Heatup_Current","Parameters":opnimUnitParametersObject},
							"Heatup_Duration":{"Path":"Cfg/Heatup_Duration","Parameters":opnimUnitParametersObject},
							"Max_Boildown_Duration":{"Path":"Cfg/Max_Boildown_Duration","Parameters":opnimUnitParametersObject},
							"Reflux_Current":{"Path":"Sts/Reflux_Current","Parameters":opnimUnitParametersObject},
							"Reflux_Duration":{"Path":"Cfg/Reflux_Duration","Parameters":opnimUnitParametersObject},
							#Status
							"BoildownComplete":{"Path":"Sts/BoildownComplete","Parameters":opnimUnitParametersObject},
							"BoildownInProgress":{"Path":"Sts/BoildownInProgress","Parameters":opnimUnitParametersObject},
							"HeatUp":{"Path":"Sts/HeatUp","Parameters":opnimUnitParametersObject},
							"RefluxComplete":{"Path":"Sts/RefluxComplete","Parameters":opnimUnitParametersObject},
							"RefluxInProgress":{"Path":"Sts/RefluxInProgress","Parameters":opnimUnitParametersObject}							
							},		
				"Opnim_PPT_GLV":{
							#Bromate Addition
							"Add_20_Litres":{"Path":"Cmd/Add_20_Litres","Parameters":opnimUnitParametersObject},				
							"Add_50_Litres":{"Path":"Cmd/Add_50_Litres","Parameters":opnimUnitParametersObject},								
							"Stop_Addition":{"Path":"Cmd/Stop_Addition","Parameters":opnimUnitParametersObject},												
							"CalculatedRhodium":{"Path":"Cmd/CalculatedRhodium","Parameters":opnimUnitParametersObject},																
							"Concentration":{"Path":"Cmd/Concentration","Parameters":opnimUnitParametersObject},																				
							"DetaVolume":{"Path":"Cmd/DetaVolume","Parameters":opnimUnitParametersObject},																				
							"DetaVolumeMakeUp":{"Path":"Cmd/DetaVolumeMakeUp","Parameters":opnimUnitParametersObject},																								
							"FeedVolume":{"Path":"Cmd/FeedVolume","Parameters":opnimUnitParametersObject},																																				
							"StartAddition":{"Path":"Cmd/StartAddition","Parameters":opnimUnitParametersObject}																																		
							},
				"Opnim_IX_Column":{
							#Manual Steps
							"Rh_TO_1STCOND":{"Path":"Cmd/Rh_TO_1STCOND","Parameters":opnimUnitParametersObject},
							"Rh_TO_1STH2O":{"Path":"Cmd/Rh_TO_1STH2O","Parameters":opnimUnitParametersObject},
							"Rh_TO_1STSO2":{"Path":"Cmd/Rh_TO_1STSO2","Parameters":opnimUnitParametersObject},
							"Rh_TO_1STSTRIP":{"Path":"Cmd/Rh_TO_1STSTRIP","Parameters":opnimUnitParametersObject},
							"Rh_TO_2NDCOND":{"Path":"Cmd/Rh_TO_2NDCOND","Parameters":opnimUnitParametersObject},
							"Rh_TO_2NDDISP":{"Path":"Cmd/Rh_TO_2NDDISP","Parameters":opnimUnitParametersObject},
							"Rh_TO_2NDH2O":{"Path":"Cmd/Rh_TO_2NDH2O","Parameters":opnimUnitParametersObject},
							"Rh_TO_2NDSO2":{"Path":"Cmd/Rh_TO_2NDSO2","Parameters":opnimUnitParametersObject},
							"Rh_TO_2NDSTRIP":{"Path":"Cmd/Rh_TO_2NDSTRIP","Parameters":opnimUnitParametersObject},
							"Rh_TO_3RDDISP":{"Path":"Cmd/Rh_TO_3RDDISP","Parameters":opnimUnitParametersObject},
							"Rh_TO_BACKWASH":{"Path":"Cmd/Rh_TO_BACKWASH","Parameters":opnimUnitParametersObject},
							#Flow Param
							"Rh_BACKWASH_SP":{"Path":"Cfg/Rh_BACKWASH_SP","Parameters":opnimUnitParametersObject},
							"Rh_COND_1ST_SP":{"Path":"Cfg/Rh_COND_1ST_SP","Parameters":opnimUnitParametersObject},
							"Rh_COND_2ND_SP":{"Path":"Cfg/Rh_COND_2ND_SP","Parameters":opnimUnitParametersObject},
							"Rh_DISPL_1ST_SP":{"Path":"Cfg/Rh_DISPL_1ST_SP","Parameters":opnimUnitParametersObject},
							"Rh_DISPL_2ND_SP":{"Path":"Cfg/Rh_DISPL_2ND_SP","Parameters":opnimUnitParametersObject},
							"Rh_DISPL_3RD_SP":{"Path":"Cfg/Rh_DISPL_3RD_SP","Parameters":opnimUnitParametersObject},
							"Rh_FEED_SP":{"Path":"Cfg/Rh_FEED_SP","Parameters":opnimUnitParametersObject},
							"Rh_H2O_1ST_SP":{"Path":"Cfg/Rh_H2O_1ST_SP","Parameters":opnimUnitParametersObject},
							"Rh_H2O_2ND_SP":{"Path":"Cfg/Rh_H2O_2ND_SP","Parameters":opnimUnitParametersObject},
							"Rh_SO2_1ST_SP":{"Path":"Cfg/Rh_SO2_1ST_SP","Parameters":opnimUnitParametersObject},
							"Rh_SO2_2ND_SP":{"Path":"Cfg/Rh_SO2_2ND_SP","Parameters":opnimUnitParametersObject},
							"Rh_STRIP_1ST_SP":{"Path":"Cfg/Rh_STRIP_1ST_SP","Parameters":opnimUnitParametersObject},
							"Rh_STRIP_2ND_SP":{"Path":"Cfg/Rh_STRIP_2ND_SP","Parameters":opnimUnitParametersObject},
							#Column Status
							"Feed_Cycle":{"Path":"Sts/Feed_Cycle","Parameters":opnimUnitParametersObject},
							"Rh_BACKWASH":{"Path":"Sts/Rh_BACKWASH","Parameters":opnimUnitParametersObject},
							"Rh_COND_1ST":{"Path":"Sts/Rh_COND_1ST","Parameters":opnimUnitParametersObject},
							"Rh_COND_2ND":{"Path":"Sts/Rh_COND_2ND","Parameters":opnimUnitParametersObject},
							"Rh_DFSHL_7100Column":{"Path":"Sts/Rh_DFSHL_7100Column","Parameters":opnimUnitParametersObject},
							"Rh_DISP_1ST":{"Path":"Sts/Rh_DISP_1ST","Parameters":opnimUnitParametersObject},
							"Rh_DISP_2ND":{"Path":"Sts/Rh_DISP_2ND","Parameters":opnimUnitParametersObject},
							"Rh_DISP_3RD":{"Path":"Sts/Rh_DISP_3RD","Parameters":opnimUnitParametersObject},
							"Rh_FEED_FLAG":{"Path":"Sts/Rh_FEED_FLAG","Parameters":opnimUnitParametersObject},
							"Rh_H2O_1ST":{"Path":"Sts/Rh_H2O_1ST","Parameters":opnimUnitParametersObject},
							"Rh_H2O_2ND":{"Path":"Sts/Rh_H2O_2ND","Parameters":opnimUnitParametersObject},
							
#=========== Left out because hard coded into Opnim IX Column	UDT						
#							"Rh_HS_7100_2":{"Path":"Sts/Rh_HS_7100_2","Parameters":opnimUnitParametersObject},
#							"Rh_LSH_7130C":{"Path":"Sts/Rh_LSH_7130C","Parameters":opnimUnitParametersObject},
#							"Rh_LSH_7130E":{"Path":"Sts/Rh_LSH_7130E","Parameters":opnimUnitParametersObject},
#							"Rh_LSH_7130F":{"Path":"Sts/Rh_LSH_7130F","Parameters":opnimUnitParametersObject},
#							"Rh_LSH_7960":{"Path":"Sts/Rh_LSH_7960","Parameters":opnimUnitParametersObject},

							"Rh_PAUSE_7100Column":{"Path":"Sts/Rh_PAUSE_7100Column","Parameters":opnimUnitParametersObject},
							"Rh_SO2_1ST":{"Path":"Sts/Rh_SO2_1ST","Parameters":opnimUnitParametersObject},
							"Rh_SO2_2ND":{"Path":"Sts/Rh_SO2_2ND","Parameters":opnimUnitParametersObject},
							"Rh_STP_COMP_7Column":{"Path":"Sts/Rh_STP_COMP_7Column","Parameters":opnimUnitParametersObject},
							"Rh_STRIP_1ST":{"Path":"Sts/Rh_STRIP_1ST","Parameters":opnimUnitParametersObject},
							"Rh_STRIP_2ND":{"Path":"Sts/Rh_STRIP_2ND","Parameters":opnimUnitParametersObject},
							"Rh_VLVS_7100Column":{"Path":"Sts/Rh_VLVS_7100Column","Parameters":opnimUnitParametersObject},
							"Rh_SO2_1ST":{"Path":"Sts/Rh_SO2_1ST","Parameters":opnimUnitParametersObject},
							"Rh_SO2_1ST":{"Path":"Sts/Rh_SO2_1ST","Parameters":opnimUnitParametersObject},
							"Rh_STP_COMP_7Column":{"Path":"Sts/Rh_STP_COMP_7Column","Parameters":opnimUnitParametersObject},
							"Rh_STRIP_1ST":{"Path":"Sts/Rh_STRIP_1ST","Parameters":opnimUnitParametersObject},
							"Rh_STRIP_2ND":{"Path":"Sts/Rh_STRIP_2ND","Parameters":opnimUnitParametersObject},
							"Rh_VLVS_7100Column":{"Path":"Sts/Rh_VLVS_7100Column","Parameters":opnimUnitParametersObject},
							#Volume Param
#=========== Left out because hard coded into Opnim IX Column	UDT									
#							"Rh_BACKWASH_VOL":{"Path":"Cfg/Rh_BACKWASH_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_COND_1ST_VOL":{"Path":"Cfg/Rh_COND_1ST_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_COND_2ND_VOL":{"Path":"Cfg/Rh_COND_2ND_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_DISPL_1ST_VOL":{"Path":"Cfg/Rh_DISPL_1ST_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_DISPL_2ND_VOL":{"Path":"Cfg/Rh_DISPL_2ND_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_DISPL_3RD_VOL":{"Path":"Cfg/Rh_DISPL_3RD_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_FEED_VOL":{"Path":"Cfg/Rh_FEED_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_H2O_1ST_VOL":{"Path":"Cfg/Rh_H2O_1ST_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_H2O_2ND_VOL":{"Path":"Cfg/Rh_H2O_2ND_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_SO2_1ST_VOL":{"Path":"Cfg/Rh_SO2_1ST_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_SO2_2ND_VOL":{"Path":"Cfg/Rh_SO2_2ND_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_STRIP_1ST_VOL":{"Path":"Cfg/Rh_STRIP_1ST_VOL","Parameters":opnimUnitParametersObject},
#							"Rh_STRIP_2ND_VOL":{"Path":"Cfg/Rh_STRIP_2ND_VOL","Parameters":opnimUnitParametersObject},
							#Parameters
#=========== Left out because hard coded into Opnim IX Column	UDT	
#							"Rh_AUTO_7100":{"Path":"Cmd/Rh_AUTO_7100","Parameters":opnimUnitParametersObject},
#							"Rh_HS_7100_1":{"Path":"Cmd/Rh_HS_7100_1","Parameters":opnimUnitParametersObject},
#							"Rh_MAN_7100":{"Path":"Cmd/Rh_MAN_7100","Parameters":opnimUnitParametersObject},
							
							
							"Rh_AUTO_7100Column":{"Path":"Cmd/Rh_AUTO_7100Column","Parameters":opnimUnitParametersObject},
							"Rh_CONTINUE_7Column":{"Path":"Cmd/Rh_CONTINUE_7Column","Parameters":opnimUnitParametersObject},
							"Rh_MAN_7100Column":{"Path":"Cmd/Rh_MAN_7100Column","Parameters":opnimUnitParametersObject},
							"Rh_STOP_STEP_7Column":{"Path":"Cmd/Rh_STOP_STEP_7Column","Parameters":opnimUnitParametersObject},
							"Rh_TO_1STDISPColumn":{"Path":"Cmd/Rh_TO_1STDISPColumn","Parameters":opnimUnitParametersObject}
							
				
							},	
				"Rh_7210_30_A_B":{							
							#Bromate Addition
							"Add_20_Litres":{"Path":"Cmd/Add_20_Litres","Parameters":opnimUnitParametersObject},				
							"Add_50_Litres":{"Path":"Cmd/Add_50_Litres","Parameters":opnimUnitParametersObject},								
							"Stop_Addition":{"Path":"Cmd/Stop_Addition","Parameters":opnimUnitParametersObject}										
							},
				"Rh_6003C":{},
				"Rh_6670":{},
				"Rh_6000":{},
				"Rh_7100A":{},
				"Rh_IX_Columns":{},
				"Rh_GLV_7310":{},
				"Rh_Reset_Brom":{},
				"Rh_7060":{},
				"Rh_7090_HCL":{},
				"Rh_7090":{},
				"Rh_DeminMakeUp_7080":{},				
				"Rh_6030":{},
				"Rh_7043_5_Organic_Make_up":{},
				"Rh_7981":{},
				"Rh_7096_Chlorine_Supply":{},
				"Rh_HCL_Supply_Header":{},
				"Rh_NitricAddition_7030_8030":{}
																		
				
							}
#Impala A2 Control Module Mapping
controlModuleA2Ign = {
				#Digital Inputs
				"b_DigitalInput":"DI",
				#Digital Outputs
				"b_DigitalOutput":"DO",
				#Analog Inputs
				"b_AnalogueInput":"AI",
				"b_AnalogueInput_001":"AI",
				#Analog Outputs
				"b_AnalogueOutput":"AO",
				#Controllers
				"b_PID":"Controller",
				"b_PID_DO":"Controller",
				#Motors
				"b_DiscreteMotor":"Motor",
				#Valves
				"b_DiscreteValve":"Valve",
				"b_DiscreteValve_Resin":"Valve",
				"b_Handvalve":"Valve",
				#Totalisers
				"b_Totaliser":"Totaliser"				
				}


#TypeID Control Module Mapping
controlModuleTypeID = {
					"DI":"Application Default/Control Modules/DI",
					"DO":"Application Default/Control Modules/DO",
					"AI":"Application Default/Control Modules/AI",
					"AO":"Application Default/Control Modules/AO",
					"Controller":"Application Default/Control Modules/Controller",
					"Motor":"Application Default/Control Modules/Motor",
					"Valve":"Application Default/Control Modules/Valve",
					"Totaliser":"Application Default/Control Modules/Totaliser"
						}

#Control Module Attributes
controlModuleAttributes = {
				#Digital Input
				"DI":{
					#Alarm Delays
					"AlarmDelay":{"Path":"Alarms/State","Parameters":{"DefaultValue":10,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},																																																																					
					#General
					"Input": {"Path":"In/Input","Parameters":{"ValueSource":"opc"}},
					"Action": {"Path":"Cfg/Action","Parameters":{"DefaultValue":False,"ValueSource":"memory","reverse":True}},
					"AlarmAction": {"Path":"Cfg/AlarmHealthyState","Parameters":{"DefaultValue":True,"ValueSource":"memory","reverse":True}}				
					 },						
						
				#Digital Output
				"DO":{
					#General
					"Output":{"Path":"Out/Output","Parameters":{"ValueSource":"opc"}},
					"Interlock":{"Path":"Interlock/Operation","Parameters":{"ValueSource":"udtInstance","TypeID":"Standard/Primitives/Interlock Primitive","InterlockName":"Operation"}},
					"DisableManualMode": {"Path":"Cfg/DisableManualMode","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},
					"DeviceAcquired":{"Path":"Cmd/OperationActive","Parameters":{"ValueSource":"opc"}}
					},
				#Analog Input
				"AI":{		
					#Alarm Setpoints
					"AlarmHighLimit":{"Path":"Alarms/High","Parameters":{"DefaultValue":0,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},
					"AlarmHighHighLimit":{"Path":"Alarms/HighHigh","Parameters":{"DefaultValue":0,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},
					"AlarmLowLimit":{"Path":"Alarms/Low","Parameters":{"DefaultValue":0,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},					
					"AlarmLowLowLimit":{"Path":"Alarms/LowLow","Parameters":{"DefaultValue":0,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},					
					"HighRateAlarmLimit":{"Path":"Alarms/HighRate","Parameters":{"DefaultValue":1,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},										
					"LowRateAlarmLimit":{"Path":"Alarms/LowRate","Parameters":{"DefaultValue":1,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},																													
					#Alarm Delays
					"DelayBadData":{"Path":"Alarms/BadData","Parameters":{"DefaultValue":10,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},																																																																
					"DelayHighRate":{"Path":"Alarms/HighRate","Parameters":{"DefaultValue":10,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},																																																																
					"DelayLowRate":{"Path":"Alarms/LowRate","Parameters":{"DefaultValue":10,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},																																																																
																																																																											
					"Value/EngUnits": {"Path":"Params.EngUnits","Parameters":{}},						
					"Value.Precision":{"Path":"Sts/Value.FormatString","Parameters":{}},
					"SetPoint":{"Path":"Cfg/Target","Parameters":{"ValueSource":"opc"}},
					"Value":{"Path":"Sts/Value","Parameters":{"ValueSource":"opc","ScalingDefaultValues":{"rawLow":0,"rawHigh":100,"engLow":-6,"engHigh":106,"scaledLow":0,"scaledHigh":100}}},
					"DeviceAcquired":{"Path":"Cmd/OperationActive","Parameters":{"ValueSource":"opc"}}
					},
				#Analog Output
				"AO":{
					#Alarm Setpoints	
					"ClosedThreshold":{"Path":"Alarms/Limit","Parameters":{"DefaultValue":5,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},
					
					#Alarm Delays
					"DelayAlarmFailure":{"Path":"Alarms/Limit","Parameters":{"DefaultValue":10,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}},				
					#General
					"Value/EngUnits": {"Path":"Params.EngUnits","Parameters":{}},
					"Value.Precision":{"Path":"Sts/Value.FormatString","Parameters":{}},
					"LimitClosed":{"Path":"Sts/LimitClosed","Parameters":{"ValueSource":"opc"}},
					"Mode": {"Path":"Cfg/InternalExternalSelect","Parameters":{}}, #Memory on UDT. Mapping for Historising Check
					"DisableManualMode":{"Path":"Cfg/DisableManualMode","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},
					"Value":{"Path":"Cmd/InternalSetpoint","Parameters":{"ValueSource":"opc","ScalingDefaultValues":{"rawLow":0,"rawHigh":100,"engLow":-6,"engHigh":106,"scaledLow":0,"scaledHigh":100}}},
					"Interlock":{"Path":"Interlock/Operation","Parameters":{"ValueSource":"udtInstance","TypeID":"Standard/Primitives/Interlock Primitive","InterlockName":"Operation"}},
					"DeviceAcquired":{"Path":"Cmd/OperationActive","Parameters":{"ValueSource":"opc"}}
					},
				#Controller
				"Controller":{
					#Alarm Setpoints
					"DeviationToleranceNegative":{"Path":"Cfg/DeviationNegativeLimit","Parameters":{"DefaultValue":10,"ValueSource":"memory"}},					
					"DeviationTolerancePositive":{"Path":"Cfg/DeviationPositiveLimit","Parameters":{"DefaultValue":10,"ValueSource":"memory"}},					
										
					#General
					"AO": {"Path":"Params.OutputTagPath","Parameters":{}},
					"AI": {"Path":"Params.AnalogInputTagPath","Parameters":{}},
					"ControlVariable/EngUnits": {"Path":"Params.OutputEngUnits","Parameters":{}},
					"ProcessVariable/EngUnits": {"Path":"Params.ProcessVariableEngUnits","Parameters":{}},
					"DisableManualMode":{"Path":"Cfg/DisableManualMode","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},
					"ModeStatus":{"Path":"Sts/ModeStatus","Parameters":{"ValueSource":"opc"}},
					
					"DeviceAcquired":{"Path":"Cmd/OperationActive","Parameters":{"ValueSource":"opc"}},				
				
					"ControlVariable":	{"Path":"Out/Output","Parameters":{}}, #Memory on UDT. Mapping for Historising Check
					"ProcessVariable":	{"Path":"In/ProcessVariable","Parameters":{}}, #Memory on UDT. Mapping for Historising Check	
					"SetPoint":	{"Path":"Sts/Setpoint","Parameters":{}} #Memory on UDT. Mapping for Historising Check							
				},
				#Motor
				"Motor":{
					"RunFieldSwitch":{"Path":"In/LocalStart","Parameters":{"ValueSource":"opc"}},
					"StopFieldSwitch":{"Path":"In/LocalStop","Parameters":{"ValueSource":"opc"}},
					"Overload":{"Path":"In/Available","Parameters":{"ValueSource":"opc"}},
					"Output":{"Path":"Out/Start","Parameters":{"ValueSource":"opc"}},
					"InterlockBypass":{"Path":"In/InterlockBypass","Parameters":{"ValueSource":"opc"}},
					"Interlock":{"Path":"Interlock/Operation","Parameters":{"ValueSource":"udtInstance","TypeID":"Standard/Primitives/Interlock Primitive","InterlockName":"Operation"}},
					"DeviceAcquired":{"Path":"Cmd/OperationActive","Parameters":{"ValueSource":"opc"}},
					
					"StatusRunning":	{"Path":"Sts/Running","Parameters":{}}, #Memory on UDT. Mapping for Historising Check		
					"StatusStopped":	{"Path":"Sts/Stopped","Parameters":{}} #Memory on UDT. Mapping for Historising Check	
					},

				#Valve
 				"Valve": {			
 					#Alarm Setpoints		
 					"AlarmPositionAction":{"Path":"Alarms/Position","Parameters":{"DefaultValue":0,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}}, 	
 					#Alarm Delays
 					"DelayFailureClose":{"Path":"Alarms/CloseLimit","Parameters":{"DefaultValue":15,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}}, 	
 					"DelayFailureOpen":{"Path":"Alarms/OpenLimit","Parameters":{"DefaultValue":15,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}}, 
  					"DelayPositionAlarm":{"Path":"Alarms/Position","Parameters":{"DefaultValue":10,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}}, 																				
 					#General 					
					"EnableLimitOpen": {"Path":"Cfg/EnableLimitOpen","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},	
					"EnableLimitClosed": {"Path":"Cfg/EnableLimitClosed","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},		
					"Action": {"Path":"Cfg/FailSafePosition","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},	
					"EnableDualAction": {"Path":"Cfg/EnableDualAction","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},	
					"DisableManualMode": {"Path":"Cfg/DisableManualMode","Parameters":{"DefaultValue":False,"ValueSource":"memory"}},					
					"LimitOpen": {"Path":"In/Opened","Parameters":{"ValueSource":"opc"}},
					"LimitClosed":{"Path":"In/Closed","Parameters":{"ValueSource":"opc"}},
					"OutputOpen":{"Path":"Out/Open","Parameters":{"ValueSource":"opc"}},
					"OutputClose":{"Path":"Out/Close","Parameters":{"ValueSource":"opc"}},
					"Interlock":{"Path":"Interlock/Operation","Parameters":{"ValueSource":"udtInstance","TypeID":"Standard/Primitives/Interlock Primitive","InterlockName":"Operation"}},
					"DeviceAcquired":{"Path":"Cmd/OperationActive","Parameters":{"ValueSource":"opc"}},
					"StatusClosed":	{"Path":"Sts/Closed","Parameters":{}}, #Purely an Expression on the UDT. Mapping for Historising Check
					"StatusOpen":	{"Path":"Sts/Opened","Parameters":{}}, #Purely an Expression on the UDT. Mapping for Historising Check
					"MaintenanceStrokeCount":{"Path":"Sts/StrokeCount","Parameters":{}}#Purely an Expression on the UDT. Mapping for Historising Check
						},
				#Totaliser
				"Totaliser":{
					#Alarm Setpoints
					"AlarmHighLimit":{"Path":"Alarms/High","Parameters":{"DefaultValue":0,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}}, 
					"BadDataAnalogueThreshold":{"Path":"Alarms/Communication","Parameters":{"DefaultValue":0,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}}, 		
					#Alarm Delays
					"DelayBadDataAlarm":{"Path":"Alarms/Communication","Parameters":{"DefaultValue":10,"ValueSource":"udtInstance","TypeID":"Standard/Alarms/Alarm Primitive"}}, 
					
					#General
					"Target": {"Path":"Cfg/Target","Parameters":{"DefaultValue":0,"ValueSource":"memory"}},
					"Value/EngUnits": {"Path":"EngUnits","Parameters":{}},
					"Value.Precision":{"Path":"Sts/Value.FormatString","Parameters":{}},
					"Value":{"Path":"Sts/Value","Parameters":{"ValueSource":"opc"}},
					"Value.Analogue":{"Path":"In/Input","Parameters":{"ValueSource":"opc"}},
					"DeviceAcquired":{"Path":"Cmd/OperationActive","Parameters":{"ValueSource":"opc"}}
						}
						}
#==================================== GetA2MigrationMappingObject ==========================
#Main script that returns the overall mapping object, mapping Model, A2 Control Modules and Units to equivalent Ignition Folders, CMs and IMs
def GetA2MigrationMappingObject():

	mappingObject = {}
	requiredA2ControlModuleKeys = controlModuleA2Ign.keys()
	requiredA2ImplementationModuleKeys = implementationModuleA2Ign.keys()
	
	#Control Modules
	for requiredA2ControlModuleKey in requiredA2ControlModuleKeys:
		requiredIgnControlModuleObject = getControlModuleInfo(controlModuleA2Ign[requiredA2ControlModuleKey])
		mappingObject[requiredA2ControlModuleKey] = requiredIgnControlModuleObject
	
	#Implementation Modules
	for requiredA2ImplementationModuleKey in requiredA2ImplementationModuleKeys:
		requiredA2ImplementationModuleKeyObject = implementationModuleA2Ign[requiredA2ImplementationModuleKey]
		requiredIgnImplementationModuleKey = requiredA2ImplementationModuleKeyObject["IgnTypeIDKey"]
		requiredIgnImplementationModuleTagName = requiredA2ImplementationModuleKeyObject["TagName"]
		requiredIgnControlModuleObject = getImplementationModuleInfo(requiredIgnImplementationModuleKey,requiredIgnImplementationModuleTagName)
		mappingObject[requiredA2ImplementationModuleKey] = requiredIgnControlModuleObject	
	
	return mappingObject


#============================================================================================
#=================================== Control Modules ========================================
#============================================================================================


#==================================== GetDefaultObjectInfo =================================
def getDefaultControlModuleObjectInfo():
	
	objectInfoMapping = {
						"ContainedName":{"Path":"Params.ContainedName","Parameters":{}},
						"Description":{"Path":"Params.Description","Parameters":{}},
						"Area":{"Path":"Params.ShortDescription","Parameters":{}},
						"Tagname":{"Path":"Params.ShortDescription","Parameters":{}}	
							}
	
	return objectInfoMapping

#=================================== getControlModuleInfo ===================================
def getControlModuleInfo(ControlModule):
	controlModule = ControlModule
	mappingObject = {
					"typeId":controlModuleTypeID[controlModule],
					"Attributes":controlModuleAttributes[controlModule],
					"ObjectInfo":getDefaultControlModuleObjectInfo()
						}		
	return mappingObject
	
#============================================================================================
#=================================== Implementation Modules =================================
#============================================================================================

#==================================== GetDefaultObjectInfo =================================
def getDefaultImplementationModuleObjectInfo():
	
	objectInfoMapping = {
						"Description":{"Path":"Params.Description","Parameters":{}},
						"Area":{"Path":"Params.ShortDescription","Parameters":{}},
						"Tagname":{"Path":"Params.ShortDescription","Parameters":{}}	
							}
	
	return objectInfoMapping

#=================================== getImplementationModuleInfo ============================
def getImplementationModuleInfo(ImplementationModule,TagName):
	implementationModule = ImplementationModule	
	tagName = TagName
	mappingObject = {
					"typeId":implementationModuleTypeID[implementationModule],
					"tagName":tagName,
					"Attributes":implementationModuleAttributes[implementationModule],
					"ObjectInfo":getDefaultImplementationModuleObjectInfo()
						}		
			
	return	mappingObject	
	
#====================================== GetHandValveTagObject ===============================
#Function that returns tags required for Cfg.IsHandValve tag in Valve Control Module
def GetHandValveTagObject(IsHandValve = True):
	handValveObject = Standard.Utilities.A2Migration.GetFolderTagDefinition("Cfg")
	tagObject = Standard.Utilities.A2Migration.GetAtomicTagDefinition(tagName = "IsHandValve",valueSource = "memory")
	tagObject = Standard.Utilities.A2Migration.getMemoryTagDefinition(tagObject,valueSourceParameters = {"value":IsHandValve})
	
	handValveObject["tags"].append(tagObject)
	
	return handValveObject

#====================================== GetPulseGenTagObject ===============================
#Function that returns tags required for Cfg.PulseGenEnable tag in PID Control Module
def GetPulseGenTagObject(PulseGenEnable = True):
	pidFolderObject = Standard.Utilities.A2Migration.GetFolderTagDefinition("Cfg")
	tagObject = Standard.Utilities.A2Migration.GetAtomicTagDefinition(tagName = "PulseGenEnable",valueSource = "memory")
	tagObject = Standard.Utilities.A2Migration.getMemoryTagDefinition(tagObject,valueSourceParameters = {"value":PulseGenEnable})
	
	pidFolderObject["tags"].append(tagObject)
	
	return pidFolderObject
						
#====================================== GetIgnitionUnitInstanceNamefromRuntimeInstanceName ========
#Function used when verifying that all tags in the current historian are present and being historised in Ignition
#Naming convention is not Standard when it comes to units and 	needs to be mapped manually for each unit
def GetIgnitionUnitInstanceNamefromRuntimeInstanceName(RuntimeInstanceName):
	runTimeTagInstanceName = RuntimeInstanceName
	isControlModule = False
	#Replace common paramter names with "" in runTimeTagInstanceName 
	parameterStrings = ["_HMI_GLV_Status","_HMI_Parameters","_Addition_Control","_Valve_Control","_Hand_Switch"
						"_Bromate_Addition","_DetaVolControl","_Flow_Parameters","_Status","_Volume_Parameters",
						"_Manual_Steps","_Parameters","_Rh_Bromate_Addition"
						]
	for parameterString in parameterStrings:
		runTimeTagInstanceName = runTimeTagInstanceName.replace(parameterString,"")	
				 
	#Opnim_Barr_GLV N/A
		
	#Opnim_GLV
	if "Rh_6660" in runTimeTagInstanceName: 
		runTimeTagInstanceName = "Rh_GLV_6660"
	elif "Rh_GLV_7900C" in  runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7900C"
	elif "Rh_8100" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_IR_GLV8100"
	elif "Rh_8200" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_IR_GLV8200"
	#Opnim_Ir_Glovebox_8103_8703
	elif "8103" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_Ir_GloveBox_8103"
	elif "8703" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_Ir_GloveBox_8703"	
	#Opnim_Ir_Glovebox_8303_8503
	elif "8303" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_Ir_GloveBox_8303"
	elif "8503" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_Ir_GloveBox_8503"
	#Opnim_IR_GLV
	elif "Rh_8500" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_IR_GLV_8500"
	elif "Rh_8600" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_IR_GLV_8600"
	#Opnim_Ir_GLV_2
	elif "Rh_HS_8300" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_8300"
	elif "Rh_HS_8400" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_8400"
	#Opnim_IX_GLV
	elif "Rh_7240A" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7240A"
	elif "Rh_7240B" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7240B"
	elif "Rh_7700" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7700"
	#Opnim_PPT_GLV
	elif "Rh_7210A" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7210A_N"
	elif "Rh_7210B" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7210B_N"
	elif "Rh_7230A" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7230A_N"
	elif "Rh_7230B" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7230B_N"		
	#Opnim_IX_Column N/A
	#Rh_7210_30_A_B
	elif "Rh_7210A" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7210A"
	elif "Rh_7210B" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7210B" 
	elif "Rh_7230A" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7230A" 	
	elif "Rh_7230B" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV_7230B" 	
	#Individual Instances
	elif "Rh_7060" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_7060E_F_HCL_Strip_Make_Up"
	elif "Rh_7090"  in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_CL2HCL_MakeUp"	
	elif "Rh_7300A" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV7300A"	
	elif "Rh_7300B" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_GLV7300B"	
	elif "Rh_Cl2_EmergencyStop" in runTimeTagInstanceName:
		runTimeTagInstanceName = "Rh_7096_Chlorine_Supply"
	elif "Rh_Deta_Makeup" in runTimeTagInstanceName:
		 runTimeTagInstanceName = "Rh_6030"
	elif "Rh_DeminMakeUp" in runTimeTagInstanceName:
		 runTimeTagInstanceName = "Rh_DeminMakeUp_7080"	
	elif "Rh_DeminMakeUp" in runTimeTagInstanceName:
		 runTimeTagInstanceName = "Rh_DeminMakeUp_7080"				 
	elif "Rh_IX_Global" in runTimeTagInstanceName:
		 runTimeTagInstanceName = "Rh_IX_Columns"
	elif "Rh_MakeUP_Vol_7043_5"	in runTimeTagInstanceName or "Rh_MakeUP_Vol_7043_5" in runTimeTagInstanceName:
		 runTimeTagInstanceName = "Rh_7043_5_Organic_Make_up" 
	elif "Rh_NitricAddition_7030_8030" in runTimeTagInstanceName:
		 runTimeTagInstanceName = "Rh_NitricAcid_7070_7030"
	
		 	 	 
	#Control Modules that were not updated with the correct Contained Name
	elif "Rh_LSH_7100K" in runTimeTagInstanceName:
		 runTimeTagInstanceName = "Rh_LSH_7100A" 	 
		 isControlModule = True	 
	elif "Rh_PSH_7100K" in runTimeTagInstanceName:
		 runTimeTagInstanceName ="Rh_PSH_7100A"	
		 isControlModule = True	 
	elif "Rh_TISH_7510" in runTimeTagInstanceName:
		 runTimeTagInstanceName ="Rh_TAH_7510"	
		 isControlModule = True	 		 
	elif "Rh_UY_7100KA" in runTimeTagInstanceName:
		 runTimeTagInstanceName ="Rh_UY_7100AA"	
		 isControlModule = True	 
	elif "Rh_UY_7100KB" in runTimeTagInstanceName:
		 runTimeTagInstanceName ="Rh_UY_7100AB"
		 isControlModule = True	 
	  	 	 	 	 	 	  	 	 	 	 	 	 	  	 	 	 	 	 	  	 	 	 	 	 	 
		  	 	 	 	 	 	  	 	 	 	 	 	 	  	 	 	 	 	 	  	 	 	 	 	 	 	  	 	 	 	 	 	  	 	 	 	 	 	 	  	 	 	 	 	 	  	 	 	 	 	 	 	  	 	 	 	 	 	  	 	 	 	 	 	 	  	 	 	 	 	 	  	 	 	 	 	 	 
	return runTimeTagInstanceName,isControlModule
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
	
	

