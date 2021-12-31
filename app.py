from flask import Flask,json, request, jsonify
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from collections import Counter


UPLOAD_FOLDER = '\archivitos'


app = Flask(__name__,static_folder='templates', static_url_path='')
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


@app.route('/prueba',methods=['POST'])
@cross_origin()
def prueba():
    df = pd.read_csv("archivo1.csv") # data frame
    data = request.get_json(force=True)
    fecha = data['fecha']
    dias = data['dias']
    casos = data['casos']
    trend = linear_model.LinearRegression()
    # plt.plot(df[dias],df[casos],color='blue', marker='o',linestyle ='solid')
    # plt.title("Line Chart") # Titulo
    # plt.xlabel("dias") # titulo ejex
    # plt.ylabel("casos") #titulo ejey
    # plt.show()


    return jsonify("data: Si jalé bien los datos")


@app.route('/reportes',methods=['POST'])
@cross_origin()
def reportes():
    dataweb = request.get_json(force =True)
    data = dataweb['reporte']

    if (data == 1 ):
        df = pd.read_csv("archivo1.csv") # data frame
        data = request.get_json(force=True)
        fecha = data['fecha']
        dias = data['dias']
        casos = data['casos']
      
        return jsonify({"Reporte": "Este es el reporte 1"})
    elif(data == 2 ):
        return jsonify({"Reporte": "Este es el reporte 2"})
    elif(data == 3 ):
        return jsonify({"Reporte": data})
    elif(data == 4 ):
        return jsonify({"Reporte": data})
    elif(data == 5 ):
        return jsonify({"Reporte": data})
    elif(data == 6 ):
        return jsonify({"Reporte": data})
    elif(data == 7 ):
        return jsonify({"Reporte": data})
    elif(data == 8 ):
        return jsonify({"Reporte": data})
    elif(data == 9 ):
        return jsonify({"Reporte": data})
    elif(data == 10 ):
        return jsonify({"Reporte": data})
    elif(data == 11 ):
        return jsonify({"Reporte": data})
    elif(data == 12 ):
        return jsonify({"Reporte": data})
    elif(data == 13 ):
        return jsonify({"Reporte": data})
    elif(data == 14 ):
        return jsonify({"Reporte": data})
    elif(data == 15 ):
        return jsonify({"Reporte": data})
    elif(data == 16 ):
        return jsonify({"Reporte": data})
    elif(data == 17 ):
        return jsonify({"Reporte": data})
    elif(data == 18 ):
        return jsonify({"Reporte": data})
    elif(data == 19 ):
        return jsonify({"Reporte": data})
    elif(data == 20 ):
        return jsonify({"Reporte": data})
    elif(data == 21 ):
        return jsonify({"Reporte": data})
    elif(data == 22 ):
        return jsonify({"Reporte": data})
    elif(data == 23 ):
        return jsonify({"Reporte": data})
    elif(data == 24 ):
        return jsonify({"Reporte": data})
    elif(data == 25 ):
        return jsonify({"Reporte": data})





@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()

