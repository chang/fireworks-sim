import pygame
import random
from firework import Firework, Trail, random_sound, random_patriotic_sound
from pygame.locals import *
flags = DOUBLEBUF

WIN_WIDTH = 800
WIN_HEIGHT = 600
NUM_FIREWORKS = 5
NUM_FW_STREAMERS = 30
NUM_STREAMER_STREAMERS = 5
STREAMER_TRAILS = True
STREAMER_DIST = 120
BOOM_SOUNDS = False
PATRIOTIC_MODE = False

pygame.init()
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags)
pygame.display.set_caption('Firework Show')
clock = pygame.time.Clock()

if PATRIOTIC_MODE:
	pygame.mixer.music.load("boom_sounds/NATIONAL_ANTHEM.wav")
	pygame.mixer.music.play(loops = 20)

fireworks = [Firework(WIN_WIDTH, WIN_HEIGHT, PATRIOTIC_MODE) for _ in range(NUM_FIREWORKS)]
streamers = []
trails = []


running = True
while running:

	for event in pygame.event.get():
		quit_key = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
		if event.type == pygame.QUIT or quit_key:
			running = False

	display.fill((0, 0, 0))  # reset screen to black before it's drawn
	
	new_surfaces = []
	fireworks_to_remove = []
	trails_to_remove = []
	streamers_to_remove = []

	# render all fireworks
	for i, firework in enumerate(fireworks):
		firework.update()
		(firework_rendered, firework_pos) = firework.draw()
		display.blit(firework_rendered, firework_pos)  # (0,0) are the top-left coordinates
		new_surfaces.append(firework.draw_rect())

		if firework.at_peak():
			firework.explode()
			streamers.append(firework.make_streamers(NUM_FW_STREAMERS))

			if BOOM_SOUNDS:
				if PATRIOTIC_MODE:
					boom = pygame.mixer.Sound("boom_sounds/" + random_patriotic_sound())
				else:
					boom = pygame.mixer.Sound("boom_sounds/" + random_sound())
				pygame.mixer.Sound.play(boom)

			afterglow = firework.afterglow_fullscreen(WIN_WIDTH, WIN_HEIGHT)
			display.blit(afterglow[0], afterglow[1])

		# remove from array if off screen
		if firework.vel_y < 0 and firework.pos_y > WIN_HEIGHT:
			fireworks_to_remove.append(firework)

		if firework.on_upwards_path():
			trails.append(Trail(firework.pos_x, firework.pos_y, firework.size, firework.color))

	for i, trail in enumerate(trails):
		trail.update()
		(trail_rend, trail_pos)  = trail.draw()
		display.blit(trail_rend, trail_pos)

		if trail.has_decayed():
			trails_to_remove.append(trail)

	for i, streamer_group in enumerate(streamers):
		for s in streamer_group:
			s.update()
			(s_rendered, s_pos) = s.draw()
			display.blit(s_rendered, s_pos)

			# need to optimize performance of streamer trails - over 10 fireworks causes FPS dip
			if STREAMER_TRAILS:
				trails.append(Trail(s.pos_x, s.pos_y, s.size, s.color, is_streamer = True))

		if s.dist_fallen > STREAMER_DIST:
			streamers_to_remove.append(streamer_group)

	# test firework removal
	fireworks = [fw for fw in fireworks if fw not in fireworks_to_remove]
	fireworks += [Firework(WIN_WIDTH, WIN_HEIGHT, PATRIOTIC_MODE) for _ in range(len(fireworks_to_remove))]
	trails = [t for t in trails if t not in trails_to_remove]
	streamers = [s for s in streamers if s not in streamers_to_remove]

	# reset screen and set frame rate
	print(clock.get_fps())
	pygame.display.update()
	clock.tick(60)
