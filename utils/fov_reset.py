import pymem
import pymem.process
import ctypes
import keyboard
from Offsets import *

def main():
    try :
        pm_memory = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return

    inputFOV = 90
    engine = pymem.process.module_from_name(pm_memory.process_handle, "engine.dll").lpBaseOfDll
    client = pymem.process.module_from_name(pm_memory.process_handle, "client.dll").lpBaseOfDll
    lcbase = pm_memory.read_int(client + dwLocalPlayer)
    c=0
    while c < 3000 :
        pm_memory.write_int(lcbase + m_iFOV, inputFOV)
        c+=1
        
if __name__ == '__main__':
    main()