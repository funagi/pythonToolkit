#pragma rtGlobals=1		// Use modern global access method.
Menu "&OOMMF"
	"Find vortex cores...", OpenOMFBatch2()
	//"Import Vortex Field File...", ParseOMF()
End
//将vortex trilayer nanodisk dynamics 的omf文件进行批处理：将mz分量map成为二维图像，通过拟合得到vortex core position, 
// old : basename需要手工输入
Function OpenOMFBatch()
	Variable refNum
	String S_path,S_filename
	Open /D /R /F="OOMMF Field Files (*.o?f):.o?f;" /M="Choose an OOMMF File" refNum
	If( CmpStr(S_filename,"")==0 )
		return 0
	Endif
	String /G Path=ParseFilePath(1,S_Filename,":",1,0)
	
	String basename="rotating-Oxs_TimeDriver-Magnetization-00-", filename
	Variable step=20, maxvalue=100,minvalue=0,i,count
	Prompt basename, "Input basename:"
	Prompt step, "Input step size:"
	Prompt minvalue, "Input min value:"
	Prompt maxvalue, "Input max value:"
	DoPrompt "Enter parameters", basename,step,minvalue,maxvalue
	count=(maxvalue-minvalue)/step
	Make/N=(count,5)/D/O datatable
	NewPath Data path
	For (i=minvalue;i<maxvalue;i+=step)
		sprintf filename, "%s%07d.omf", basename, i
		parseData(filename, (i-minvalue)/step, datatable)
	Endfor
End

// new : 自动提取basename
Function OpenOMFBatch2()
	Variable refNum
	String S_path,S_filename
	Open /D /R /F="OOMMF Field Files (*.o?f):.o?f;" /M="Choose an OOMMF File" refNum
	If( CmpStr(S_filename,"")==0 )
		return 0
	Endif
	String /G Path=ParseFilePath(1,S_Filename,":",1,0)
	String /G Filename0=ParseFilePath(0,S_Filename,":",1,0)
	
	String basename=Filename0[0,strlen(Filename0)-12], filename
	Variable step=20, maxvalue=100,minvalue=0,i,count
	Prompt step, "Input step size:"
	Prompt minvalue, "Input min value:"
	Prompt maxvalue, "Input max value:"
	DoPrompt "Enter parameters", step,minvalue,maxvalue
	count=(maxvalue-minvalue)/step
	Make/N=(count,5)/D/O datatable
	NewPath Data Path
	For (i=minvalue;i<maxvalue;i+=step)
		//printf "%s%07d.omf", basename, i
		sprintf filename, "%s%07d.omf", basename, i
		parseData(filename, (i-minvalue)/step, datatable)
	Endfor
End
//对单个omf文件处理
function parseData(filename, position, wname)
	String filename
	Variable position
	wave wname
	Variable timevalue
	wave coef
	//find time
	Grep /E="Total simulation time" /LIST /P=Data filename
	If(V_value==1)
		sscanf S_value, "# Desc:  Total simulation time: %es;", timevalue
	Else
		Print "Can't load basic properties from target file."
		return 0
	Endif
	//find peaks
	LoadWave /A /B="C=1,N='_skip_';C=1,N='_skip_';C=1,N=mz1;" /D /G /O /W /P=Data filename
	duplicate/O mz1 mz2
	Redimension/N=(100,100,3) mz1,mz2
	DeletePoints/M=2 1,2, mz1
	DeletePoints/M=2 0,2, mz2
	Redimension/N=(-1,-1) mz1,mz2
	peak(mz1)
	wname[position][1]=coef[2]
	wname[position][2]=coef[4]
	peak(mz2)
	wname[position][3]=coef[2]
	wname[position][4]=coef[4]
	//write time value
	wname[position][0]=timevalue
End
//找到mz并拟合寻峰
function peak (mz)
wave mz
make/N=7/D/O coef
variable i, j, flag=0, x, y
for (i=0;i<100;i+=1)
	for (j=0;j<100;j+=1)
		if(mz[i][j]>=flag)
		 	flag=mz[i][j]
		 	x=i
		 	y=j
		endif
	endfor
endfor
// printf "peakposition x=%g, y=%g" x, y 
CurveFit/NTHR=0 Gauss2D kwCWave=coef,  mz[x-10,x+10][y-10,y+10]/D
end

