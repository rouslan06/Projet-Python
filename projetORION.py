###################################################################################
##################### PROJET ORION COMPATIBLE WINDOWS ET MAC ######################
###################################################################################

from tkinter import *
from PIL import Image, ImageTk
from random import randint
import os
import sys                         ################################################
                                   ##           /!\   ATTENTION  /!\             ##
import platform                    ##                                            ##
if platform.system() == 'Darwin':  ##   L'INSTALLATION DU PLUGIN TKMACOSX EST    ##
    from tkmacosx import Button    ##  NECESSAIRE POUR UNE UTILISATION SOUS MAC  ##
                                   ################################################
# creation de la fenetre ORION
root = Tk()
root.title("Projet ORION")

# ajuster l'image 
Largeur, Hauteur = 1030, 600

# je n'autorise pas le redimensionnement
root.resizable(width=False, height=False)

# Creation Canvas
canvas = Canvas(root, width=Largeur, height=Hauteur)
canvas.pack()

######################################
###### PARAMETRAGE DES BOUTONS #######
######################################

def bouton_jour_inactif():
    if (bouton_jour['state'] == NORMAL):bouton_jour['state'] = DISABLED
    else:bouton_jour['state'] = NORMAL
        
def bouton_jour_actif():
    if (bouton_jour['state'] == DISABLED):bouton_jour['state'] = NORMAL
    else:bouton_jour['state'] = DISABLED
        
def bouton_nuit_inactif():
    if (bouton_nuit['state'] == DISABLED):bouton_nuit['state'] = NORMAL
    else:bouton_nuit['state'] = DISABLED
        
def bouton_nuit_actif():
    if (bouton_nuit['state'] == NORMAL):bouton_nuit['state'] = DISABLED
    else:bouton_nuit['state'] = NORMAL

def bouton_animation_ciel_inactif():
    if (rotation_ciel['state'] == NORMAL):rotation_ciel['state'] = DISABLED
    else:rotation_ciel['state'] = NORMAL

def bouton_animation_ciel_actif():
    if (rotation_ciel['state'] == DISABLED):rotation_ciel['state'] = NORMAL
    else:rotation_ciel['state'] = DISABLED
        
def bouton_play_inactif():
    if (bouton_ON['state'] == NORMAL):bouton_ON['state'] = DISABLED
    else:bouton_ON['state'] = NORMAL
        
def bouton_play_actif():
    if (bouton_ON['state'] == DISABLED):bouton_ON['state'] = NORMAL
    else:bouton_ON['state'] = DISABLED
        
def bouton_pause_inactif():
    if (bouton_OFF['state'] == NORMAL):bouton_OFF['state'] = DISABLED
    else:bouton_OFF['state'] = NORMAL
        
######################################
    
def jour():
    canvas.delete('all')
    
    bg_jour = PhotoImage(file='jour.png')
    canvas.create_image(-1, 0, image = bg_jour, anchor = NW)
    
    # fond d'ecran pour le menu
    if platform.system() == 'Darwin': # version MAC
        gris2 = PhotoImage(file='gris.png') 
        gris_menu = canvas.create_image(898, 3, image=gris2, anchor=NW)
    else: # version WINDOWS
        gris2 = PhotoImage(file='gris.png') 
        gris_menu = canvas.create_image(898, 2, image=gris2, anchor=NW)
    
    # importation de nuage
    # nuage = PhotoImage(file='nuage2.png')
    # canvas.create_image(0, 0, image=nuage, anchor = NW)
    
    ville_jour = PhotoImage(file='ville.png') 
    canvas.create_image(451,436,image=ville_jour)
    
    canvas.update()
    
    bouton_jour_inactif()
    bouton_nuit_actif()
    bouton_animation_ciel_inactif()
    bouton_pause_inactif() # fonction bloqué dans jour car entre en conflit (inverse les boutons)
    
    root.mainloop()

def animation_ciel(): # ralentit très fortement l'animation et fait chauffer le CPU
    global i, ciel_nuit
    
    i=i+1
    canvas.delete()
    #canvas.update()
    image = Image.open('sky3.png')
    bg_nuit_2 = ImageTk.PhotoImage(image.rotate(i))
    canvas.create_image(500, 300, image = bg_nuit_2)
    
    canvas.lift(lune) # .lift pour mettre a l'avant
    canvas.lift(etoile)
    canvas.lift(ville_nuit)
    canvas.lift(gris_menu)
    
    canvas.update()
    
    root.after(1, animation_ciel)

