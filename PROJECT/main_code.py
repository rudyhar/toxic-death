from tracking_code import *
import random
import pygame.freetype
import gif_pygame


import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "resources")
frame_index = 0
running = True
tick = 0
lobby_area = 1
glob_ascend_check = 0
ascend_timer = 300
coord_list_left = []
coord_list_right = []


life = 2000

room_bg = pg.Surface((568, 320))

# life



def main():

    global running
    global tick
    global frame_index
    global lobby_area
    global data_dir
    global main_dir
    global ascend_timer
    global life
    global coord_list_left
    global coord_list_right

    
    # for quick coord list loading

    motion_track_and_extract_body_part_coord_lists()
    # save_coord_lists()
    # print("loading coords")
    # load_coord_lists()
    # print("done loading coords")

    # pg setup
    pg.init()

    screen = pg.display.set_mode((568, 320))
    clock = pg.time.Clock()
    pg.display.set_caption("TOXIC DEATH")
    # pg.mouse.set_visible(False)



    if not pg.font:
        print("Warning, fonts disabled")
    if not pg.mixer:
        print("Warning, sound disabled")


    guy = Guy()
    rh = right_Hand()
    lh = left_hand()
    rf = right_foot()
    lf = left_foot()
    hd = head()
    bd = body()

    pained = load_sound("cough2.mp3")
    dropped = load_sound("splash.mp3")

    candy = load_sound("candy_mountain.mp3")
    park_vibes = load_sound("park_vibes.mp3")
    real_love = load_sound("real_love.mp3")



    guy.add(rh, lh, rf, lf, hd, bd)

    allsprites = pg.sprite.RenderPlain((guy))

    background = pg.Surface(screen.get_size())
    background = background.convert()

    background.fill((170, 238, 187))

    screen.blit(background, (0, 0))

    pg.display.flip()


    # fire gif
    onename = os.path.join(data_dir, "fire1.gif")
    fire_gif = gif_pygame.load(onename)
    
    real_love.play()


    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close your window

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")


        if hd.ascensioned == 1:

            allsprites.remove(rh)
            allsprites.remove(lh)
            allsprites.remove(rf)
            allsprites.remove(lf)

        allsprites.update()



        if frame_index >= len(right_hand_coord_list) - 1:
            frame_index = 0


        if lobby_area == 1:
            if tick >= 0:
                background.fill((100,100,0))
            if tick >= 120:
                background.fill((0, 0, 100))
            if tick >= 240:
                background.fill((100, 0, 0))
            if tick >= 360:
                background.fill((0, 100, 0))
            if tick >= 480:
                tick = 0

            
        
        
        if lobby_area == 2:
            background = load_image("new_park.png")[0]

        if lobby_area == 3:
            background = bd.room_bg
            

        

        # FALLINGSHIT FROM THE SKY
        if tick % 120 == 0:

            print("HI_HELLO")

            # generate a random bool

            # if its true creare friend
            # if false create lit

            coin_flip = bool(random.getrandbits(1))
            
            if coin_flip:
                friend_icon = icon("friends.png", 1)
                guy.add(friend_icon)

            else:
                literacy_icon = icon("slow_breathing.png", 0)
                guy.add(literacy_icon)

        # catch_attempt



        for little_icon in iter(guy):

            if little_icon.friend == 1:
                if rh.catch_attempt(little_icon.rect):
                    guy.cleanup()
                    lobby_area = 3
                    real_love.stop()
                    park_vibes.stop()
                    candy.play()
                    break
                if lh.catch_attempt(little_icon.rect):
                    guy.cleanup()
                    lobby_area = 3
                    real_love.stop()
                    park_vibes.stop()
                    candy.play()
                    break


            elif little_icon.friend == 0:
                if rh.catch_attempt(little_icon.rect):
                    guy.cleanup()
                    lobby_area = 2
                    real_love.stop()
                    candy.stop()
                    park_vibes.play()
                    break
                if lh.catch_attempt(little_icon.rect):
                    guy.cleanup()
                    lobby_area = 2
                    real_love.stop()
                    candy.stop()
                    park_vibes.play()
                    break

        if lobby_area == 2 or lobby_area == 3:
            # START SCENCION SEQUENCE
            hd.ascension()

            if ascend_timer <= 0:
                lobby_area = 1
                candy.stop()
                park_vibes.stop()
                real_love.play()

                ascend_timer = 300

            # start ascend timer
            ascend_timer -= 1

        else:
            hd.de_ascend()
            tick = tick + 1

            if tick % 5 == 0:
                frame_index += 1

        allsprites = pg.sprite.RenderPlain((guy))

        
        # RENDER YOUR GAME HERE
        screen.blit(background, (0, 0))

        if hd.ascensioned == True:
            allsprites.remove(lf)
            allsprites.remove(rf)
            allsprites.remove(rh)
            allsprites.remove(lh)
            allsprites.remove(bd)
            allsprites.add(bd)
            
        

        string_life = str(life) 


        font = pygame.font.Font(None, 40)
        text = font.render(string_life, 0, (255, 10, 10))
        text1 = font.render("LIFE", 0, (255, 10, 10), (210,0,0))
        # center = (background.get_width() / 2, background.get_height() / 2)

        # textpos = text.get_rect(center=center)
        textpos = (background.get_width() - 100, background.get_height() - 300)
        textpos1 = (background.get_width() - 160, background.get_height() - 300)


        allsprites.draw(screen)

        screen.blit(text, textpos)
        screen.blit(text1, textpos1)


        

        if lobby_area == 1:
            life -= 1

        if life <= 0:
            break # doom , game over
        
       

        
        
        if life % 200 == 0:

            # Get random x coordinate
            x_nom = random.randint(0, 568)

            # Create coordinate tuple
            coord = (x_nom, 320)

            # Add coordinate to appropriate list
            if random.choice([True, False]):
                coord_list_left.append(coord)
                pained.play()

            else:
                coord_list_right.append(coord)
                dropped.play()


        if lobby_area == 1:
            transparency = (1 / (life/100)) * 100

            for x in fire_gif.get_surfaces():
                x.set_alpha(transparency)

            fire_gif.render(screen, (10, 10))

            # Draw red line from left leg to all coordinates in coord_list_left
            for coord in coord_list_left:
                pygame.draw.line(screen, (255,0,0), lf.rect.center, coord)

            # Draw red line from right leg to all coordinates in coord_list_right
            for coord in coord_list_right:
                pygame.draw.line(screen, (255,0,0), rf.rect.center, coord)

    


        pg.display.flip()

        clock.tick(60)  # limits FPS to 60


    pg.quit()   

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname).convert_alpha()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound    


