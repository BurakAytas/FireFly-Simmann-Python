import random
import math


class FireflyAlgorithm():

    def __init__(self, D, NP, nFES, alpha, betamin, gamma, LB, UB, function):
        self.D = D  # Problemin boyutu
        self.NP = NP  # Popülasyon Boyutu
        self.nFES = nFES  # Fonksiyon değerlendirme sayısı
        self.alpha = alpha  # Alfa parametresi
        self.betamin = betamin  # Beta parametresi
        self.gamma = gamma  # Gamma parametresi
        # Fitness değerine göre Firefly türü
        self.Index = [0] * self.NP
        self.Fireflies = [[0 for i in range(self.D)]
                          for j in range(self.NP)]  # firefly faktör
        self.Fireflies_tmp = [[0 for i in range(self.D)] for j in range(
            self.NP)]  # orta düzey pop
        self.Fitness = [0.0] * self.NP  # fitness değeri
        self.I = [0.0] * self.NP  # Işık Şiddeti
        self.nbest = [0.0] * self.NP  # En iyi Çözüm (şimdilik)
        self.LB = LB  # alt sınır
        self.UB = UB  # üst sınır
        self.fbest = None  # En iyi çözüm
        self.evaluations = 0
        self.Fun = function

    def init_ffa(self):
        for i in range(self.NP):
            for j in range(self.D):
                self.Fireflies[i][j] = random.uniform(
                    0, 1) * (self.UB - self.LB) + self.LB
            self.Fitness[i] = 1.0  # çekiciliği başlatmak
            self.I[i] = self.Fitness[i]

    def alpha_new(self, a):
        delta = 1.0 - math.pow((math.pow(10.0, -4.0) / 0.9), 1.0 / float(a))
        return (1 - delta) * self.alpha

    def sort_ffa(self):  #kabarcık sıralama uygulaması
        for i in range(self.NP):
            self.Index[i] = i

        for i in range(0, (self.NP - 1)):
            j = i + 1
            for j in range(j, self.NP):
                if (self.I[i] > self.I[j]):
                    z = self.I[i]  # çekicilik alışverişi
                    self.I[i] = self.I[j]
                    self.I[j] = z
                    z = self.Fitness[i]  # değişim uygunluğu
                    self.Fitness[i] = self.Fitness[j]
                    self.Fitness[j] = z
                    z = self.Index[i]  # değişim endeksleri
                    self.Index[i] = self.Index[j]
                    self.Index[j] = z

    def replace_ffa(self):  # eski popülasyonu yeni Endeks değerlerine göre değiştirir
        # orijinal nüfusu geçici bir alana kopyalar
        for i in range(self.NP):
            for j in range(self.D):
                self.Fireflies_tmp[i][j] = self.Fireflies[i][j]

        # EA anlamında nesil seçimi
        for i in range(self.NP):
            for j in range(self.D):
                self.Fireflies[i][j] = self.Fireflies_tmp[self.Index[i]][j]

    def FindLimits(self, k): #limitleri bulur
        for i in range(self.D):
            if self.Fireflies[k][i] < self.LB:
                self.Fireflies[k][i] = self.LB
            if self.Fireflies[k][i] > self.UB:
                self.Fireflies[k][i] = self.UB

    def move_ffa(self): #firefly yönlendirir
        for i in range(self.NP):
            scale = abs(self.UB - self.LB)
            for j in range(self.NP):
                r = 0.0
                for k in range(self.D):
                    r += (self.Fireflies[i][k] - self.Fireflies[j][k]) * \
                         (self.Fireflies[i][k] - self.Fireflies[j][k])
                r = math.sqrt(r)
                if self.I[i] > self.I[j]:  # daha parlak ve daha çekici için
                    beta0 = 1.0
                    beta = (beta0 - self.betamin) * \
                           math.exp(-self.gamma * math.pow(r, 2.0)) + self.betamin
                    for k in range(self.D):
                        r = random.uniform(0, 1)
                        tmpf = self.alpha * (r - 0.5) * scale
                        self.Fireflies[i][k] = self.Fireflies[i][
                                                   k] * (1.0 - beta) + self.Fireflies_tmp[j][k] * beta + tmpf
            self.FindLimits(i)

    def Run(self):
        self.init_ffa()

        while self.evaluations < self.nFES:

            # isteğe bağlı alfa azaltımı
            self.alpha = self.alpha_new(self.nFES / self.NP)

            # yeni çözümleri değerlendirmek
            for i in range(self.NP):
                self.Fitness[i] = self.Fun(self.D, self.Fireflies[i])
                self.evaluations = self.evaluations + 1
                self.I[i] = self.Fitness[i]

            # ateş böceklerini ışık yoğunluğuna göre sıralamak
            self.sort_ffa()
            # yaşlı nüfusun yerini al
            self.replace_ffa()
            # en iyiyi bul
            self.fbest = self.I[0]
            # tüm ateş böceklerini daha iyi yerlere taşıyın
            self.move_ffa()

        return self.fbest


def Gold(D, sol): # Goldstein–Price Fonksiyonu
    obj = ((1 + (sol[0] + sol[1] + 1) ** 2 * (19 - 14 * sol[0] + 3 * (sol[0] ** 2) - 14 * sol[1] + 6 * sol[0] * sol[1] + 3 * (sol[1] ** 2))) * (30 + (2 * sol[0] - 3 * sol[1]) ** 2 * (18 - 32 * sol[0] + 12 * (sol[0] ** 2) + 48 * sol[1] - 36 * sol[0] * sol[1] + 27 * (sol[1] ** 2))))
    return obj

def Beale(D, sol): # Beale Fonksiyonu
    obj = (1.5 - sol[0] + sol[0]*sol[1])**2 + (2.25 - sol[0] + sol[0]*sol[1]**2)**2 + (2.625 - sol[0] + sol[0]*sol[1]**3)**2
    return obj

def Ackley(D, sol): # Ackley Fonksiyonu
    obj = -math.exp(-math.sqrt(0.5 * (sol[0] ** 2 + sol[1] ** 2))) - math.exp(0.5 * (math.cos(2 * math.pi * sol[0]) + math.cos(2 * math.pi * sol[1]))) + math.e + math.exp(1)
    return obj

def Levi(D, sol): # Levi Fonksiyonu
    obj = (math.sin(3*sol[0]*math.pi))**2 + ((sol[0] - 1)**2)*(1 + math.sin(3*sol[1]*math.pi)**2) + ((sol[1] - 1)**2)*(1 + math.sin(2*sol[1]*math.pi)**2)
    return obj

Algorithm = FireflyAlgorithm(2, 20, 1000, 0.5, 0.2, 1.0, -2.0, 2.0, Gold)
Best = Algorithm.Run()
print("Gold = ",Best)

Algorithm = FireflyAlgorithm(2, 20, 1000, 0.5, 0.2, 1.0, -4.5, 4.5, Beale)
Best = Algorithm.Run()
print("Beale = ",Best)

Algorithm = FireflyAlgorithm(2, 20, 1000, 0.5, 0.2, 1.0, -5.0, 5.0, Ackley)
Best = Algorithm.Run()
print("Ackley = ",Best)

Algorithm = FireflyAlgorithm(2, 20, 1000, 0.5, 0.2, 1.0, -10.0, 10.0, Levi)
Best = Algorithm.Run()
print("Levi = ",Best)


