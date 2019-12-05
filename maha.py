import numpy as np
import matplotlib.pyplot as plt

divide = 2 #状態量の数
R = np.zeros((divide,divide))    #相関行列
invR = np.zeros((divide,divide)) #相関行列の逆行列
avg = np.zeros(divide)           #平均値
std = np.zeros(divide)           #標準偏差
make = 0

p = 0.95        #マハラノビス距離p=0.95で2σ
md_sikii = 2.448#MDの閾値95%で2.448
div = 50        #Mt楕円の分割数

def maha(x):
    global make, R, invR, avg, std

    N, _ = x.shape #Nはデータ数
    xx = np.copy(x)
    xx = np.array(xx,dtype="float32")
    x_return = []

    #各状態量から平均値を引く
    for i in range(divide):
        if make == 0:
            avg[i] = np.mean(x[:,i])
        for j in range(N):
            xx[j,i] = xx[j,i] - avg[i]

    #各状態量を標準偏差で割る
    for i in range(divide):
        if make == 0:
            std[i] = np.std(x[:,i])
        for j in range(N):
            xx[j,i] = xx[j,i] / std[i]

    #make=0のときだけ計算
    if make == 0:
        R = np.corrcoef(xx.transpose())
        invR = np.linalg.inv(R)
        make = 1

    #MD^2の計算
    for i in range(N):
        d0 = xx[i,:]
        d1 = np.dot(d0,invR)
        d2 = np.dot(d1,d0)/divide
        x_return.append(d2)

    return x_return

if __name__ == '__main__':

    curve_c = np.zeros((2,div+1))

    #正常データの作成
    x1 = np.random.normal(1, 0.3, (1, 50))
    y1 = np.random.normal(1, 0.3, (1, 50))
    x2 = np.random.normal(1.5, 0.3, (1, 50))
    y2 = np.random.normal(1.5, 0.3, (1, 50))

    #テストデータの作成
    test1 = np.array([1.02,1.5])
    test1 = test1.reshape((1,2))
    test2 = np.array([0.5,2])
    test2 = test2.reshape((1,2))

    #正常データの形を整える
    data = []
    data.append(x1)
    data.append(x2)
    data.append(y1)
    data.append(y2)
    data = np.array(data)
    data = data.reshape(2,100)
    data = data.transpose()
    print(data.shape)

    #単位空間の作成
    _ = maha(data)

    #テストデータのマハラノビス距離
    md_1 = maha(test1)
    md_2 = maha(test2)

    #楕円のデータ
    low = np.corrcoef(data[:,0],data[:,1])[0,1]

    for i in range(div+1):
        r = (-2*(1-low**2)*np.log(1-p)/(1-2*low*np.sin(i*2*np.pi/div)*np.cos(i*2*np.pi/div)))**0.5
        curve_c[0,i] = avg[0] + std[0]*r*np.cos(i*2*np.pi/div)
        curve_c[1,i] = avg[1] + std[1]*r*np.sin(i*2*np.pi/div)

    #可視化
    plt.figure()

    plt.subplot(1,2,1)
    plt.scatter(x1, y1, c="green", s=50)
    plt.scatter(x2, y2, c="green", s=50)
    plt.scatter(test1[:,0],test1[:,1],c="m", s=50)
    plt.scatter(test2[:,0],test2[:,1],c="red", s=50)
    plt.xlabel("T")
    plt.ylabel("KN")

    plt.plot(curve_c[0],curve_c[1],c="c",label="MD^2=2.448")
    plt.legend()

    plt.subplot(1,2,2)
    plt.bar([1,2], [md_1[0], md_2[0]], align="center")
    plt.grid(True)
    plt.xticks([1,2], ["Purple", "Red"])
    plt.ylabel("MD^2")
    plt.grid(True)

    plt.show()