def play(): # ca relance le programme pour revenir en mode nuit
            # je viens de me rendre compte qu'une classe __init__() aurait été mieux
    restart = sys.executable
    os.execl(restart, restart, * sys.argv)
    
def pause():
    canvas.delete('all') # On efface tout
    
    # fond d'ecran princial
    if platform.system() == 'Darwin': # version MAC
        gris3 = PhotoImage(file='gris.png') 
        canvas.create_image(3, 3, image=gris3, anchor=NW)
    else: # version WINDOWS
        gris3 = PhotoImage(file='gris.png') 
        canvas.create_image(3, 2, image=gris3, anchor=NW)

    # fond d'ecran pour le menu
    if platform.system() == 'Darwin': # version MAC
        gris2 = PhotoImage(file='gris.png') 
        gris_menu = canvas.create_image(898, 3, image=gris2, anchor=NW)
    else: # version WINDOWS
        gris2 = PhotoImage(file='gris.png') 
        gris_menu = canvas.create_image(898, 2, image=gris2, anchor=NW)   
    
    # text_OFF = Label(root , text='Animation_OFF', font=('Verdana', 15))
    # vtext_OFF.place(x=400, y=250)
    # text_OFF.configure(width=128,height=46)
    
    chat = PhotoImage(file='chat.png') 
    canvas.create_image(425,220,image=chat, anchor=NW)
    
    bouton_jour_inactif()
    bouton_pause_inactif()
    bouton_animation_ciel_inactif()
    bouton_play_actif()
    
    root.mainloop()

def animation(): # fonction incluant lune et etoile pour les faire fonctionner en même temps
    global lune, etoile, xStop, yStop, x_move, y_move, counter, i
   
    # animation de la lune
    # mouvement de la lune si < à largeur sinon supression et re creation
    if canvas.coords(lune)[0]<Largeur:
        canvas.move(lune,5,-1) # orientation du mouvement "x=5,y=-1"
    else:
        canvas.delete(lune)
        lune = canvas.create_image(0, Hauteur/4, image=moon,anchor=NW)
        canvas.update()
        
    counter = counter + 1
    
    # animation de l'etoile
    # creation et mouvement de l'etoile tous les 20 pas sinon supression 
    # et re creation avec coordonnees aleatoires
    if counter > 20:
        if (canvas.coords(etoile)[0]<xStop
        and canvas.coords(etoile)[1]<yStop
        and canvas.coords(etoile)[0]>0
        and canvas.coords(etoile)[1]>0): # delemitation de l'etoile
            
            canvas.move(etoile,x_move,y_move)
        else:
            canvas.delete(etoile)
            counter=0
            # re creation de variables aleatoires
            x0 = randint(0,Largeur-155)
            y0 = randint(0,Hauteur-300)
            xStop = randint(10,Largeur-155)
            yStop = randint(10,Hauteur-300)
            taille = randint(2,5)
            x_move = randint(2,5)
            y_move = randint(2,5)
            # re creation de l'etoile avec des coordonnées nouveaux
            etoile = canvas.create_oval(x0, y0, x0+taille, y0+taille, fill="white")
            
            canvas.lift(gris_menu)
            
            canvas.update()
            
    root.after(30,animation) # delai de l'animation en milliseconde
    
######################################
    
# creation de variables aleatoires
x0 = randint(0,Largeur-155)
y0 = randint(0,Hauteur-300)
xStop = randint(10,Largeur-155)
yStop = randint(10,Hauteur-300)
taille = randint(2,5)
x_move = randint(2,5)
y_move = randint(2,5)

# ajout du ciel en fond
bg_nuit = PhotoImage(file='sky.png')
ciel_nuit = canvas.create_image(0, 0, image = bg_nuit, anchor = NW) # -500, -200

# fond d'ecran pour le menu
if platform.system() == 'Darwin': # version MAC
    gris2 = PhotoImage(file='gris.png') 
    gris_menu = canvas.create_image(898, 3, image=gris2, anchor=NW)
else: # version WINDOWS
    gris2 = PhotoImage(file='gris.png') 
    gris_menu = canvas.create_image(898, 2, image=gris2, anchor=NW)

# importation de la ville
ville = PhotoImage(file='ville.png') 
ville_nuit = canvas.create_image(0, 270, image=ville, anchor=NW) 
                                                   
# importation de l'image de la lune
moon = PhotoImage(file='lune.png')
lune = canvas.create_image(0, Hauteur/4, image=moon, anchor = NW)

# creation de l'etoile
etoile = canvas.create_oval(x0, y0, x0+taille, y0+taille, fill="white")

# creation de fenetres
fenetre1 = canvas.create_oval(680, 300, 684, 305, fill="#b3f0ff")
fenetre2 = canvas.create_oval(669, 344, 673, 349, fill="#b3f0ff")
fenetre3 = canvas.create_oval(710, 315, 714, 320, fill="white")
fenetre4 = canvas.create_oval(435, 400, 439, 405, fill="white")
fenetre5 = canvas.create_oval(415, 410, 419, 415, fill="white")

counter=0 # initialisation de counter à 0 pour le nombre de pas
i=0 # initialisation de l'inclinaison de l'image à 0 degré

# lancement de la fonction
animation()

######################################
############ LES BOUTONS #############
######################################

# les dimensions des boutons seront adaptés suivant
# l'os sur lequel est lancé le programme

if platform.system() == 'Darwin': # version MAC
    
    bouton_jour = Button(
        root,
        text="Jour",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 15),
        command=jour)

    bouton_jour.place(x=913, y=20)
    bouton_jour.config(width=105, height=25)

    bouton_nuit = Button(
        root,
        text="Nuit",
        state=DISABLED,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 15),
        command=play)

    bouton_nuit.place(x=913, y=55)
    bouton_nuit.config(width=105, height=25)

    ######################################

    # ralentit très fortement l'animation et fait chauffer le CPU
    rotation_ciel = Button(
        root,
        text="Ciel (Beta)",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 15),
        command=animation_ciel)

    rotation_ciel.place(x=913, y=105)
    rotation_ciel.config(width=105, height=25)

    ######################################

    bouton_ON = Button(
        root,
        text="PLAY",
        state=DISABLED,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 15),
        command=play)

    bouton_ON.place(x=913, y=160)
    bouton_ON.config(width=105, height=25)

    bouton_OFF = Button(
        root,
        text="PAUSE",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 15),
        command=pause)

    bouton_OFF.place(x=913, y=195)
    bouton_OFF.config(width=105, height=25)

    ######################################

    bouton_quitter = Button(
        root,
        text="Quitter",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 15),
        command=root.destroy)

    bouton_quitter.place(x=913, y=245)
    bouton_quitter.config(width=105, height=25)

else: # version WINDOWS
    
    bouton_jour = Button(
        root,
        text="Jour",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 12),
        command=jour)

    bouton_jour.place(x=913, y=25)
    bouton_jour.config(width=9, height=1)

    bouton_nuit = Button(
        root,
        text="Nuit",
        state=DISABLED,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 12),
        command=play)

    bouton_nuit.place(x=913, y=70)
    bouton_nuit.config(width=9, height=1)

    ######################################

    # ralentit très fortement l'animation et fait chauffer le CPU
    rotation_ciel = Button(
        root,
        text="Ciel (Beta)",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 12),
        command=animation_ciel)

    rotation_ciel.place(x=913, y=130)
    rotation_ciel.config(width=9, height=1)

    ######################################

    bouton_ON = Button(
        root,
        text="PLAY",
        state=DISABLED,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 12),
        command=play)

    bouton_ON.place(x=913, y=190)
    bouton_ON.config(width=9, height=1)

    bouton_OFF = Button(
        root,
        text="PAUSE",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 12),
        command=pause)

    bouton_OFF.place(x=913, y=235)
    bouton_OFF.config(width=9, height=1)

    ######################################

    bouton_quitter = Button(
        root,
        text="Quitter",
        state=NORMAL,
        fg='black',
        bg='#96c0eb',
        font=('comicsans', 12),
        command=root.destroy)
    
    bouton_quitter.place(x=913, y=295)
    bouton_quitter.config(width=9, height=1)
    

root.mainloop()



