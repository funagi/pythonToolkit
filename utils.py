import ctypes,sys

def printc(string='', color='white', end='\n'):
    colormap = {
        'white' : 0x0007,
        'green' : 0x02|0x08,
        'red' : 0x04|0x08
    }

    if color in colormap:
        colorbin = colormap[color]
    else:
        print 'Invalid Color Code!'
        colorbin = colormap[white]

    std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
    bools = ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, colorbin)
    sys.stdout.write(string)
    bools = ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, 0x0007)