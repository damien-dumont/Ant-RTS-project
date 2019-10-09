import pygame,random,math
from pygame.locals import *

class Hero(pygame.sprite.Sprite):
	
	def __init__(self, x, y,DIRECTION,upKeyPressed,downKeyPressed,leftKeyPressed,rightKeyPressed, leftMousePressed,HP, game):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.step1 = pygame.image.load("Sprites/Ant-1.png").convert_alpha()
		self.step2 = pygame.image.load("Sprites/Ant-mid.png").convert_alpha()
		self.step3 = pygame.image.load("Sprites/Ant-3.png").convert_alpha()
		self.right_walk = [self.right1,self.right2]
		self.left_walk = [self.left1, self.left2]
		self.up_walk = [self.up1, self.up2]
		self.down_walk = [self.down1,self.down2]
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
		self.oneKeyPressed = oneKeyPressed
		self.RIGHT, self.LEFT, self.UP, self.DOWN = "right left up down".split()
		self.game = game


		self.perso_angle = 0

		self.vitessex = 0
		self.vitessey = 0

		self.coordx = 300
		self.coordy = 300

		self.centerc = None



		self.game = game

		self.vitessex = 0
		self.accx = 0

		self.vitessey = 0
		self.accy = 0


	def walk(self):
		pass


	def centerPos(self):
		self.center = (self.rect.x + 55, self.rect.y + 74)

	def update(self):
		self.centerPos()
		for mob in self.mobs:
			mob.hero_pos = self.center

		if self.downKeyPressed:
			self.vitessex = 0.1 * math.cos((-(self.perso_angle-360)+90) * (3.14/180))
			self.vitessey = 0.1 * math.sin((-(self.perso_angle-360)+90) * (3.14/180))
			mob_hit_list = pygame.sprite.spritecollide(self, self.mobs, False)
			for mob in mob_hit_list:
				if mob.hitpoint > 0:
					self.rect.bottom = mob.rect.top
					
		if self.upKeyPressed:
			self.vitessex = -0.1 * math.cos((-(self.perso_angle-360)+90) * (3.14/180))
			self.vitessey = -0.1 * math.sin((-(self.perso_angle-360)+90) * (3.14/180))
			mob_hit_list = pygame.sprite.spritecollide(self, self.mobs, False)
			for mob in mob_hit_list:
				if mob.hitpoint > 0:
					self.rect.top = mob.rect.bottom

		if self.leftKeyPressed:
			self.perso_angle = (self.perso_angle + 1) % 360
			self.perso_rotated_surf = pygame.transform.rotate(self.image, self.perso_angle)
			self.rect = self.perso_rotated_surf.get_rect(center=self.centerc)

		if self.rightKeyPressed:
			self.perso_angle = (self.perso_angle - 1) % 360
			self.perso_rotated_surf = pygame.transform.rotate(self.image, self.perso_angle)
			self.rect = self.perso_rotated_surf.get_rect(center=self.centerc)

		self.coordx += self.vitessex
		self.rect.x = self.coordx
		self.accx = 0


		self.coordy += self.vitessey
		self.rect.y = self.coordy
		self.accy = 0


		

		#programmer sélection 
		'''
		if self.leftMousePressed:
			'''
				
		if not (self.rightKeyPressed or self.leftKeyPressed or self.upKeyPressed or self.downKeyPressed) :
			wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
			mob_hit_list = pygame.sprite.spritecollide(self, self.mobs, False)


			self.image = self.step2

			direction = self.nearest_mob_direction

			if direction == "up":
				for mob in mob_hit_list:
					if mob.hitpoint > 0:
						self.rect.bottom = mob.rect.top

			if direction == "down":				
				for mob in mob_hit_list:
					if mob.hitpoint > 0:
						self.rect.top = mob.rect.bottom

			if direction == "left":
				for mob in mob_hit_list:
					if mob.hitpoint > 0:
						self.rect.right = mob.rect.left

			if direction == "right":
				for mob in mob_hit_list:
					if mob.hitpoint > 0:
						self.rect.left = mob.rect.right

		self.ticker_weapon += 1 
		self.ticker += 1
		if self.ticker % 8 == 0:
			self.current_frame = (self.current_frame + 1) % 2



class Killed_Mob(object):
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y


 
class Room(object):
	wall_list = None
	def __init__(self):
		
class GameMain():
	done = False
	
	def __init__(self,width = 1920, height = 1080):
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()

		self.arial_font = pygame.font.SysFont("arial", 30)
		self.width, self.height = width, height
		pygame.display.set_caption("Ants")
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
		self.hero = Hero(100,200,"UP",False,False,False,False,False,False,20, self)
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
				if self.hero_isdead :
					self.handle_events_title()
					self.draw_title()
				else:
					self.handle_events()
					self.draw()
					self.all_sprite_list.update()
					self.hero.nearestMob()
					self.hero.mobs.update()
					self.current_room.bullet.update()
					self.current_room.enemy_bullet.update()
					self.change_room()
					self.killed()
			elif self.current_screen == "title":
				self.handle_events_title()
				self.draw_title()
			self.clock.tick(60)
		
		pygame.quit()
	
	def killed(self):
		bullet_hit_list = self.current_room.bullet
		for bullet in bullet_hit_list:
			for mob in self.hero.mobs:
				if  bullet.rect.x <= 0 or bullet.rect.x > 1920 or bullet.rect.y <= 0 or bullet.rect.y > 1080 :
					bullet.kill()
				if pygame.sprite.collide_rect(mob, bullet):
					mob.hitpoint -= self.hero.bullet_damage
					bullet.kill()
					if mob.hitpoint <= 0:
						mob_x, mob_y = mob.rect.x, mob.rect.y
						self.current_room.killed_mob.append(Killed_Mob(mob.name, mob_x, mob_y))
						mob.kill()
			for wall in self.hero.walls :
				if pygame.sprite.collide_rect(wall, bullet):
					bullet.kill()

		enemy_bullet_hit_list = self.current_room.enemy_bullet
		for enemy_bullet in enemy_bullet_hit_list :
			if  enemy_bullet.rect.x <= 0 or enemy_bullet.rect.x > 1920 or enemy_bullet.rect.y <= 0 or enemy_bullet.rect.y > 1080 :
				enemy_bullet.kill()
			if pygame.sprite.collide_rect(self.hero, enemy_bullet):
				self.hero.HP -= 1
				enemy_bullet.kill()
			for wall in self.hero.walls :
				if pygame.sprite.collide_rect(wall, enemy_bullet):
					enemy_bullet.kill()



	def draw_title(self):
		self.screen.fill(Color("Black"))
		credit = pygame.image.load("backgrounds/background_menu.png")
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
		self.current_room.planet.draw(self.screen)				
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
			
			elif event.type == MOUSEMOTION :
				self.hero.bullet_direction = event.pos

			elif event.type == MOUSEBUTTONUP :
				if pygame.mouse.get_pressed() == (0, 0, 0):
					self.hero.leftMousePressed = False


if __name__ == "__main__":
	game = GameMain()
	game.main_loop()
