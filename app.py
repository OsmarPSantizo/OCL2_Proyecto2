from flask import Flask,json, request, jsonify
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from collections import Counter
import numpy as np
from io import StringIO



UPLOAD_FOLDER = '\archivitos'


app = Flask(__name__,static_folder='templates', static_url_path='')
archivotrabajar= """"""
CORS(app)

@app.route('/reportes',methods=['POST'])
@cross_origin()
def reportes():
    dataweb = request.get_json(force =True)
    reporte = dataweb['reporte']
    archivotrabajar = StringIO(dataweb['content'])
    tipoarchivo = dataweb['tipoa']
    if tipoarchivo == "csv":
        df = pd.read_csv(archivotrabajar) # data frame
    elif tipoarchivo == "xls":
        df = pd.read_excel(archivotrabajar) # data frame
    else:
        return  jsonify({"Reporte": "El tipo de archivo no es compatible"})

    if (reporte == 1 ):
        
        fecha = dataweb['fecha']
        dias = dataweb['dias']
        casos = dataweb['casos']
        # plt.plot(df[dias],df[casos],color='blue', marker='o',linestyle ='solid')
        # plt.title("Line Chart") # Titulo
        # plt.xlabel("dias") # titulo ejex
        # plt.ylabel("casos") #titulo ejey
        # plt.show()
                
      
        return jsonify({"Reporte": dias })
    elif(reporte == 2 ):
        
        prediccion = dataweb['predic']
        dias = dataweb['dias']
        casos = dataweb['casos']
        x = np.asarray(df[dias]).reshape(-1,1)
        y = df[casos]

        regr = linear_model.LinearRegression()
        regr.fit(x,y)
        y_pred = regr.predict(x)

        # plt.scatter(x,y, color='black')
        # plt.plot(x,y_pred,color='blue',linewidth=3)

        # plt.ylim(0,5000)
        # plt.show()
        print(regr.coef_)
        print(regr.predict([[prediccion]]))


        return jsonify({"Reporte": str(regr.predict([[prediccion]]))})
    elif(reporte == 3 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 4 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 5 ):
        return jsonify({"Reporte":reporte})
    elif(reporte == 6 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 7 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 8 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 9 ):
        return jsonify({"Reporte":reporte})
    elif(reporte == 10 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 11 ):
        return jsonify({"Reporte": reporte})
    elif(reporte== 12 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 13 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 14 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 15 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 16 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 17 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 18 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 19 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 20 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 21 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 22 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 23 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 24 ):
        return jsonify({"Reporte": reporte})
    elif(reporte == 25 ):
        return jsonify({"Reporte": reporte})





@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()

