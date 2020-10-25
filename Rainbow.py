import sys
sys.path.insert(1, 'utils/')
from wallhack import main as wh
from bhop import main as a_bhop
from bhop_legit import main as a_legit_bhop
from triggerbot import main as tg
from noflash import main as nf
from rcs import main as rcs_p
from radar import main as radar
from aimbot import main as ai
from aimbot_rage import main as ai_r
from ragemode import main as rmh
from crosshair_hack import main as ch
from rapidfire import main as rfw
from fov import main as fh
from fov_reset import main as fh_reset
from thirdperson import main as thp_h
from rank_reveal import main as rr
from chams import main as chams
from chams_reset import main as chams_r
from hitsound import main as hitsound
from soundesp import main as soundesp
from silent import main as silent_ai
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from PIL import ImageTk,Image
from multiprocessing import *
import warnings
warnings.simplefilter("ignore")
import threading
import multiprocessing
import ctypes
import os
import pymem
import pymem.process
import keyboard

window = Tk()
first = 1
delay_tg = 0.1
key_tg = "shift"
smooth_ai = 4
key_ai = "f"
fov_ai = 10
fov_fh = 90
thp = "x"
rapidfire_key = "c"
silent_key = "f"
aim_rage = False
bhop_legit = False
rcs_percent = 100

def create_temp_file() :
    os.system("cd configs/ && del temp.temp")
    with open("configs/temp.temp", "a") as c :

        global delay_tg
        global key_tg
        global key_ai
        global smooth_ai
        global fov_ai
        global fov_fh
        global thp
        global rapidfire_key
        global silent_key
        global rcs_percent
        rcs_percent = str(rcs_percent)
        rcs_percent = rcs_percent.replace(" ", "")
        rcs_percent = rcs_percent.replace("\n", "")
        delay_tg = delay_tg.replace(" ", "")
        delay_tg = delay_tg.replace("\n", "")
        key_tg = key_tg.replace(" ", "")
        key_tg = key_tg.replace("\n", "")
        key_ai = key_ai.replace(" ", "")
        key_ai = key_ai.replace("\n", "")
        smooth_ai = smooth_ai.replace(" ", "")
        smooth_ai = smooth_ai.replace("\n", "")
        fov_ai = fov_ai.replace(" ", "")
        fov_ai = fov_ai.replace("\n", "")
        fov_fh = fov_fh.replace(" ", "")
        fov_fh = fov_fh.replace("\n", "")
        thp = thp.replace(" ", "")
        thp = thp.replace("\n", "")
        rapidfire_key = rapidfire_key.replace(" ", "")
        rapidfire_key = rapidfire_key.replace("\n", "")
        silent_key = silent_key.replace("\n", "")
        silent_key = silent_key.replace("\n", "")

        c.write("#Triggerbot\n")
        c.write(str(delay_tg))
        c.write("\n")
        c.write(key_tg)
        c.write("\n")
        c.write("#Aimbot\n")
        c.write(key_ai)
        c.write("\n")
        c.write(str(smooth_ai))
        c.write("\n")
        c.write(str(fov_ai))
        c.write("\n")
        c.write("#FOV\n")
        c.write(str(fov_fh))
        c.write("\n")
        c.write("#Third person\n")
        c.write(str(thp))
        c.write("\n")
        c.write("#Rapid Fire\n")
        c.write(str(rapidfire_key))
        c.write("\n")
        c.write("#RCS\n")
        c.write(str(rcs_percent))
        c.write("\n")
        c.write("#Silent Aim\n")
        c.write(str(silent_key))
        c.close()
    
    f = open("configs/path.txt", "w")
    f.write("temp.temp")
    f.close()

