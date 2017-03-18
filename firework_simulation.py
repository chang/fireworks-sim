import pygame
from firework import Firework


# consts
WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60

# init all pygame functionality
pygame.init()
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('hi')
clock = pygame.time.Clock()

# create fireworks
fireworks = []
for _ in range(10):
	fw = Firework(WIN_WIDTH, WIN_HEIGHT)
	fireworks.append(fw)



### RUN PYGAME
running = True
while running:

	for event in pygame.event.get():
		# print(event)  # log event
		quit_key = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
		if event.type == pygame.QUIT or quit_key:
			running = False

	display.fill((0, 0, 0))  # reset screen to black before it's drawn
	
	
	# render all fireworks
	for i,firework in enumerate(fireworks):
		firework.update()
		(firework_rendered, firework_pos) = firework.draw()
		display.blit(firework_rendered, firework_pos)  # (0,0) are the top-left coordinates

		# remove from array if off screen
		if firework.vel_y < 0 and firework.pos_y > WIN_HEIGHT:
			fireworks.pop(i)
			fireworks.append(Firework(WIN_WIDTH, WIN_HEIGHT))

			


	# reset screen and set frame rate
	pygame.display.flip()
	clock.tick(FPS)









