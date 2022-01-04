from flask import Flask,json, request, jsonify,Response
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import matplotlib
import pandas as pd
from scipy.sparse import data
from sklearn.metrics.pairwise import paired_distances
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from collections import Counter
import numpy as np
from io import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from sklearn.cluster import KMeans
from datetime import date
from datetime import datetime as dt




UPLOAD_FOLDER = '\archivitos'

listagraficas = [1000]

app = Flask(__name__,static_folder='templates', static_url_path='')
archivotrabajar= """"""
CORS(app)

@app.route('/plot.png')
@cross_origin()
def plot_png():
    fig = listagraficas[0]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



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

    if (reporte == 1 ): #Tendencia de la infección por Covid-19 en un País.
        dates = []
        new_labels = []
        fpais = dataweb['pais']
        fecha = dataweb['fecha']
        casos = dataweb['casos']
        npais = dataweb['npais']
        
        #Convertir las fechas en ordninales
        df[fecha] = pd.to_datetime(df[fecha],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[fecha]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',fpais],as_index=False)[casos].sum()

        dfn = df.loc[df[fpais] == npais]
        x = np.asarray(dfn['date_ordinal'])[:,np.newaxis]
        y = np.asarray(dfn[casos])[:,np.newaxis]
        
        # Grado 3
        grados = 3
        caracteristicas = PolynomialFeatures(degree = grados)
        x_transformada = caracteristicas.fit_transform(x)

        #fit lineal
        model = LinearRegression().fit(x_transformada, y)
        y_new = model.predict(x_transformada)

        # calculate rmse and r2
        rmse = np.sqrt(mean_squared_error(y, y_new))
        r2 = r2_score(y, y_new)
       
        x_new_min = x[0,0]
        x_new_max = x[-1,-1]

        x_new = np.linspace(x_new_min, x_new_max, 50)
        x_new = x_new[:,np.newaxis]

        x_new_transform = caracteristicas.fit_transform(x_new)
        y_new = model.predict(x_new_transform)
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))

        new_labels = np.asarray(new_labels)

        # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        # plot the prediction
        ax.scatter(x,y)
        ax.plot(x_new, y_new, color='red', linewidth=3)
        ax.set_xlim(x_new_min,x_new_max)
        ax.set_title("Tendencia del número de infectados de COVID-19\n " + "Grado = " + str(grados) + "; RMSE = " +str(round(rmse,2)) + " ; R2 = " + str(round(r2,2)), fontsize=10)
        ax.set_xticks(np.asarray(dfn['date_ordinal']),labels=new_labels)
        ax.set_xlabel('Dias')
        ax.set_ylabel('Casos')
        listagraficas[0] = fig
                
        return jsonify({"Reporte": "En la grafica se puede observar el comportamiento de los casos de COVID-19 "})


    elif(reporte == 2 ):  #Predicción de Infectados en un País.
        dates = []
        new_labels = []
        prediccion = dataweb['predic']
        dias = dataweb['dias']
        casos = dataweb['casos']
        cpais = dataweb['cpais']
        npais = dataweb['pais']

        #Convertir las fechas en ordninales
        df[dias] = pd.to_datetime(df[dias],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[dias]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',cpais],as_index=False)[casos].sum()

        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn['date_ordinal'])  #x = np.asarray(dfn[dias])
        y = np.asarray(dfn[casos])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        print('RMSE: ', rmse)
        print ('R2: ',r2)

        # # Prediccion
    
        prediccion = dt.strptime(prediccion, '%Y-%m-%d').date()
        prediccion = prediccion.toordinal()

        x_new_min = 0.0
        x_new_max = int(prediccion)

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
        
        #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))

        new_labels = np.asarray(new_labels)


         # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='coral',linewidth=3)
        ax.scatter(x,y)
        ax.set_ylabel("Casos")
        ax.set_xlabel("Dias")
        ax.set_title("Prediccion de infectados en " + npais + "\n" + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        ax.set_xticks(np.asarray(dfn['date_ordinal']),labels=new_labels) ##Agregar
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig
     
        return jsonify({"Reporte": str(round(y_new[-1,-1], 2)) + " para la fecha " + str(dt.fromordinal(prediccion)).replace('00:00:00','')})


    elif(reporte == 3 ):   #Indice de Progresión de la pandemia.
        dates = []
        new_labels = []
        fpais = dataweb['pais']
        fecha = dataweb['fecha']
        casos = dataweb['casos']
        npais = dataweb['npais']
        
        #Convertir las fechas en ordninales
        df[fecha] = pd.to_datetime(df[fecha],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[fecha]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',fpais],as_index=False)[casos].sum()

        dfn = df.loc[df[fpais] == npais]
        x = np.asarray(dfn['date_ordinal'])[:,np.newaxis]
        y = np.asarray(dfn[casos])[:,np.newaxis]
        
        # Grado 3
        grados = 3
        caracteristicas = PolynomialFeatures(degree = grados)
        x_transformada = caracteristicas.fit_transform(x)

        #fit lineal
        model = LinearRegression().fit(x_transformada, y)
        y_new = model.predict(x_transformada)

        # calculate rmse and r2
        rmse = np.sqrt(mean_squared_error(y, y_new))
        r2 = r2_score(y, y_new)
       
        x_new_min = x[0,0]
        x_new_max = x[-1,-1]

        x_new = np.linspace(x_new_min, x_new_max, 50)
        x_new = x_new[:,np.newaxis]
        pendiente = model.coef_[np.size(model.coef_)-4][3]
        x_new_transform = caracteristicas.fit_transform(x_new)
        y_new = model.predict(x_new_transform)
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))

        new_labels = np.asarray(new_labels)

        # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        # plot the prediction
        ax.scatter(x,y)
        ax.plot(x_new, y_new, color='red', linewidth=3)
        ax.set_xlim(x_new_min,x_new_max)
        ax.set_title("Porgresion de la pandemia \n " + "Grado = " + str(grados) + "; RMSE = " +str(round(rmse,2)) + " ; R2 = " + str(round(r2,2)), fontsize=10)
        ax.set_xticks(np.asarray(dfn['date_ordinal']),labels=new_labels)
        ax.set_xlabel('Dias')
        ax.set_ylabel('Casos')
        listagraficas[0] = fig
                
        return jsonify({"Reporte": "El indice de progresión es " + str(pendiente) + " , con esto podremos saber si la recta se comporta de forma descendente o ascendente"})
        

    elif(reporte == 4 ):  #Predicción de mortalidad por COVID en un Departamento.
        
        dates = []
        new_labels = []
        prediccion = dataweb['predict']
        dias = dataweb['dia']
        muertes = dataweb['muertes']
        cdepartamento = dataweb['cdepartamento']
        sdepartamento = dataweb['sdepartamento']
        #Convertir las fechas en ordninales
        df[dias] = pd.to_datetime(df[dias],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[dias]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',cdepartamento],as_index=False)[muertes].sum()


        dfn = df.loc[df[cdepartamento] == sdepartamento]

        x = np.asarray(dfn['date_ordinal'])
        y = np.asarray(dfn[muertes])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion
        prediccion = dt.strptime(prediccion, '%Y-%m-%d').date()
        prediccion = prediccion.toordinal()
        x_new_min = 0.0
        x_new_max = int(prediccion)

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
        #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))

        new_labels = np.asarray(new_labels)
         # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='coral',linewidth=3)
        ax.scatter(x,y)
        ax.grid()
        ax.set_ylabel("Casos")
        ax.set_xlabel("Dias")
        ax.set_title("Prediccion de mortalidad en " + sdepartamento + "\n" + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        #
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig
     
        return jsonify({"Reporte": str(round(y_new[-1,-1], 2)) + " muertes para el día " + str(dt.fromordinal(prediccion)).replace('00:00:00','')+" con el resultado de R2 podemos saber que tan exacto es nuestro modelo para la prediccion de datos, si está más cerca de 1 es porque nuestras variables tendrán mayor correlación"})

   
    elif(reporte == 5 ):  #Predicción de mortalidad por COVID en un País.
        dates = []
        new_labels = []
        prediccion = dataweb['predict']
        dias = dataweb['dia']
        muertes = dataweb['muertes']
        cpais = dataweb['cpais']
        spais = dataweb['spais']
        #Convertir las fechas en ordninales
        df[dias] = pd.to_datetime(df[dias],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[dias]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',cpais],as_index=False)[muertes].sum()
        dfn = df.loc[df[cpais] == spais]
        # dfn[dias] = pd.to_datetime(dfn[dias])                       ##ESTA PARTE ES PARA LAS FECHAS
        # dfn[dias]=dfn[dias].map(dt.datetime.toordinal)
        x = np.asarray(dfn['date_ordinal'])
        y = np.asarray(dfn[muertes])
        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion
        prediccion = dt.strptime(prediccion, '%Y-%m-%d').date()
        prediccion = prediccion.toordinal()
        x_new_min = 0.0
        x_new_max = int(prediccion)

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]
        x_new_transf = polynomial_features.fit_transform(x_new)
        y_new = model.predict(x_new_transf)
        #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))

        new_labels = np.asarray(new_labels)
         # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='coral',linewidth=3)
        ax.scatter(x,y)
        ax.grid()
        ax.set_ylabel("Dias")
        ax.set_xlabel("Casos")
        ax.set_title("Prediccion de infectados en " + spais + "\n" + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        #ax.set_xticks(np.asarray(dfn['date_ordinal']),labels=new_labels) ##Agregar
   
        listagraficas[0] = fig
     
        return jsonify({"Reporte": "Habrán "+str(round(y_new[-1,-1], 2)) + "muertros para el día " + str(dt.fromordinal(prediccion)).replace('00:00:00','') +" con el resultado de R2 podemos saber que tan exacto es nuestro modelo para la prediccion de datos, si está más cerca de 1 es porque nuestras variables tendrán mayor correlación"})


    elif(reporte == 6 ):  #Análisis del número de muertes por coronavirus en un País.
        dates = []
        new_labels = []
        dias = dataweb['dia']
        muertes = dataweb['muertes']
        cpais = dataweb['cpais']
        spais = dataweb['spais']
         #Convertir las fechas en ordninales
        df[dias] = pd.to_datetime(df[dias],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[dias]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',cpais],as_index=False)[muertes].sum()


        dfn = df.loc[df[cpais] == spais]
        x = np.asarray(dfn['date_ordinal']).reshape(-1,1)
        y = np.asarray(dfn[muertes]).reshape(-1,1)
        regresion_lineal = LinearRegression()  
        regresion_lineal.fit(x, y)  
        Y_pred = regresion_lineal.predict(x)  

        x_new_min = x[0]
        x_new_max = x[-1]
        # PARTE PARA LA GRAFICA
        #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))
        fig,ax = plt.subplots(layout='constrained')

        ax.set_xlim(x_new_min,x_new_max)  
        ax.set_title('Numero de muertes en ' + spais +"\n" + "Modelo entrenado: " + str(round(regresion_lineal.coef_[0][0],2)) + 'X+' + str(round(regresion_lineal.intercept_[0],2)), fontsize=10)
        ax.set_xticks(np.asarray(dfn['date_ordinal']),labels=new_labels) ##Agregar
        ax.set_xlabel('Dias')
        ax.set_ylabel('Muertes')
        ax.scatter(x, y)
        ax.plot(x, Y_pred, color='black')
        ax.legend(('Regresion lineal','Data'), loc='upper right')
        
        listagraficas[0] = fig
        
        return jsonify({"Reporte": "Con el modelo " + str(round(regresion_lineal.coef_[0][0],2)) + 'X+' + str(round(regresion_lineal.intercept_[0],2)) + " creado a partir de los datos ingresado podemos predecir las muertes ingresando el valor en x. "})


    elif(reporte == 7 ):  #Tendencia del número de infectados por día de un País.
        dates = []
        new_labels = []
        fpais = dataweb['pais']
        fecha = dataweb['fecha']
        casos = dataweb['casos']
        npais = dataweb['npais']
        #Convertir las fechas en ordninales
        df[fecha] = pd.to_datetime(df[fecha],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[fecha]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',fpais],as_index=False)[casos].sum()

        dfn = df.loc[df[fpais] == npais]
        #dfn[fecha] = pd.to_datetime(dfn[fecha])
        x = np.asarray(dfn['date_ordinal'])[:,np.newaxis]
        y = np.asarray(dfn[casos])[:,np.newaxis]
        
        # Grado 3
        grados = 3
        caracteristicas = PolynomialFeatures(degree = grados)
        x_transformada = caracteristicas.fit_transform(x)

        #fit lineal
        model = LinearRegression().fit(x_transformada, y)
        y_new = model.predict(x_transformada)

        # calculate rmse and r2
        rmse = np.sqrt(mean_squared_error(y, y_new))
        r2 = r2_score(y, y_new)
        print('RMSE: ', rmse)
        print('R2: ', r2)

        x_new_min = x[0,0]-2
        x_new_max = x[-1,-1]+2

        x_new = np.linspace(x_new_min, x_new_max, 50)
        x_new = x_new[:,np.newaxis]

        x_new_transform = caracteristicas.fit_transform(x_new)
        y_new = model.predict(x_new_transform)


        # PARTE PARA LA GRAFICA
         #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))
        fig,ax = plt.subplots(layout='constrained')
        # plot the prediction
        ax.scatter(x,y)
        ax.plot(x_new, y_new, color='red', linewidth=3)
        ax.set_xlim(x_new_min,x_new_max)
        ax.set_title("Tendencia del número de infectados de COVID-19\n " + "Grado = " + str(grados) + "; RMSE = " +str(round(rmse,2)) + " ; R2 = " + str(round(r2,2)), fontsize=10)
        ax.set_xlabel('Dias')
        ax.set_ylabel('Casos')
        ax.set_xticks(np.asarray(dfn['date_ordinal']),labels=new_labels) ##Agregar
        listagraficas[0] = fig
                
        return jsonify({"Reporte": "En la grafica se puede observar el comportamiento de los casos por día de COVID-19 "})


    elif(reporte == 8 ):  #Predicción de casos de un país para un año.
        dates = []
        new_labels = []
        cpais = dataweb['cpais']
        npais = dataweb['npais']
        dias = dataweb['fecha']
        anio  = dataweb['anio']
        prediccion = dataweb['predict']
         #Convertir las fechas en ordninales
        df[dias] = pd.to_datetime(df[dias],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[dias]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',cpais],as_index=False)[anio].sum()

        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn['date_ordinal'])
        y = np.asarray(dfn[anio])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion
        prediccion = dt.strptime(prediccion, '%Y-%m-%d').date()
        prediccion = prediccion.toordinal()
        x_new_min = 0.0
        x_new_max = int(prediccion)

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
         # PARTE PARA LA GRAFICA
          #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='coral',linewidth=3)
        ax.scatter(x,y)
        ax.grid()
        ax.set_ylabel("Dias")
        ax.set_xlabel("Casos")
        
        ax.set_title("Prediccion de casos en " + npais + "\n" + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig

        return jsonify({"Reporte": str(round(y_new[-1,-1], 2)) + " para el año " + str(dt.fromordinal(prediccion)).replace('00:00:00','')})


    elif(reporte == 9 ): #Tendencia de la vacunación de en un País.
        dates = []
        new_labels = []
        fpais = dataweb['pais']
        fecha = dataweb['fecha']
        vacunas = dataweb['vacunas']
        npais = dataweb['npais']
          #Convertir las fechas en ordninales
        df[fecha] = pd.to_datetime(df[fecha],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[fecha]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',fpais],as_index=False)[vacunas].sum()

        dfn = df.loc[df[fpais] == npais]
        #dfn[fecha] = pd.to_datetime(dfn[fecha])
        x = np.asarray(dfn['date_ordinal'])[:,np.newaxis]
        y = np.asarray(dfn[vacunas])[:,np.newaxis]
        
        # Grado 3
        grados = 3
        caracteristicas = PolynomialFeatures(degree = grados)
        x_transformada = caracteristicas.fit_transform(x)

        #fit lineal
        model = LinearRegression().fit(x_transformada, y)
        y_new = model.predict(x_transformada)

        # calculate rmse and r2
        rmse = np.sqrt(mean_squared_error(y, y_new))
        r2 = r2_score(y, y_new)
        print('RMSE: ', rmse)
        print('R2: ', r2)

        x_new_min = x[0,0]-2
        x_new_max = x[-1,-1]+2

        x_new = np.linspace(x_new_min, x_new_max, 50)
        x_new = x_new[:,np.newaxis]

        x_new_transform = caracteristicas.fit_transform(x_new)
        y_new = model.predict(x_new_transform)


        # PARTE PARA LA GRAFICA
          #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))
        fig,ax = plt.subplots(layout='constrained')
        # plot the prediction
        ax.scatter(x,y)
        ax.plot(x_new, y_new, color='red', linewidth=3)
        ax.set_xlim(x_new_min,x_new_max)
        ax.set_title("Tendencia del número de vacunados \n " + "Grado = " + str(grados) + "; RMSE = " +str(round(rmse,2)) + " ; R2 = " + str(round(r2,2)), fontsize=10)
        ax.set_xticks(np.asarray(dfn['date_ordinal']),labels=new_labels) ##Agregar
        ax.set_xlabel('Dias')
        ax.set_ylabel('Casos')
        listagraficas[0] = fig
                
        return jsonify({"Reporte": "En la grafica se puede observar el comportamiento de las personas vacunadas "})


    elif(reporte == 10 ):  #Ánalisis Comparativo de Vacunaciópn entre 2 paises.
        dates = []
        new_labels = []
        cvacunados = dataweb['cvacunados']
        cpais = dataweb['cpais']
        n1pais = dataweb['n1pais']
        n2pais = dataweb['n2pais']
        dias = dataweb['dias']

        #Convertir las fechas en ordninales
        df[dias] = pd.to_datetime(df[dias],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[dias]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',cpais],as_index=False)[cvacunados].sum()
        dfn = df.loc[df[cpais] == n1pais]
        x = np.asarray(dfn['date_ordinal'])
        y = np.asarray(dfn[cvacunados])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion

        x_new_min = 0.0
        x_new_max = int(x[-1])

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
         # PARTE PARA LA GRAFICA CONFIRMADOS
         #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='red',linewidth=3)
        ax.scatter(x,y)
        ax.grid()



        dfnn = df.loc[df[cpais] == n2pais]
        x = np.asarray(dfnn['date_ordinal'])
        y = np.asarray(dfnn[cvacunados])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion

        x_new_min = 0.0
        x_new_max = int(x[-1])

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
        # PARTE PARA LA GRAFICA MUERTOS

        ax.plot(x_new,y_new, color ='blue',linewidth=3)
        ax.scatter(x,y)
        ax.grid()

        ax.set_ylabel("Casos")
        ax.set_xlabel("Dias")
        ax.set_title("Comparación de vacunados entre "+ str(n1pais)+ " y "+ str(n2pais)+"\n"  + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig
     
        return jsonify({"Reporte": "La grafica muestra la comparación de vacunados :3 " })

    elif(reporte == 11 ):  #Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo
        cpais = dataweb['cpais']        
        npais = dataweb['npais']        
        confirmados = dataweb['confirmados']
        confirmadosh = dataweb['cantidah']
        dias=dataweb['dias']
        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn[confirmados].replace(np.nan,0))
        y = np.asarray(dfn[confirmadosh].replace(np.nan,0))
        x_prom = sum(x)
        y_prom = sum(y) 
        
        porcentaje = (y_prom*100)/(x_prom)
        print(porcentaje)
        labels = 'Hombres', 'Mujeres'
        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        listagraficas[0] = fig1

        return jsonify({"Reporte": "El porcentaje de hombres infectados por COVID-19 en " + str(npais) + " es de " +str(round(porcentaje,1)) +"%"})

    elif(reporte== 12 ):  # Ánalisis Comparativo entres 2 paises o continentes.
        dates = []
        new_labels = []
        ccomparacion = dataweb['ccomparacion']
        cpais = dataweb['cpais']
        n1pais = dataweb['n1pais']
        n2pais = dataweb['n2pais']
        dias = dataweb['dias']

        #Convertir las fechas en ordninales
        df[dias] = pd.to_datetime(df[dias],dayfirst=True,infer_datetime_format=True)
        df['date_ordinal'] = pd.to_datetime(df[dias]).apply(lambda date: date.toordinal())
        df = df.groupby(['date_ordinal',cpais],as_index=False)[ccomparacion].sum()
        dfn = df.loc[df[cpais] == n1pais]
        x = np.asarray(dfn['date_ordinal'])
        y = np.asarray(dfn[ccomparacion])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion

        x_new_min = 0.0
        x_new_max = int(x[-1])

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
         # PARTE PARA LA GRAFICA CONFIRMADOS
         #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='red',linewidth=3)
        ax.scatter(x,y)
        ax.grid()



        dfnn = df.loc[df[cpais] == n2pais]
        x = np.asarray(dfnn['date_ordinal'])
        y = np.asarray(dfnn[ccomparacion])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion

        x_new_min = 0.0
        x_new_max = int(x[-1])

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
        # PARTE PARA LA GRAFICA MUERTOS

        ax.plot(x_new,y_new, color ='blue',linewidth=3)
        ax.scatter(x,y)
        ax.grid()

        ax.set_ylabel("Casos")
        ax.set_xlabel("Dias")
        ax.set_title("Comparación de" +str(ccomparacion)+ " entre "+ str(n1pais)+ " y "+ str(n2pais)+"\n"  + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig
     
        return jsonify({"Reporte": "La grafica muestra la comparación de " +str(ccomparacion)+ " :3 " })


    elif(reporte == 13 ): #Muertes promedio por casos confirmados y edad de covid 19 en un País.
        cpais = dataweb['cpais']        
        npais = dataweb['npais']        
        confirmados = dataweb['confirmados']
        muertos = dataweb['cmuertos']
        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn[confirmados].replace(np.nan,0))
        y = np.asarray(dfn[muertos].replace(np.nan,0))
        y_prom = sum(y)/len(y) 
        x_prom = sum(x)
        
        
        porcentaje = ((y_prom)/(x_prom))*100
        print(porcentaje)
        labels = 'Muertes', 'Casos Activos'

        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.legend(labels)
        ax1.set_title('No se grafica')
        listagraficas[0] = fig1

        return jsonify({"Reporte": "Las muertes promedio por casos confirmados son " + str(round(y_prom,2))})

    elif(reporte == 14 ): #Muertes según regiones de un país - Covid 19.
        cpais = dataweb['cpais']        
        npais = dataweb['npais']        
        confirmados = dataweb['confirmados']
        muertos = dataweb['cmuertos']
        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn[confirmados].replace(np.nan,0))
        y = np.asarray(dfn[muertos].replace(np.nan,0))
        x_prom = sum(x)
        y_prom = sum(y) 
        
        porcentaje = (y_prom*100)/(x_prom)
        print(porcentaje)
        labels = 'Muertes', 'Positivos'

        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.legend(labels)
        ax1.set_title('Porcentaje de muertes sobre casos confirmados')
        listagraficas[0] = fig1

        return jsonify({"Reporte": "El porcentaje de muertos por COVID-19 en la region de " + str(npais) + " es de " +str(round(porcentaje,1)) +"%"})


    elif(reporte == 15 ): #Tendencia de casos confirmados de Coronavirus en un departamento de un País.
        dates = []
        new_labels = []
        dias= dataweb['dias']
        casos = dataweb['casos']
        cpais = dataweb['cpais']
        npais = dataweb['npais']
        cdepar = dataweb['cdepar']
        ndepar = dataweb['ndepar']
       
        #Filtro pais
        dfn = df.loc[df[cpais] == npais]
        #Filtro Departamento
        dfn2 = dfn.loc[dfn[cdepar] == ndepar]

         #Convertir las fechas en ordninales
        dfn2[dias] = pd.to_datetime(dfn2[dias],dayfirst=True,infer_datetime_format=True)
        dfn2['date_ordinal'] = pd.to_datetime(dfn2[dias]).apply(lambda date: date.toordinal())
        dfn2 = dfn2.groupby(['date_ordinal',cdepar],as_index=False)[casos].sum()

        #dfn[fecha] = pd.to_datetime(dfn[fecha])
        x = np.asarray(dfn2['date_ordinal'])[:,np.newaxis]
        y = np.asarray(dfn2[casos])[:,np.newaxis]
        
        # Grado 3
        grados = 3
        caracteristicas = PolynomialFeatures(degree = grados)
        x_transformada = caracteristicas.fit_transform(x)

        #fit lineal
        model = LinearRegression().fit(x_transformada, y)
        y_new = model.predict(x_transformada)

        # calculate rmse and r2
        rmse = np.sqrt(mean_squared_error(y, y_new))
        r2 = r2_score(y, y_new)
  
        x_new_min = x[0,0]-2
        x_new_max = x[-1,-1]+2

        x_new = np.linspace(x_new_min, x_new_max, 50)
        x_new = x_new[:,np.newaxis]

        x_new_transform = caracteristicas.fit_transform(x_new)
        y_new = model.predict(x_new_transform)


        # PARTE PARA LA GRAFICA
        #Convertir de ordinal a fecha
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))

        fig,ax = plt.subplots(layout='constrained')
        # plot the prediction
        ax.scatter(x,y)
        ax.plot(x_new, y_new, color='red', linewidth=3)
        ax.set_xlim(x_new_min,x_new_max)
        ax.set_title("Tendencia de casos positivos de COVID-19 en " +str(npais) + " \nen el departamento de " +str(ndepar) + "\n " + "Grado = " + str(grados) + "; RMSE = " +str(round(rmse,2)) + " ; R2 = " + str(round(r2,2)), fontsize=10)
        ax.set_xlabel('Dias')
        ax.set_ylabel('Casos')
        ax.set_xticks(np.asarray(dfn2['date_ordinal']),labels=new_labels) ##Agregar
        listagraficas[0] = fig
                
        return jsonify({"Reporte": "En la grafica se puede observar el comportamiento de los confirmados con COVID-19 por día en el pais de  " +str(npais) + ", en el departamento de "+str(ndepar) })
        

    elif(reporte == 16 ): #Porcentaje de muertes frente al total de casos en un país, región o continente.
        cpais = dataweb['cpais']        
        npais = dataweb['npais']        
        confirmados = dataweb['confirmados']
        muertos = dataweb['cmuertos']
        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn[confirmados])
        y = np.asarray(dfn[muertos])
        x_prom = sum(x)
        y_prom = sum(y) 
        
        porcentaje = (y_prom*100)/(x_prom)
        print(porcentaje)
        labels = 'Fallecidos', 'Confirmados'

        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.legend(labels)
        ax1.set_title('Porcentaje de muertes sobre casos confirmados')
        listagraficas[0] = fig1

        return jsonify({"Reporte": "El porcentaje de muertos por COVID-19 en " + str(npais) + " es de " +str(round(porcentaje,1)) +"%"})


    elif(reporte == 17 ): #Tasa de comportamiento de casos activos en relación al número de muertes en un continente.
        
        cpais = dataweb['pais']        
        npais = dataweb['npais']        
        confirmados = dataweb['confirmados']
        muertos = dataweb['muertos']
        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn[confirmados])
        y = np.asarray(dfn[muertos])
        y_prom = sum(y) 
        x_prom = sum(x)
        
        
        porcentaje = ((y_prom)/(x_prom))*100
        print(porcentaje)
        labels = 'Muertes', 'Casos Activos'

        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.legend(labels)
        ax1.set_title('Tasa de comportamiento de ' + str(npais))
        listagraficas[0] = fig1

        return jsonify({"Reporte": "La tasa de comportamiento de casos activos en " + str(npais) + " es de " +str(round(porcentaje,1)) +"%"})
        
    elif(reporte == 18 ): #Comportamiento y clasificación de personas infectadas por COVID-19 por municipio en un País.
        dates = []
        new_labels = []
        dias= dataweb['dias']
        casos = dataweb['casos']
        cpais = dataweb['cpais']
        npais = dataweb['npais']
        cdepar = dataweb['cdepar']
        ndepar = dataweb['ndepar']
        #Filtro pais
        dfn = df.loc[df[cpais] == npais]
        #Filtro Municipio
        dfn2 = dfn.loc[dfn[cdepar] == ndepar]
        #dfn[fecha] = pd.to_datetime(dfn[fecha])

         #Convertir las fechas en ordninales
        dfn2[dias] = pd.to_datetime(dfn2[dias],dayfirst=True,infer_datetime_format=True)
        dfn2['date_ordinal'] = pd.to_datetime(dfn2[dias]).apply(lambda date: date.toordinal())
        dfn2 = dfn2.groupby(['date_ordinal',cdepar],as_index=False)[casos].sum()

    
        x = np.asarray(dfn2[dias].replace(np.nan,0)).reshape(-1,1)
        y = np.asarray(dfn2[casos].replace(np.nan,0))
        
        regr = linear_model.LinearRegression()
        regr.fit(x,y)
        y_pred = regr.predict(x)
        for item in x:
            new_date = date.fromordinal(int(item))
            dates.append(new_date)
        for item in dates:
            new_labels.append(item.strftime("%d/%m/%Y"))
        fig,ax = plt.subplots(layout='constrained')
        # plot the prediction
        ax.scatter(x,y, color='black')
        ax.plot(x,y_pred,color='blue',linewidth=3)
        ax.set_xlabel('Dias')
        ax.set_ylabel('Casos')
        ax.set_xticks(np.asarray(dfn2['date_ordinal']),labels=new_labels) ##Agregar
        listagraficas[0] = fig

        return jsonify({"Reporte": "La grafica muestra el comportamiento lineal simple de las personas infectadas por COVID-19 con un coeficiente "})


    elif(reporte == 19 ): #Predicción de muertes en el último día del primer año de infecciones en un país.
        canio = dataweb['canio']
        nanio = dataweb['canio']
        dias = dataweb['fecha']
        muertes  = dataweb['muertes']


        dfn = df.loc[df[canio] == nanio]

        x = np.asarray(dfn[dias])
        y = np.asarray(dfn[muertes])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion

        x_new_min = 0.0
        x_new_max = 365 # 365 porque es para el último día del año

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
         # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='coral',linewidth=3)
        ax.scatter(x,y)
        ax.grid()
        ax.set_ylabel("Dias")
        ax.set_xlabel("Casos")
        ax.set_title("Prediccion de muertos al final del año \n" + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig

        return jsonify({"Reporte": "Habrán" +str(round(y_new[-1,-1], 2)) + " muertos por COVID-19 para el ultimo día del año"})


    elif(reporte == 20 ): #Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19
        cpais = dataweb['pais']        
        npais = dataweb['npais']        
        confirmados = dataweb['confirmados']
        muertos = dataweb['muertos']
        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn[confirmados])
        y = np.asarray(dfn[muertos])
        y_prom = sum(y) 
        x_prom = sum(x)
        
        
        porcentaje = ((y_prom)/(x_prom))*100
        print(porcentaje)
        labels = 'Muertes(Tasa de mortalidad)', 'Tasa de crecimiento'

        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.legend(labels)
        ax1.set_title('Tasa de Mortalidad de ' + str(npais))
        listagraficas[0] = fig1

        return jsonify({"Reporte": "La tasa de mortalidad por COVID-19 en " + str(npais) + " es de " +str(round(porcentaje,1)) +"%" + "La tasa de crecimiento es de " + str(round(100-porcentaje,1)) + "%"})


    elif(reporte == 21 ): #Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor
        
        prediccion = dataweb['predict']
        dias = dataweb['dias']
        muertes = dataweb['muertos']
        confirmados = dataweb['confirmados']

        x = np.asarray(df[dias])
        y = np.asarray(df[confirmados])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion

        x_new_min = 0.0
        x_new_max = int(prediccion)

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
        resultdeath = str(round(y_new[-1,-1], 2))
         # PARTE PARA LA GRAFICA CONFIRMADOS
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='red',linewidth=3)
        ax.scatter(x,y)
        ax.grid()

        x = np.asarray(df[dias])
        y = np.asarray(df[muertes])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion

        x_new_min = 0.0
        x_new_max = int(prediccion)

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
         # PARTE PARA LA GRAFICA MUERTOS
        ax.plot(x_new,y_new, color ='blue',linewidth=3)
        ax.scatter(x,y)
        ax.grid()

        ax.set_ylabel("Casos")
        ax.set_xlabel("Dias")
        ax.set_title("Prediccion de infectados y muertos  en el mundo para el día  " + str(prediccion) +"\n"  + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig
     
        return jsonify({"Reporte": "Habrán "+ resultdeath + " muertos y  " + str(round(y_new[-1,-1], 2)) + " infectados en el mundo para el día "+ str(prediccion)})
        
    elif(reporte == 22 ): #Tasa de mortalidad por coronavirus (COVID-19) en un país.
        cpais = dataweb['pais']        
        npais = dataweb['npais']        
        confirmados = dataweb['confirmados']
        muertos = dataweb['muertos']
        dfn = df.loc[df[cpais] == npais]

        x = np.asarray(dfn[confirmados])
        y = np.asarray(dfn[muertos])
        y_prom = sum(y) 
        x_prom = sum(x)
        
        
        porcentaje = ((y_prom)/(x_prom))*100
        print(porcentaje)
        labels = 'Muertes(Tasa de mortalidad)', 'Infectados'

        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.legend(labels)
        ax1.set_title('Tasa de Mortalidad de ' + str(npais))
        listagraficas[0] = fig1

        return jsonify({"Reporte": "La tasa de mortalidad por COVID-19 en " + str(npais) + " es de " +str(round(porcentaje,1)) +"%"})

    elif(reporte == 23 ): #Factores de muerte por COVID-19 en un país.
        cpais = dataweb['pais']        
        npais = dataweb['npais']     
        nfactor = dataweb['nfactor']   
        confirmados = dataweb['confirmados']
        muertos = dataweb['muertos']
        dfn = df.loc[df[cpais] == npais]

        dfn2 = df.loc[dfn[confirmados] == nfactor]

        x = np.asarray(dfn[confirmados])
        y = np.asarray(dfn[muertos])
        y_prom = sum(y) 
        x_prom = sum(x)
        
        
        porcentaje = ((y_prom)/(x_prom))*100
        print(porcentaje)
        labels = 'Muertes(Tasa de mortalidad)', 'Infectados'

        sizes = [porcentaje, 100-porcentaje]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.legend(labels)
        ax1.set_title('Tasa de Mortalidad de ' + str(npais))
        listagraficas[0] = fig1

        return jsonify({"Reporte": "La tasa de mortalidad por COVID-19 en " + str(npais) + " es de " +str(round(porcentaje,1)) +"%"})

    elif(reporte == 24 ): #Comparación entre el número de casos detectados y el número de pruebas de un país.

        cpais = dataweb['cpais']
        npais = dataweb['npais']
        confirmados = dataweb['confirmados']
        pruebas = dataweb['pruebas']
        dfn = df.loc[df[cpais] == npais]
        datos = []
        # print(np.asarray(dfn[pruebas]))
        # print(np.asarray(dfn[confirmados]))
        item = 0
        while item < np.size(np.asarray(dfn[pruebas])):
            datos.append([np.asarray(dfn[pruebas])[item],np.asarray(dfn[confirmados])[item]]) 
            item = item +1

        X = np.array(datos)
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(X)
        # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        # plot the prediction
        ax.scatter(X[:,0],X[:,1], c=kmeans.labels_, cmap='rainbow')
        ax.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color='black')
        ax.set_title("Comparación entre el numero de casos detectados\n y el numero de pruebas de " +str(npais), fontsize=10)
        ax.set_xlabel('Dias')
        ax.set_ylabel('Casos')
        listagraficas[0] = fig


        return jsonify({"Reporte": "Con la siguiente gráfica se puede observar como hubieron diferentes "+
        "agrupaciones en donde se puede observar los cambios entre los casos y días "})

    elif(reporte == 25 ): #Predicción de casos confirmados por día
        prediccion = dataweb['predict']
        cdias = dataweb['cdias']
        casos = dataweb['casos']

        x = np.asarray(df[cdias])
        y = np.asarray(df[casos])

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]
        no_degree = 3
        polynomial_features = PolynomialFeatures(degree= no_degree)
        x_transf = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_transf,y)

        y_new = model.predict(x_transf)
        rmse = np.sqrt(mean_squared_error(y,y_new))
        r2 = r2_score(y,y_new)

        # # Prediccion
        x_new_min = 0.0
        x_new_max = int(prediccion)

        x_new = np.linspace(x_new_min, x_new_max,50)
        x_new = x_new[:,np.newaxis]

        x_new_transf = polynomial_features.fit_transform(x_new)

        y_new = model.predict(x_new_transf)
        # PARTE PARA LA GRAFICA
        fig,ax = plt.subplots(layout='constrained')
        ax.plot(x_new,y_new, color ='coral',linewidth=3)
        ax.scatter(x,y)
        ax.grid()
        ax.set_ylabel("Dias")
        ax.set_xlabel("Casos")
        ax.set_title("Prediccion de infectados al día " + prediccion + "\n" + "RMSE: " + str(round(rmse,2)) + ", R2: "+ str(round(r2,2) ), fontsize=10)
        
        #ax.xlim(x_new_min,x_new_max)
        listagraficas[0] = fig
     
        return jsonify({"Reporte": "Habrán: " +str(round(y_new[-1,-1], 2)) + " infectados para el día " + prediccion})
     


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()

