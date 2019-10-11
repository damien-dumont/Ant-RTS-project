import pygame,random,math
from pygame.locals import *

class Hero(pygame.sprite.Sprite):
	
	def __init__(self, x, y,DIRECTION,upKeyPressed,downKeyPressed,leftKeyPressed,rightKeyPressed, leftMousePressed, rightMousePressed, oneKeyPressed, HP, game):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.perso_rotated_surf = pygame.image.load("Sprites/Ant-rot.png").convert_alpha()
		self.step1 = pygame.image.load("Sprites/Ant-1.png").convert_alpha()
		self.step2 = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.step3 = pygame.image.load("Sprites/Ant-3.png").convert_alpha()
		self.step4 = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.rect = self.image.get_rect(center=(75,75))
		self.step = [self.step1,self.step2,self.step3,self.step4]
		self.perso_angle = 0
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
		self.coordx = 1920/2
		self.coordy = 1080/2
		self.centerc = None
		self.perso_angle = 0
		self.selection = 0, 0
		self.selectionned = False
		self.xdest = 0
		self.ydest = 0
		self.angledeg = 0


	def centerPos(self):
		self.center = (self.rect.x + 56, self.rect.y + 75)
		self.centerc = (self.coordx, self.coordy)

	def update(self):

		xc, yc = self.center
		xd, yd = self.selection

		if self.leftMousePressed:
			xm, ym = self.selection
			if xm >= (xc - 56) and xm < (xc + 56) and ym >= (yc - 75) and ym < (yc + 75):
				self.selectionned = True
			else:
				self.selectionned = False

		if self.rightMousePressed:
			self.xdest = xd
			self.ydest = yd
			if (xd-xc) >= 0:
				if (yd-yc) == 0:
					self.vitessey = 0
					self.vitessex = -5
				if (yd-yc) > 0:
					angled = (math.atan((xd-xc)/(yd-yc)))
					self.angledeg = ((angled*180) / 3.1415) + 90 #1
					if self.selectionned == True:
						angle2 = (self.angledeg * 3.1415) / 180
						self.vitessex = -5 * math.cos(angle2)
						self.vitessey = 5 * math.sin(angle2)
				if (yd-yc) < 0:
					angled = (math.atan((xd-xc)/(yd-yc)))
					self.angledeg = ((angled*180) / 3.1415) + 270 #2
					if self.selectionned == True:
						angle2 = (self.angledeg * 3.1415) / 180
						self.vitessex = -5 * math.cos(angle2)
						self.vitessey = 5 * math.sin(angle2)
			if (xd-xc) < 0:
				if (yd-yc) == 0:
					self.vitessey = 0
					self.vitessex = 5
				if (yd-yc) > 0:
					angled = (math.atan((xd-xc)/(yd-yc)))
					self.angledeg = ((angled*180) / 3.1415) + 90 #3
					if self.selectionned == True:
						angle2 = (self.angledeg * 3.1415) / 180
						self.vitessex = -5 * math.cos(angle2)
						self.vitessey = 5 * math.sin(angle2)
				if (yd-yc) < 0:
					angled = (math.atan((xd-xc)/(yd-yc)))
					self.angledeg = ((angled*180) / 3.1415) + 270 #4
					if self.selectionned == True:
						angle2 = (self.angledeg * 3.1415) / 180
						self.vitessex = -5 * math.cos(angle2)
						self.vitessey = 5 * math.sin(angle2)

			if self.vitessey != 0 or self.vitessex != 0:			
				self.perso_angle = (self.angledeg + 90)
				self.perso_rotated_surf = pygame.transform.rotate(self.image, self.perso_angle)
				self.rect = self.perso_rotated_surf.get_rect(center=(75,75))

		if xc >= (self.xdest - 10) and xc <= (self.xdest + 10) and yc >= (self.ydest - 10) and yc <= (self.ydest + 10):
			self.vitessex = 0
			self.vitessey = 0

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

		if self.vitessey != 0 or self.vitessex != 0:
			self.image = self.step[self.current_frame]
			self.perso_rotated_surf = pygame.transform.rotate(self.image, self.perso_angle)



class Room(object):
	wall_list = None
	def __init__(self):
		self.mob_list = pygame.sprite.Group()
		self.bullet = pygame.sprite.Group()
		self.enemy_bullet = pygame.sprite.Group()

class Room1(Room):
	def __init__(self):
		Room.__init__(self)
		self.background = pygame.image.load("room/room1.png").convert_alpha()
		mobs = []

class GameMain():
	done = False
	
	def __init__(self,width = 1920, height = 1080):
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()

		self.arial_font = pygame.font.SysFont("arial", 30)
		self.width, self.height = width, height
		pygame.display.set_caption("Space War !")
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
		self.hero = Hero(100,200,"UP",False,False,False,False,False,False,False,20, self)
		self.bullet = pygame.sprite.Group()	
		self.all_sprite_list = pygame.sprite.Group()
		self.all_sprite_list.add(self.hero)
		self.rooms = [[Room1()]]
		self.clock = pygame.time.Clock()
		self.current_x = 0
		self.current_y = 0
		self.current_room = self.rooms[self.current_y][self.current_x]
		self.hero.mobs = self.rooms[self.current_y][self.current_x].mob_list


		self.current_screen = "title"
		
	def main_loop(self):
		while not self.done:
			if self.current_screen == "game":
					self.handle_events()
					self.hero.centerPos()
					self.draw()
					self.all_sprite_list.update()
					self.hero.mobs.update()
					self.current_room.bullet.update()
					self.current_room.enemy_bullet.update()
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
		self.screen.blit(self.hero.perso_rotated_surf, self.hero.rect)
		self.current_room.mob_list.draw(self.screen)
		self.current_room.bullet.draw(self.screen)
		self.current_room.enemy_bullet.draw(self.screen)			
		pygame.display.flip()

	def change_room(self):
		if self.hero.coordx > 1921 :
			self.hero.coordx = 0
			self.current_room = self.rooms[self.current_y][self.current_x]
			bullet_hit_list = self.current_room.bullet

		elif self.hero.coordx < 0 :
			self.hero.coordx = 1919
			self.current_room = self.rooms[self.current_y][self.current_x]
			bullet_hit_list = self.current_room.bullet

		elif self.hero.coordy < 0 :
			self.hero.coordy = 1079
			self.current_room = self.rooms[self.current_y][self.current_x]
			bullet_hit_list = self.current_room.bullet


		elif self.hero.coordy > 1080 :
			self.hero.coordy = 0
			self.current_room = self.rooms[self.current_y][self.current_x]
			bullet_hit_list = self.current_room.bullet

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