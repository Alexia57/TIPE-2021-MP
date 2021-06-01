import pygame
import time
import math
import random
import matplotlib.pyplot as plt
import numpy as np



# Initialisation de l'affichage
pygame.init()
clock = pygame.time.Clock()

resolutionEcran = (600,600)
FPS = 60
greenColor = (50,210,50)
redColor = (200,10,10)
greyColor = (100,100,100)
whiteColor = (230,230,230)
blackColor = (0, 0, 0)
blueColor = (80, 150, 255)
orangeColor =(255,90,10)
arialFontFPS = pygame.font.SysFont("arial", 15)
pygame.display.set_caption("TIPE")


# Initialisation des paramètres du modèle
NombreDIndividus = 300
NombreMaladeInit_E = 0
NombreMaladeInit_I = 1
dureeInfectionMin = 600
dureeInfectionMax = 1000
dureeIncubationMin = 100
dureeIncubationMax = 200
ProbaInfectionContact = 0.2
TauxMortalite = 0.1

vacc = False
TauxVacc = 0.0005

NbCumuleInfecte = 0

NbS = NombreDIndividus - NombreMaladeInit_E - NombreMaladeInit_I
NbE = NombreMaladeInit_E
NbI = NombreMaladeInit_I
NbR = 0
NbM = 0
t = 0
listeGeneral = []

dictBalles = {}
dictBallesMortes = {}

# fonction qui retourne la somme de 2 vecteurs
def sommeVect(angle1, taille1, angle2, taille2):
    dx = math.sin(angle1)*taille1 + math.sin(angle2)*taille2
    dy = math.cos(angle1)*taille1 + math.cos(angle2)*taille2
    taille = math.hypot(dx, dy)
    angle = math.atan2(dx, dy)
    return (angle,taille,dx,dy)

# fonction qui retourne le p.s. de 2 vecteurs
def produitScalaire(angle1, taille1, angle2, taille2):
    return taille2*taille1*math.cos(angle1-angle2)

