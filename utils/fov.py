import pymem
from Offsets import *

def main() :
    try :
        pm = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return

    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire la variable button
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 9 :
                inputFOV = line
            if line_nmb >= 10 :
                config_file.close()
                break
            line_nmb = line_nmb + 1
    
    inputFOV = inputFOV.replace("\n", "")
    inputFOV = inputFOV.replace(" ", "")
    inputFOV = int(inputFOV)

    m_iDefaultFOV = (0x332C)

    player = pm.read_int(client + dwLocalPlayer)
    fov = player + m_iDefaultFOV

    if True:
        pm.write_int(fov, inputFOV)

if __name__ == "__main__" :
    main()