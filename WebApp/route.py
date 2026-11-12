from flask import Blueprint, request,render_template, redirect, url_for, session, flash,    send_from_directory, abort

import os

import random
import json
import string

main = Blueprint("main", __name__)

# Dossier où se trouve route.py, WebApp/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dossier parent, carAI/
PROJECT_ROOT = os.path.dirname(BASE_DIR)

PYTHONAPP_DIR = os.path.join(PROJECT_ROOT, "pythonApp")

# Sous-dossiers
DATA_DIR = os.path.join(PYTHONAPP_DIR, "Data")
IMG_DIR = os.path.join(PYTHONAPP_DIR, "img")


@main.route('/assets/pythonapp/img/<path:filename>')
def pythonapp_img(filename):
    # Empêche les chemins dangereux comme ../../secret.png
    safe_filename = os.path.basename(filename)

    if not safe_filename:
        abort(404)

    allowed_extensions = (".png", ".jpg", ".jpeg", ".gif", ".webp")

    if not safe_filename.lower().endswith(allowed_extensions):
        abort(404)

    return send_from_directory(IMG_DIR, safe_filename)



@main.route('/')
def accueil():
    return render_template('Accueil.html')

@main.route('/graphique')
def graphique():
    return render_template('Graph.html')

@main.route('/simulation', methods=['POST', 'GET'])
def simulation():
    return render_template('WatchAI.html')

@main.route('/choose_network', methods=['POST', 'GET'])
def choose_network():
    donnes = request.form
    nb = donnes.get('Nb')
    if not nb:
        nb = 1
    else:
        nb = int(nb)
    Map = donnes.get('Map')
    if not Map:
        Map = 0
    else:
        Map = int(Map)
    return render_template('Network.html', nb=nb, Map=Map)

@main.route('/simulations', methods=['POST', 'GET'])
def simulations():
    Files = ["pythonApp/Data/AI_data_for_stat_Map0.json",
              "pythonApp/Data/AI_data_for_stat_Map0(1).json",
              "pythonApp/Data/AI_data_for_stat_Map1.json",
              "pythonApp/Data/AI_data_for_stat_Map1(0).json"]

    Files = [
    os.path.join(DATA_DIR, "AI_data_for_stat_Map0.json"),
    os.path.join(DATA_DIR, "AI_data_for_stat_Map0(1).json"),
    os.path.join(DATA_DIR, "AI_data_for_stat_Map1.json"),
    os.path.join(DATA_DIR, "AI_data_for_stat_Map1(0).json")
    ]

    donnes = request.form
    if 'nb' not in donnes or 'Map' not in donnes:
        return redirect('/')
    nb = int(donnes.get('nb'))
    Map = donnes.get('Map')
    data = []
    Folders = []
    Folders_open = []
    DataReturn = []
    # Recup les data des nerrones voulus
    for i in range(nb):
        data.append([nb, donnes.get('gen_' + str(i)), donnes.get('Fichier_' + str(i)), donnes.get('place_' + str(i))])
        Folders.append(donnes.get('Fichier_' + str(i)))
    # Recherche des data dans les fichiers
    Folders = list(set(Folders))
    for i in range(len(Folders)):
        with open(Files[int(Folders[i])], 'r') as f:
            Folders_open.append(json.load(f))
    # Maintenant qu'on a chargé tous les fichiers nessésaires en memoire recherchont dedans
    for i in range(nb):
        DataReturn.append([nb, Folders_open[Folders.index(data[i][2])][data[i][1]][int(data[i][3])-1]])
    return render_template('simulations.html', Map=Map, Data=DataReturn)