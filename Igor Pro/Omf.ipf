#pragma rtGlobals=1		// Use modern global access method.
#include <All Gizmo Procedures>
Menu "&OOMMF"
	"Import OOMMF File...", OpenOMF()
	//"Import Vortex Field File...", ParseOMF()
End

Function deg(mx,my,x,y,degree)
wave mx,my,degree
variable x,y
variable i,j
for(i=0;i<x;i+=1)
	for(j=0;j<y;j+=1)
		if((mx[i][j]==0)&&(my[i][j]==0))
			degree[i][j]=0
		else
			if(my[i][j]>=0)
				degree[i][j]=acos(mx[i][j]/(sqrt(mx[i][j]^2+my[i][j]^2)))
			else
				degree[i][j]=2*Pi-acos(mx[i][j]/(sqrt(mx[i][j]^2+my[i][j]^2)))
			endif
		endif
	endfor
endfor
end

Function ParseDisk(degree,r,x,y)
	wave degree
	Variable r,x,y
	Variable i,j
	For(i=0;i<x;i+=1)
		For(j=0;j<y;j+=1)
			If((i-r)^2+(j-r)^2>(r-1)^2)
				degree[i][j][3]=0
			Endif
		Endfor
	Endfor
End

Function OpenOMF()
	Variable refNum
	String S_path,S_filename
	Open /D /R /F="OOMMF Field Files (*.o?f):.o?f;" /M="Choose an OOMMF File" refNum
	If( CmpStr(S_filename,"")==0 )
		return 0
	Endif
	String /G Filename=ParseFilePath(0,S_Filename,":",1,0)
	String /G Path=ParseFilePath(1,S_Filename,":",1,0)
	ParseOMF()
End

Function ParseOMF()
	String /G Filename,Path
	Variable x,y,z,maxvalue
	NewPath Data Path
	//---------------------Gather infomation from omf file---------------------------
	Grep /E="((xnodes|ynodes|znodes|ValueRangeMaxMag): )\d+" /LIST /P=Data Filename
	If(V_value==4)
		sscanf S_value, "# xnodes: %d;# ynodes: %d;# znodes: %d;# ValueRangeMaxMag: %d;", x,y,z,maxvalue
	Else
		Print "Can't load basic properties from target file."
		return 0
	Endif
	
	If((x==0)||(y==0)||(z==0)||(maxvalue==0))
		sscanf S_value, "# ValueRangeMaxMag: %d;# xnodes: %d;# ynodes: %d;# znodes: %d;", maxvalue,x,y,z
	Endif
	
	If((x==0)||(y==0)||(z==0)||(maxvalue==0))
		Print "Can't load basic properties from target file."
		Print S_value
		return 0
	Endif
	//------------------------Load wave from omf file--------------------------------
	LoadWave /B="C=1,N=mx1;C=1,N=my1;C=1,N=mz1;" /D /G /W /P=Data Filename
	Wave mx2,my2,mz2,mx1,my1,mz1
	//Prompt x, "Enter X size: "
	//Prompt y, "Enter Y size: "
	//Prompt z, "Enter Z size: "
	//Prompt maxvalue, "Enter Saturation Magnetization: "
	//DoPrompt "Enter X, Y, Z and Maximum Magnetization: ", x,y,z,maxvalue
	//-----------------------------------Copy wave-----------------------------------
	duplicate mx1 mx2
	duplicate my1 my2
	duplicate mz1 mz2
	//--------------------------------Normalize waves----------------------------------
	mz1/=maxvalue
	mz2/=maxvalue
	//------------------------------Set wave dimensions--------------------------------
	Redimension/N=(x,y,z) mx1,my1,mz1,mx2,my2,mz2
	DeletePoints/M=2 1,z-1, mx1,my1,mz1
	DeletePoints/M=2 0,z-1, mx2,my2,mz2
	Redimension/N=(-1,-1) mx1,my1,mz1,mx2,my2,mz2
	//-----------------------------Generate degree waves-------------------------------
	make/O/N=(x,y)/D degree1
	make/O/N=(x,y)/D degree2
	deg(mx1,my1,x,y,degree1)
	deg(mx2,my2,x,y,degree2)
	
	//----------------------------------Create Gizmo-----------------------------------
	Execute "NewGizmo/N=Gizmo0"
	Execute "AppendToGizmo DefaultSurface=root:mz1"
	Execute "AppendToGizmo nextSurface=root:mz2"
	//Execute "AppendToGizmo attribute blendFunc={GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA} name=BlendFunc"
	//Execute "ModifyGizmo opName=enableBlend,operation=enable,data=GL_BLEND"
	
	Execute "ModifyGizmo makeColorWave={degree1,rainbowcycle,0}"
	//Execute "degree1_C[][][3]=(degree1[p][q]==0)?(0):(1)"
	ParseDisk(degree1_c,x/2,x,y)
	Execute "ModifyGizmo makeColorWave={degree2,rainbowcycle,0}"
	//Execute "degree2_C[][][3]=(degree2[p][q]==0)?(0):(1)"
	ParseDisk(degree2_c,x/2,x,y)
	Execute "ModifyGizmo ModifyObject=surface0 property={surfaceColorWave,degree1_C}"
	Execute "ModifyGizmo ModifyObject=surface0 property={surfaceColorType,3}"
	Execute "ModifyGizmo ModifyObject=surface1 property={surfaceColorWave,degree2_C}"
	Execute "ModifyGizmo ModifyObject=surface1 property={surfaceColorType,3}"
	Execute "WMGP#AddBlendingToGizmo()"
	Execute "RemoveFromGizmo displayItem=axes0"
	mz2+=2.1
	//-----------------------------Export Current Graph------------------------------------
	Execute "ExportGizmo /P=Path as Filename+\".bmp\""
End