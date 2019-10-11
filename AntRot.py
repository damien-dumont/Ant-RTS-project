import pygame,random,math
from pygame.locals import *

class Hero(pygame.sprite.Sprite):
	
	def __init__(self, x, y,DIRECTION,upKeyPressed,downKeyPressed,leftKeyPressed,rightKeyPressed, leftMousePressed, rightMousePressed, oneKeyPressed, HP, game, pos=(0, 0), size=(150, 150)):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.original_image = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.original_image = pygame.Surface(size)
		pygame.draw.line(self.original_image, (255, 0, 255), (size[0] / 2, 0), (size[0] / 2, size[1]), 3)
		pygame.draw.line(self.original_image, (0, 255, 255), (size[1], 0), (0, size[1]), 3)
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.angle = 0


		self.step1 = pygame.image.load("Sprites/Ant-1.png").convert_alpha()
		self.step2 = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.step3 = pygame.image.load("Sprites/Ant-3.png").convert_alpha()
		self.step4 = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.step = [self.step1,self.step2,self.step3,self.step4]
		self.ticker = 0
		self.rect.x = x
		self.rect.y = y
		self.center = None
		self.DIRECTION = DIRECTION
		self.upKeyPressed = upKeyPressed
		self.downKeyPressed = downKeyPressed
		self.leftKeyPressed = leftKeyPressed
		self.rightKeyPressed = rightKeyPressed
		self.leftMousePressed = leftMousePressed
		self.rightMousePressed = rightMousePressed
		self.oneKeyPressed = oneKeyPressed
		self.RIGHT, self.LEFT, self.UP, self.DOWN = "right left up down".split()
		self.game = game
		self.current_frame = 0

		self.vitessex = 0
		self.accx = 0
		self.vitessey = 0
		self.accy = 0
		self.coordx = 300
		self.coordy = 300

		self.centerc = None
		self.perso_angle = 0

		self.selection = None
		self.selectionned = False



	def update(self):


		if self.downKeyPressed:
			self.accx = 0.1 * math.cos((-(self.perso_angle-360)+90) * (3.14/180))
			self.accy = 0.1 * math.sin((-(self.perso_angle-360)+90) * (3.14/180))

			self.image = self.step[self.current_frame]
					
		if self.upKeyPressed:
			self.accx = -0.1 * math.cos((-(self.perso_angle-360)+90) * (3.14/180))
			self.accy = -0.1 * math.sin((-(self.perso_angle-360)+90) * (3.14/180))

			self.image = self.step[self.current_frame]

		if self.leftKeyPressed:
			self.image = pygame.transform.rotate(self.original_image, self.angle)
			self.angle += 5 % 360  # Value will reapeat after 359. This prevents angle to overflow.
			x, y = self.rect.center  # Save its current center.
			self.rect = self.image.get_rect()  # Replace old rect with new rect.
			self.rect.center = (x, y)  # Put the new rect's center at old center.

		if self.rightKeyPressed:
			self.image = pygame.transform.rotate(self.original_image, self.angle)
			self.angle -= 5 % 360  # Value will reapeat after 359. This prevents angle to overflow.
			x, y = self.rect.center  # Save its current center.
			self.rect = self.image.get_rect()  # Replace old rect with new rect.
			self.rect.center = (x, y)  # Put the new rect's center at old center.

		xc, yc = self.rect.center

		if self.leftMousePressed:
			xm, ym = self.selection
			if xm >= (xc):
				if xm < (xc + 150):
					if ym >= (yc):
						if ym < (yc + 150):
							self.selectionned = True
						else:
							self.selectionned = False
					else:
						self.selectionned = False
				else:
					self.selectionned = False
			else:
				self.selectionned = False

		if self.rightMousePressed:
			xd, yd = self.selection
			angled = (math.atan((xd-xc)/(yd-yc)))
			if (xd-xc) >= 0:
				if (yd-yc) >= 0:
					angledeg = ((angled*180) / 3.1415) + 180
					if self.selectionned == True:
						self.angle = angledeg
						self.vitessex = 10 * math.cos(angled)
						self.vitessey = 10 * math.sin(angled)
				if (yd-yc) < 0:
					angledeg = ((angled*180) / 3.1415) + 180
					if self.selectionned == True:
						self.angle = angledeg
						self.vitessex = 10 * math.cos(angled)
						self.vitessey = 10 * math.sin(angled)
			if (xd-xc) < 0:
				angledeg = ((angled*180) / 3.1415) + 180
				if self.selectionned == True:
					self.angle = angledeg
					self.vitessex = 10 * math.cos(angled)
					self.vitessey = 10 * math.sin(angled)

		print(self.angle)
		self.ticker += 1
		if self.ticker % 8 == 0:
			self.current_frame = (self.current_frame + 1) % 4

		self.vitessex += self.accx
		self.coordx += self.vitessex
		self.rect.x = self.coordx
		self.accx = 0


		self.vitessey += self.accy
		self.coordy += self.vitessey
		self.rect.y = self.coordy
		self.accy = 0


