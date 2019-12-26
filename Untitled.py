#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader


# In[3]:


class rosen():
    divide = 2
    ekiData= []
    ekiDict=[]
    rosenAvg=[0,0]
    rosenStd=[0,0]
    invR=[]
    R=[]
    x_return = []
    ekiData2=np.array([])
    div = 1000
    curve_c = np.zeros((2,div+1))
    def __init__(self, ekiurl):
        self.url  = ekiurl
        self.ekiData= []
        self.ekiDetailData=[]
        self.ekiDict=[]
        self.rosenAvg=[0,0]
        self.rosenStd=[0,0]
        self.ekiAvg=[]
        self.ekiStd=[]
        self.curve_c = np.zeros((2,self.div+1))
        self. x_return =[]
        self.R = np.zeros((self.divide,self.divide))
        self.rosenInvR=np.zeros((self.divide,self.divide))
        self.ekiInvR=np.zeros((self.divide,self.divide))
        self.getData()
        self.avg()
        self.rosenMaha()
        self.ekiMaha()
        self.daen()
        


    def getData(self):
        with open(self.url,encoding="utf-8") as f:
            l = json.load(f)
            self.ekiDict = l
            for i in l:
                addlist = []
                addlist2=[]
                addlist3=[]
                addlist.append(i.get('stlong'))
                addlist.append(i.get('stlat'))
                addlist2.append(i.get('stlong'))
                addlist2.append(i.get('stlat'))
                self.ekiData.append(addlist)
                addlist3.append(addlist2)
                addlist = []
                addlist2=[]
                addlist.append(i.get('stlong')) 
                addlist.append(i.get('endlat')) 
                addlist2.append(i.get('endlong')) 
                addlist2.append(i.get('endlat')) 
                self.ekiData.append(addlist)
                addlist3.append(addlist2)
                self.ekiDetailData.append(addlist3)
            self.ekiData2 = np.copy(self.ekiData)
    def avg(self):
        for i in range(self.divide):
            sumx = 0
            tmp =[]
            for j in range(len(self.ekiData)):
                tmp.append(self.ekiData[j][i])
                sumx = sumx + self.ekiData[j][i]
            self.rosenAvg[i] = sumx / len(self.ekiData)
            self.rosenStd[i] = np.std(tmp)
        for i in self.ekiDetailData:
            addlist=[]
            addlist2=[]
            for k in range(self.divide):
                sumx = 0
                tmp = []
                for j in i:               
                    tmp.append(j[k])
                    sumx =sumx + j[k]
                addlist.append(sumx/len(i))
                addlist2.append(np.std(tmp))
            self.ekiAvg.append(addlist)
            self.ekiStd.append(addlist2)
              
                    
    def rosenMaha(self):
        x = np.copy(self.ekiData)
        for i in range(self.divide):
            for j in range(len(self.ekiData)):
                x[j][i] = x[j][i] - self.rosenAvg[i]
                x[j][i] = x[j][i] / self.rosenStd[i]
        R = np.corrcoef(x.transpose())
        self.rosenInvR = np.linalg.inv(R)
    def ekiMaha(self):
        data = [[1,-1],[-1,1]]
        self.ekiInvR = np.array(data)
    def daen(self):
        low = np.corrcoef(self.ekiData2[:,0],self.ekiData2[:,1])[0,1]
        p = 0.97
        for i in range(self.div+1):
            r = (-2*(1-low**2)*np.log(1-p)/(1-2*low*np.sin(i*2*np.pi/self.div)*np.cos(i*2*np.pi/self.div)))**0.5
            self.curve_c[0,i] = self.rosenAvg[0] + self.rosenStd[0]*r*np.cos(i*2*np.pi/self.div)
            self.curve_c[1,i] = self.rosenAvg[1] + self.rosenStd[1]*r*np.sin(i*2*np.pi/self.div)
    def getRosenMaha(self,position):
        self.x_return=[]
        x = np.copy(position)
        for i in range(self.divide):
            x[i] = x[i] - self.rosenAvg[i]
            x[i] = x[i] / self.rosenStd[i]
        d0 = x
        d1 = np.dot(d0,self.rosenInvR)
        d2 = np.dot(d1,d0)/self.divide
        self.x_return.append(d2)
        return d2
    def getEki(self,position):
        lenreturn=[]
        for j in range(len(self.ekiAvg)):
            x = np.copy(position)
            for i in range(self.divide):
                x[i] = x[i] - self.ekiAvg[j][i]
                x[i] = x[i] / self.ekiStd[j][i]
            d0 = x
            d1 = np.dot(d0,self.ekiInvR)
            d2 = np.dot(d1,d0)/self.divide
            if d2 < 2.48:
                return (self.ekiDict[j].get("name"))


