import pygame
import random


def get_random_color():
     """
     returns list of colors
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


class Firework:
	def __init__(self):
		self.pos_x = 0
		self.pos_y = 0
		self.len_x = 30
		self.len_y = 30
		
		self.vel_x = 0
		self.vel_y = 15
		self.acc_x = 0
		self.acc_y = -.3

		self.alpha = 500
		self.alpha_decay = 0
		self.color = (0, 128, 255)

		pass

	def random_firework_type(self, win_width, win_height):
		# position
		self.pos_x = win_width * random.random()
		self.pos_y = win_height - self.len_y  # no actual need to adjust
		
		# size
		self.len_x = random.randrange(10, 20, 1)
		self.len_y = self.len_x

		# velocity
		self.vel_x = random.uniform(-1, 1)
		self.vel_y = random.uniform(15, 20)

		# color
		self.color = get_random_color()


	def update(self):
		self.pos_x += self.vel_x
		self.pos_y += -1 * self.vel_y  # times -1 so positive vel_y is up

		self.vel_x += self.acc_x
		self.vel_y += self.acc_y

		# begin decaying alpha at top
		if not self.alpha_decay and self.vel_y < 0:
			self.alpha_decay = -10
		self.alpha += self.alpha_decay

		pass


	def draw(self):
		"""
		returns dict of 'color' in a tuple of RGB vals and a pygame.Rect object
		"""
		fw = pygame.Surface((self.len_x, self.len_y))
		fw.set_alpha(self.alpha)
		fw.fill(self.color)

		pos = (self.pos_x, self.pos_y)
		
		return (fw, pos)















