import pygame as p
import math
import time
import json
import random
import re

File_Name0 = "pythonApp/Data/AI_data_for_stat_Map0.json"#"IA_data_Better_Score.json"#"AI_data.json"  
File_Name1 = "pythonApp/Data/AI_data_for_stat_Map1.json"
File_Name10 = "pythonApp/Data/AI_data_for_stat_Map1(0).json"
File_Name01 = "pythonApp/Data/AI_data_for_stat_Map0(1).json"

Map = input("Map ?") # -------- Input utilisateur ---------------

File_Name = False
while not File_Name:
    File = input("File : 0, 1, 01, 10 ?") # ------ Pas besoin --------

    if File == "0":
        File_Name = File_Name0
    elif File == "1":
        File_Name = File_Name1
    elif File == "01":
        File_Name = File_Name01
    elif File == "10":
        File_Name = File_Name10

Temps_gen = random.randint(20, 30)

p.init()

def writeData(nerroneData, gen, i, score, parent, tempGen, nbCheck, tempsLastCheck): # liste, gen, i(le 1 est le meilleurs, le 2 le deuxième, ect et le 11 les meilleurs de ce qui ce sont crach(et s'il y en a pas c'est 0.0 pour tout))
    with open(File_Name, "r") as f:
        nerrone = json.load(f)

    if gen not in nerrone:
        nerrone[gen] = []

    with open(File_Name, "w") as f:
        newNerrone = nerroneData
        newData = {"nb" : i, "score" : score, "parents": parent, "TimeGen": tempGen, "tempsLastCheck": tempsLastCheck, "nbCheckpoint": nbCheck, "nerrone": newNerrone}
        nerrone[gen].append(newData)
        nerrone = json.dumps(nerrone, indent=4)
        data = re.sub(r'\[\s+([-?\d.,\s]+)\s+\]', lambda match: f"[{', '.join(match.group(1).split())}]", nerrone)
        data = data.replace(",,", ",").replace("[,", "[")
        f.write(data)

def readData(gen, i, file): 
    with open(file, "r") as f:
        nerrone = json.load(f)
    return nerrone[gen][i] # mettre ["nerrone"] pour le résaux de nerrone 

def get_File(file): 
    with open(file, "r") as f:
        nerrone = json.load(f)
    return nerrone # retourne tout le fichier pour s'en servir sans faire de request à chaque utilisation !

with open(File_Name, "r") as f:
    nerrone = json.load(f)
    nb_gen = len(nerrone)

screen = p.display.set_mode((800, 600))
delay_capteur = 0.5
old_time = time.time()
clock = p.time.Clock()
if Map == "0":
    bg =  p.image.load("pythonApp/img/Background.png").convert()
elif Map == "3":
    bg = p.image.load("pythonApp/img/Background3.png").convert()
else:
    bg =  p.image.load("pythonApp/img/Background1.png").convert() #--------------------------------
checkpoint = p.image.load("pythonApp/img/Checkpoint.png").convert_alpha()

if Map == 0:
    checkpoint_order = [[66, 350, 0],
                    [66, 300, 0],
                    [66, 250, 0],
                    [65, 200, 20],
                    [56, 156, -10],
                    [110, 130, -80],
                    [140, 126, -90],
                    [170, 138, 215],
                    [190, 169, 17],
                    [189, 215, -5],
                    [183, 266, 0],
                    [192, 317, 20],
                    [240, 360, 70],
                    [285, 363, 90],
                    [330, 363, 90],
                    [390, 335, 130],
                    [409, 300, -25],
                    [387, 242, 45],
                    [335, 207, 50],
                    [288, 155, 0],
                    [325, 125, -62],
                    [370, 115, 90],
                    [420, 115, 90],
                    [470, 115, 90],
                    [520, 115, 90],
                    [570, 115, 90],
                    [620, 110, 90],
                    [660, 120, 62],
                    [678, 150, 10],
                    [660, 192, -60],
                    [611, 210, -60],
                    [575, 236, -23],
                    [572, 278, 25],
                    [624, 320, 65],
                    [677, 338, 65],
                    [713, 380, 0],
                    [710, 410, -30],
                    [690, 445, -50],
                    [625, 470, 95],
                    [568, 425, 35],
                    [535, 400, 90],
                    [509, 412, 138],
                    [490, 435, 145],
                    [475, 465, 155],
                    [465, 515, 135],
                    [410, 525, 90],
                    [330, 500, 40],
                    [290, 500, 135],
                    [255, 513, 95],
                    [210, 526, 90],
                    [160, 526, 90],
                    [80, 523, 45],
                    [66, 450, 0],
                    [66, 400, 0]
                ]