def config_loader() :

    #Création de la fenêtre
    conf_loader = Tk()
    w = 300
    h = 115
    ws = conf_loader.winfo_screenwidth()
    hs = conf_loader.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    conf_loader.geometry('%dx%d+%d+%d' % (w, h, x, y))
    conf_loader.title('Config Loader')
    conf_loader.iconbitmap("images/rainbow.ico")
    conf_loader.config(background='#f0f0f0')

    #Création du texte
    conf_text = StringVar()
    label1 = Label(conf_loader, text = 'Load a config :', font=(40))  #Load a config (titre)
    label1.place(relx=1, x=-190, y=0, anchor=NE)                      #Load a config (titre)
    
    #Création de la liste déroulante pour les fichiers
    folder = "configs/"
    filelist = [fname for fname in os.listdir(folder) if fname.endswith('.cfg')]
    optmenu = ttk.Combobox(conf_loader, values=filelist, state='readonly')
    #global optmenu
    optmenu.place(relx=1, x=-155, y=25, anchor=NE)

    #Création du texte
    bouton2 = Button(conf_loader, text="Load", font=(40), command= lambda: path_writer())     #Load (path writer boutton)
    bouton2.place(relx=1, x=-100, y=20, anchor=NE)                                            #Load (path writer boutton)
    label2 = Label(conf_loader, text = 'Export current config :', font=(40))       #Export the config (titre)
    label2.place(relx=1, x=-145, y=60, anchor=NE)                                  #Export the config (titre)
    label3 = Label(conf_loader, text = 'Export as :', font=(40))                   #Export the config as (titre)
    label3.place(relx=1, x=-221, y=82, anchor=NE)                                  #Export the config as (titre)
    conf_entry = Entry(conf_loader, textvariable = conf_text, width=15)            #Nom de la config (entrée)
    conf_entry.place(relx=1, x=-125, y=85, anchor=NE)                              #Nom de la config (entrée)
    label4 = Label(conf_loader, text = '.cfg', font=(40))                          #.cfg (titre)
    label4.place(relx=1, x=-100, y=82, anchor=NE)                                  #.cfg (titre)
    bouton3 = Button(conf_loader, text="Export", font=(40), command= lambda: export())          #Export (boutton)
    bouton3.place(relx=1, x=-25, y=79, anchor=NE)                                               #Export (boutton)

    def path_writer() :         #Sous programme qui note le chemin d'accès dans configs/path.txt
        config = optmenu.get()
        global config
        f = open("configs/path.txt", "w")
        f.write(config)
        f.close()

        #On met à jour les valeurs en les changeants par celles de la config choisie
        with open("configs/"+config) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 2 :
                    delay_tg = line
                    global delay_tg
                if line_nmb == 3 :
                    key_tg = line[0:-1]
                    global key_tg
                if line_nmb == 5 :
                    key_ai = line
                    global key_ai
                if line_nmb == 6 :
                    smooth_ai = line
                    global smooth_ai
                if line_nmb == 7 :
                    fov_ai = line
                    global fov_ai
                if line_nmb == 9 :
                    fov_fh = line
                    global fov_fh
                if line_nmb == 11 :
                    thp = line
                    global thp
                if line_nmb == 13 :
                    rapidfire_key = line
                    global rapidfire_key
                if line_nmb == 15 :
                    rcs_percent = line
                    global rcs_percent
                if line_nmb == 17 :
                    silent_key = line
                    global silent_key
                if line_nmb >= 18 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
        
        #On met à jour dans les configs
        rcs_print = rcs_percent
        delay_tg_print = delay_tg
        key_tg_print = key_tg
        key_ai_print = key_ai
        smooth_ai_print = smooth_ai
        fov_ai_print = fov_ai
        fov_fh_print = fov_fh
        thp_print = thp
        rapidfire_print = rapidfire_key
        silent_print = silent_key
        global silent_print
        global rcs_print
        global thp_print
        global fov_fh_print
        global fov_ai_print
        global smooth_ai_print
        global key_ai_print
        global delay_tg_print
        global key_tg_print
        global rapidfire_print

        #On met une message box
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Config Loaded !', 'Success', 0)

    def export() :                      #Sous programme qui exporte la configuration actuelle
        conf_name = conf_entry.get()
        with open("configs/"+conf_name+".cfg", "a") as c :

            global delay_tg
            global key_tg
            global key_ai
            global smooth_ai
            global fov_ai
            global fov_fh
            global thp
            global silent_key
            global rapidfire_key
            global rcs_percent
            rcs_percent = rcs_percent.replace(" ", "")
            rcs_percent = rcs_percent.replace("\n", "")
            delay_tg = delay_tg.replace(" ", "")
            delay_tg = delay_tg.replace("\n", "")
            key_tg = key_tg.replace(" ", "")
            key_tg = key_tg.replace("\n", "")
            key_ai = key_ai.replace(" ", "")
            key_ai = key_ai.replace("\n", "")
            smooth_ai = smooth_ai.replace(" ", "")
            smooth_ai = smooth_ai.replace("\n", "")
            fov_ai = fov_ai.replace(" ", "")
            fov_ai = fov_ai.replace("\n", "")
            fov_fh = fov_fh.replace(" ", "")
            fov_fh = fov_fh.replace("\n", "")
            thp = thp.replace(" ", "")
            thp = thp.replace("\n", "")
            rapidfire_key = rapidfire_key.replace(" ", "")
            rapidfire_key = rapidfire_key.replace("\n", "")
            silent_key = silent_key.replace("\n", "")
            silent_key = silent_key.replace(" ", "")

            c.write("#Triggerbot\n")
            c.write(str(delay_tg))
            c.write("\n")
            c.write(key_tg)
            c.write("\n")
            c.write("#Aimbot\n")
            c.write(key_ai)
            c.write("\n")
            c.write(str(smooth_ai))
            c.write("\n")
            c.write(str(fov_ai))
            c.write("\n")
            c.write("#FOV\n")
            c.write(str(fov_fh))
            c.write("\n")
            c.write("#Third person\n")
            c.write(str(thp))
            c.write("\n")
            c.write("#Rapid Fire\n")
            c.write(str(rapidfire_key))
            c.write("\n")
            c.write("#RCS\n")
            c.write(str(rcs_percent))
            c.write("\n")
            c.write("#Silent Aim\n")
            c.write(str(silent_key))
            c.close()

        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Config exported in configs/'+conf_name+'.cfg !', 'Success', 0)

    conf_loader.mainloop()


