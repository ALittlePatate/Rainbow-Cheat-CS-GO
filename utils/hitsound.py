import pymem
import winsound
import time
from Offsets import *

def main() :
    m_totalHitsOnServer = (0xA3A8)

    try :
        pm = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

    while True :
        player = pm.read_int(client + dwLocalPlayer)
        
        hitsound = pm.read_int(player + m_totalHitsOnServer)

        if hitsound > 0:
            pm.write_int(player + m_totalHitsOnServer, 0)

            winsound.PlaySound("sounds/skeet.wav", winsound.SND_FILENAME)

        time.sleep(0.1)
if __name__ == "__main__" :
    main()