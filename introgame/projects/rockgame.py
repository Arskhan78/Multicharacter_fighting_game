import pygame
from pygame.constants import K_SPACE
from pygame.locals import K_a, K_d, K_ESCAPE, QUIT
import random
import math

pygame.init()
pygame.font.init()

FPS = 60
WIDTH = 700
HEIGHT = 500
leftBorder = 0
groundSize = WIDTH

pygame.display.set_caption("METEOR SHOWER")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
arialFont = pygame.font.SysFont('Arial', 50)

# ---------------------------
sceneIndex = 0
timeTick = 0
score = 0

playerX = WIDTH / 2
isInvincible = False
invincibleTime = 0
playerColor = [110, 195, 200]
health = 3


meteorPos = []
meteorVelo = []
meteorSize = []

gameoverMsg = arialFont.render(f"GAME OVER, Your score is {score} ", True, [250, 0, 0])
msgRect = gameoverMsg.get_rect(center=(WIDTH/2, HEIGHT/2 - 30))
#screen.blit(gameoverMsg, msgRect)

playagain = arialFont.render("Press SPACEBAR to play again", True,[250, 0, 0])
msg2Rect = playagain.get_rect(center=(350, HEIGHT/2 + 100))
#screen.blit(playagain, msg2Rect)

play =  arialFont.render("Press SPACEBAR to play METEOR", True,[250, 0, 0])
msg3Rect = playagain.get_rect(center=(WIDTH/2.25, HEIGHT/2 - 30))
#screen.blit(play, msg3Rect)
 
scoreText = arialFont.render(str(score), True, [0, 0, 0])


def generateMeteor():
	meteorPos.append([ random.randint(int(leftBorder + 10), int(leftBorder+groundSize - 10)) , 0])
	meteorVelo.append([int(random.uniform(-100, 100)), random.randrange(250, 400)])
	meteorSize.append(random.randint(20, 35))
  # print(f"{meteorPos}\n{meteorVelo}\n-----")

def isHit(playerX, pos, size):
	distance = math.hypot(playerX + 10 - pos[0], HEIGHT - 50 - pos[1])
  	# 10 = Player Hitbox Radious
  	# size - meteor radius
	if distance < 10 + size:
		return True
	# HITBOX of player is a circle to make the game easier due to the FRAMERATE
	return False

def meteorLogic():
	for i in range(len(meteorPos)):  # For every meteor
		# If 'i'th meteor is in-screen
		if i < len(meteorPos) and \
		-meteorSize[i] < meteorPos[i][0] < WIDTH + meteorSize[i] and \
		meteorPos[i][1] < HEIGHT-40 - meteorSize[i]:
			meteorPos[i][0] += meteorVelo[i][0] / FPS 
			meteorPos[i][1] += meteorVelo[i][1] / FPS
			pygame.draw.circle(screen, [93, 80, 77], meteorPos[i], meteorSize[i])

			# Hit Check
			global isInvincible
			global health
			if meteorPos[i][1] > HEIGHT - 90:  # if meteor is close to surface
				if not isInvincible and isHit(playerX, meteorPos[i], meteorSize[i]):
					isInvincible = True
					health -= 1

		# i < len(meteorPos) is there to avoid FRAME CRASH
		# For same reason, `try` is there
		else:
			try:
				del meteorPos[i]
				del meteorVelo[i]
				del meteorSize[i]
			except:
				pass


# ----------------------------
running = True
while running:
	# ----- EVENTS -----
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
			if event.key == pygame.K_SPACE:
				if sceneIndex != 1: 
					sceneIndex = 1

	# Menu
	if sceneIndex == 0:
		screen.blit(play, msg3Rect)

	# Ingame
	elif sceneIndex == 1:
		# ----- In-game logics -----
		# Player Move (Holding is not event somehow)
		if playerX > leftBorder:
			if pygame.key.get_pressed()[K_a]:
				playerX -= 150/FPS
		else:
			playerX + 150/FPS
		
		if playerX < leftBorder + groundSize -20:
			if pygame.key.get_pressed()[K_d]:
				playerX += 150/FPS
		else:
			playerX -= 150/FPS


		# SCORE
		score = (timeTick*10) //FPS
		scoreText = arialFont.render(str(score), True, [0, 0, 0])
		

		# Border decrease
		if groundSize > WIDTH * (2/7):  # Until the 2/7 of the screen
			leftBorder = score*(3/10)	# Narrows in speed of 3/10
			groundSize = WIDTH - leftBorder*2


		# Invincible time
		if isInvincible:
			playerColor = [180, 0, 0]
			invincibleTime += 1
			if invincibleTime % (FPS * 1.5) == 0:
				isInvincible = False
				invincibleTime = 0
				playerColor = [110, 195, 200]

		# GENERATE METEOR
		if timeTick % (FPS * 0.2) == 0:  # Every n secondes
			generateMeteor()

		
		# ----- DRAWING -----
		for i in range (100): 
			screen.fill((255 - i, 255 - i, 255 - i))
		

		# GROUND
		pygame.draw.rect(screen, [137, 69, 54], [leftBorder, HEIGHT - 40, groundSize, 40])

		# Player
		pygame.draw.rect(screen, playerColor, [playerX, HEIGHT - 60, 20, 20])

		# METEOR + Hit Check
		meteorLogic()

		# UIs
		screen.blit(scoreText, [10, 50])
		for i in range(health):
			pygame.draw.rect(screen, [200,0,0], [15 + i*62,15, 60, 30])


		timeTick += 1
		if health <= 0:
			sceneIndex = 2

	# Gameover
	elif sceneIndex == 2:
		screen.fill([70,70,70])
		gameoverMsg = arialFont.render(f"GAME OVER, Your score is {score} ", True, [250, 0, 0])
		# GAMEOVER		
		screen.blit(gameoverMsg, msgRect)
		screen.blit(playagain, msg2Rect)

		health = 3
		meteorPos = []
		meteorVelo = []
		meteorSize = []
		playerX = WIDTH/2 - 10
		timeTick = 0
			
	pygame.display.flip()
	clock.tick(FPS)
	# ----LOOP ENDS HERE----

pygame.quit()