# In[4]:


odakyu_e = rosen("data/odakyu_e.json")
odakyu_h = rosen("data/odakyu_h.json")
dento = rosen("data/data.json")
toyoko=rosen("data/toyoko.json")
keio_h=rosen("data/keio_h.json")


# In[5]:


plt.figure()
plt.scatter(odakyu_h.ekiData2[:,0],odakyu_h.ekiData2[:,1], c="b", s=10)
plt.scatter(odakyu_e.ekiData2[:,0],odakyu_e.ekiData2[:,1], c="c", s=10)
plt.scatter(dento.ekiData2[:,0],dento.ekiData2[:,1], c="g", s=10)
plt.scatter(toyoko.ekiData2[:,0],toyoko.ekiData2[:,1], c="r", s=10)
plt.scatter(keio_h.ekiData2[:,0],keio_h.ekiData2[:,1], c="m", s=10)
plt.xlabel("long")
plt.ylabel("lat")
plt.plot(odakyu_e.curve_c[0],odakyu_e.curve_c[1],c="c")
plt.plot(odakyu_h.curve_c[0],odakyu_h.curve_c[1],c="b")
plt.plot(dento.curve_c[0],dento.curve_c[1],c="g")
plt.plot(toyoko.curve_c[0],toyoko.curve_c[1],c="r")
plt.plot(keio_h.curve_c[0],keio_h.curve_c[1],c="m")

plt.show()


# In[6]:


position = [139.6367183,35.651283]
print(odakyu_h.getRosenMaha(position))
print(odakyu_e.getRosenMaha(position))
print(dento.getRosenMaha(position))
print(toyoko.getRosenMaha(position))
print(keio_h.getRosenMaha(position))


# In[18]:


ax = plt.axes(projection=ccrs.PlateCarree())
# 落としてきた行政区域のshpファイルを指定
tokyo = 'N03-190101_13_GML/N03-19_13_190101.shp'
kanagawa = 'N03-190101_14_GML/N03-19_14_190101.shp'
chiba = 'N03-190101_12_GML/N03-19_12_190101.shp'
saitama = 'N03-190101_11_GML/N03-19_11_190101.shp'
rosen = 'N02-18_GML/N02-18_RailroadSection.shp'
eki = 'N02-18_GML/N02-18_Station.shp'
def add_geometries(fname):
    shapes = list(shpreader.Reader(fname).geometries())
    ax.add_geometries(shapes, ccrs.PlateCarree(), edgecolor='white', facecolor='lightgray', alpha=0.3)
def add_rosengeometries(fname):
    shapes = list(shpreader.Reader(fname).geometries())
    ax.add_geometries(shapes, ccrs.PlateCarree(), edgecolor='gray', facecolor='none', alpha=0.3)
def add_ekigeometries(fname):
    shapes = list(shpreader.Reader(fname).geometries())
    ax.add_geometries(shapes, ccrs.PlateCarree(), edgecolor='black',facecolor='none', alpha=0.3)
