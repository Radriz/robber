import pygame
from models import *  # импорт всех классов
import random


class Level():
    def __init__(self, screen, width, height, save):
        self.move = Movement
        self.save = save
        self.width = width
        self.height = height
        self.screen = screen
        self.ground = 127
        self.monstr = []
        self.cur_res_font = pygame.font.Font(None, 50)
        self.human = Stand_Human((width / 4, height - self.ground))  # создаем объект класса
        self.house = House((1470, height - self.ground - 60))
        self.door = Door((1469, height - self.ground + 10))
        self.boiler = Boiler((100, height - self.ground - 10))
        self.platform = Platform((750, height - self.ground - 30))
        self.button = pygame.Rect(width // 2 - 200, height // 2 - 250, 400, 300)
        self.gold = Gold_coins((99, 600))
        self.back_ground = Background(self.width, self.height)
        self.list_gold = []
        self.in_boiler = False  # контролирует находился ли я шаг назад в бойлере
        self.acc = 3  # ускорение
        self.vel = None  # скорость передвижения
        self.RED_MONSTER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.RED_MONSTER_EVENT, 3000)

    def check_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.vel = -35
            elif event.type == self.RED_MONSTER_EVENT:
                mon = Red_Monster((random.randint(200, self.width - 300), self.height - self.ground - 850))
                self.monstr.append(mon)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = list(pygame.mouse.get_pos())  # [x,y]
                if event.button == 1 and self.button.collidepoint(mouse_position[0], mouse_position[1]):
                    return True

    def update_action(self):
        pressed = pygame.key.get_pressed()
        human_width, human_hight = self.human.image.get_size()
        if self.vel is not None:  # скорость None когда он стоит на земле
            self.vel += self.acc
            self.human.rect.centery += self.vel
            if pygame.sprite.collide_rect(self.human, self.platform):  # стоять на платформе
                self.human.rect.centery = self.height - self.ground - 178
                self.vel = 0

        if self.human.rect.centery >= self.height - self.ground:  # приземление и фиксирование на земле
            self.human.rect.centery = self.height - self.ground
            self.vel = None
        if self.human.rect.centery < human_width // 2:  # уперся наверх
            self.human.rect.centery = human_width // 2
            self.vel = 0

        for mon in self.monstr.copy():
            mon.rect.centery += 3
            if mon.rect.centery > self.height + 100:
                self.monstr.remove(mon)
            if pygame.sprite.collide_mask(self.human, mon):
                self.human.gold = False
        if pressed[
            pygame.K_LEFT] and self.human.rect.centerx - human_width // 2 > 100:  # человек упирается влево от экрана на половину своего размера
            self.human.rect.centerx -= 15  # скорость его движения
            if pygame.sprite.collide_mask(self.human, self.platform):
                self.human.rect.centerx += 15
            self.human = Movement(self.human.rect.center, self.human.gold)
            self.human.flip("l")
        if pressed[pygame.K_RIGHT] and self.human.rect.centerx + human_width // 2 < 1500:
            self.human.rect.centerx += 15
            if pygame.sprite.collide_mask(self.human, self.platform):
                self.human.rect.centerx -= 15
            self.human = Movement(self.human.rect.center, self.human.gold)
            self.human.flip("r")

    def show(self):
        self.screen.fill((255, 255, 255))  # очистка экрана приложения

        self.screen.blit(self.back_ground.image, self.back_ground.rect)  # наложение заднего фона
        self.screen.blit(self.human.image, self.human.rect)
        self.screen.blit(self.house.image, self.house.rect)
        self.screen.blit(self.boiler.image, self.boiler.rect)
        self.screen.blit(self.platform.image, self.platform.rect)

        for mon in self.monstr:
            self.screen.blit(mon.image, mon.rect)
        cur_res = self.cur_res_font.render(f"в банке {len(self.list_gold)} руб.", True, (255, 0, 0))  # текст результата
        res_rect = cur_res.get_rect()
        res_rect.center = (130, self.height - self.ground - 130)
        self.screen.blit(cur_res, res_rect)
        if pygame.sprite.collide_mask(self.human, self.house) and self.human.rect.centerx > 620:  # он зашел в дом
            self.human.gold = True
            self.screen.blit(self.door.image, self.door.rect)

        if pygame.sprite.collide_mask(self.human, self.boiler) and self.human.rect.centerx < 200:
            if self.in_boiler == False and self.human.gold == True:
                gold = Gold_coins((random.randint(90, 120),
                                   random.randint(self.height - self.ground - 30, self.height - self.ground - 10)))
                self.list_gold.append(gold)
                self.human.gold = False
            self.in_boiler = True
        else:
            self.in_boiler = False
        for gold in self.list_gold:
            self.screen.blit(gold.image, gold.rect)
        if len(self.list_gold) == 1:
            pygame.draw.rect(self.screen, "green", self.button, 999, 30)
            button_text = self.cur_res_font.render(f" next level ", True, (0, 0, 0))
            button_text_rect = button_text.get_rect()
            button_text_rect.center = (self.width // 2, self.height - self.ground - 370)
            self.screen.blit(button_text, button_text_rect)


class Level_two(Level):
    def __init__(self, screen, width, height, save):
        super().__init__(screen, width, height, save)
        # self.ak_47 = AK_47((random.randint(100, self.height - 100), random.randint(0, self.width - 400)))
        self.ak_47 = AK_47((400, 500))
        self.with_gun = False
        self.bullets = []
        self.kill_monster = 0
        pygame.time.set_timer(self.RED_MONSTER_EVENT, 2000)
        self.fireballs = []
        self.FIREBALLS_EVENT = pygame.USEREVENT + 2

    def check_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.vel = -35
                elif event.key == pygame.K_d and self.with_gun:
                    bullet = Bullet(
                        (self.ak_47.rect.centerx + self.ak_47.image.get_width() // 2
                         if self.ak_47.direction == "r"
                         else self.ak_47.rect.centerx - self.ak_47.image.get_width() // 2, self.ak_47.rect.centery))
                    bullet.flip(self.ak_47.direction)
                    self.bullets.append(bullet)
            elif self.FIREBALLS_EVENT == event.type:
                centr = None
                for mon in self.monstr:
                    if isinstance(mon, Big_Monster):  # он возвращает тру если  объекта MOn
                        centr = mon.rect.center

                fireball_r = Fireball((centr[0], random.randint(centr[1] - 100, centr[1] + 100)))
                fireball_l = Fireball((centr[0], random.randint(centr[1] - 100, centr[1] + 100)))
                fireball_r.direction = "r"
                fireball_l.direction = "l"
                self.fireballs.append(fireball_l)
                self.fireballs.append(fireball_r)
            elif event.type == self.RED_MONSTER_EVENT:
                if self.kill_monster < 3:
                    mon = Red_Monster((random.randint(200, self.width - 300), self.height - self.ground - 850))
                else:
                    mon = Big_Monster((random.randint(300, self.width - 400), self.height - self.ground - 850))
                    self.kill_monster = 0
                self.monstr.append(mon)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = list(pygame.mouse.get_pos())  # [x,y]
                if event.button == 1 and self.button.collidepoint(mouse_position[0], mouse_position[1]):
                    return True

    def update_action(self):
        pressed = pygame.key.get_pressed()
        human_width, human_hight = self.human.image.get_size()
        if self.vel is not None:  # скорость None когда он стоит на земле
            self.vel += self.acc
            self.human.rect.centery += self.vel
            if pygame.sprite.collide_rect(self.human, self.platform):  # стоять на платформе

                self.human.rect.centery = self.height - self.ground - 178
                self.vel = 0

        if self.human.rect.centery >= self.height - self.ground:  # приземление и фиксирование на земле

            if self.human.down:
                self.human.rect.centery = self.height - self.ground + 50
            else:
                self.human.rect.centery = self.height - self.ground
            self.vel = None
        if self.human.rect.centery < human_width // 2:  # уперся наверх
            self.human.rect.centery = human_width // 2
            self.vel = 0

        for mon in self.monstr.copy():
            if isinstance(mon, Big_Monster) and mon.rect.centery > self.height - self.ground - 120:
                if not mon.on_ground:
                    mon.rect.centery -= 15
                    mon.on_ground = True
                    pygame.time.set_timer(self.FIREBALLS_EVENT, 500)

            else:
                mon.rect.centery += 3
            if mon.rect.centery > self.height + 100:
                self.monstr.remove(mon)
            if pygame.sprite.collide_mask(self.human, mon):
                self.human.gold = False
        if pressed[
            pygame.K_LEFT] and self.human.rect.centerx - human_width // 2 > 100:  # человек упирается влево от экрана на половину своего размера
            self.human.rect.centerx -= 15  # скорость его движения
            if pygame.sprite.collide_mask(self.human, self.platform):
                self.human.rect.centerx += 15
            self.human = Movement(self.human.rect.center, self.human.gold)
            if self.with_gun:
                self.ak_47.flip("l")
            self.human.flip("l")

        if pressed[pygame.K_RIGHT] and self.human.rect.centerx + human_width // 2 < 1500:
            self.human.rect.centerx += 15
            if pygame.sprite.collide_mask(self.human, self.platform):
                self.human.rect.centerx -= 15
            self.human = Movement(self.human.rect.center, self.human.gold)
            if self.with_gun:
                self.ak_47.flip("r")  # чтобы оружие направлялась вправо
            self.human.flip("r")

    def show(self):
        self.screen.fill((255, 255, 255))  # очистка экрана приложения

        if self.with_gun:
            self.ak_47.location = (self.human.rect.centerx, self.human.rect.centery - 10)
            self.ak_47.rect.center = self.ak_47.location

        self.screen.blit(self.back_ground.image, self.back_ground.rect)  # наложение заднего фона
        self.screen.blit(self.human.image, self.human.rect)
        self.screen.blit(self.ak_47.image, self.ak_47.rect)
        self.screen.blit(self.boiler.image, self.boiler.rect)
        self.screen.blit(self.platform.image, self.platform.rect)
        self.screen.blit(self.house.image, self.house.rect)

        for fireball in self.fireballs.copy():
            if fireball.direction == "r":
                fireball.rect.centerx += 10
            else:
                fireball.rect.centerx -= 10
            if -100 < fireball.rect.centerx < self.width + 100:  # если пуля в экране отображается иначе удаляется
                self.screen.blit(fireball.image, fireball.rect)
            else:
                self.fireballs.remove(fireball)

        for mon in self.monstr:
            self.screen.blit(mon.image, mon.rect)
        cur_res = self.cur_res_font.render(f"в банке {len(self.list_gold)} руб.", True, (255, 0, 0))  # текст результата
        res_rect = cur_res.get_rect()
        res_rect.center = (130, self.height - self.ground - 130)
        self.screen.blit(cur_res, res_rect)
        if pygame.sprite.collide_mask(self.human, self.house) and self.human.rect.centerx > 620:  # он зашел в дом
            self.human.gold = True
            self.screen.blit(self.door.image, self.door.rect)

        if pygame.sprite.collide_mask(self.human, self.ak_47):
            self.with_gun = True

        if pygame.sprite.collide_mask(self.human, self.boiler) and self.human.rect.centerx < 200:
            if self.in_boiler == False and self.human.gold == True:
                gold = Gold_coins((random.randint(90, 120),
                                   random.randint(self.height - self.ground - 30, self.height - self.ground - 10)))
                self.list_gold.append(gold)
                self.human.gold = False
            self.in_boiler = True
        else:
            self.in_boiler = False
        for gold in self.list_gold:
            self.screen.blit(gold.image, gold.rect)
        if len(self.list_gold) == 1:
            pygame.draw.rect(self.screen, "green", self.button, 999, 30)
            button_text = self.cur_res_font.render(f" next level ", True, (0, 0, 0))
            button_text_rect = button_text.get_rect()
            button_text_rect.center = (self.width // 2, self.height - self.ground - 370)
            self.screen.blit(button_text, button_text_rect)
        for bullet in self.bullets.copy():  # пробегаемся по списку из всех пуль
            if bullet.direction == "r":  # в зависимости от направления сдвигаем ее
                bullet.rect.centerx += 50
            else:
                bullet.rect.centerx -= 50
            if -100 < bullet.rect.centerx < self.width + 100:  # если пуля в экране отображается иначе удаляется
                self.screen.blit(bullet.image, bullet.rect)
            else:
                self.bullets.remove(bullet)
        for fireball in self.fireballs.copy():
            if pygame.sprite.collide_mask(self.human, fireball):
                if self.human.direction == "r" and fireball.direction == "r":
                    self.human.rot_center(-90)
                elif self.human.direction == "r" and fireball.direction == "l":
                    self.human.rot_center(90)
                elif self.human.direction == "l" and fireball.direction == "r":
                    self.human.rot_center(-90)
                elif self.human.direction == "l" and fireball.direction == "l":
                    self.human.rot_center(90)

                # else:
                #     self.human.rot_center(-90)

        for mon in self.monstr.copy():  # стреляем и монстр удаляется
            for bullet in self.bullets.copy():
                if pygame.sprite.collide_mask(bullet, mon):
                    if bullet not in mon.bullet_shot:
                        mon.bullet_shot.append(bullet)
                    if mon.live == len(mon.bullet_shot):
                        self.monstr.remove(mon)
                        self.kill_monster += 1
                        pygame.time.set_timer(self.FIREBALLS_EVENT, 0)
                    self.bullets.remove(bullet)


class Level_three(Level):
    def __init__(self, screen, width, height, save):
        super().__init__(screen, width, height, save)
        # self.ak_47 = AK_47((random.randint(100, self.height - 100), random.randint(0, self.width - 400)))
        self.back_ground_two = Background_two(self.width, self.height)
        self.platform = []
        self.MINI_PLATFORMS_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(self.MINI_PLATFORMS_EVENT, 1000)
        self.background_list = [self.back_ground_two]

    def check_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.vel = -35




            elif event.type == self.MINI_PLATFORMS_EVENT:
                plat = Mini_platforms((self.width + 300, random.randint(300, (self.height - self.ground))))
                self.platform.append(plat)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = list(pygame.mouse.get_pos())  # [x,y]
                if event.button == 1 and self.button.collidepoint(mouse_position[0], mouse_position[1]):
                    return True

    def update_action(self):
        pressed = pygame.key.get_pressed()
        human_width, human_hight = self.human.image.get_size()

        if self.vel is not None:  # скорость None когда он стоит на земле
            self.vel += self.acc
            self.human.rect.centery += self.vel
        # if self.background_list[-1].rect.centerx < self.width // 2:
        #     back_ground_two = Background_two(self.width * 3, self.height)
        #     self.background_list.append(back_ground_two)
        # for back_ground_two in self.background_list.copy():
        #     back_ground_two.rect.centerx -= 2  # если центр икс минус то движение влево
        #     if back_ground_two.rect.centerx < -1000:
        #         self.background_list.remove(back_ground_two)
        self.back_ground_two.delta -= 1
        if self.back_ground_two.delta == -self.width:
            self.back_ground_two.delta = 0

        if self.human.rect.centery >= self.height - self.ground:  # приземление и фиксирование на земле

            if self.human.down:
                self.human.rect.centery = self.height - self.ground + 50
            else:
                self.human.rect.centery = self.height - self.ground
            self.vel = None
        if self.human.rect.centery < human_width // 2:  # уперся наверх
            self.human.rect.centery = human_width // 2
            self.vel = 0
        for plat in self.platform.copy():
            plat.rect.centerx -= 3  # если центр икс минус то движение влево
            if plat.rect.centerx < -200:
                self.platform.remove(plat)
        block_right = False
        block_left = False

        for plat in self.platform:
            plat_w, plat_h =  plat.image.get_size()
            if pygame.sprite.collide_mask(self.human, plat):
                if self.human.rect.centerx < plat.rect.centerx-plat_w//2:
                    self.human.rect.centerx -= 3
                    block_right = True
                elif self.human.rect.centerx > plat.rect.centerx + plat_w//2:
                    block_left = True
                elif self.human.rect.centery > plat.rect.centery + plat_h//2 :
                    self.human.rect.centery = plat.rect.centery + plat_h // 2 + human_hight//2
                    self.vel = 0
                else:
                    self.human.rect.centery = plat.rect.centery -plat_h // 2 - human_hight + 65
                    self.vel = 0

        if pressed[
            pygame.K_LEFT] and self.human.rect.centerx - human_width // 2 > 100  and block_left == False:  # человек упирается влево от экрана на половину своего размера
            self.human.rect.centerx -= 15  # скорость его движения

            self.human = Movement(self.human.rect.center, self.human.gold)
            self.human.flip("l")

        if pressed[pygame.K_RIGHT] and self.human.rect.centerx + human_width // 2 < 1500 and block_right ==False:
            self.human.rect.centerx += 15

            self.human = Movement(self.human.rect.center, self.human.gold)
            self.human.flip("r")

    def show(self):
        self.screen.fill((255, 255, 255))  # очистка экрана приложения
        # for backgroun_two in self.background_list:
        #     self.screen.blit(backgroun_two.image, backgroun_two.rect)
        self.screen.blit(self.back_ground_two.image, (self.back_ground_two.delta, 0))
        self.screen.blit(self.back_ground_two.image, (self.back_ground_two.delta + self.width, 0))
        self.screen.blit(self.human.image, self.human.rect)

        for plat in self.platform:
            self.screen.blit(plat.image, plat.rect)