class Room(object):
	wall_list = None
	def __init__(self):
		self.killed_mob = []

class Room1(Room):
	def __init__(self):
		Room.__init__(self)
		self.background = pygame.image.load("room/room1.png").convert_alpha()

class GameMain():
	done = False

	def __init__(self,width = 1920, height = 1080):
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()

		self.arial_font = pygame.font.SysFont("arial", 30)
		self.width, self.height = width, height
		pygame.display.set_caption("Space War !")
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
		self.hero = Hero(100,200,"UP",False,False,False,False,False,False,False,20, self, pos=(150, 150))
		self.all_sprite_list = pygame.sprite.Group()
		self.all_sprite_list.add(self.hero)
		self.rooms = [[Room1()]]
		self.clock = pygame.time.Clock()
		self.current_x = 0
		self.current_y = 0
		self.current_room = self.rooms[self.current_y][self.current_x]

		self.current_screen = "title"
		
	def main_loop(self):
		while not self.done:
			if self.current_screen == "game":
					self.handle_events()
					self.draw()
					self.all_sprite_list.update()
					self.change_room()
			elif self.current_screen == "title":
				self.handle_events_title()
				self.draw_title()
			self.clock.tick(60)
		
		pygame.quit()

	def draw_title(self):
		self.screen.fill(Color("Black"))
		credit = pygame.image.load("background_menu.jpg")
		self.screen.blit(credit,(0,0))
		pygame.display.flip()

	def handle_events_title(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					self.current_screen = "game"
				if event.key == K_F4 :
					self.done = True
		
	def draw(self):
		self.screen.fill((255,255, 255))
		background = self.current_room.background
		self.screen.blit(background,(0,0))
		self.all_sprite_list.draw(self.screen)			
		pygame.display.flip()

	def change_room(self):
		if self.hero.coordx > 1921 :
			self.hero.coordx = 0
			self.current_room = self.rooms[self.current_y][self.current_x]

		elif self.hero.coordx < 0 :
			self.hero.coordx = 1919
			self.current_room = self.rooms[self.current_y][self.current_x]

		elif self.hero.coordy < 0 :
			self.hero.coordy = 1079
			self.current_room = self.rooms[self.current_y][self.current_x]

		elif self.hero.coordy > 1080 :
			self.hero.coordy = 0
			self.current_room = self.rooms[self.current_y][self.current_x]

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type == KEYDOWN :
				if event.key == (K_LALT and K_F4):
					self.done = True
				elif event.key == K_w:
					self.hero.upKeyPressed = True
					self.hero.downKeyPressed = False
				elif event.key == K_s:
					self.hero.downKeyPressed = True
					self.hero.upKeyPressed = False
				elif event.key == K_a:
					self.hero.leftKeyPressed = True
					self.hero.rightKeyPressed = False
				elif event.key == K_d:
					self.hero.rightKeyPressed = True
					self.hero.leftKeyPressed = False
				elif event.key == K_q:
					self.hero.oneKeyPressed = True

			elif event.type == KEYUP:
				if event.key == K_w:
					self.hero.upKeyPressed = False
				elif event.key == K_s:					
					self.hero.downKeyPressed = False

				elif event.key == K_a:				
					self.hero.leftKeyPressed = False

				elif event.key == K_d:					
					self.hero.rightKeyPressed = False

				elif event.key == K_q:
					self.hero.oneKeyPressed = False

			if event.type == MOUSEBUTTONDOWN :
				if pygame.mouse.get_pressed() == (1, 0, 0):
					self.hero.leftMousePressed = True

				if pygame.mouse.get_pressed() == (0, 0, 1):
					self.hero.rightMousePressed = True

			elif event.type == MOUSEMOTION :
				self.hero.selection = event.pos

			elif event.type == MOUSEBUTTONUP :
				if pygame.mouse.get_pressed() == (0, 0, 0):
					self.hero.leftMousePressed = False

				if pygame.mouse.get_pressed() == (0, 0, 0):
					self.hero.rightMousePressed = False

if __name__ == "__main__":
	game = GameMain()
	game.main_loop()