#pragma rtGlobals=1		// Use modern global access method.
Menu "&OOMMF"
	"Find vortex cores...", OpenOMFBatch2()
End
//将vortex trilayer nanodisk dynamics 的omf文件进行批处理：将mz分量map成为二维图像，通过拟合得到vortex core position, 
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
	Variable z=3
	Prompt step, "Input step size:"
	Prompt minvalue, "Input min value:"
	Prompt maxvalue, "Input max value:"
	Prompt z, "Input Z-Slice:"
	DoPrompt "Enter parameters", step,minvalue,maxvalue,z
	count=(maxvalue-minvalue)/step
	Make/N=(count,5)/D/O datatable
	NewPath Data Path
	
	//显示进度条窗口
	NewPanel /N=Progress /W=(285,111,739,193)
	ValDisplay valdisp0, pos={18,32}, size={342,18}
	ValDisplay valdisp0, limits={0,maxvalue,0},barmisc={0,0}
	ValDisplay valdisp0, mode=3, frame=0
	ValDisplay valdisp0, value=_NUM:0
	Button bStop, pos={375,32}, size={50,20}, title="Stop"
	TitleBox message, pos={18,12}, Title="Searching for vortex cores ... ", frame=0
	TitleBox timebox, pos={18,57}, Title="", frame=0
	DoUpdate /W=Progress /E=1
	variable time0 = ticks,timeelapsed,timeremaining
	For (i=minvalue;i<maxvalue;i+=step)
		sprintf filename, "%s%07d.omf", basename, i
		parseData(filename, (i-minvalue)/step, datatable, z)
		//更新进度条的值
		ValDisplay valdisp0, value=_NUM:i+1, win=Progress
		DoUpdate /W=Progress
		timeelapsed = ticks-time0
		timeremaining = timeelapsed*(maxvalue-i)/i
		TitleBox message, Title="Searching for vortex cores ... ("+num2str((i-minvalue)/step)+"/"+num2str((maxvalue-minvalue)/step)+")"
		TitleBox timebox, Title="Time Elapsed: "+Secs2Time(timeelapsed/60,5)+"  Time Remaining: "+Secs2Time(timeremaining/60,5)
		if (V_Flag == 2)
			break
		Endif
	Endfor
	KillWindow Progress
End
//对单个omf文件处理
function parseData(filename, position, wname, z)
	String filename
	Variable position,z
	wave wname
	Variable timevalue
	wave coef
	//find time
	Grep /E="Total simulation time" /Q /LIST /P=Data filename
	If(V_value==1)
		sscanf S_value, "# Desc:  Total simulation time: %es;", timevalue
	Else
		Print "Can't load basic properties from target file."
		return 0
	Endif
	//find peaks
	LoadWave /A /B="C=1,N='_skip_';C=1,N='_skip_';C=1,N=mz1;" /D /G /O /Q /W /P=Data filename
	duplicate/O mz1 mz2
	Redimension/N=(100,100,z) mz1,mz2
	DeletePoints/M=2 1,z-1, mz1
	DeletePoints/M=2 0,z-1, mz2
	Redimension/N=(-1,-1) mz1,mz2
	wavetransform/o abs mz1 //将矩阵去绝对值后在进行寻峰（峰值也有可能是最小值）
	wavetransform/o abs mz2 
	peak(mz1)
	wname[position][1]=coef[2]
	wname[position][2]=coef[4]
	peak(mz2)
	wname[position][3]=coef[2]
	wname[position][4]=coef[4]
	//write time value
	wname[position][0]=timevalue*1e9 //单位换算为ns
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
CurveFit/NTHR=0 /Q /N /W=2 Gauss2D kwCWave=coef,  mz[x-10,x+10][y-10,y+10]/D
end

Function Example1()
Variable i
for(i=0;i<5;i+=1)
print i
endfor
End