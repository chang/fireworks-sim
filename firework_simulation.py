import pygame
import random
from firework import Firework


WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60

# init all pygame vars
pygame.init()
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('hi')
clock = pygame.time.Clock()

# create fireworks
fireworks = []
streamers = []
for _ in range(7):
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

		# explode if at peak
		if firework.vel_y < random.uniform(0, 2) and not firework.exploded:
			firework.explode()
			streamers.append(firework.make_streamers(50))
			firework.exploded = True

		# remove from array if off screen
		if firework.vel_y < 0 and firework.pos_y > WIN_HEIGHT:
			fireworks.pop(i)
			fireworks.append(Firework(WIN_WIDTH, WIN_HEIGHT))


	for i,streamer_group in enumerate(streamers):
		for s in streamer_group:
			s.update()
			(s_rendered, s_pos) = s.draw()
			display.blit(s_rendered, s_pos)

		# remove streamer group if fallen far enough
		if s.dist_fallen > 200:
			streamers.pop(i)


	# reset screen and set frame rate
	pygame.display.flip()
	clock.tick(FPS)