else:
    checkpoint_order = [[120, 368, 320],
                        [155, 210, 45],
                        [155, 130, 90],
                        [415, 115, 90],
                        [580, 165, 45],
                        [590, 310, 315],
                        [590, 395, 45],
                        [370, 530, 90],
                        [112, 500, 45]
    ]                 


def Checkpoint(car, checkpoint):
    if car.checkpoint_nb <= len(checkpoint_order):
        checkpoint_return = p.transform.rotate(checkpoint, checkpoint_order[car.checkpoint_nb-1][2])
    else:
        car.checkpoint_nb = 1
        checkpoint_return = p.transform.rotate(checkpoint, checkpoint_order[car.checkpoint_nb-1][2])
    rect_o = checkpoint.get_rect(topleft=(checkpoint_order[car.checkpoint_nb-1][0], checkpoint_order[car.checkpoint_nb-1][1]))
    rect = checkpoint_return.get_rect(center=rect_o.center)
    car.rect = car.image.get_rect(center=(car.x, car.y))
    #screen.blit(checkpoint_return, rect.topleft)
    mask1 = p.mask.from_surface(car.image)
    mask2 = p.mask.from_surface(checkpoint_return)
    offset = (rect.x - car.rect.x, rect.y - car.rect.y)
    if mask1.overlap(mask2, offset):
        car.nbCheckpointPass += 1
        car.checkpoint_time = time.time()
        if car.checkpoint_nb != len(checkpoint_order):
            car.checkpoint_nb += 1
        else:
            car.checkpoint_nb = 1