# Classe Balle qui représente un individu
class Balle(pygame.sprite.Sprite):
	global dictBalles, ProbaInfectionContact, dureeInfection, NbS, NbI, NbR
	def __init__(self, x, y, idballe, dateFinInfection = 0, dateFinIncubation=0 , vaMourir = False, masse = 1, rayon = 15, vitesse = 0, angle = 0, couleur = greenColor):
	    super(Balle, self).__init__()
	    dictBalles[idballe] = self
	    self.id = idballe
	    self.sain = True
	    self.invincible = False
	    self.contagieux = False
	    self.dureeInfection = 0
	    self.dateFinInfection = dateFinInfection
	    self.vaMourir = vaMourir
	    self.dateFinIncubation = dateFinIncubation
	    self.scoreInfection = 0
	    self.masse = masse
	    self.rayon = rayon
	    self.x = x
	    self.y = y
	    self.vitesse = vitesse
	    self.angle = angle
	    self.surface = pygame.Surface((self.rayon*2, self.rayon*2),pygame.SRCALPHA)
	    pygame.draw.circle(self.surface, couleur, [self.rayon,self.rayon], self.rayon)
	    self.mask = pygame.mask.from_surface(self.surface)
	    self.rect = self.surface.get_rect()
	# Rebond sur le contour
	def rebondContour(self):
	    if pygame.sprite.collide_mask(self, contour):
	        offx = int(self.x)
	        offy = int(self.y)
	        dx = contour.mask.overlap_area(self.mask, (offx+1,offy)) - contour.mask.overlap_area(self.mask, (offx-1,offy))
	        dy = contour.mask.overlap_area(self.mask, (offx,offy+1)) - contour.mask.overlap_area(self.mask, (offx,offy-1))
	        if dx != 0 or dy != 0:
	            if dy == 0:
	                if dx > 0:
	                    alpha = math.pi/2
	                else:
	                    alpha = 3*math.pi/2
	            else:
	                alpha = math.atan2(dx,dy)
	            
	            self.angle = math.fmod(math.pi + 2*alpha - self.angle, 2*math.pi)
	            angleN = math.atan2(dx,dy)
	            nb = contour.mask.overlap_area(self.mask, (offx,offy))
	            
	            self.x -= math.sin(angleN)*(nb/40)
	            self.y -= math.cos(angleN)*(nb/40)
	            
	            self.vitesse = self.vitesse
	            return True
	        return False
	    return False
    # Rebond entre les balles
	@staticmethod # méthode propre à la classe entière, pas associée à une Balles
	def collision(dictBalles):
		global NbS, NbE, NbI, NbCumuleInfecte

		couplesballes = []
		for couple in enumerate(dictBalles):
			couplesballes.append(couple)

		# On parcourt tous les couples de balles
		for i in range(len(couplesballes)):
			for j in range(i+1,len(couplesballes)):
				b1 = dictBalles[couplesballes[i][1]]
				b2 = dictBalles[couplesballes[j][1]]
				dx = b1.x + b1.rayon - b2.x - b2.rayon
				dy = b1.y + b1.rayon - b2.y - b2.rayon
				distance = math.hypot(dx, dy)
				# On test si le couple de balle (b1,b2) se touche
				if distance < b1.rayon + b2.rayon:
					# traitement de la collision
				    angleNormal = math.atan2(dx,dy)
				    masseTotale = b1.masse + b2.masse
				    v1nTaille = produitScalaire(b1.angle, b1.vitesse, angleNormal, 1)
				    v2nTaille = produitScalaire(b2.angle, b2.vitesse, angleNormal, 1)
				    v1nTailleP = (v1nTaille*(b1.masse - b2.masse) + 2*b2.masse*v2nTaille)/masseTotale
				    v2nTailleP = (v2nTaille*(b2.masse - b1.masse) + 2*b1.masse*v1nTaille)/masseTotale
				    (v1tAngle, v1tTaille, dxt1, dyt1) = sommeVect(b1.angle, b1.vitesse, angleNormal, -v1nTaille)
				    (v2tAngle, v2tTaille, dxt2, dyt2) = sommeVect(b2.angle, b2.vitesse, angleNormal, -v2nTaille)

				    (b1.angle, b1.vitesse, dx1, dy1) = sommeVect(v1tAngle, v1tTaille, angleNormal, v1nTailleP)
				    (b2.angle, b2.vitesse, dx2, dy2) = sommeVect(v2tAngle, v2tTaille, angleNormal, v2nTailleP)

				    depassement = (b1.rayon + b2.rayon - distance)/2
				    b1.x += math.sin(angleNormal)*depassement
				    b1.y += math.cos(angleNormal)*depassement
				    b2.x -= math.sin(angleNormal)*depassement
				    b2.y -= math.cos(angleNormal)*depassement
				    # fin de traitement de la collision
				    # traitement de la transmission de la maladie
				    if start:
				        if b1.sain and b2.contagieux:
				        	if random.random() < ProbaInfectionContact:
				        		b2.scoreInfection += 1
				        		NbS -= 1
				        		NbE += 1
				        		# changement de couleur de b1
				        		b1.surface = pygame.Surface((b1.rayon*2, b1.rayon*2),pygame.SRCALPHA)
				        		pygame.draw.circle(b1.surface, orangeColor, [b1.rayon,b1.rayon], b1.rayon)
				        		b1.mask = pygame.mask.from_surface(b1.surface)
				        		# fin changement de couleur de b1
				        		b1.sain = False
				        		b1.dateFinIncubation = random.randint(dureeIncubationMin,dureeIncubationMax)
				        		b1.dateFinInfection = random.randint(dureeInfectionMin,dureeInfectionMax)
				        		if random.random() < TauxMortalite:
				        			b1.vaMourir = True
				        elif b2.sain and b1.contagieux:
				        	if random.random() < ProbaInfectionContact:
				        		b1.scoreInfection += 1
				        		NbS -= 1
				        		NbE += 1
				        		# changement de couleur de b2
				        		b2.surface = pygame.Surface((b2.rayon*2, b2.rayon*2),pygame.SRCALPHA)
				        		pygame.draw.circle(b2.surface, orangeColor, [b2.rayon,b2.rayon], b2.rayon)
				        		b2.mask = pygame.mask.from_surface(b2.surface)
				        		# fin changement de couleur de b2
				        		b2.sain = False
				        		b2.dateFinIncubation = random.randint(dureeIncubationMin,dureeIncubationMax)
				        		b2.dateFinInfection = random.randint(dureeInfectionMin,dureeInfectionMax)
				        		if random.random() < TauxMortalite:
				        			b2.vaMourir = True
	# deplacement des balles et mise a jour de l'etat de la balle
	def move(self):
		global NbS, NbE, NbI, NbR, NbM, TauxVacc, vacc
		self.rebondContour()
		dx = math.sin(self.angle)*self.vitesse
		dy = math.cos(self.angle)*self.vitesse
		self.x += dx*60/FPS
		self.y += dy*60/FPS
		## vaccination
		if vacc:
			if self.sain:
				if random.random() < TauxVacc:
					NbS-=1
					NbR+=1
					self.surface = pygame.Surface((self.rayon*2, self.rayon*2),pygame.SRCALPHA)
					pygame.draw.circle(self.surface, blueColor, [self.rayon,self.rayon], self.rayon)
					self.mask = pygame.mask.from_surface(self.surface)
					self.invincible = True
					self.sain = False
		## maladie
		if not self.sain and not self.invincible: # on incremente de temps passé malade
			self.dureeInfection += 1
			# on regarde si la balle est à la fin de l'incubation / maladie
			if self.dureeInfection == self.dateFinIncubation:
				NbE-=1
				NbI+=1
				self.contagieux = True
				self.surface = pygame.Surface((self.rayon*2, self.rayon*2),pygame.SRCALPHA)
				pygame.draw.circle(self.surface, redColor, [self.rayon,self.rayon], self.rayon)
				self.mask = pygame.mask.from_surface(self.surface)
			elif self.dureeInfection > self.dateFinInfection:
				self.dureeInfection = 0
				self.contagieux = False
				# on regarde si la balle va mourir à la fin de sa maladie
				if self.vaMourir:
					self.surface = pygame.Surface((self.rayon*2, self.rayon*2),pygame.SRCALPHA)
					pygame.draw.circle(self.surface, blackColor, [self.rayon,self.rayon], self.rayon)
					self.mask = pygame.mask.from_surface(self.surface)
					dictBallesMortes[self.id] = self
					NbI -= 1
					NbM += 1
					return self.id
				else:
					self.surface = pygame.Surface((self.rayon*2, self.rayon*2),pygame.SRCALPHA)
					pygame.draw.circle(self.surface, greyColor, [self.rayon,self.rayon], self.rayon)
					self.mask = pygame.mask.from_surface(self.surface)
					self.invincible = True
					NbI -= 1
					NbR += 1
		return False

	# affichage 
	def draw(self, surface):
	    if math.hypot(self.x - resolutionEcran[0]/2, self.y - resolutionEcran[1]/2) > 2000:
	        self.x = resolutionEcran[0]/2
	        self.y = resolutionEcran[1]/2
	    self.rect = pygame.Rect(self.x, self.y, self.rayon*2, self.rayon*2)
	    surface.blit(self.surface, [self.x,self.y])

