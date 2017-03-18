import pygame
import random


def get_random_color():
     """
     returns a random choice of color
     """
     colors = [[255,255,255], #White
               [255,64,0],    #Red
               [255,128,0],   #Orange
               [255,204,0],   #Yellow-orange
               [192,255,0],   #Yellow-green
               [64,255,0],    #Bright green
               [0,255,128],   #Sea green
               [0,255,255],   #Aqua
               [0,128,255],   #Turquoise
               [0,48,255],    #Bright blue
               [128,0,255],   #Indigo
               [255,0,255]]   #Magenta
     return random.choice(colors)


class Particle:
	"""
	a general particle class with physics
	"""
	def __init__(self):
		self.pos_x = 0
		self.pos_y = 0
		self.len_x = 0
		self.len_y = 0
		
		self.vel_x = 0
		self.vel_y = 0
		self.acc_x = 0
		self.acc_y = 0

		self.alpha = 500
		self.alpha_decay = 0
		self.color = (255, 255, 255)

		
	def update(self):
		self.pos_x += self.vel_x
		self.pos_y += -1 * self.vel_y  # times -1 so positive vel_y is up

		self.vel_x += self.acc_x
		self.vel_y += self.acc_y

		self.alpha += self.alpha_decay


	def draw(self):
		"""
		returns dict of 'color' in a tuple of RGB vals and a pygame.Rect object
		"""
		surf = pygame.Surface((self.len_x, self.len_y))
		surf.set_alpha(self.alpha)
		surf.fill(self.color)

		pos = (self.pos_x, self.pos_y)
		
		return (surf, pos)


class Firework(Particle):

	def __init__(self, win_width, win_height):
		Particle.__init__(self)
		self.random_firework(win_width, win_height)
		self.exploded = False


	def random_firework(self, win_width, win_height):
		# position
		self.pos_x = win_width * random.random()
		self.pos_y = win_height - self.len_y  # no actual need to adjust
		
		# size
		self.len_x = random.randrange(5, 10)
		self.len_y = self.len_x

		# velocity
		self.vel_x = random.uniform(-.2, .2)
		self.vel_y = random.uniform(10, 20)

		# acceleration
		self.acc_y = -0.3

		# color
		self.color = get_random_color()


	def update(self):
		Particle.update(self)

		# explode firework if peak is reached
		if self.vel_y < 0:
			self.explode()


	def explode(self):
		self.alpha_decay = -10
		streamers = [Streamer(self.pos_x, self.pos_y) for _ in range(15)]



class Streamer(Particle):
	def __init__(self, fw_pos_x, fw_pos_y):
		Particle.__init__(self)
		self.random_streamer(fw_pos_x, fw_pos_y)
























