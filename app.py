from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import pandas as pd
from sklearn import preprocessing
from matplotlib import pyplot as plt
from collections import Counter



app = Flask(__name__,static_folder='my-app/build', static_url_path='')
CORS(app)
@app.route('/api',methods=['GET'])
@cross_origin()
def index():
    df = pd.read_csv("Libro1.csv") # data frame


    le = preprocessing.LabelEncoder() # 

    x1_encoded = le.fit_transform(df['x1'].to_numpy()) #Aquí la codificamos con fit_transform se le envia data frame la columna x1, lo pasamos a un arreglo con to_numpy
    x2_encoded = le.fit_transform(df['x2'].to_numpy())#Aquí la codificamos con fit_transform se le envia data frame la columna x2, lo pasamos a un arreglo con to_numpy
    y_encoded = le.fit_transform(df['y'].to_numpy())#Aquí la codificamos con fit_transform se le envia data frame la columna y, lo pasamos a un arreglo con to_numpy


    return{
        "tutorial": "Flask React "+ str(x1_encoded) + " " + str(x2_encoded) + " " + str(y_encoded)
    }


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')




if __name__ == '__main__':
    app.run()