# Classe bordure
class Bordure(pygame.sprite.Sprite):
    def __init__(self):
        super(Bordure, self).__init__()
        self.surface = pygame.Surface(resolutionEcran, pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (164,156,189), pygame.Rect(0, 0, resolutionEcran[0], resolutionEcran[1]), width = 10)
        self.mask = pygame.mask.from_surface(self.surface)
        self.x = 0
        self.y = 0
        self.rect = self.surface.get_rect()

    def reload(self):
        self.surface = pygame.Surface(resolutionEcran, pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (164,156,189), pygame.Rect(0, 0, resolutionEcran[0], resolutionEcran[1]), width = 10)
        self.mask = pygame.mask.from_surface(self.surface)
        self.x = 0
        self.y = 0
        self.rect = self.surface.get_rect()

    def draw(self, surface):
        self.rect = pygame.Rect(self.x, self.y, resolutionEcran[0], resolutionEcran[1])
        surface.blit(self.surface, [0, 0])


# Initialisation de la creation/placement des balles
for k in range(1,NombreDIndividus+1):
	x = random.random()*(resolutionEcran[0]-60)+30
	y = random.random()*(resolutionEcran[1]-60)+30
	vitesse = 1
	angle = 2*math.pi*random.random()
	if NombreMaladeInit_I > 0:
		NombreMaladeInit_I -= 1
		dateFinInfection = random.randint(dureeInfectionMin,dureeInfectionMax)
		vaMourir = False
		if random.random() < TauxMortalite:
			vaMourir = True
		balle = Balle(x, y, idballe=k, dateFinInfection = dateFinInfection, dateFinIncubation=-1, vaMourir= vaMourir, masse = 1, rayon = 8, couleur = redColor, vitesse=vitesse, angle=angle)
		balle.sain = False
		balle.contagieux = True
	elif NombreMaladeInit_E > 0:
		NombreMaladeInit_E -= 1
		dateFinIncubation = random.randint(dureeIncubationMin,dureeIncubationMax)
		dateFinInfection = random.randint(dureeInfectionMin,dureeInfectionMax)
		vaMourir = False
		if random.random() < TauxMortalite:
			vaMourir = True
		balle = Balle(x, y, idballe=k, dateFinInfection = dateFinInfection, dateFinIncubation = dateFinIncubation, vaMourir= vaMourir, masse = 1, rayon = 8, couleur = orangeColor, vitesse=vitesse, angle=angle)
		balle.sain = False
		balle.contagieux = False
	else:
		balle = Balle(x, y, idballe=k, masse = 1, rayon = 8, vitesse=vitesse, angle=angle)

