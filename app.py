from flask import Flask,json, request, jsonify,Response
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import matplotlib
import pandas as pd
from sklearn import linear_model,datasets
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from collections import Counter
import numpy as np
from io import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random

import datetime as dt



UPLOAD_FOLDER = '\archivitos'

listagraficas = [1000]

app = Flask(__name__,static_folder='templates', static_url_path='')
archivotrabajar= """"""
CORS(app)

@app.route('/plot.png')
@cross_origin()
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    np.random.seed(19680801)  # seed the random number generator.
    data = {'a': np.arange(50),
            'c': np.random.randint(0, 50, 50),
            'd': np.random.randn(50)}
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    ax.scatter('a', 'b', c='c', s='d', data=data)
    ax.set_xlabel('entry a')
    ax.set_ylabel('entry b')
    return fig




@app.route('/reportes',methods=['POST'])
@cross_origin()
def reportes():
    dataweb = request.get_json(force =True)
    reporte = dataweb['reporte']
    archivotrabajar = StringIO(dataweb['content'])
    tipoarchivo = dataweb['tipoa']
    if tipoarchivo == "csv":
        df = pd.read_csv(archivotrabajar) # data frame
    elif tipoarchivo == "xlsx":
        df = pd.read_excel(dataweb['content'],index_col=0) # data frame
    else:
        return  jsonify({"Reporte": "El tipo de archivo no es compatible"})

    if (reporte == 1 ):
        #Tendencia de la infección por Covid-19 en un País.
        fpais = dataweb['pais']
        fecha = dataweb['fecha']
        casos = dataweb['casos']
        npais = dataweb['npais']
        
        dfn = df.loc[df[fpais] == npais]
        #dfn[fecha] = pd.to_datetime(dfn[fecha])
        x = np.asarray(dfn[fecha]).reshape(-1,1)
        y = dfn[casos]
        x_train = x[:-20]
        x_test = x[-20:]
        y_train = y[:-20]
        y_test = y[-20:]
        regr = linear_model.LinearRegression()
        regr.fit(x_train,y_train)
        y_pred = regr.predict(x_test)
       

        plt.scatter(x_test,y_test,color='black')
        plt.plot(x_test,y_pred,color='blue',linewidth=3)
        plt.show()
        plt.figure()
                
        return jsonify({"Reporte": "xd"})
    elif(reporte == 2 ):
        #Predicción de Infertados en un País.
        prediccion = dataweb['predic']
        dias = dataweb['dias']
        casos = dataweb['casos']
        x = np.asarray(df[dias]).reshape(-1,1)
        y = df[casos]

        regr = linear_model.LinearRegression()
        regr.fit(x,y)
        y_pred = regr.predict(x)

        plt.scatter(x,y, color='black')
        plt.plot(x,y_pred,color='blue',linewidth=3)       
        plt.show()
        
        print(regr.predict([[prediccion]]))

        return jsonify({"Reporte": str(regr.predict([[prediccion]])).replace('[','')})
    elif(reporte == 3 ):
        #Indice de Progresión de la pandemia.
        return jsonify({"Reporte": reporte})
    elif(reporte == 4 ):
        #Predicción de mortalidad por COVID en un Departamento.

        prediccion = dataweb['predict']
        dias = dataweb['dia']
        muertes = dataweb['muertes']
        cdepartamento = dataweb['cdepartamento']
        sdepartamento = dataweb['sdepartamento']
        dfn = df.loc[df[cdepartamento] == sdepartamento]
        x = np.asarray(dfn[dias]).reshape(-1,1)
        y = dfn[muertes]
        regr = linear_model.LinearRegression()
        regr.fit(x,y)
        y_pred = regr.predict(x)
        plt.scatter(x,y, color='black')
        plt.plot(x,y_pred,color='blue',linewidth=3)
        plt.show()
        print(regr.predict([[dataweb['predict']]]))

        return jsonify({"Reporte": str(regr.predict([[dataweb['predict']]])).replace('[','').replace(']','')})
    elif(reporte == 5 ):
        #Predicción de mortalidad por COVID en un País.
        prediccion = dataweb['predict']
        dias = dataweb['dia']
        muertes = dataweb['muertes']
        cpais = dataweb['cpais']
        spais = dataweb['spais']
        dfn = df.loc[df[cpais] == spais]
        dfn[dias] = pd.to_datetime(dfn[dias])
        dfn[dias]=dfn[dias].map(dt.datetime.toordinal)
        
        x = np.asarray(dfn[dias]).reshape(-1,1)
        y = dfn[muertes]
        regr = linear_model.LinearRegression()
        regr.fit(x,y)
        y_pred = regr.predict(x)
        plt.scatter(x,y, color='black')
        plt.plot(x,y_pred,color='blue',linewidth=3)
        #dfn[dias]=dfn[dias].apply(dt.datetime.fromordinal)
        plt.show()
       

        return jsonify({"Reporte":"xd"})
    elif(reporte == 6 ):
        #Análisis del número de muertes por coronavirus en un País.
        return jsonify({"Reporte": reporte})
    elif(reporte == 7 ):
    #Tendencia del número de infectados por día de un País.
        fpais = dataweb['pais']
        fecha = dataweb['fecha']
        casos = dataweb['casos']
        npais = dataweb['npais']
        
        dfn = df.loc[df[fpais] == npais]
        #dfn[fecha] = pd.to_datetime(dfn[fecha])
        x = np.asarray(dfn[fecha]).reshape(-1,1)
        y = dfn[casos]
        x_train = x[:-20]
        x_test = x[-20:]
        y_train = y[:-20]
        y_test = y[-20:]
        regr = linear_model.LinearRegression()
        regr.fit(x_train,y_train)
        y_pred = regr.predict(x_test)
       

        plt.scatter(x_test,y_test,color='black')
        plt.plot(x_test,y_pred,color='blue',linewidth=3)
        plt.show()
        plt.figure()
                
        return jsonify({"Reporte": reporte})

    elif(reporte == 8 ):
        #Predicción de casos de un país para un año.
        return jsonify({"Reporte": reporte})
    elif(reporte == 9 ):
        #Tendencia de la vacunación de en un País.
        return jsonify({"Reporte":reporte})
    elif(reporte == 10 ):
        #Ánalisis Comparativo de Vacunaciópn entre 2 paises.
        return jsonify({"Reporte": reporte})
    elif(reporte == 11 ):
        #Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo
        return jsonify({"Reporte": reporte})
    elif(reporte== 12 ):
        #Ánalisis Comparativo entres 2 o más paises o continentes.
        return jsonify({"Reporte": reporte})
    elif(reporte == 13 ):
        #Muertes promedio por casos confirmados y edad de covid 19 en un País.
        return jsonify({"Reporte": reporte})
    elif(reporte == 14 ):
        #Muertes según regiones de un país - Covid 19.
        return jsonify({"Reporte": reporte})
    elif(reporte == 15 ):
        #Tendencia de casos confirmados de Coronavirus en un departamento de un País.
        return jsonify({"Reporte": reporte})
    elif(reporte == 16 ):
        #Porcentaje de muertes frente al total de casos en un país, región o continente.
        return jsonify({"Reporte": reporte})
    elif(reporte == 17 ):
        #Tasa de comportamiento de casos activos en relación al número de muertes en un continente.
        return jsonify({"Reporte": reporte})
    elif(reporte == 18 ):
        #Comportamiento y clasificación de personas infectadas por COVID-19 por municipio en un País.
        return jsonify({"Reporte": reporte})
    elif(reporte == 19 ):
        #Predicción de muertes en el último día del primer año de infecciones en un país.
        return jsonify({"Reporte": reporte})
    elif(reporte == 20 ):
        #Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19
        return jsonify({"Reporte": reporte})
    elif(reporte == 21 ):
        #Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor
        return jsonify({"Reporte": reporte})
    elif(reporte == 22 ):
        #Tasa de mortalidad por coronavirus (COVID-19) en un país.
        return jsonify({"Reporte": reporte})
    elif(reporte == 23 ):
        #Factores de muerte por COVID-19 en un país.
        return jsonify({"Reporte": reporte})
    elif(reporte == 24 ):
        #Comparación entre el número de casos detectados y el número de pruebas de un país.
        return jsonify({"Reporte": reporte})
    elif(reporte == 25 ):
        #Predicción de casos confirmados por día
        return jsonify({"Reporte": reporte})





@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()