class Guy(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)  # call Sprite initializer

    def cleanup(self):
        for sprite in self:
            if sprite.friend != -1:
                self.remove(sprite) 

    # def update(self):
    #     print("hey!")


class icon(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    global tick

    def __init__(self, image, id):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image(image)
        self.grav = (0,3)
        # self.rect.inflate(-55, -55)
        self.rect.midbottom = (random.randint(0,568), 0)

        if id:
            self.friend = 1
        elif id == 0:
            self.friend = 0
        else:
            self.friend = -1

    def update(self):

        if tick % 5 == 0:
            self.rect.move_ip(self.grav)

        if self.rect.y >= 150:
            self.kill()

    
class right_Hand(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    global frame_index

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer

        self.image, self.rect = load_image("hand_right.png")
        self.friend = -1

    def update(self):
        self.rect.center = right_hand_coord_list[frame_index]

    def catch_attempt(self, target):
        """returns true if the fist collides with the target"""
        hitbox = self.rect
    
        hit = hitbox.colliderect(target)
        return hit




        # if not self.punching:
        #     self.punching = True
        #     hitbox = self.rect.inflate(-5, -5)
        #     return hitbox.colliderect(target.rect)
   
class left_hand(pg.sprite.Sprite):
    global frame_index
    global cleanup_icons

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer

        self.image, self.rect = load_image("hand_left.png")
        self.friend = -1

    def update(self):
        self.rect.center = left_hand_coord_list[frame_index]

    def catch_attempt(self, target):
        """returns true if the fist collides with the target"""
        hitbox = self.rect
        hit = hitbox.colliderect(target)
        return hit


class right_foot(pg.sprite.Sprite):
    global frame_index

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("slipper_right.png")
        self.friend = -1

    def update(self):
        self.rect.center = right_foot_coord_list[frame_index]


class left_foot(pg.sprite.Sprite):
    global frame_index

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("slipper_left.png")
        self.friend = -1

    def update(self):
        self.rect.center = left_foot_coord_list[frame_index]


class body(pg.sprite.Sprite):

    room_bg
    images = []
    tick = 0

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer

        pic1 = load_image("body_crumpled1.png")
        pic2 = load_image("body_crumpled2.png")
        pic3 = load_image("body_crumpled3.png")

        pic4 = load_image("funroom_raw.png")
        pic5 = load_image("funroom_raw2.png")





        self.images.append(pic1)
        self.images.append(pic2)
        self.images.append(pic3)
        self.images.append(pic4)
        self.images.append(pic5)

        self.room_bg = pic4[0]

        self.image, self.rect = self.images[0]
        self.friend = -1

    def update(self):


        self.tick += 1

        if self.tick >= 0:
            self.image, self.rect = self.images[0]
            self.room_bg = self.images[3][0]


        if self.tick >= 20:
            self.image, self.rect = self.images[1]
            self.room_bg = self.images[4][0]
        
        if self.tick >= 40:
            self.image, self.rect = self.images[2]
            self.tick = 0
            self.room_bg = self.images[3][0]

        self.rect.center = body_coord_list[frame_index]


class head(pg.sprite.Sprite):

    ascensioned = 0
    global frame_index
    global glob_ascend_check

    checker_one = 0
    checker_two = 0
    

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("face.png")
        self.offset = (0, -80)
        self.asc_offset = (0, -10)
        self.friend = -1
        self.pic4 = load_image("acending_char.png")

    def update(self):
        if self.ascensioned:
            self.asc_face()
            self.rect.center = body_coord_list[frame_index]
            self.rect.center = body_coord_list[frame_index]
            self.rect.move_ip(self.asc_offset)

        else:
            self.normal_face()
            self.rect.center = body_coord_list[frame_index]
            self.rect.center = body_coord_list[frame_index]
            self.rect.move_ip(self.offset)

    def normal_face(self):

        if self.checker_one:
            self.image, self.rect = load_image("face.png")
            self.checker_one = 0


    def asc_face(self):
 
        if self.checker_two:
            self.image, self.rect = load_image("acending_char.png")
            self.checker_two = 0


        

    def ascension(self):
        self.ascensioned = 1
        self.checker_one = 1
        self.checker_two = 1
    
    def de_ascend(self):
        self.ascensioned = 0




if __name__ == "__main__":
    main()





