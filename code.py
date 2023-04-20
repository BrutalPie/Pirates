from pygame import *
direction = "right"

#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
    
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#клас головного гравця
class Player(GameSprite):
    #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self):  
        # Спершу рух по горизонталі
        if packman.rect.x <= win_width-60 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if packman.rect.y <= win_height-85 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # йдемо вниз
            for p in platforms_touched:
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self,direction):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top+40, 15, 15, 15)
        if direction == "left":
            bullets_left.add(bullet)
        elif direction == "right":
            bullets_right.add(bullet)
#клас спрайту-ворога
class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

   #рух ворога
    def update(self,x1,x2):
        if self.rect.x <= x1: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# клас спрайту-кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #рух ворога


    def update(self,direction):
        if direction == "left":
            self.rect.x -= self.speed
            # зникає, якщо дійде до краю екрана
            if self.rect.x < 0:
                self.kill()
        elif direction == "right":
            self.rect.x += self.speed
            # зникає, якщо дійде до краю екрана
            if self.rect.x > win_width:
                self.kill()
BLACK = (0,0,0)
#Створюємо віконце
win_width = 1366
win_height = 768
display.set_caption("Labirint")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load("cave.png"),(1366,768)) # задаємо колір відповідно до колірної схеми RGB


#Створюємо групу для стін
barriers = sprite.Group()

#створюємо групу для куль
bullets_left = sprite.Group()
bullets_right = sprite.Group()
#Створюємо групу для монстрів
monsters = sprite.Group()
coins = sprite.Group()

#Створюємо стіни картинки
w1 = GameSprite('stone.jpg', 283,240, 400,40)
w5 = GameSprite('stone.jpg', 283,240, 40,400)
w3 = GameSprite('stone.jpg', 283,110, 400,40)
w2 = GameSprite('stone.jpg', 683,488, 400,40)
w4 = GameSprite('stone.jpg', 1043,228, 40,400)
w6 = GameSprite('stone.jpg', 283,-250, 40,400)
purse = GameSprite('purse.png', 1290,690, 80,80)
murders = GameSprite('kill.png', 1240,10, 130,130)

#додаємо стіни до групи
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(purse)
barriers.add(murders)
#створюємо спрайти
packman = Player('Pirat.png', 3, win_height - 90, 80, 85, 0, 0)
monster1 = Enemy('Pumpkin.png', 328, 285, 50, 80, 5)
monster2 = Enemy('Pumpkin.png', 988, 403, 50, 80, 3)
monster3 = Enemy('Pumpkin.png', 1088, 488, 50, 80, 4)
monster4 = Enemy('Pumpkin.png', 228, 240, 50, 80, 2)

coin1 = GameSprite('coin.png', 330,60, 50,50)
coin2 = GameSprite('coin.png', 990,530, 50,50)

final_sprite = GameSprite('Pirat.png', win_width/2-100/2, win_height/2-100/2, 100, 100)

#додаємо монстра до групи
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)

coins.add(coin1)
coins.add(coin2)

money = 0
murder = 0
strike = 0

font.init()
font = font.SysFont('monospaced', 80)



#змінна, що відповідає за те, як закінчилася гра
finish = False
#ігровий цикл
run = True
while run:
    
    #цикл спрацьовує кожну 0.05 секунд
    time.delay(5)
        #перебираємо всі події, які могли статися
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                direction = "left"
                packman.x_speed = -3
            elif e.key == K_d:
                direction = "right"
                packman.x_speed = 3
            elif e.key == K_w:
                packman.y_speed = -3
            elif e.key == K_s:
                packman.y_speed = 3
        
            elif e.key == K_SPACE:
                    packman.fire(direction)
                    strike+=1

        elif e.type == KEYUP:
            if e.key == K_a:
                packman.x_speed = 0
            elif e.key == K_d:
                packman.x_speed = 0 
            elif e.key == K_w:
                packman.y_speed = 0
            elif e.key == K_s:
                packman.y_speed = 0
            #вбити ворогів
            elif e.key == K_t:
                monster1.kill()
                monster2.kill()
                monster3.kill()
                monster4.kill()

#перевірка, що гра ще не завершена
    if not finish:
        #оновлюємо фон кожну ітерацію
        window.blit(back,(0,0))#зафарбовуємо вікно кольором
        win = font.render(str(money),True,(59, 58, 120))
        window.blit(win,(1250,700))#Лічильник монет
        
        killl = font.render(str(murder),True,(59, 58, 120))
        window.blit(killl,(1290,130))

        #запускаємо рухи спрайтів
        packman.update()
        bullets_left.update("left")
        bullets_right.update("right")
        
        #оновлюємо їх у новому місці при кожній ітерації циклу
        packman.reset()
        #рисуємо стіни 2
        bullets_left.draw(window)
        bullets_right.draw(window)
        barriers.draw(window)
        

        kil = sprite.groupcollide(monsters, bullets_left, True, True)
        kil_1 = sprite.groupcollide(monsters, bullets_right, True, True)
        

        monster1.update(323,993)
        monster2.update(323,993)
        monster3.update(1088,win_width-55)
        monster4.update(0,228)

        monsters.draw(window)
        sprite.groupcollide(bullets_left, barriers, True, False)
        sprite.groupcollide(bullets_right, barriers, True, False)

        coins.draw(window)
        hits = sprite.groupcollide(bullets_left, coins, True, True)
        hits_1 = sprite.groupcollide(bullets_right, coins, True, True)

        if hits or hits_1:
            money+=1#Лічильник монет

        if kil or kil_1:
            murder+=1#Лічильник вбивств

        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            # обчислюємо ставлення
            img = transform.scale(image.load("lose.png"),(1366,768))
            d = img.get_width() // img.get_height()
            
            window.blit(img, (0, 0))
    
        if len(monsters) == 0:
            final_sprite.reset()
            if sprite.collide_rect(packman, final_sprite):
                finish = True
                img = transform.scale(image.load("win.png"),(1368,768))
                window.blit(img, (0, 0))
        

    display.update()