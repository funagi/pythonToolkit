import ctypes
dll = ctypes.cdll.LoadLibrary('ttp_lrcsh.dll')
#windll
x = ctypes.c_void_p()
c = dll.ttpGetSoundAddIn(x)
print x
print c

print str(c)
