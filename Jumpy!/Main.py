# This is the video series I started this with: https://www.youtube.com/watch?v=uWvb3QzA48c&t=3s
# Jumpy! (a platform game)
# Art from Kenney.nl
# Happy Tune by https://opengameart.org/content/happy-tune
# Acrostics bu Cityfires

import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump2.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Powerup6.wav'))
        # load misc
        misc_dir = path.join(self.dir, 'misc')

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        # add in the platforms
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'happytune.wav'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)

    def update(self):
        # Game Loop Update
        self.all_sprites.update()

        # spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2.5)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2.5)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2.5)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 1

        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for PowerUp in pow_hits:
            if PowerUp.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # DEATH!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number of platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH-width), random.randrange(-75, -30))

    def events(self):
        # Game Loop Events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop Draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        # Scoreboard
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        # after drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # Game Splash/Start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'happytune.wav'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        jumpy_logo = pg.image.load("img/Jumpy.png")
        jumpy_logo = pg.transform.scale(jumpy_logo, (30 * 9, 30 * 9))
        game_logo = jumpy_logo
        self.screen.blit(game_logo, (105, 40))
        fslogo = pg.image.load("img/falconshark-white.png")
        fslogo = pg.transform.scale(fslogo, (30 * 3, 30 * 3))
        logo = fslogo
        self.screen.blit(logo, (390, 520))
        #self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump!", 20, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play", 20, WHITE, WIDTH / 2, HEIGHT * 5 / 8)
        self.draw_text("High Score: " + str(self.highscore), 20, WHITE, WIDTH / 2, HEIGHT * 6 / 8)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # Game Over/Continue screen
        pg.mixer.music.load(path.join(self.snd_dir, 'happytune.wav'))
        pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 20, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 20, WHITE, WIDTH / 2, HEIGHT * 5 / 8)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 20, WHITE, WIDTH / 2, HEIGHT /2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 20, WHITE, WIDTH / 2, HEIGHT /2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
