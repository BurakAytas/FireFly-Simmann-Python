
# matplotlib and numpy packages must also be installed
import numpy as np
import matplotlib.pyplot as plt
import random
import math


print("\n1 --> Goldstein–Price Fonksiyonu ")
print("2 --> Beale Fonksiyonu ")
print("3 --> Ackley Fonksiyonu ")
print("4 --> Levi Fonksiyonu \n ")
kontrol = True
sec = 0
while(kontrol):
    sec = int(input("Kullanmak istediginiz test fonksiyonunun numarasını giriniz : "))
    if(sec != 1 and sec != 2 and sec != 3 and sec != 4):
        print("Gecerli bir değer giriniz.")
    else:
        kontrol = False
def f(x):
    if (sec == 1):  # Goldstein–Price Fonksiyonu
        obj = ((1 + (x[0] + x[1] + 1)**2 * (19 - 14*x[0] + 3*(x[0]**2) - 14*x[1] + 6*x[0]*x[1] + 3*(x[1]**2))) * (30 + (2*x[0] - 3*x[1])**2 * (18 - 32*x[0] + 12*(x[0]**2) + 48*x[1] - 36*x[0]*x[1] + 27*(x[1]**2))))
    elif (sec == 2): # Beale Fonksiyonu
         obj = (1.5 - x[0] + x[0] * x[1]) ** 2 + (2.25 - x[0] + x[0] * x[1] ** 2) ** 2 + (2.625 - x[0] + x[0] * x[1] ** 3) ** 2
    elif (sec == 3): # Ackley Fonksiyonu
         obj = -math.exp(-math.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))) - math.exp(0.5 * (math.cos(2 * math.pi * x[0]) + math.cos(2 * math.pi * x[1]))) + math.e + math.exp(1)
    elif (sec == 4): # Levi Fonksiyonu
         obj = (math.sin(3*x[0]*math.pi))**2 + ((x[0] - 1)**2)*(1 + math.sin(3*x[1]*math.pi)**2) + ((x[1] - 1)**2)*(1 + math.sin(2*x[1]*math.pi)**2)

    return obj


def altust(x):
    if (sec == 1):  # Goldstein–Price Fonksiyonu
        sinir = 2.0
    elif (sec == 2): # Beale Fonksiyonu
        sinir = 4.5
    elif (sec == 3): # Ackley Fonksiyonu
        sinir = 5.0
    elif (sec == 4): # Levi Fonksiyonu
        sinir = 10.0

    return sinir

# Konum
x_start = [0.8, -0.5]

n = 40 # Döngü sayısı
m = 100 # Döngü başına deneme sayısı
na = 0.0 # Kabul edilen çözüm sayısı
p1 = 0.7 # Başlangıçta daha kötü çözümü kabul etme olasılığı
p50 = 0.001 # Sonunda daha kötü çözümü kabul etme olasılığı
t1 = -1.0/math.log(p1) # Başlangıç sıcaklığı
t50 = -1.0/math.log(p50) # Son sıcaklık
frac = (t50/t1)**(1.0/(n-1.0)) # Her döngüde kesirli azalma
x = np.zeros((n+1,2)) # X'i başlat
x[0] = x_start
xi = np.zeros(2)
xi = x_start
na = na + 1.0
xc = np.zeros(2) # Şu ana kadarki en iyi sonuçlar
xc = x[0]
fc = f(xi)
fs = np.zeros(n+1)
fs[0] = fc
t = t1 # Şuanki sıcaklık
DeltaE_avg = 0.0 # DeltaE Ortalama
for i in range(n):
    print('Döngü: ' + str(i) + ' Sıcaklık : ' + str(t))
    for j in range(m):
        # Yeni deneme noktaları oluşturun
        xi[0] = xc[0] + random.random() - 0.5
        xi[1] = xc[1] + random.random() - 0.5
        # Üst ve alt sınırlara kırpın
        sinir = altust(sec)
        xi[0] = max(min(xi[0],sinir),-sinir)
        xi[1] = max(min(xi[1],sinir),-sinir)
        DeltaE = abs(f(xi)-fc)
        if (f(xi)>fc):
            # Daha kötü bir çözüm bulunursa DeltaE_avg'yi başlatın
            # ilk yinelemede
            if (i==0 and j==0): DeltaE_avg = DeltaE
            # amaç işlevi daha kötü
            # kabul olasılığı oluştur
            p = math.exp(-DeltaE/(DeltaE_avg * t))
            # daha kötü noktayı kabul edip etmeyeceğinizi belirleyin
            if (random.random()<p):
                # daha kötü çözümü kabul et
                accept = True
            else:
                # daha kötü çözümü kabul etmez
                accept = False
        else:
            # amaç işlevi daha düşük ise otomatik olarak kabul eder
            accept = True
        if (accept==True):
            # güncelleme şu anda kabul edilen çözüm
            xc[0] = xi[0]
            xc[1] = xi[1]
            fc = f(xc)
            # kabul edilen çözüm sayısını artırın
            na = na + 1.0
            # güncelle DeltaE_avg
            DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na
    # Her döngünün sonunda en iyi x değerlerini kaydedin
    x[i+1][0] = xc[0]
    x[i+1][1] = xc[1]
    fs[i+1] = fc
    # Sonraki döngü için sıcaklığı düşürün
    t = frac * t

# cevabı yazdır
print('En iyi çözüm: ' + str(xc))
print('En iyi hedef: ' + str(fc))



fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(fs,'r.-')
ax1.legend(['Objective'])
ax2 = fig.add_subplot(212)
ax2.plot(x[:,0],'b.-')
ax2.plot(x[:,1],'g--')
ax2.legend(['x1','x2'])

# Şekli PNG olarak kaydedin
plt.savefig('iterations.png')

plt.show()