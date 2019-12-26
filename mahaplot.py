#!/usr/bin/env python
# coding: utf-8

# In[3]:


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
import os


# In[4]:


class rosen():
    divide = 2
    ekiData= []
    rosenData=[]
    ekiDict=[]
    rosenAvg=[0,0]
    rosenStd=[0,0]
    invR=[]
    R=[]
    x_return = []
    ekiData2=np.array([])
    div = 1000
    curve_c = np.zeros((2,div+1))
    def __init__(self, ekiurl,rosenurl):
        self.ekiurl  = ekiurl
        self.rosenurl  = rosenurl
        self.rosenMahaUrl  = "rosenmaha/"+ekiurl.lstrip('rosenjson/')
        self.ekiMahaUrl  = "ekimaha/"+ekiurl.lstrip('rosenjson/')
        self.ekiData= []
        self.rosenData= []
        self.ekiDetailData=[]
        self.ekiDict=[]
        self.rosenAvg=[0,0]
        self.rosenStd=[0,0]
        self.ekiAvg=[]
        self.ekiStd=[]
        self.ekiInvR=[]
        self.ekiInvR2=[]
        self.ekiname=[]
        self.curve_c = np.zeros((2,self.div+1))
        self. x_return =[]
        self.R = np.zeros((self.divide,self.divide))
        self.rosenInvR=np.zeros((self.divide,self.divide))
        self.ekiInvR=np.zeros((self.divide,self.divide))
        self.getData()
        self.daen()
        


    def getData(self):
        with open(self.rosenurl,encoding="utf-8") as f:
            l = json.load(f)
            for i in l:
                for j in i.get("geometry").get("coordinates"):
                    self.ekiData.append(j)
            self.ekiData2 = np.copy(self.ekiData)
        if os.path.isfile(self.rosenMahaUrl) == True :
            with open(self.rosenMahaUrl,encoding="utf-8") as f:
                l = json.load(f)
                self.rosenAvg=l.get('Avg')
                self.rosenStd=l.get('Std')
                self.rosenInvR=l.get('InvR')
        else :
            self.avg(self.rosenMahaUrl) 
        with open(self.rosenurl,encoding="utf-8") as f:
            l = json.load(f)
            self.ekiDict = l
        if os.path.isfile(self.ekiMahaUrl) == True :
            with open(self.ekiMahaUrl,encoding="utf-8") as f:
                l = json.load(f)
                x = 0
                for i in l:
                    self.ekiAvg.append(i.get('Avg'))
                    self.ekiStd.append(i.get('Std'))
                    self.ekiInvR2.append(i.get('InvR'))
                    self.ekiname.append(i.get('name'))
                    x = x + 1
        else :
            self.ekiavg(self.ekiMahaUrl) 
    def avg(self,url):
        url = url
        for i in range(self.divide):
            sumx = 0
            tmp =[]
            for j in range(len(self.ekiData)):
                tmp.append(self.ekiData[j][i])
                sumx = sumx + self.ekiData[j][i]
            self.rosenAvg[i] = sumx / len(self.ekiData)
            self.rosenStd[i] = np.std(tmp)          
        self.rosenMaha(url)
    def ekiavg(self,url):
        url = url
        for ia in range(len(self.ekiDict)):
            i = self.ekiDict[ia]
            addAvg=[]
            addStd=[]
            addlist1=[]
            addlist2=[]
            for j in range(self.divide):
                sumx = 0
                tmp =[]
                x = i.get("geometry").get("coordinates")
                for k in x :                      
                    tmp.append(k[j])
                    sumx = sumx + k[j]
                addAvg.append(sumx / len(i.get("geometry").get("coordinates")))
                tmp.append(sumx / len(i.get("geometry").get("coordinates"))- 0.0002)
                tmp.append(sumx / len(i.get("geometry").get("coordinates"))+ 0.0002)
                addlist1.append(sumx / len(i.get("geometry").get("coordinates"))- 0.0002)
                addlist2.append(sumx / len(i.get("geometry").get("coordinates"))+ 0.0002)
                ansst = np.std(tmp)
                if ansst < 0.0001:
                    ansst = 0.0001
                addStd.append(ansst) 
            self.ekiAvg.append(addAvg)
            self.ekiStd.append(addStd)
            self.ekiDict[ia].get("geometry").get("coordinates").append(addlist1)
            self.ekiDict[ia].get("geometry").get("coordinates").append(addlist2)
        self.ekiMaha(url)
    def rosenMaha(self,url):
        url= url
        x = np.copy(self.ekiData)
        for i in range(self.divide):
            for j in range(len(self.ekiData)):
                x[j][i] = x[j][i] - self.rosenAvg[i]
                x[j][i] = x[j][i] / self.rosenStd[i]
        R = np.corrcoef(x.transpose())
        self.rosenInvR = np.linalg.inv(R)
        tmp = {}
        with open(url,encoding="utf-8",mode='w' ) as f:
            tmp = {}
            tmp["Avg"] =  self.rosenAvg
            tmp["Std"]= self.rosenStd
            tmp["InvR"]= self.rosenInvR.tolist()
            tmp["name"]= self.ekiurl.lstrip('rosenjson/').rstrip('.json')
            json.dump(tmp,f)
        with open('rosenmaha/rosenmaha.json',mode='ab+' ) as f:
            f.seek(-1,2)                           # ファイルの末尾（2）から -1 文字移動
            f.truncate()                           # 最後の文字を削除し、JSON 配列を開ける（]の削除）
            f.write(' , '.encode())                # 配列のセパレーターを書き込む
            f.write(json.dumps(tmp).encode())     # 辞書を JSON 形式でダンプ書き込み
            f.write(']'.encode())  
    def ekiMaha(self,url):
        url= url
        for i in range(len(self.ekiDict)):
            j = self.ekiDict[i].get("geometry").get("coordinates")
            x = np.copy(j)
            for k in range(self.divide):
                for l in range(len(x)):
                    print(i)
                    x[l][k] = x[l][k] - self.ekiAvg[i][k]
                    if x[l][k] == 0:
                        x[l][k] = x[l][k] + 0.00002
                    x[l][k] = x[l][k] / self.ekiStd[i][k]
            R = np.corrcoef(x.transpose())
            addlist3=np.linalg.inv(R).tolist()
            self.ekiInvR2.append(addlist3)
            if i == 0:
                with open(url,encoding="utf-8",mode='x' ) as f:
                    f.write("[")
                    tmp = {}
                    tmp["Avg"] =  self.ekiAvg[i]
                    tmp["Std"]= self.ekiStd[i]
                    tmp["InvR"]= addlist3
                    tmp["name"]= self.ekiDict[i].get("properties").get("N02_005")
                    json.dump(tmp,f)
                    f.write("]")
            else:
                with open(url,mode='ab+' ) as f:
                    tmp = {}
                    tmp["Avg"] =  self.ekiAvg[i]
                    tmp["Std"]= self.ekiStd[i]
                    tmp["InvR"]= addlist3
                    tmp["name"]= self.ekiDict[i].get("properties").get("N02_005")
                    f.seek(-1,2)                           # ファイルの末尾（2）から -1 文字移動
                    f.truncate()                           # 最後の文字を削除し、JSON 配列を開ける（]の削除）
                    f.write(' , '.encode())                # 配列のセパレーターを書き込む
                    f.write(json.dumps(tmp).encode())     # 辞書を JSON 形式でダンプ書き込み
                    f.write(']'.encode())  
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


# In[5]:


江ノ島線=rosen("rosenjson/江ノ島線.json","rosenekijson/江ノ島線.json")


# In[48]:


plt.figure()
ax = plt.axes()
ax.scatter(江ノ島線.ekiData2[:,0],江ノ島線.ekiData2[:,1], c="c", s=10)
ax.scatter(江ノ島線.rosenAvg[0],江ノ島線.rosenAvg[1],marker="+",s=50)
ax.plot(江ノ島線.curve_c[0],江ノ島線.curve_c[1],c="c")
ax.plot(江ノ島線.curve_c[0],江ノ島線.curve_c[1],c="c")
circle=plt.Circle(xy=(江ノ島線.rosenAvg[0], 江ノ島線.rosenAvg[1]), radius=0.13, fc='none', ec='r')
ax.add_patch(circle)
plt.axis('scaled')
ax.set_aspect('equal')
plt.show()


# In[ ]:





# In[ ]:




