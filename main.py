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
    ekiData= []
    ekiDict=[]
    def __init__(self, ekiurl):
        self.url  = ekiurl
        self.getData()


    def getData(self):
        with open(self.url) as f:
            l = json.load(f)
            self.ekiDict = l
            for i in l:
                addlist = []
                addlist.append(i.get('stlat')) 
                addlist.append(i.get('stlong'))
                self.ekiData.append(addlist)
                addlist = []
                addlist.append(i.get('endlat')) 
                addlist.append(i.get('endlong')) 
                self.ekiData.append(addlist)



    def ave(self):
        pass

odakyu = rosen("data/odakyu.json")

print(odakyu.ekiData)