class car:
    def __init__(self, nb):
        self.TimeLast = 0
        self.Parent = 0
        self.checkpoint_time = time.time()
        data_color = nb % 10
        self.car = data_color + 1
        self.crach = False
        self.score = 0
        self.timeStart = 0 # mettre time.time()
        self.EndTrain = False
        self.checkpoint_nb = 1
        self.nbCheckpointPass = 0
        self.image = p.image.load("pythonApp/img/Car"+str(self.car)+".png")
        if Map == "0":
            self.x = 95
            self.y = 410
        else:
            self.x = 129 #220
            self.y = 390 #300
        self.direction = 0
        self.nb = nb
        self.CurentSpeed = 0
        self.MaxSpeed = 5
        self.capteurMaxDist = 100
        self.data = []
        self.image_origin = p.image.load("pythonApp/img/Car"+str(self.car)+".png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def avancer(self, vitesse): # -1 < vitesse < 1
        if self.CurentSpeed > vitesse:
            vitesse_M = self.CurentSpeed - 0.2
            if vitesse_M < vitesse:
                vitesse_M = vitesse
        elif self.CurentSpeed < vitesse:
            vitesse_M = self.CurentSpeed + 0.05
            if vitesse_M > vitesse:
                vitesse_M = vitesse
        else:
            vitesse_M = self.CurentSpeed
        self.CurentSpeed = vitesse_M
        self.rect = self.image.get_rect(center=(self.x+5, self.y+10))

    def tourner(self, puissance): # -10 < puissance < 10
        if self.direction + puissance < 270 and self.direction + puissance > -90:
            self.direction += puissance
        else:
            if self.direction + puissance > 270:
                self.direction = self.direction + puissance - 360
            else:
                self.direction = self.direction + puissance + 360
        self.image = p.transform.rotate(self.image_origin, -self.direction)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        

    def capteurs(self):
        self.data = []
        t = math.radians(self.direction)
        Lx = -1
        Ly = -8
        def create_captor(change, dif):
            origin_x = self.x + (Lx+dif)*math.cos(t) - (Ly+1)*math.sin(t)
            origin_y = self.y + (Lx+dif)*math.sin(t) + (Ly+1)*math.cos(t)

            step_x = math.sin((self.direction+change)*math.pi/180)
            step_y = math.cos((self.direction+change)*math.pi/180)
            #origin_x = self.x + 5#*math.sin((self.direction)*math.pi/180)
            #origin_y = self.y + 2#*math.cos((self.direction)*math.pi/180)
            #p.draw.line(screen, (255, 0, 0), (origin_x, origin_y), (origin_x + step_x*self.capteurMaxDist, origin_y - step_y*self.capteurMaxDist), 2)
            for i in range(self.capteurMaxDist):
                try:
                    pixel = bg.get_at((round(origin_x+i*step_x), round(origin_y-i*step_y)))
                    if pixel == (181, 230, 29, 255) or pixel == (34, 177, 76, 255):
                        self.data.append(i/self.capteurMaxDist)
                        return
                except IndexError:
                    self.data.append(0.0)
                    return
            self.data.append(1.0)
        create_captor(-40, -6)
        create_captor(-20, -2)
        create_captor(0, 0)
        create_captor(20, 2)
        create_captor(40, 6)

    def score_cal(self):
        self.TimeLast = (time.time() - self.checkpoint_time)
        self.score = self.nbCheckpointPass*1000 + self.TimeLast
        self.Parent = cars.index(self) % 10


def SaveBestCar(cars):
    global nb_gen
    score = {}
    best_crach = [0, 0]
    nb_crach = 0
    for car in cars:
        if car.crach == False:
            score[cars.index(car)] = car.score
        else:
            nb_crach += 1
            if car.score > best_crach[1]:
                best_crach[0] = cars.index(car)
                best_crach[1] = car.score
    scores_tries = sorted(score.items(), key=lambda item: item[1], reverse=True)  #Trie 
    if len(scores_tries) < 10:
        if len(scores_tries) == 0:
            for i in range(10):
                scores_tries.append([best_crach[0], best_crach[1]])
        else:
            for i in range(10-len(scores_tries)):
                scores_tries.append([scores_tries[0][0], 0]) #pour voir que c'est une recup à cause des crach 
    scores_tries = scores_tries[:10]  #garde les 10 premières
    i = 0
    for data in scores_tries:
        writeData(dataRun[data[0]], str(nb_gen), i, data[1], cars[data[0]].Parent, Temps_gen, cars[data[0]].nbCheckpointPass, cars[data[0]].TimeLast)
        i += 1
    writeData(dataRun[best_crach[0]], str(nb_gen), 10, best_crach[1], cars[best_crach[0]].Parent, Temps_gen, cars[best_crach[0]].nbCheckpointPass, cars[best_crach[0]].TimeLast)
    return start(50)

        
    


def Train_AI(car, nerrone):
    if car.EndTrain == False:
        car.y -= (car.CurentSpeed*3)*math.sin((car.direction+90)*math.pi/180)
        car.x -= (car.CurentSpeed*3)*math.cos((car.direction+90)*math.pi/180)
        car.capteurs()
        Input = car.data
        output = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0]]
        for k in range(len(nerrone)):
            for j in range(len(output[k])):
                if k == 0:
                    for i in range(len(Input)):
                        if k == 0:
                            output[k][j] += Input[i] * nerrone[k][i][j]
                        elif k == 1:
                            output[k][j] += output[k-1][i] * nerrone[k][i][j]    
                else:
                    for i in range(len(output[k-1])):
                        if k == 0:
                            output[k][j] += Input[i] * nerrone[k][i][j]
                        elif k == 1:
                            output[k][j] += output[k-1][i] * nerrone[k][i][j]    
        avancer = output[len(output)-1][1]
        if avancer > 1:
            avancer = 1
        elif avancer < 0:
            avancer = 0
        turn = output[len(output)-1][0]
        if turn > 1:
            turn = 1
        elif turn < -1:
            turn = 0
        car.avancer(avancer)
        car.tourner(turn*20)
        global old_time, delay_capteur
        Checkpoint(car, checkpoint)
        if time.time() - car.timeStart > Temps_gen:
            car.EndTrain = True
        if time.time() - old_time > delay_capteur:
            old_time = time.time()
            #car.capteurs()
        if car.data == [0, 0, 0, 0, 0]: # L'ia est dans le mur
            car.crach = True
            car.EndTrain = True
        if car.EndTrain:
            car.score_cal()
            # écrire le poid des input pour les output dans un fichier
            return
    

def Show_AI(car, nerrone):
    #print(nerrone)
    car.y -= (car.CurentSpeed*3)*math.sin((car.direction+90)*math.pi/180)
    car.x -= (car.CurentSpeed*3)*math.cos((car.direction+90)*math.pi/180)
    car.capteurs()
    Input = car.data
    #print(Input)
    output = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0]]
    for k in range(len(nerrone)):
        for j in range(len(output[k])):
            if k == 0:
                for i in range(len(Input)):
                    if k == 0:
                        output[k][j] += Input[i] * nerrone[k][i][j]
                    elif k == 1:
                        output[k][j] += output[k-1][i] * nerrone[k][i][j]    
            else:
                for i in range(len(output[k-1])):
                    if k == 0:
                        output[k][j] += Input[i] * nerrone[k][i][j]
                    elif k == 1:
                        output[k][j] += output[k-1][i] * nerrone[k][i][j]    
    avancer = output[len(output)-1][1]
    if avancer > 1:
        avancer = 1
    elif avancer < 0:
        avancer = 0
    turn = output[len(output)-1][0]
    if turn > 1:
        turn = 1
    elif turn < -1:
        turn = 0
    car.avancer(avancer)
    car.tourner(turn*20)

def newGen(First):
    dataTrain = []
    dataRun = []
    if First:
        First = False
        for _ in range(10):
            dataTrain.append([
        [
            [random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100],   
            [random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100],   
            [random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100],  
            [random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100], 
            [random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100, random.randint(-100, 100)/100]
        ],
        [
            [random.randint(0, 100)/100, random.randint(0,100)/100],
            [random.randint(0, 100)/100, random.randint(0,100)/100],   
            [random.randint(0, 100)/100, random.randint(0,100)/100],
            [random.randint(0, 100)/100, random.randint(0,100)/100],
            [random.randint(0, 100)/100, random.randint(0,100)/100],
            [random.randint(0, 100)/100, random.randint(0,100)/100]
        ]
    ])
    else:
        for i in range(10):
            dataTrain.append(readData(str(nb_gen-1), i, File_Name)["nerrone"])
    #  dataTrain   #les données de l'anciène génération
    for i in range(10):
        dataRun.append(dataTrain[i]) # pour les dix premiers identique au meilleurs de l'ancienne génération
    for _ in range(4): 
        for i in range(10):
            # Couche 0 corrigée
            layer0 = []
            for j in range(5):
                row = []
                for k in range(6):
                    data = dataTrain[i][0][j][k] + random.randint(-10, 10)/100
                    if data < -1: data = -1
                    elif data > 1: data = 1
                    row.append(data)  
                layer0.append(row)

            # Couche 1 corrigée  
            layer1 = []
            for j in range(6):
                row = []
                for k in range(2):
                    data = dataTrain[i][1][j][k] + random.randint(-10, 10)/100
                    if data < 0: data = 0
                    elif data > 1: data = 1
                    row.append(data)
                layer1.append(row)

            child = [layer0, layer1]
            dataRun.append(child)
    return dataRun # liste des 50 cerveaux à tester puis enregistrer dans le json

    
def loop(cars, nerrones):
    if Train:
        for car in cars:
            nerrone = nerrones[cars.index(car)]
            screen.blit(car.image, car.image.get_rect(center=(car.x, car.y)))
            if car.EndTrain == False:
                Train_AI(car, nerrone)
    else:
        for car in cars:
            nerrone = nerrones[cars.index(car)]
            screen.blit(car.image, car.image.get_rect(center=(car.x, car.y)))
            if car.EndTrain == False:
                car.capteurs()
                Show_AI(car, nerrone)


def start(nb_ai, First=False):
    global Temps_gen, nb_gen
    Temps_gen = random.randint(20, 30)
    cars = []
    with open(File_Name, "r") as f:
        nerrone = json.load(f)
        nb_gen = len(nerrone)
    if Train:
        print(nb_gen)
    dataRun = newGen(First)
    for i in range(nb_ai):
        cars.append(car(i+1))
        cars[i].timeStart = time.time()
    if not Train:
        return cars, dataRun
    else:
        return cars, dataRun, nb_gen

Show_Data = False if input("Show ?").upper() == "FALSE" else True #---------- False --------

if not Show_Data:
    Train = False if input("Train ? ").upper() == "FALSE" else True # ----- False ------
    First = False
    if Train:
        cars, dataRun, nb_gen = start(50, First)
    else:
        nerrone_list = [["1000", 0, File_Name0], ["1000", 0, File_Name10], ["1000", 0, File_Name01], ["1000", 0, File_Name1]]
        nerrones = []
        for i in range(len(nerrone_list)):
            nerrones.append(readData(nerrone_list[i][0], nerrone_list[i][1], nerrone_list[i][2])["nerrone"])
        cars, dataRun = start(len(nerrone_list))
else:
    File_Data = [get_File(File_Name0), get_File(File_Name01), get_File(File_Name1), get_File(File_Name10)]

def GetData(gen, File):
    File = int(File)
    print()
    print("--------- Fichier :" ,str(File), "----------")
    print("-------- Genération :" ,str(gen), "---------")
    for i in range(10): 
        print("Place", File_Data[File][str(gen)][i]["nb"]+1)
        print("Score", File_Data[File][str(gen)][i]["score"])
        print("Parent", File_Data[File][str(gen)][i]["parents"]+1)
        print("------------------------------------")


while True:
    if not Show_Data:
        screen.blit(bg, (0, 0))
        Checkpoint(cars[0], checkpoint)
        if Train:
            loop(cars, dataRun)
            end=0
            for c in cars:
                if c.EndTrain:
                    end += 1
            if end == 50:
                cars, dataRun, nb_gen = SaveBestCar(cars)
        else:
            loop(cars, nerrones)
    else:
        GetData(input("Genération ? "), input("Fichier à utiliser ? (0, 1, 2, 3) ? ")) #-------- Input utilisateur ----------
    p.display.flip()
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            quit()
    clock.tick(60)