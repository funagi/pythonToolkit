# coding = utf-8
import py2exe,sys
from distutils.core import setup


if len(sys.argv)==1:
    sys.argv.append('py2exe')
    
includes = ["encodings", "encodings.*"]
options = {"py2exe":
    {"compressed": 1, #compress
    "optimize": 2,
    "ascii": 1,
    "includes":includes,
    "bundle_files": 1 #pack all files into a single exe }
    }
}
data_files = ["Microsoft.VC90.CRT.manifest","msvcr90.dll"]
setup(console=[{'script':'local.py',"icon_resources" : [(1, "local.ico")]}],
      options=options,
      zipfile = None,
      data_files = data_files
	)
