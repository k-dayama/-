import numpy as np
import scipy as sc
from scipy import linalg
from scipy import spatial
import scipy.spatial.distance
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import pylab
import json

class rosen():
    divide = 2
    ekiData= []
    ekiDict=[]
    ekiAvg=[0,0]
    ekiStd=[0,0]
    invR=[]
    x_return = []
    ekiData2=np.array
    div = 50
    curve_c = np.zeros((2,div+1))
    def __init__(self, ekiurl):
        self.url  = ekiurl
        self.getData()
        self.avg()
        self.maha()
        self.daen()
        


    def getData(self):
        with open(self.url) as f:
            l = json.load(f)
            self.ekiDict = l
            for i in l:
                addlist = []
                addlist.append(i.get('stlong'))
                addlist.append(i.get('stlat')) 
                self.ekiData.append(addlist)
                addlist = []
                addlist.append(i.get('endlong')) 
                addlist.append(i.get('endlat')) 
                self.ekiData.append(addlist)
            self.ekiData2 = np.copy(self.ekiData)


    def avg(self):
        for i in range(self.divide):
            sumx = 0
            tmp =[]
            for j in range(len(self.ekiData)):
                tmp.append(self.ekiData[j][i])
                sumx = sumx + self.ekiData[j][i]
            self.ekiAvg[i] = sumx / len(self.ekiData)
            self.ekiStd[i] = np.std(tmp)
    def maha(self):
        x = np.copy(self.ekiData)
        for i in range(self.divide):
            for j in range(len(self.ekiData)):
                x[j][i] = x[j][i] - self.ekiAvg[i]
                x[j][i] = x[j][i] / self.ekiStd[i]
        R = np.corrcoef(x.transpose())
        self.invR = np.linalg.inv(R)
        for i in range(len(self.ekiData)):
            d0 = x[i,:]
            d1 = np.dot(d0,self.invR)
            d2 = np.dot(d1,d0)/self.divide
        self.x_return.append(d2)
    def daen(self):
        low = np.corrcoef(self.ekiData2[:,0],self.ekiData2[:,1])[0,1]
        p = 0.99
        for i in range(self.div+1):
            r = (-2*(1-low**2)*np.log(1-p)/(1-2*low*np.sin(i*2*np.pi/self.div)*np.cos(i*2*np.pi/self.div)))**0.5
            self.curve_c[0,i] = self.ekiAvg[0] + self.ekiStd[0]*r*np.cos(i*2*np.pi/self.div)
            self.curve_c[1,i] = self.ekiAvg[1] + self.ekiStd[1]*r*np.sin(i*2*np.pi/self.div)

    #可視化


odakyu = rosen("data/odakyu.json")
dento = rosen("data/data.json")

plt.figure()

plt.scatter(odakyu.ekiData2[:,0],odakyu.ekiData2[:,1], c="green", s=50)
plt.scatter(dento.ekiData2[:,0],dento.ekiData2[:,1], c="m", s=50)
plt.xlabel("long")
plt.ylabel("lat")

plt.plot(odakyu.curve_c[0],odakyu.curve_c[1],c="c")
plt.plot(dento.curve_c[0],dento.curve_c[1],c="m")

plt.show()
