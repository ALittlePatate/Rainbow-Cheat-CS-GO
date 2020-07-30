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

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire la variable button
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 9 :
                button = line
            if line_nmb >= 10 :
                config_file.close()
                break
            line_nmb = line_nmb + 1
    
    inputFOV = inputFOV.replace("\n", "")
    inputFOV = inputFOV.replace(" ", "")
    inputFOV = int(inputFOV)

    engine = pymem.process.module_from_name(pm_memory.process_handle, "engine.dll").lpBaseOfDll
    client = pymem.process.module_from_name(pm_memory.process_handle, "client.dll").lpBaseOfDll
    lcbase = pm_memory.read_int(client + dwLocalPlayer)

    c = 0
    while c < 3000:
        pm_memory.write_int(lcbase + m_iFOV, inputFOV)
        c+=1

if __name__ == '__main__':
    main()