add_geometries(chiba)
add_geometries(kanagawa)
add_geometries(tokyo)
add_geometries(saitama)
add_rosengeometries(rosen)
add_ekigeometries(eki)
# 東京あたりを描画
ax.set_extent([139.3, 139.8, 35.3, 35.8], ccrs.PlateCarree())
ax.scatter(odakyu_h.ekiData2[:,0],odakyu_h.ekiData2[:,1], c="b", s=10)
ax.scatter(odakyu_e.ekiData2[:,0],odakyu_e.ekiData2[:,1], c="c", s=10)
ax.scatter(dento.ekiData2[:,0],dento.ekiData2[:,1], c="g", s=10)
ax.scatter(toyoko.ekiData2[:,0],toyoko.ekiData2[:,1], c="r", s=10)
ax.scatter(keio_h.ekiData2[:,0],keio_h.ekiData2[:,1], c="m", s=10)
ax.plot(odakyu_e.curve_c[0],odakyu_e.curve_c[1],c="c")
ax.plot(odakyu_h.curve_c[0],odakyu_h.curve_c[1],c="b")
ax.plot(dento.curve_c[0],dento.curve_c[1],c="g")
ax.plot(toyoko.curve_c[0],toyoko.curve_c[1],c="r")
ax.plot(keio_h.curve_c[0],keio_h.curve_c[1],c="m")
plt.show()


# In[8]:


class jikkenData():
    positions=[]
    jikkenDict=[]
    dataUrl=""
    positions2=[]
    collectEki=[]
    collectRosen=""
    ansRosen=[]
    ansEki=[]
    mahas=[]
    rosenList=["odakyu_h","odakyu_e","dento","toyoko","keio_h"]
    def __init__(self, dataUrl):
        self.positions=[]
        self.positions2=[]
        self.mahas=[]
        self.jikkenDict=[]
        self.dataUrl=dataUrl
        self.collectEki=[]
        self.collectRosen=""
        self.ansRosen=[]
        self.ansEki=[]
        self.getData()
        self.getRosenMahas()
        self.getRosen()
    def getData(self):
        with open(self.dataUrl,encoding="utf-8") as f:
            l = json.load(f)
            self.jikkenDict = l
            for i in l:
                addlist = []
                addlist.append(i.get('longitude'))
                addlist.append(i.get('latitude')) 
                self.positions.append(addlist)
            self.positions2 = np.copy(self.positions)
    def getRosenMahas(self):
        for i in self.positions:
            addlist = []
            addlist.append(odakyu_h.getRosenMaha(i))
            addlist.append(odakyu_e.getRosenMaha(i))
            addlist.append(dento.getRosenMaha(i))
            addlist.append(toyoko.getRosenMaha(i))
            addlist.append(keio_h.getRosenMaha(i))
            self.mahas.append(addlist)
    def getRosen(self):
        for i in self.mahas:
            addlist = []
            for j in range(len(i)):
                if float(i[j]) < 2.48:
                    addlist.append(self.rosenList[j])
            self.ansRosen.append(addlist)
    def getEki(self):
        for i in range(len(self.positions)):
            addlist = []
            for j in self.ansRosen[i]:
                if(j == "odakyu_h"):
                    addlist.append(odakyu_h.getEki(self.positions[i]))
                if(j == "odakyu_e"):
                    addlist.append(odakyu_e.getEki(self.positions[i]))
                if(j == "dento"):
                    addlist.append(dento.getEki(self.positions[i]))
                if(j == "toyoko"):
                    addlist.append(toyoko.getEki(self.positions[i]))
                if(j == "keio"):
                    addlist.append(keio.getEki(self.positions[i]))
            self.ansEki.append(addlist)
        print(self.ansEki)


# In[9]:


test0702= jikkenData("data/0702test.json")
test0927=jikkenData("data/0927test.json")


# In[10]:


test0702.getEki()


# In[ ]:





# In[ ]:




