#--------------------------------------------------------------ExcelToList--------------------------------------------	
def ExcelToList(bytesIn = None,fileName=None, hasHeaders = False, sheetNum = 0, firstRow = None, lastRow = None, firstCol = None, lastCol = None):
	import org.apache.poi.ss.usermodel.WorkbookFactory as WorkbookFactory
	import org.apache.poi.ss.usermodel.DateUtil as DateUtil
	from java.io import ByteArrayInputStream
	from java.io import FileInputStream
	from java.util import Date
	
	"""
	   Function to create a dataset from an Excel spreadsheet. It will try to automatically detect the boundaries of the data,
	   but helper parameters are available:
	   params:
	   		fileName   - The path to the Excel spreadsheet. (required)
	   		hasHeaders - If true, uses the first row of the spreadsheet as column names.
	   		sheetNum   - select the sheet to process. defaults to the first sheet.
	   		firstRow   - select first row to process. 
	   		lastRow    - select last row to process.
	   		firstCol   - select first column to process
	   		lastCol    - select last column toprocess
	"""
	if fileName is None:
		fileStream = ByteArrayInputStream(bytesIn)
	else:
		fileStream = FileInputStream(fileName)

	wb = WorkbookFactory.create(fileStream)
	
	sheet = wb.getSheetAt(sheetNum)

	if firstRow is None:
		firstRow = sheet.getFirstRowNum()
	if lastRow is None:
		lastRow = sheet.getLastRowNum()

	data = []
	for i in range(firstRow , lastRow + 1):
		row = sheet.getRow(i)
		print str(i).zfill(3), list(row)
		if i == firstRow:
			if firstCol is None:
				firstCol = row.getFirstCellNum()

			if lastCol is None:
				lastCol  = row.getLastCellNum()
			else:
				# if lastCol is specified add 1 to it.
				lastCol += 1
			if hasHeaders:
				headers = list(row)[firstCol:lastCol]
			else:
				headers = ['Col'+str(i) for i in range(firstCol, lastCol)] 
		rowOut = []
		rowObject = {}
		for j in range(firstCol, lastCol):
			if i == firstRow and hasHeaders:
				pass
			else:
				#system.perspective.print("Colum:" + str(j) + "--Row:" + str(i))
				cell = row.getCell(j)
				cellType = None
				if cell is not None:
					cellType = cell.getCellType().toString()
				if cellType == 'NUMERIC':
					if DateUtil.isCellDateFormatted(cell):
						value =  cell.dateCellValue
					else:
						value = cell.getNumericCellValue()
						if value == int(value):
							value = int(value)
					if str(value) == "NULL" or str(value) == "#N/A" or str(value) == "":
						value = None
				elif cellType == 'STRING':
					value = cell.getStringCellValue()
					if value == "NULL" or value == "#N/A" or str(value) == "":
						value = None
				elif cellType == 'BOOLEAN':
					value = cell.getBooleanCellValue()
					if value == "NULL" or value == "#N/A" or str(value) == "":
						value = None
				elif cellType == 'BLANK':
					value = None	
				elif cellType == 'FORMULA':
					formulatype=str(cell.getCachedFormulaResultType())
					if formulatype == 'NUMERIC':
						if DateUtil.isCellDateFormatted(cell):
							value =  cell.dateCellValue
						else:
							value = cell.getNumericCellValue()
							if value == int(value):
								value = int(value)
						if str(value) == "NULL" or str(value) == "#N/A" or str(value) == "":
							value = None
					elif formulatype == 'STRING':
						value = cell.getStringCellValue()
						if value == "NULL" or value == "#N/A" or str(value) == "":
							value = None
					elif formulatype == 'BOOLEAN':
						value = cell.getBooleanCellValue()
						if value == "NULL" or value == "#N/A" or str(value) == "":
							value = None
					elif formulatype == 'BLANK':
						value = None
				else:
					value = None	
				rowOut.append(value)
				headerName = headers[j]
				rowObject[headerName] = value
		if len(rowOut) > 0:
			rowOut.append(rowObject)
			data.append(rowObject)

	fileStream.close()
	return data