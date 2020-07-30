import pymem
import re
import time

def main() :
    try :
        pm = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire la variable delay_mh
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 5 :
                delay_mh = line
                delay_mh = float(delay_mh[0:-1])
                delay_mh = delay_mh.replace(" ", "")
            if line_nmb >= 4 :
                config_file.close()
                break
            line_nmb = line_nmb + 1

    
    client = pymem.process.module_from_name(pm.process_handle,
                                            'client.dll')

    clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
    address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',
                                            clientModule).start()

    while True :
        old = str(pm.read_uchar(address))
        pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)
    time.sleep(0.1)

if __name__ == '__main__':
    main()