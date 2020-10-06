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

    m_iDefaultFOV = (0x332C)

    player = pm.read_int(client + dwLocalPlayer)
    fov = player + m_iDefaultFOV
    default = 90

    if True:
        pm.write_int(fov, default)

if __name__ == "__main__" :
    main()