contour = Bordure()

windowSurface = pygame.display.set_mode(resolutionEcran, pygame.RESIZABLE)


running = True
start = False
end = False
affiche = False
# Boucle principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not start:
            	print("Start !")
            	start = True
            elif event.key == pygame.K_RETURN and not end:
            	print("End !")
            	end = True
            	affiche = True

    # condition vaccination
    if (NbE + NbI) > NombreDIndividus*0.4 and not vacc:
    	vacc = True
    	tVacc = t

    if start and not end:
    	listeGeneral.append([t, NbS, NbE, NbI, NbR, NbM])
    	t += 1
    	listeIdMort = []
    	for idb in dictBalles:
    		b = dictBalles[idb]
    		idmort = b.move()
    		if idmort:
    			listeIdMort.append(idmort)
    	for idb in listeIdMort:
    		del dictBalles[idb]

    Balle.collision(dictBalles)

    windowSurface.fill(whiteColor)

    for idb in dictBallesMortes:
    	b = dictBallesMortes[idb]
    	b.draw(windowSurface)

    for idb in dictBalles:
    	b = dictBalles[idb]
    	b.draw(windowSurface)

    

    contour.draw(windowSurface)
    pygame.display.flip()
    clock.tick(FPS)

    if affiche:
    	affiche = False

    	SumR = 0
    	SumCumuleInfecte = 0
    	for idb in dictBalles:
    		b = dictBalles[idb]
    		SumR += b.scoreInfection
    	for idb in dictBallesMortes:
    		b = dictBallesMortes[idb]
    		SumR += b.scoreInfection
    	R_moy = SumR / NombreDIndividus
    	print(f"Le R moyen vaut : {R_moy}")

    	listeGeneral = np.array(listeGeneral)
    	plt.figure()
    	plt.plot(listeGeneral[:,0],listeGeneral[:,1],c="g",label="sain")
    	plt.plot(listeGeneral[:,0],listeGeneral[:,2],c="orange",label="exposé")
    	plt.plot(listeGeneral[:,0],listeGeneral[:,3],c="r",label="infecté")
    	plt.plot(listeGeneral[:,0],listeGeneral[:,4],c="grey",label="retabli")
    	plt.plot(listeGeneral[:,0],listeGeneral[:,5],c="black",label="mort")
    	if vacc:
    		plt.vlines(tVacc, ymin=0, ymax=NombreDIndividus, colors="b", linestyle="dashed")
    	plt.legend()
    	plt.savefig("evolution.png")