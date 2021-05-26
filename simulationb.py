import pygame
import time
import math
import random
import matplotlib.pyplot as plt
import numpy as np


pygame.init()
clock = pygame.time.Clock()

resolutionEcran = (600,600)
FPS = 60
greenColor = (50,255,50)
redColor = (255,50,50)
greyColor = (100,100,100)
whiteColor = (230,230,230)
blackColor = (0, 0, 0)
blueColor = (80, 150, 255)
arialFontFPS = pygame.font.SysFont("arial", 15)
pygame.display.set_caption("TIPE")

NombreDIndividus = 300
NombreMaladeInit = 1
dureeInfectionMin = 600
dureeInfectionMax = 1000
ProbaInfectionContact = 0.2
TauxMortalite = 0.1


NbS = NombreDIndividus - NombreMaladeInit
NbI = NombreMaladeInit
NbR = 0
NbM = 0
t = 0
listeGeneral = []

dictBalles = {}
dictBallesMortes = {}

def sommeVect(angle1, taille1, angle2, taille2):
    dx = math.sin(angle1)*taille1 + math.sin(angle2)*taille2
    dy = math.cos(angle1)*taille1 + math.cos(angle2)*taille2
    taille = math.hypot(dx, dy)
    angle = math.atan2(dx, dy)
    return (angle,taille,dx,dy)

def produitScalaire(angle1, taille1, angle2, taille2):
    return taille2*taille1*math.cos(angle1-angle2)

class Balle(pygame.sprite.Sprite):
	global dictBalles, ProbaInfectionContact, dureeInfection, NbS, NbI, NbR
	def __init__(self, x, y, idballe, dateFinInfection = 0, vaMourir = False, masse = 1, rayon = 15, vitesse = 0, angle = 0, couleur = greenColor):
	    super(Balle, self).__init__()
	    dictBalles[idballe] = self
	    self.id = idballe
	    self.sain = True
	    self.contagieux = False
	    self.dureeInfection = 0
	    self.dateFinInfection = dateFinInfection
	    self.vaMourir = vaMourir
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

	def rebondContour(self):
	    if pygame.sprite.collide_mask(self, contour) and selectedBalle != self:
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
	            
	            self.x -= math.sin(angleN)*(nb/40)#(math.sin(self.angle)*self.vitesse/1.8)*60/FPS
	            self.y -= math.cos(angleN)*(nb/40)#(math.cos(self.angle)*self.vitesse/1.8)*60/FPS
	            
	            self.vitesse = self.vitesse
	            return True
	        return False
	    return False
        
	@staticmethod
	def collision(dictBalles):
		global NbS, NbI

		couplesballes = []
		for couple in enumerate(dictBalles):
			couplesballes.append(couple)

		for i in range(len(couplesballes)):
			for j in range(i+1,len(couplesballes)):
				b1 = dictBalles[couplesballes[i][1]]
				b2 = dictBalles[couplesballes[j][1]]
				dx = b1.x + b1.rayon - b2.x - b2.rayon
				dy = b1.y + b1.rayon - b2.y - b2.rayon
				distance = math.hypot(dx, dy)
				if distance < b1.rayon + b2.rayon:
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

				    if start:
				        if b1.sain and b2.contagieux:
				        	if random.random() < ProbaInfectionContact:
				        		NbS -= 1
				        		NbI += 1
				        		b1.surface = pygame.Surface((b1.rayon*2, b1.rayon*2),pygame.SRCALPHA)
				        		pygame.draw.circle(b1.surface, redColor, [b1.rayon,b1.rayon], b1.rayon)
				        		b1.mask = pygame.mask.from_surface(b1.surface)
				        		b1.contagieux = True
				        		b1.sain = False
				        		b1.dateFinInfection = random.randint(dureeInfectionMin,dureeInfectionMax)
				        		if random.random() < TauxMortalite:
				        			b1.vaMourir = True
				        elif b2.sain and b1.contagieux:
				        	if random.random() < ProbaInfectionContact:
				        		NbS -= 1
				        		NbI += 1
				        		b2.surface = pygame.Surface((b2.rayon*2, b2.rayon*2),pygame.SRCALPHA)
				        		pygame.draw.circle(b2.surface, redColor, [b2.rayon,b2.rayon], b2.rayon)
				        		b2.mask = pygame.mask.from_surface(b2.surface)
				        		b2.contagieux = True
				        		b2.sain = False
				        		b2.dateFinInfection = random.randint(dureeInfectionMin,dureeInfectionMax)
				        		if random.random() < TauxMortalite:
				        			b2.vaMourir = True

	def move(self):
		global NbS, NbI, NbR, NbM
		self.rebondContour()
		dx = math.sin(self.angle)*self.vitesse
		dy = math.cos(self.angle)*self.vitesse
		self.x += dx*60/FPS
		self.y += dy*60/FPS
		## maladie
		if not self.sain and self.contagieux:
			self.dureeInfection += 1
		if self.dureeInfection > self.dateFinInfection:
			self.dureeInfection = 0
			self.contagieux = False
			if self.vaMourir:
				self.surface = pygame.Surface((self.rayon*2, self.rayon*2),pygame.SRCALPHA)
				pygame.draw.circle(self.surface, whiteColor, [self.rayon,self.rayon], self.rayon)
				self.mask = pygame.mask.from_surface(self.surface)
				dictBallesMortes[self.id] = self
				NbI -= 1
				NbM += 1
				return self.id
			else:
				self.surface = pygame.Surface((self.rayon*2, self.rayon*2),pygame.SRCALPHA)
				pygame.draw.circle(self.surface, greyColor, [self.rayon,self.rayon], self.rayon)
				self.mask = pygame.mask.from_surface(self.surface)
				NbI -= 1
				NbR += 1
		return False


	def draw(self, surface):
	    if math.hypot(self.x - resolutionEcran[0]/2, self.y - resolutionEcran[1]/2) > 2000:
	        self.x = resolutionEcran[0]/2
	        self.y = resolutionEcran[1]/2
	    self.rect = pygame.Rect(self.x, self.y, self.rayon*2, self.rayon*2)
	    surface.blit(self.surface, [self.x,self.y])


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


