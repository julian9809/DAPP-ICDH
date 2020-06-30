import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import sklearn
import os
from flask import json

def recomendaciones(usuario,elecciones):
    users = pd.read_csv("users.csv")
    images = pd.read_csv("images.csv")
    clasificacion = pd.read_csv("election.csv")    
    print(usuarios_test(clasificacion,users))
    n_users = clasificacion.idUser.unique().shape[0]
    n_images = clasificacion.IdImage.unique().shape[0]
    print (str(n_users) + ' users')
    print (str(n_images) + ' images')
    #plt.hist(clasificacion.election,bins=8)
    #plt.show()
    print("prueba")
    print(clasificacion.groupby(["election"])["idUser"].count())
    print("prueba")
    matrix = pd.pivot_table(clasificacion, values='election', index='idUser', columns='IdImage').fillna(0)
    print(matrix)
    ratings = matrix.values
    sparsity = float(len(ratings.nonzero()[0]))
    sparsity /= (ratings.shape[0] * ratings.shape[1])
    sparsity *= 100
    print('Sparsity: {:4.2f}%'.format(sparsity))
    ratings_train, ratings_test = train_test_split(ratings, test_size=0.1, random_state=42)
    print(ratings_train.shape)
    print(ratings_test.shape)
    sim_matrix = 1 - sklearn.metrics.pairwise.cosine_distances(ratings)
    print(sim_matrix.shape)
    #plt.imshow(sim_matrix);
    #plt.colorbar()
    #plt.show()
    #separar las filas y columnas de train y test
    sim_matrix_train = sim_matrix[0:5,0:5]
    sim_matrix_test = sim_matrix[5:6,5:6]
    print("MATRICES DE SIMUILITUD")
    print(sim_matrix_train.shape)
    print(sim_matrix_test.shape)
    users_predictions = sim_matrix_train.dot(ratings_train) / np.array([np.abs(sim_matrix_train).sum(axis=1)]).T
    print("PREDICCIONES")
    print(users_predictions.shape)
    #plt.rcParams['figure.figsize'] = (20.0, 5.0)
    #plt.imshow(users_predictions)
    #plt.colorbar()
    #plt.show()
    imagen = 0
    puntaje = 0
    user = usuario
    data = users[users['user'] == user]
    usuario_ver = data.iloc[0]['idUser'] - 1 # resta 1 para obtener el index de pandas.
    print("USUARIO"+repr(usuario_ver))
    user0=users_predictions.argsort()[usuario_ver]
    print(user0)
    # Veamos los tres recomendados con mayor puntaje en la predic para este usuario
    for i, aImage in enumerate(user0[-15:]):
        selImage = images[images['idImage']==(aImage+1)]
        imagen = selImage.iloc[0]['idImage']
        puntaje = users_predictions[usuario_ver][aImage]
        if puntaje >= 0.51:
            elecciones['election'].append({
                'imagen':repr(imagen),
                'puntaje':repr(puntaje)
            })
            with open('election.json','w')as file:
                json.dump(elecciones,file,indent=4)
    return "exito"

def usuarios_test(clasificacion,users):
    n_usuarios = users.idUser.unique().shape[0]
    n_users = clasificacion.idUser.unique().shape[0]
    n_images = clasificacion.IdImage.unique().shape[0]
    if n_users == n_usuarios:
        for i in range(0,2):
            for j in range(0,n_images):
                idUser = "test"+repr(i)
                idImage = j
                election = 0
                archivo = "election.csv"
                fieldnames = ['idUser', 'IdImage','election']
                datos = [[idUser,idImage,election]]
                data = pd.DataFrame(datos, columns=fieldnames)
                data.to_csv(archivo, index=None, mode="a", header=not os.path.isfile(archivo))
        return "agregados"
    return "no agregados"