def aimbot_conf() :

    #Création de la fenêtre
    aimbot_conf = Tk()
    w = 400
    h = 230
    ws = aimbot_conf.winfo_screenwidth()
    hs = aimbot_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    aimbot_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    aimbot_conf.title('Aimbot Configuration')
    aimbot_conf.iconbitmap("images/rainbow.ico")
    aimbot_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    try :
        str(key_ai_print)
    except Exception as e:
        with open("configs/"+path) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 7 :
                    key_ai_print = line[0:-1]
                    global key_ai_print
                if line_nmb == 8 :
                    smooth_ai = line[0:-1]
                    smooth_ai_print = str(smooth_ai)
                    global smooth_ai_print
                if line_nmb == 9 :
                    fov_ai = line[0:-1]
                    fov_ai_print = str(fov_ai)
                    global fov_ai_print
                if line_nmb >= 10 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    
    #Création du texte	
    smooth_ai = " "
    key_ai = "a"
    fov_ai = "b"
    #On crée les variables des couleurs
    green = '#0BFF14'
    red = '#FF0B0B'
    label1 = Label(aimbot_conf, text = 'Smooth value :', font=(40))               #Smooth (titre)
    label1.place(relx=1, x=-290, y=0, anchor=NE)                                  #Smooth (titre)
    label3 = Label(aimbot_conf, text = 'Current value : '+str(smooth_ai_print), font=(40))     #Smooth (current)
    label3.place(relx=1, x=-63, y=0, anchor=NE)                                                #Smooth (current)
    ai_entry = Entry(aimbot_conf, textvariable = smooth_ai, width=25)             #Smooth (entrée)
    ai_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #Smooth (entrée)
    bouton = Button(aimbot_conf, text="Submit", font=(40), command= lambda: aimbot_conf_save_delay(ai_entry, aimbot_conf))              #Smooth (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #Smooth (boutton)
    label2 = Label(aimbot_conf, text = 'Keybind :', font=(40))                #Keybind (titre)
    label2.place(relx=1, x=-330, y=60, anchor=NE)                             #Keybind (titre)
    ai_entry2 = Entry(aimbot_conf, textvariable = key_ai, width=25)           #Keybind (entrée)
    ai_entry2.place(relx=1, x=-243, y=90, anchor=NE)                          #Keybind (entrée)
    label4 = Label(aimbot_conf, text = 'Current value : '+str(key_ai_print), font=(40))                                      #Keybind (current)
    label4.place(relx=1, x=-67, y=65, anchor=NE)                                                                             #Keybind (current)
    bouton2 = Button(aimbot_conf, text="Submit", font=(40), command= lambda: aimbot_conf_save_key(ai_entry2, aimbot_conf))   #Keybind (bouton)
    bouton2.place(relx=1, x=-173, y=85, anchor=NE)                                                                           #Keybind (bouton)
    label5 = Label(aimbot_conf, text = 'FOV :', font=(40))                    #Fov (titre)
    label5.place(relx=1, x=-353, y=125, anchor=NE)                            #Fov (titre)
    ai_entry3 = Entry(aimbot_conf, textvariable = fov_ai, width=25)           #Fov (entrée)
    ai_entry3.place(relx=1, x=-243, y=150, anchor=NE)                         #Fov (entrée)
    label6 = Label(aimbot_conf, text = 'Current value : '+str(fov_ai_print), font=(40))                                      #Fov (current)
    label6.place(relx=1, x=-55, y=125, anchor=NE)                                                                            #Fov (current)
    bouton3 = Button(aimbot_conf, text="Submit", font=(40), command= lambda: aimbot_conf_save_fov(ai_entry3, aimbot_conf))   #Fov (bouton)
    bouton3.place(relx=1, x=-173, y=145, anchor=NE)                                                                          #Fov (bouton)
    if aim_rage == False :
        Aimbot_rage = Button(aimbot_conf, text="Rage on/off", bg=red, fg='#000000', font=(40), command= lambda: Aimbot_rage.configure(background = aimbot_rage(aimbot_conf, green, red, Aimbot_rage))) #Aimbot Rage (button)
        Aimbot_rage.place(relx=1, x=-15, y=190, anchor=NE)   #Aimbot Rage (button)
    if aim_rage == True :
        Aimbot_rage = Button(aimbot_conf, text="Rage on/off", bg=green, fg='#000000', font=(40), command= lambda: Aimbot_rage.configure(background = aimbot_rage(aimbot_conf, green, red, Aimbot_rage))) #Aimbot Rage (button)
        Aimbot_rage.place(relx=1, x=-15, y=190, anchor=NE)   #Aimbot Rage (button)
    
    def aimbot_rage(aimbot_conf, green, red, Aimbot_rage) :
        #Si la couleur du boutton == rouge alors on la change en vert
        #Et vice-versa
        curent_cl = Aimbot_rage.cget('bg')
        if curent_cl == red :
            #On appelle le aimbot
            aim_rage = True
            global aim_rage
            return green
        elif curent_cl == green :
            aim_rage = False
            global aim_rage
            return red

        buttons(window)

    def aimbot_conf_save_fov(ai_entry3, aimbot_conf) :     #On récupère le texte et on fait apparaître une fenêtre
        fov_ai = ai_entry3.get()
        fov_ai_print = fov_ai
        global fov_ai_print
        print("fov")
        print(fov_ai)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour la variable de délai du aimbot
        global fov_ai
        create_temp_file()

    def aimbot_conf_save_delay(ai_entry, aimbot_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        smooth_ai = ai_entry.get()
        smooth_ai_print = smooth_ai
        global smooth_ai_print
        print("smooth")
        print(smooth_ai)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour la variable de délai du aimbot
        global smooth_ai
        create_temp_file()

    def aimbot_conf_save_key(ai_entry2, aimbot_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        key_ai = ai_entry2.get()
        key_ai_print = key_ai
        global key_ai_print
        print("key aimbot")
        print(key_ai)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour la variable de délai du aimbot
        global key_ai
        create_temp_file()

    aimbot_conf.mainloop()

def triggerbot_conf() :

    #Création de la fenêtre
    triggerbot_conf = Tk()
    w = 400
    h = 125
    ws = triggerbot_conf.winfo_screenwidth()
    hs = triggerbot_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    triggerbot_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    triggerbot_conf.title('Triggerbot Configuration')
    triggerbot_conf.iconbitmap("images/rainbow.ico")
    triggerbot_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    try :
        str(key_tg_print)
    except Exception as e:
        with open("configs/"+path) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 2 :
                    delay_tg = line[0:-1]
                    delay_tg_print = str(delay_tg)
                    global delay_tg_print
                if line_nmb == 3 :
                    key_tg_print = line[0:-1]
                    global key_tg_print
                if line_nmb >= 4 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    
    #Création du texte	
    delay_tg = " "
    delay_tg2 = "a"
    label1 = Label(triggerbot_conf, text = 'Delay : (default = 0.1)', font=(40))  #Délai (titre)
    label1.place(relx=1, x=-247, y=0, anchor=NE)                                  #Délai (titre)
    label3 = Label(triggerbot_conf, text = 'Current value : '+str(delay_tg_print), font=(40)) #Délai (current)
    label3.place(relx=1, x=-53, y=0, anchor=NE)                                                #Délai (current)
    tg_entry = Entry(triggerbot_conf, textvariable = delay_tg, width=25)          #Délai (entrée)
    tg_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #Délai (entrée)
    bouton = Button(triggerbot_conf, text="Submit", font=(40), command= lambda: triggerbot_conf_save_delay(tg_entry, triggerbot_conf))  #Délai (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #Délai (boutton)
    label2 = Label(triggerbot_conf, text = 'Keybind :', font=(40))                #Keybind (titre)
    label2.place(relx=1, x=-330, y=60, anchor=NE)                                 #Keybind (titre)
    tg_entry2 = Entry(triggerbot_conf, textvariable = delay_tg2, width=25)        #Keybind (entrée)
    tg_entry2.place(relx=1, x=-243, y=90, anchor=NE)                              #Keybind (entrée)
    label4 = Label(triggerbot_conf, text = 'Current value : '+str(key_tg_print), font=(40)) #Keybind (current)
    label4.place(relx=1, x=-48, y=65, anchor=NE)                                            #Keybind (current)
    bouton2 = Button(triggerbot_conf, text="Submit", font=(40), command= lambda: triggerbot_conf_save_key(tg_entry2, triggerbot_conf))   #Keybind (bouton)
    bouton2.place(relx=1, x=-173, y=85, anchor=NE)                                                                                       #Keybind (bouton)
    

    def triggerbot_conf_save_delay(tg_entry, triggerbot_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        delay_tg = tg_entry.get()
        delay_tg_print = delay_tg
        global delay_tg_print
        print("delay")
        print(delay_tg)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour la variable de délai du Triggerbot
        global delay_tg
        create_temp_file()

    def triggerbot_conf_save_key(tg_entry2, triggerbot_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        key_tg = tg_entry2.get()
        key_tg_print = key_tg
        global key_tg_print
        print("key")
        print(key_tg)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour la variable de délai du Triggerbot
        global key_tg
        create_temp_file()

    triggerbot_conf.mainloop()

def fov_conf() :

    #Création de la fenêtre
    fov_conf = Tk()
    w = 400
    h = 60
    ws = fov_conf.winfo_screenwidth()
    hs = fov_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    fov_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    fov_conf.title('FOV Configuration')
    fov_conf.iconbitmap("images/rainbow.ico")
    fov_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    try :
        str(fov_fh_print)
    except Exception as e:
        with open("configs/"+path) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 11 :
                    fov_fh = line[0:-1]
                    fov_fh_print = str(fov_fh)
                    global fov_fh_print
                if line_nmb >= 12 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    
    #Création du texte	
    fov_fh = " "
    label1 = Label(fov_conf, text = 'FOV :', font=(40))  #FOV (titre)
    label1.place(relx=1, x=-353, y=0, anchor=NE)                                        #FOV (titre)
    label3 = Label(fov_conf, text = 'Current value : '+str(fov_fh_print), font=(40)) #FOV (current)
    label3.place(relx=1, x=-53, y=0, anchor=NE)                                                #FOV (current)
    fh_entry = Entry(fov_conf, textvariable = fov_fh, width=25)          #FOV (entrée)
    fh_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #FOV (entrée)
    bouton = Button(fov_conf, text="Submit", font=(40), command= lambda: fov_conf_save_delay(fh_entry, fov_conf))  #FOV (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #FOV (boutton)

    def fov_conf_save_delay(fh_entry, fov_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        fov_fh = fh_entry.get()
        fov_fh_print = fov_fh
        global fov_fh_print
        print("fh delay")
        print(fov_fh)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour la variable de délai du fov
        global fov_fh
        create_temp_file()

    fov_conf.mainloop()

def thp_conf() :

    #Création de la fenêtre
    thp_conf = Tk()
    w = 400
    h = 60
    ws = thp_conf.winfo_screenwidth()
    hs = thp_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    thp_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    thp_conf.title('Third person Configuration')
    thp_conf.iconbitmap("images/rainbow.ico")
    thp_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    try :
        str(thp_print)
    except Exception as e:
        with open("configs/"+path) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 13 :
                    thp = line[0:-1]
                    thp_print = str(thp)
                    global thp_print
                if line_nmb >= 14 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    
    #Création du texte	
    thp = " "
    label1 = Label(thp_conf, text = 'Keybind :', font=(40))  #Keybind (titre)
    label1.place(relx=1, x=-330, y=0, anchor=NE)                                        #Keybind (titre)
    label3 = Label(thp_conf, text = 'Current value : '+str(thp_print), font=(40)) #Keybind (current)
    label3.place(relx=1, x=-53, y=0, anchor=NE)                                                #Keybind (current)
    thp_entry = Entry(thp_conf, textvariable = thp, width=25)          #Keybind (entrée)
    thp_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #Keybind (entrée)
    bouton = Button(thp_conf, text="Submit", font=(40), command= lambda: thp_conf_save_delay(thp_entry, thp_conf))  #Keybind (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #Keybind (boutton)

    def thp_conf_save_delay(thp_entry, thp_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        thp = thp_entry.get()
        thp_print = thp
        global thp_print
        print("thp keybind")
        print(thp)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour la variable de délai du thirdperson
        global thp
        create_temp_file()

    thp_conf.mainloop()

def rapidfire_conf() :

    #Création de la fenêtre
    rapidfire_conf = Tk()
    w = 400
    h = 60
    ws = rapidfire_conf.winfo_screenwidth()
    hs = rapidfire_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    rapidfire_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    rapidfire_conf.title('Rapid Fire Configuration')
    rapidfire_conf.iconbitmap("images/rainbow.ico")
    rapidfire_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    try :
        str(rapidfire_print)
    except Exception as e:
        with open("configs/"+path) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 13 :
                    rapidfire_key = line[0:-1]
                    rapidfire_print = str(rapidfire_key)
                    global rapidfire_print
                if line_nmb >= 14 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    
    #Création du texte	
    rapidfire_key = " "
    label1 = Label(rapidfire_conf, text = 'Keybind :', font=(40))  #Keybind (titre)
    label1.place(relx=1, x=-330, y=0, anchor=NE)                                        #Keybind (titre)
    label3 = Label(rapidfire_conf, text = 'Current value : '+str(rapidfire_print), font=(40)) #Keybind (current)
    label3.place(relx=1, x=-53, y=0, anchor=NE)                                                #Keybind (current)
    rapidfire_entry = Entry(rapidfire_conf, textvariable = rapidfire_key, width=25)          #Keybind (entrée)
    rapidfire_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #Keybind (entrée)
    bouton = Button(rapidfire_conf, text="Submit", font=(40), command= lambda: rapidfire_conf_save_key(rapidfire_entry, rapidfire_conf))  #Keybind (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #Keybind (boutton)

    def rapidfire_conf_save_key(rapidfire_entry, rapidfire_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        rapidfire_key = rapidfire_entry.get()
        rapidfire_print = rapidfire_key
        global rapidfire_print
        print("rapidfire keybind")
        print(rapidfire_key)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour le keybind du rapidfire
        global rapidfire_key
        create_temp_file()

    rapidfire_conf.mainloop()

def silent_conf() :

    #Création de la fenêtre
    silent_conf = Tk()
    w = 400
    h = 60
    ws = silent_conf.winfo_screenwidth()
    hs = silent_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    silent_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    silent_conf.title('Silent Aim Configuration')
    silent_conf.iconbitmap("images/rainbow.ico")
    silent_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 17 :
                silent_key = line
                silent_key = silent_key.replace(" ", "")
                silent_key = silent_key.replace("\n", "")
                silent_print = str(silent_key)
                global silent_print
            if line_nmb >= 18 :
                config_file.close()
                break
            line_nmb = line_nmb + 1
    
    #Création du texte	
    silent_key = " "
    label1 = Label(silent_conf, text = 'Keybind :', font=(40))  #Keybind (titre)
    label1.place(relx=1, x=-330, y=0, anchor=NE)                                        #Keybind (titre)
    label3 = Label(silent_conf, text = 'Current value : '+str(silent_print), font=(40)) #Keybind (current)
    label3.place(relx=1, x=-53, y=0, anchor=NE)                                                #Keybind (current)
    silent_entry = Entry(silent_conf, textvariable = silent_key, width=25)          #Keybind (entrée)
    silent_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #Keybind (entrée)
    bouton = Button(silent_conf, text="Submit", font=(40), command= lambda: silent_conf_save_key(silent_entry, silent_conf))  #Keybind (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #Keybind (boutton)

    def silent_conf_save_key(silent_entry, silent_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        silent_key = silent_entry.get()
        silent_print = silent_key
        global silent_print
        print("silent aim keybind")
        print(silent_key)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour le keybind du silent aim
        global silent_key
        create_temp_file()

    silent_conf.mainloop()

def test_conf() :

    #Création de la fenêtre
    rcs_conf = Tk()
    w = 400
    h = 60
    ws = rcs_conf.winfo_screenwidth()
    hs = rcs_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    rcs_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    rcs_conf.title('Recoil Control System Configuration')
    rcs_conf.iconbitmap("images/rainbow.ico")
    rcs_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    try :
        str(rcs_print)
    except Exception as e:
        with open("configs/"+path) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 15 :
                    rcs_percent = line
                    rcs_print = str(rcs_percent)
                    global rcs_print
                if line_nmb >= 16 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    
    #Création du texte	
    rcs_percent = " "
    label1 = Label(rcs_conf, text = 'Perfect Percentage :', font=(40))  #Perfect Percentage (titre)
    label1.place(relx=1, x=-250, y=0, anchor=NE)                                        #Perfect Percentage (titre)
    label3 = Label(rcs_conf, text = 'Current value : '+str(rcs_print), font=(40)) #Perfect Percentage (current)
    label3.place(relx=1, x=-53, y=0, anchor=NE)                                                #Perfect Percentage (current)
    rcs_entry = Entry(rcs_conf, textvariable = rcs_percent, width=25)          #Perfect Percentage (entrée)
    rcs_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #Perfect Percentage (entrée)
    bouton = Button(rcs_conf, text="Submit", font=(40), command= lambda: rcs_conf_save_percent(rcs_entry, rcs_conf))  #Perfect Percentage (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #Perfect Percentage (boutton)

    def rcs_conf_save_percent(rcs_entry, rcs_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        rcs_percent = rcs_entry.get()
        rcs_print = rcs_percent
        global rcs_print
        print("rcs percent")
        print(rcs_percent)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour le Perfect Percentage du rcs
        global rcs_percent
        create_temp_file()

    rcs_conf.mainloop()

def rcs_conf() :

    #Création de la fenêtre
    rcs_conf = Tk()
    w = 400
    h = 60
    ws = rcs_conf.winfo_screenwidth()
    hs = rcs_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    rcs_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    rcs_conf.title('Recoil Control System Configuration')
    rcs_conf.iconbitmap("images/rainbow.ico")
    rcs_conf.config(background='#f0f0f0')

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On met à jour les valeurs en les changeants par celles de la config choisie si c'est la première fois dans le programme
    try :
        str(rcs_print)
    except Exception as e:
        with open("configs/"+path) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 15 :
                    rcs_percent = line
                    rcs_print = str(rcs_percent)
                    global rcs_print
                if line_nmb >= 16 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    
    #Création du texte	
    rcs_percent = " "
    label1 = Label(rcs_conf, text = 'Perfect Percentage :', font=(40))  #Perfect Percentage (titre)
    label1.place(relx=1, x=-250, y=0, anchor=NE)                                        #Perfect Percentage (titre)
    label3 = Label(rcs_conf, text = 'Current value : '+str(rcs_print), font=(40)) #Perfect Percentage (current)
    label3.place(relx=1, x=-53, y=0, anchor=NE)                                                #Perfect Percentage (current)
    rcs_entry = Entry(rcs_conf, textvariable = rcs_percent, width=25)          #Perfect Percentage (entrée)
    rcs_entry.place(relx=1, x=-243, y=25, anchor=NE)                               #Perfect Percentage (entrée)
    bouton = Button(rcs_conf, text="Submit", font=(40), command= lambda: rcs_conf_save_percent(rcs_entry, rcs_conf))  #Perfect Percentage (boutton)
    bouton.place(relx=1, x=-173, y=20, anchor=NE)                                                                                       #Perfect Percentage (boutton)

    def rcs_conf_save_percent(rcs_entry, rcs_conf) :    #On récupère le texte et on fait apparaître une fenêtre
        rcs_percent = rcs_entry.get()
        rcs_print = rcs_percent
        global rcs_print
        print("rcs percent")
        print(rcs_percent)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Value updated !', 'Success', 0)

        #On met à jour le Perfect Percentage du rcs
        global rcs_percent
        create_temp_file()

    rcs_conf.mainloop()

def bhop_conf() :
    global bhop_legit
    green = '#0BFF14'
    red = '#FF0B0B'

    #Création de la fenêtre
    bhop_conf = Tk()
    w = 280
    h = 50
    ws = bhop_conf.winfo_screenwidth()
    hs = bhop_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    bhop_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    bhop_conf.title('Bhop Configuration')
    bhop_conf.iconbitmap("images/rainbow.ico")
    bhop_conf.config(background='#f0f0f0')
    
    if bhop_legit == False :
        Bhop_legit_conf = Button(bhop_conf, text="Legit on/off", bg=red, fg='#000000', font=(40), command= lambda: Bhop_legit_conf.configure(background = bhop_legit_color(bhop_conf, green, red, Bhop_legit_conf))) #Aimbot Rage (button)
        Bhop_legit_conf.place(relx=1, x=-100, y=8, anchor=NE)   #Bhop legit (button)
    if bhop_legit == True :
        Bhop_legit_conf = Button(bhop_conf, text="Legit on/off", bg=green, fg='#000000', font=(40), command= lambda: Bhop_legit_conf.configure(background = bhop_legit_color(bhop_conf, green, red, Bhop_legit_conf))) #Aimbot Rage (button)
        Bhop_legit_conf.place(relx=1, x=-100, y=8, anchor=NE)   #Bhop legit (button)
    
    def bhop_legit_color(bhop_conf, green, red, Bhop_legit_conf) :
        #Si la couleur du boutton == rouge alors on la change en vert
        #Et vice-versa
        curent_cl = Bhop_legit_conf.cget('bg')
        if curent_cl == red :
            bhop_legit = True
            global bhop_legit
            return green
        elif curent_cl == green :
            bhop_legit = False
            global bhop_legit
            return red

        buttons(window)

def ragemode_info() :

    #Création de la fenêtre
    rapidfire_conf = Tk()
    w = 400
    h = 60
    ws = rapidfire_conf.winfo_screenwidth()
    hs = rapidfire_conf.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    rapidfire_conf.geometry('%dx%d+%d+%d' % (w, h, x, y))
    rapidfire_conf.title('About the Rage Mode')
    rapidfire_conf.iconbitmap("images/rainbow.ico")
    rapidfire_conf.config(background='#f0f0f0')
    
    #Création du texte	
    label1 = Label(rapidfire_conf, text = 'The Rage Mod is a combo of :', font=(40))                       #info label 1
    label1.place(relx=1, x=-100, y=0, anchor=NE)                                                           #info label 1
    label2 = Label(rapidfire_conf, text = 'The Rage Aimbot + a rage triggerbot', font=(40))              #info label 2
    label2.place(relx=1, x=-75, y=30, anchor=NE)                                                           #info label 2


    rapidfire_conf.mainloop()


def aimbot(window, green, red, Aimbot) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Aimbot.cget('bg')
    if curent_cl == red :
        if aim_rage == False :
            #On appelle le aimbot
            multiprocessing.freeze_support()
            t_ai = Process(target = ai)
            global t_ai
            t_ai.start()
        if aim_rage == True :
            multiprocessing.freeze_support()
            t_ai_r = Process(target = ai_r)
            global t_ai_r
            t_ai_r.start()
        return green
    elif curent_cl == green :
        try :
            t_ai.terminate()
        except :
            pass
        try :
            t_ai_r.terminate()
        except :
            pass
        return red

    buttons(window)

def wallhack(window, green, red, Wallhack) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Wallhack.cget('bg')
    if curent_cl == red :
        #On appelle le wallhack
        multiprocessing.freeze_support()
        t_wh = Process(target = wh)
        global t_wh
        t_wh.start()
        return green
    elif curent_cl == green :
        t_wh.terminate()
        return red

    buttons(window)

def hitsound_func(window, green, red, Hitsound) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Hitsound.cget('bg')
    if curent_cl == red :
        #On appelle le Hitsound
        multiprocessing.freeze_support()
        t_hitsound = Process(target = hitsound)
        global t_hitsound
        t_hitsound.start()
        return green
    elif curent_cl == green :
        t_hitsound.terminate()
        return red

    buttons(window)

def soundesp_func(window, green, red, SoundEsp) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = SoundEsp.cget('bg')
    if curent_cl == red :
        #On appelle le SoundEsp
        multiprocessing.freeze_support()
        t_soundesp = Process(target = soundesp)
        global t_soundesp
        t_soundesp.start()
        return green
    elif curent_cl == green :
        t_soundesp.terminate()
        return red

    buttons(window)

def test(window, green, red, Test) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Test.cget('bg')
    if curent_cl == red :
        #On appelle le SoundEsp
        multiprocessing.freeze_support()
        t_soundesp = Process(target = soundesp)
        global t_soundesp
        t_soundesp.start()
        return green
    elif curent_cl == green :
        t_soundesp.terminate()
        return red

    buttons(window)


def silentaim_func(window, green, red, SilentAim) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = SilentAim.cget('bg')
    if curent_cl == red :
        #On appelle le SilentAim
        multiprocessing.freeze_support()
        t_silent = Process(target = silent_ai)
        global t_silent
        t_silent.start()
        return green
    elif curent_cl == green :
        t_silent.terminate()
        return red

    buttons(window)

def chams_func(window, green, red, Chams) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Chams.cget('bg')
    if curent_cl == red :
        #On appelle le Chams
        try :
            t_chams_r.terminate()
        except :
            pass
        multiprocessing.freeze_support()
        t_chams = Process(target = chams)
        global t_chams
        t_chams.start()
        return green
    elif curent_cl == green :
        t_chams.terminate()

        multiprocessing.freeze_support()
        t_chams_r = Process(target = chams_r)
        global t_chams_r
        t_chams_r.start()

        return red

    buttons(window)

def fov(window, green, red, FOV) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = FOV.cget('bg')
    if curent_cl == red :
        #On appelle le fov
        try :
            t_fh_r.terminate()
        except :
            pass
        multiprocessing.freeze_support()
        t_fh = Process(target = fh)
        global t_fh
        t_fh.start()
        return green
    elif curent_cl == green :
        t_fh.terminate()

        multiprocessing.freeze_support()
        t_fh_r = Process(target = fh_reset)
        global t_fh_r
        t_fh_r.start()

        return red

    buttons(window)

def bhop(window, green, red, Bhop) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Bhop.cget('bg')
    if curent_cl == red :
        if bhop_legit == False :
            #On appelle le bhop
            multiprocessing.freeze_support()
            t_bhop = Process(target = a_bhop)
            global t_bhop
            t_bhop.start()
        if bhop_legit == True :
            multiprocessing.freeze_support()
            t_bhop_l = Process(target = a_legit_bhop)
            global t_bhop_l
            t_bhop_l.start()
        return green
    elif curent_cl == green :
        try :
            t_bhop.terminate()
        except :
            pass
        try :
            t_bhop_l.terminate()
        except :
            pass
        return red

    buttons(window)

def triggerbot(window, green, red, Triggerbot) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Triggerbot.cget('bg')
    if curent_cl == red :
        #On appelle le triggerbot
        multiprocessing.freeze_support()
        t_triggerbot = Process(target = tg)
        global t_triggerbot
        t_triggerbot.start()
        return green
    elif curent_cl == green :
        t_triggerbot.terminate()
        return red

    buttons(window)

def noflash(window, green, red, Noflash) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = Noflash.cget('bg')
    if curent_cl == red :
        #On appelle le noflash
        multiprocessing.freeze_support()
        t_noflash = Process(target = nf)
        global t_noflash
        t_noflash.start()
        return green
    elif curent_cl == green :
        t_noflash.terminate()
        return red

    buttons(window)

def rcs(window, green, red, RCS) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = RCS.cget('bg')
    if curent_cl == red :
        #On appelle le rcs
        multiprocessing.freeze_support()
        t_rcs = Process(target = rcs_p)
        global t_rcs
        t_rcs.start()
        return green
    elif curent_cl == green :
        t_rcs.terminate()
        return red

    buttons(window)

def rapidfire(window, green, red, RapidFire) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = RapidFire.cget('bg')
    if curent_cl == red :
        #On appelle le rcs
        multiprocessing.freeze_support()
        t_rapidfire = Process(target = rfw)
        global t_rapidfire
        t_rapidfire.start()
        return green
    elif curent_cl == green :
        t_rapidfire.terminate()
        return red

    buttons(window)

def ragemode(window, green, red, RageMode) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = RageMode.cget('bg')
    if curent_cl == red :
        #On appelle le rcs
        multiprocessing.freeze_support()
        t_ragemod = Process(target = rmh)
        global t_ragemod
        t_ragemod.start()
        return green
    elif curent_cl == green :
        t_ragemod.terminate()
        return red

    buttons(window)

def radarhack(window, green, red, RadarHack) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = RadarHack.cget('bg')
    if curent_cl == red :
        #On appelle le radar hack
        multiprocessing.freeze_support()
        t_radar = Process(target = radar)
        global t_radar
        t_radar.start()
        return green
    elif curent_cl == green :
        t_radar.terminate()
        return red

    buttons(window)

def moneyhack(window, green, red, MoneyHack) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = MoneyHack.cget('bg')
    if curent_cl == red :
        client = pymem.process.module_from_name(pm.process_handle, "client.dll")
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',clientModule).start()
        pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)
        return green
    elif curent_cl == green :
        client = pymem.process.module_from_name(pm.process_handle, "client.dll")
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',clientModule).start()
        pm.write_uchar(address, 000 if pm.read_uchar(address) == 0x75 else 0x75)
        return red

    buttons(window)

def crosshairhack(window, green, red, CrosshairHack) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = CrosshairHack.cget('bg')
    if curent_cl == red :
        #On appelle le crosshairHack
        multiprocessing.freeze_support()
        t_ch = Process(target = ch)
        global t_ch
        t_ch.start()
        return green
    elif curent_cl == green :
        t_ch.terminate()
        return red

    buttons(window)

def thp_w(window, green, red, THP) :

    #Si la couleur du boutton == rouge alors on la change en vert
    #Et vice-versa
    curent_cl = THP.cget('bg')
    if curent_cl == red :
        #On appelle le third person
        multiprocessing.freeze_support()
        t_thp = Process(target = thp_h)
        global t_thp
        t_thp.start()
        return green
    elif curent_cl == green :
        t_thp.terminate()
        return red

    buttons(window)



def mainmenu(window, first) :

    #On essaye de trouver le processus csgo.exe 
    try :
        pm = pymem.Pymem("csgo.exe")
        global pm
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)  
        sys.exit()

    #aaa
    with open("configs/path.txt") as f :
        try :
            path = f.readline()
        except :
            path = "default.cfg"
        f.close()

    try :
        #On met à jour les valeurs en les changeants par celles de la config choisie
        with open("configs/"+config) as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 2 :
                    delay_tg = line
                    global delay_tg
                if line_nmb == 3 :
                    key_tg = line[0:-1]
                    global key_tg
                if line_nmb == 5 :
                    key_ai = line
                    global key_ai
                if line_nmb == 6 :
                    smooth_ai = line
                    global smooth_ai
                if line_nmb == 7 :
                    fov_ai = line
                    global fov_ai
                if line_nmb == 9 :
                    fov_fh = line
                    global fov_fh
                if line_nmb == 11 :
                    thp = line
                    global thp
                if line_nmb == 13 :
                    rapidfire_key = line
                    global rapidfire_key
                if line_nmb == 15 :
                    rcs_percent = line
                    global rcs_percent
                if line_nmb == 17 :
                    silent_key = line
                    global silent_key
                if line_nmb >= 18 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
    except :
        with open("configs/default.cfg") as config_file :
            line_nmb = 1
            for line in config_file :
                if line_nmb == 2 :
                    delay_tg = line
                    global delay_tg
                if line_nmb == 3 :
                    key_tg = line[0:-1]
                    global key_tg
                if line_nmb == 5 :
                    key_ai = line
                    global key_ai
                if line_nmb == 6 :
                    smooth_ai = line
                    global smooth_ai
                if line_nmb == 7 :
                    fov_ai = line
                    global fov_ai
                if line_nmb == 9 :
                    fov_fh = line
                    global fov_fh
                if line_nmb == 11 :
                    thp = line
                    global thp
                if line_nmb == 13 :
                    rapidfire_key = line
                    global rapidfire_key
                if line_nmb == 15 :
                    rcs_percent = line
                    global rcs_percent
                if line_nmb == 17 :
                    silent_key = line
                    global silent_key
                if line_nmb >= 18 :
                    config_file.close()
                    break
                line_nmb = line_nmb + 1
        
    #On met à jour dans les configs
    rcs_print = rcs_percent
    delay_tg_print = delay_tg
    key_tg_print = key_tg
    key_ai_print = key_ai
    smooth_ai_print = smooth_ai
    fov_ai_print = fov_ai
    fov_fh_print = fov_fh
    thp_print = thp
    rapidfire_print = rapidfire_key
    silent_print = silent_key
    global silent_print
    global rcs_print
    global thp_print
    global fov_fh_print
    global fov_ai_print
    global smooth_ai_print
    global key_ai_print
    global delay_tg_print
    global key_tg_print
    global rapidfire_print
    

    #On crée les variables des couleurs
    green = '#0BFF14'
    red = '#FF0B0B'

    #On paramètre la fenêtre
    w = 1000
    h = 400
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight() 
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.title('Rainbow Cheat V4.04 by ALittlePatate')
    window.iconbitmap("images/rainbow.ico")
    window.config(background='#fcfefc')

    #On met le nom du menu en haut
    if first == 1 :
        label_title = Label(window, text=("Rainbow Cheat"), bg='#fcfefc', fg='#000000', font=(40)) 
        label_title.pack()
    else :
        pass

    #On met le fond d'écran
    if first == 1 :
        canvas=Canvas(window,width=300,height=300,highlightthickness=0)
        image=ImageTk.PhotoImage(Image.open("images/bg.gif"))
        canvas.create_image(0,0, anchor=NW, image=image)
        canvas.place(x=20, y=20)
    else :
        pass
    
    buttons(window)

def buttons(window) :
    
    #On définit les couleurs utilisées
    green = '#0BFF14'
    red = '#FF0B0B'

    #On place les bouttons

    #Aimbot
    Aimbot = Button(window, text="Aimbot", bg=red, fg='#000000', font=(40), command= lambda: Aimbot.configure(background = aimbot(window, green, red, Aimbot)))
    Aimbot.place(relx=1, x=-620, y=100, anchor=NE)
    #Config du Aimbot
    Aimbot_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: aimbot_conf())
    Aimbot_conf.place(relx=1, x=-680, y=100, anchor=NE)

    #Wallhack
    Wallhack = Button(window, text="Wallhack", bg=red, fg='#000000', font=(40), command= lambda: Wallhack.configure(background = wallhack(window, green, red, Wallhack)))
    Wallhack.place(relx=1, x=-497, y=100, anchor=NE)

    #Bhop
    Bhop = Button(window, text="Auto Bhop", bg=red, fg='#000000', font=(40), command= lambda: Bhop.configure(background = bhop(window, green, red, Bhop)))
    Bhop.place(relx=1, x=-620, y=150, anchor=NE)
    #Config du Bhop
    Bhop_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: bhop_conf())
    Bhop_conf.place(relx=1, x=-705, y=150, anchor=NE)

    #Triggerbot
    Triggerbot = Button(window, text="Triggerbot", bg=red, fg='#000000', font=(40), command= lambda: Triggerbot.configure(background = triggerbot(window, green, red, Triggerbot)))
    Triggerbot.place(relx=1, x=-435, y=150, anchor=NE)
    #Config du Triggerbot
    Triggerbot_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: triggerbot_conf())
    Triggerbot_conf.place(relx=1, x=-515, y=150, anchor=NE)

    #Noflash
    Noflash = Button(window, text="Noflash", bg=red, fg='#000000', font=(40), command= lambda: Noflash.configure(background = noflash(window, green, red, Noflash)))
    Noflash.place(relx=1, x=-620, y=200, anchor=NE)

    #RCS
    RCS = Button(window, text="RCS", bg=red, fg='#000000', font=(40), command= lambda: RCS.configure(background = rcs(window, green, red, RCS)))
    RCS.place(relx=1, x=-470, y=250, anchor=NE)
    #Config du RCS
    RCS_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: rcs_conf())
    RCS_conf.place(relx=1, x=-515, y=250, anchor=NE)

    #Radar Hack
    RadarHack = Button(window, text="RadarHack", bg=red, fg='#000000', font=(40), command= lambda: RadarHack.configure(background = radarhack(window, green, red, RadarHack)))
    RadarHack.place(relx=1, x=-620, y=250, anchor=NE)

    #Money Hack
    MoneyHack = Button(window, text="Show Money", bg=red, fg='#000000', font=(40), command= lambda: MoneyHack.configure(background = moneyhack(window, green, red, MoneyHack)))
    MoneyHack.place(relx=1, x=-472, y=200, anchor=NE)

    #Crosshair Hack
    CrosshairHack = Button(window, text="Crosshair Hack", bg=red, fg='#000000', font=(40), command= lambda: CrosshairHack.configure(background = crosshairhack(window, green, red, CrosshairHack)))
    CrosshairHack.place(relx=1, x=-620, y=300, anchor=NE)

    #FOV
    FOV = Button(window, text="FOV", bg=red, fg='#000000', font=(40), command= lambda: FOV.configure(background = fov(window, green, red, FOV)))
    FOV.place(relx=1, x=-470, y=300, anchor=NE)
    #Config du FOV
    FOV_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: fov_conf())
    FOV_conf.place(relx=1, x=-515, y=300, anchor=NE)

    #3p
    THP = Button(window, text="Third person", bg=red, fg='#000000', font=(40), command= lambda: THP.configure(background = thp_w(window, green, red, THP)))
    THP.place(relx=1, x=-225, y=100, anchor=NE)
    #Config du 3p
    THP_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: thp_conf())
    THP_conf.place(relx=1, x=-325, y=100, anchor=NE)

    #Rapid Fire
    RapidFire = Button(window, text="Rapid Fire", bg=red, fg='#000000', font=(40), command= lambda: RapidFire.configure(background = rapidfire(window, green, red, RapidFire)))
    RapidFire.place(relx=1, x=-240, y=150, anchor=NE)
    #Config du Rapid Fire
    RapidFire_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: rapidfire_conf())
    RapidFire_conf.place(relx=1, x=-325, y=150, anchor=NE)

    #Rage Mode
    RageMode = Button(window, text="Rage Mode", bg=red, fg='#000000', font=(40), command= lambda: RageMode.configure(background = ragemode(window, green, red, RageMode)))
    RageMode.place(relx=1, x=-255, y=200, anchor=NE)
    #Config du Rage Mode
    RageMode_info = Button(window, text="Info", fg='#000000', font=(40), command= lambda: ragemode_info())
    RageMode_info.place(relx=1, x=-348, y=200, anchor=NE)

    #Rank Reveal
    Rank_Reveal = Button(window, text="Rank Reveal", bg="#d96a21", fg='#000000', font=(40), command= lambda: rr())
    Rank_Reveal.place(relx=1, x=-283, y=250, anchor=NE)

    #Chams
    Chams = Button(window, text="Chams", bg=red, fg='#000000', font=(40), command= lambda: Chams.configure(background = chams_func(window, green, red, Chams)))
    Chams.place(relx=1, x=-322, y=300, anchor=NE)

    #Hitsound
    Hitsound = Button(window, text="Hitsound", bg=red, fg='#000000', font=(40), command= lambda: Hitsound.configure(background = hitsound_func(window, green, red, Hitsound)))
    Hitsound.place(relx=1, x=-100, y=100, anchor=NE)

    #Sound Esp
    SoundEsp = Button(window, text="Sound Esp", bg=red, fg='#000000', font=(40), command= lambda: SoundEsp.configure(background = soundesp_func(window, green, red, SoundEsp)))
    SoundEsp.place(relx=1, x=-85, y=150, anchor=NE)

    #Silent Aim
    SilentAim = Button(window, text="Silent Aim", bg=red, fg='#000000', font=(40), command= lambda: SilentAim.configure(background = silentaim_func(window, green, red, SilentAim)))
    SilentAim.place(relx=1, x=-35, y=200, anchor=NE)
    #Config Silent Aim
    SilentAim_conf = Button(window, text="Config", fg='#000000', font=(40), command= lambda: silent_conf())
    SilentAim_conf.place(relx=1, x=-118, y=200, anchor=NE)

    #Config Loader
    Config_loader = Button(window, text="Configs", font=(40), command= lambda: config_loader())
    Config_loader.place(relx=1, x=-925, y=360, anchor=NE)

    window.mainloop()

if __name__ == '__main__':
    freeze_support()
    mainmenu(window, first)