for k in range(1,NombreDIndividus+1):
	x = random.random()*(resolutionEcran[0]-60)+30
	y = random.random()*(resolutionEcran[1]-60)+30
	vitesse = 1
	angle = 2*math.pi*random.random()
	if NombreMaladeInit > 0:
		NombreMaladeInit -= 1
		dateFinInfection = random.randint(dureeInfectionMin,dureeInfectionMax)
		vaMourir = False
		if random.random() < TauxMortalite:
			vaMourir = True
		balle = Balle(x, y, idballe=k, dateFinInfection = dateFinInfection ,vaMourir= vaMourir, masse = 1, rayon = 8, couleur = redColor, vitesse=vitesse, angle=angle)
		balle.sain = False
		balle.contagieux = True
	else:
		balle = Balle(x, y, idballe=k, masse = 1, rayon = 8, vitesse=vitesse, angle=angle)

contour = Bordure()

windowSurface = pygame.display.set_mode(resolutionEcran, pygame.RESIZABLE)

def findBalle(x, y):
	for idb in dictBalles:
		b = dictBalles[idb]
		if math.hypot(b.x-x + b.rayon, b.y-y + b.rayon) <= b.rayon:
		    return b
	return None


selectedBalle = None
running = True
start = False
end = False
affiche = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            resolutionEcran = event.size
            contour.reload()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mousex, mousey) = pygame.mouse.get_pos()
            selectedBalle = findBalle(mousex,mousey)
        elif event.type == pygame.MOUSEBUTTONUP:
            selectedBalle = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                energieCinetique = 0
                for idb in dictBalles:
                	b = dictBalles[idb]
                	energieCinetique += (b.masse*b.vitesse**2)/2
                print("Energie cinétique du système : ",energieCinetique)
            if event.key == pygame.K_RETURN and not start:
            	print("Start !")
            	start = True
            elif event.key == pygame.K_RETURN and not end:
            	print("End !")
            	end = True
            	affiche = True

    if selectedBalle:
        (mousex, mousey) = pygame.mouse.get_pos()
        dx = mousex - selectedBalle.x - selectedBalle.rayon
        dy = mousey - selectedBalle.y - selectedBalle.rayon
        selectedBalle.angle = math.atan2(dx,dy)
        selectedBalle.vitesse = math.hypot(dx,dy)/5

    if start and not end:
    	listeGeneral.append([t, NbS, NbI, NbR, NbM])
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

    windowSurface.fill(blackColor)

    for idb in dictBallesMortes:
    	b = dictBallesMortes[idb]
    	b.draw(windowSurface)

    for idb in dictBalles:
    	b = dictBalles[idb]
    	b.draw(windowSurface)

    

    contour.draw(windowSurface)

    windowSurface.blit(arialFontFPS.render(f"{int(clock.get_fps())} FPS", True, blueColor), [5, 5])
    pygame.display.flip()

    clock.tick(FPS)

    if affiche:
    	affiche = False
    	listeGeneral = np.array(listeGeneral)
    	plt.figure()
    	plt.plot(listeGeneral[:,0],listeGeneral[:,1],label="sain")
    	plt.plot(listeGeneral[:,0],listeGeneral[:,2],label="infecté")
    	plt.plot(listeGeneral[:,0],listeGeneral[:,3],label="retablie")
    	plt.plot(listeGeneral[:,0],listeGeneral[:,4],label="mort")
    	plt.legend()
    	plt.savefig("evolution.png")