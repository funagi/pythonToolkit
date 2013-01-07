#pragma rtGlobals=1		// Use modern global access method.
Menu "&OOMMF"
	"Import Mz from OOMMF File..." , ImportMz()
End

Function ImportMz()
	// Get folder path
	String S_filename
	Open /D /R /F="OOMMF Field Files (*.o?f):.o?f;" /M="Choose a folder:" refNum
	If( CmpStr(S_filename,"")==0 )
		return 0
	Endif
	String strPath=ParseFilePath(1,S_Filename,":",1,0)
	String strName=ParseFilePath(0,S_Filename,":",1,0)
	NewPath/O/Q Path strPath
	variable Nx,Ny,Nz
	Print S_Filename
	Grep /E="((xnodes|ynodes|znodes): )\d+" /Q /LIST /P=Path strName
	If(V_value==3)
		sscanf S_value, "# xnodes: %d;# ynodes: %d;# znodes: %d;", Nx,Ny,Nz
		LoadWave /A /B="C=1,N='_skip_';C=1,N='_skip_';C=1,N=mz;" /D /G /O /Q /W /P=Path strName
		Redimension/N=(Nx,Ny,Nz) mz
	Endif
	WaveStats mz
End