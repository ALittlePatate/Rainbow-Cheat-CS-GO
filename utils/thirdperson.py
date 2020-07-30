import keyboard
import ctypes
import time
import pymem
import pymem.process
from Offsets import *

thirdperson = True

def main():
    try :
        pm_memory = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return
    
    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire la variable button
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 11 :
                button = line
            if line_nmb >= 12 :
                config_file.close()
                break
            line_nmb = line_nmb + 1
    
    button = button.replace("\n", "")
    button = button.replace(" ", "")

    engine = pymem.process.module_from_name(pm_memory.process_handle, "engine.dll").lpBaseOfDll
    client = pymem.process.module_from_name(pm_memory.process_handle, "client.dll").lpBaseOfDll
    lcbase = pm_memory.read_int(client + dwLocalPlayer)
    while True :
        if keyboard.is_pressed(button) :
            pm_memory.write_int(lcbase + m_iObserverMode, 1)
        if not keyboard.is_pressed(button) :
            pm_memory.write_int(lcbase + m_iObserverMode, 0)

if __name__ == '__main__':
    main()
