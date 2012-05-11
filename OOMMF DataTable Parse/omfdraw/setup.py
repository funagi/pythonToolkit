# coding = utf-8
import py2exe,sys
from distutils.core import setup

if len(sys.argv)==1:
    sys.argv.append('py2exe')
    
includes = ["encodings", "encodings.*"] 
options = {"py2exe":
    {"compressed": 1, #压缩
    "optimize": 2,
    "ascii": 1,
    "includes":includes,
    "bundle_files": 1 #所有文件打包成一个exe文件 }
    }
}
setup(console=['omfdraw3D.py'],options=options,zipfile = None)
