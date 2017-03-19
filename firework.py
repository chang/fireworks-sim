import pygame
import random

GRAVITY = -.3

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


def get_random_patriotic_color():
     """
     returns a random choice of color
     """
     colors = [[255,255,255], #White
               [224,22,43],    #Red
               [100,150,255]]    #Bright blue
     return random.choice(colors)


class Particle:
	"""
	a general particle class with physics
	"""
	def __init__(self):
		self.pos_x = 0
		self.pos_y = 0
		self.size = 0
		
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

	def is_off_screen(self):
		return self.pos_y > win_height

	def draw(self):
		surf = pygame.Surface((self.size, self.size))
		surf.set_alpha(self.alpha)
		surf.fill(self.color)

		pos = (self.pos_x, self.pos_y)

		return (surf, pos)

	def draw_rect(self):
		return pygame.Rect(self.pos_y, self.pos_x, self.size, self.size)


class Firework(Particle):
	"""
	single firework shell
	"""
	def __init__(self, win_width, win_height, patriotic_mode):
		Particle.__init__(self)
		self.patriotic_mode = patriotic_mode
		self.random_firework(win_width, win_height)
		self.exploded = False

	def random_firework(self, win_width, win_height):
		# position
		self.pos_x = random.normalvariate(win_width / 2, win_width / 3)
		self.pos_y = random.uniform(win_height, win_height + 20)  # no actual need to adjust
		
		# size
		self.size = random.randrange(5, 10)

		# velocity
		self.vel_x = random.uniform(-.2, .2)
		self.vel_y = random.uniform(10, 16)

		# acceleration
		self.acc_y = GRAVITY

		# color
		if self.patriotic_mode:
			self.color = get_random_patriotic_color()
		else:
			self.color = get_random_color()

	def update(self):
		Particle.update(self)
		if self.vel_y < 0:  # explode firework if peak is reached
			self.explode()

	def explode(self):
		self.alpha = 0
		self.exploded = True

	def glow(self):
		"""surrounds firework shell with glow"""
		pass

	def afterglow(self):
		"""flash of light that appears immediately after explosion"""
		afterglow_size_multiplier = 30

		ag_size = afterglow_size_multiplier * self.size
		surf = pygame.Surface((ag_size, ag_size))
		surf.set_alpha(100)
		surf.fill((255, 255, 255))
		pos = (self.pos_x - 0.5 * ag_size, self.pos_y - 0.5 * ag_size)

		return (surf, pos)

	def afterglow_fullscreen(self, win_width, win_height):
		"""flash of light that appears immediately after explosion"""
		surf = pygame.Surface((win_width, win_height))
		surf.set_alpha(100)
		surf.fill(self.color)
		pos = (0, 0)

		return (surf, pos)

	def make_streamers(self, n):
		streamers = [Streamer(self.pos_x, self.pos_y, self.size, self.color) for _ in range(n)]
		return streamers

	def at_peak(self):
		return self.vel_y < random.uniform(0, 2) and not self.exploded

	def on_upwards_path(self):
		return self.vel_y > 0


class Streamer(Particle):
	"""
	particles that shoot out from shell once exploded
	"""
	def __init__(self, pos_x, pos_y, fw_size, color):
		Particle.__init__(self)
		self.pos_x = pos_x
		self.pos_y = pos_y
		# self.acc_x = -.2

		self.color = color
		self.alpha = 300

		self.dist_fallen = 0
		self.fw_size = fw_size
		self.exploded = False

		self.random_streamer()  # is this good practice?

	def random_streamer(self):
		self.size = random.uniform(0.3 * self.fw_size, 0.6 * self.fw_size)

		self.vel_x = random.uniform(-5, 5)
		self.vel_y = random.uniform(0, 12)

		self.acc_y = GRAVITY + random.uniform(-0.1, 0)

		self.alpha_decay = random.uniform(-7, -5)

	def update(self):
		Particle.update(self)
		self.dist_fallen += -1 * self.vel_y


class Trail(Particle):
	"""
	smoke trail for the fireworks and streamers
	"""
	def __init__(self, pos_x, pos_y, size, color, is_streamer = False):
		Particle.__init__(self)
		self.pos_x, self.pos_y = pos_x, pos_y
		self.size = size
		self.color = color

		# trail specific vars
		self.size_decay = 0.07 * self.size  # in pixels per frame
		self.life = 0  # in frames
		self.decay_time = .2  # in seconds

		self.alpha = self.alpha * 0.2
		self.alpha_decay = self.alpha / 60 * self.decay_time
		self.is_streamer = is_streamer

		self.random_trail()

	def random_trail(self):
		self.pos_x += random.uniform(-0.3 * self.size, 0.3 * self.size)

	def update(self):
		Particle.update(self)
		self.life += 1
		self.pos_x += 0.5 * self.size_decay
		self.size -= self.size_decay

	def has_decayed(self):
		if self.is_streamer:
			return self.life > self.decay_time * 60 * 0.3
		else:
			return self.life > self.decay_time * 60

def random_sound():
	"""
	returns random BOOM sound
	"""
	sounds = ['BAWM.wav', 'BABABAWM.wav', 'OOGABOOGA.wav']
	return random.choice(sounds)

def random_patriotic_sound():
	"""
	returns random all-american sound
	"""
	sounds = ['MURICA.wav', 'CAW.wav', 'CAWCAW.wav']
	return random.choice(sounds)
