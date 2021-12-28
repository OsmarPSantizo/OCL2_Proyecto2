import pandas as pd
from sklearn import preprocessing
from matplotlib import pyplot as plt
from collections import Counter

df = pd.read_csv("Libro1.csv") # data frame


le = preprocessing.LabelEncoder() # 

x1_encoded = le.fit_transform(df['x1'].to_numpy()) #Aquí la codificamos con fit_transform se le envia data frame la columna x1, lo pasamos a un arreglo con to_numpy
x2_encoded = le.fit_transform(df['x2'].to_numpy())#Aquí la codificamos con fit_transform se le envia data frame la columna x2, lo pasamos a un arreglo con to_numpy
y_encoded = le.fit_transform(df['y'].to_numpy())#Aquí la codificamos con fit_transform se le envia data frame la columna y, lo pasamos a un arreglo con to_numpy


print("x1: ",x1_encoded) #imprimimos codificado
print("x2: ", x2_encoded)
print("y: ", y_encoded)

features = list(zip(x1_encoded,x2_encoded)) #Lista de tuplas en variables independientes, zip da como resultado una tupla
print("list of tuples: ", features)
print("############################")
print("Media, Mediana, Moda\n ")

df2 = pd.read_csv("Libro2.csv")

print(df2['value'].mean())  #Media de los valores
print(df2['value'].median()) #Mediana de los valores
print(df2['value'].mode())  #Moda de los valores

print("\nDesviacion estandar, varianza\n")

print(df2['value'].std(ddof=0))  # 0 = Poblacional 1= Muestral
print(df2['value'].var(ddof=0))  # 0 = Poblacional 1= Muestral

print("############################")
print("Prueba de Matplotlib\n")
print("######Lineas######\n")

plt.plot(df2['name'], df2['value'], color='blue', marker='o',linestyle ='solid') # variables , color, marker = punto circular, linea solida
plt.title("Line Chart") # Titulo
plt.xlabel("name") # titulo ejex
plt.ylabel("value") #titulo ejey
plt.show()

print("\n######Barras######\n")

plt.bar(df2['name'],df2['value'])#
plt.title("Bar Chart")
plt.xlabel("name")
plt.ylabel("value")
plt.show()

print("############################")
print("Prueba de Colections\n") 

#Contamos cuantos valores  hay
histogram = Counter(min(value // 10*10,90) for value in df2['value'])
print(histogram)
plt.bar([x+5 for x in histogram.keys()],histogram.values(),10,edgecolor=(0,0,0))
plt.axis([-5,105,0,3])
plt.xticks([10* i for i in range(11)])
plt.title("Distribucion de los valores")
plt.xlabel("Decile")
plt.ylabel("# values")
plt.show()