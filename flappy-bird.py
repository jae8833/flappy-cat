from curses import KEY_DOWN
import pygame
from sys import exit
import random

WIDTH = 600
HEIGHT = 800

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flappy-bird-3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1200, 300))
        self.rect = self.image.get_rect(bottomleft = (0, HEIGHT))
    
    def reposition(self):
        if self.rect.left <= -600:
            self.rect.left = 0
        
    def update(self):
        self.rect.x -= 5
        self.reposition() 

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk = pygame.image.load("flappy-bird-5.png").convert_alpha()
        walk = pygame.transform.scale(walk, (50, 75))
        fly = pygame.image.load("flappy-bird-6.png").convert_alpha()
        fly = pygame.transform.scale(fly, (50, 75))
        self.movement = [walk, fly] 
        self.movement_index = 0
        self.image = self.movement[self.movement_index]
        self.rect = self.image.get_rect(midleft = (WIDTH/2-50 , 300))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -7.5
            self.movement_index = 1
            self.image = self.movement[self.movement_index]
        else:
            self.movement_index = 0
            self.image = self.movement[self.movement_index]

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += self.gravity

    def dead(self):
        self.image = pygame.image.load("flappy-bird-1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 65))

    def update(self):
        self.player_input()
        self.apply_gravity()

class Pipes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("flappy-bird-4.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 400))
        self.rect = self.image.get_rect(midbottom = (x, y))
    
    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.rect.x -= 5
        self.destroy()

class Pipes2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("flappy-bird-4.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 400))
        self.image = pygame.transform.rotate(self.image, angle=180.0)
        self.rect = self.image.get_rect(midbottom = (x, y))
    
    def destroy(self):
        if self.rect.right < 0:
            self.kill()
 
    def update(self):
        self.rect.x -= 5
        self.destroy()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Cat")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill((0,0,0))
        self.clock = pygame.time.Clock()
        self.test_font = pygame.font.SysFont("arial", 50)
        self.game_active = False
        self.sky = pygame.image.load("flappy-bird-2.png")
        self.ground = pygame.sprite.GroupSingle()
        self.ground.add(Ground())
        self.bird = pygame.sprite.GroupSingle()
        self.bird.add(Bird())
        self.pipes = pygame.sprite.Group()
        self.pipes_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipes_timer, 1500)
        self.score = 0 
        self.best = 0
        self.message = self.test_font.render("Press Space to Play", False, ("#eb54e7"))
        self.message_rect = self.message.get_rect(center = (WIDTH/2, HEIGHT/2))
        pygame.mixer.music.load("bg-music.ogg")

    def display_score(self):
        if self.game_active:
            for pipe in self.pipes:
                if pipe.rect.x <= (WIDTH/2-50) < pipe.rect.x + 5:
                    self.score += 0.5
                    self.timer = 0
        score_surf = self.test_font.render(f"{int(self.score)}", False, (255,255,255))
        score_rect = score_surf.get_rect(center = (WIDTH/2, 100))
        self.screen.blit(score_surf, score_rect)
        if self.score > self.best:
            self.best = self.score
        self.best_score = self.test_font.render(f"Best Score: {int(self.best)}", False, (255,255,255))
        self.best_score_rect = self.best_score.get_rect(center = (WIDTH/2, 175))

    def collision_pipe(self):
        if pygame.sprite.spritecollide(self.bird.sprite, self.pipes, False, pygame.sprite.collide_rect_ratio(0.95)):
                self.bird.sprite.dead()
                self.game_active = False
                pygame.mixer.music.stop()
        
    def collision_bg(self):
        if self.bird.sprite.rect.top <= -15 or self.bird.sprite.rect.bottom >= 515:
            self.bird.sprite.dead()
            self.game_active = False
            pygame.mixer.music.stop()
            
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key ==pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if self.game_active and event.type == self.pipes_timer:
                    x = random.randint(700, 900)
                    y = random.randint(600, 865)
                    self.pipes.add(Pipes(x, y))
                    self.pipes.add(Pipes2(x, y-565))

                if self.game_active == False:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.pipes.empty()
                        self.score = 0
                        self.game_active = True
                        pygame.mixer.music.play(-1)
                        self.bird.sprite.rect.midleft = (WIDTH/2-50 , 300)
            
            if self.game_active:
                self.screen.blit(self.sky,(0, 0))
                self.bird.draw(self.screen)
                self.bird.update()
                self.pipes.draw(self.screen)
                self.pipes.update() 
                self.ground.draw(self.screen)
                self.ground.update()
                self.display_score()
                self.collision_pipe()
                self.collision_bg()

            else:
                self.screen.blit(self.sky,(0, 0))
                self.pipes.draw(self.screen)
                self.ground.draw(self.screen)
                self.bird.draw(self.screen)
                self.screen.blit(self.message, self.message_rect)
                self.display_score()
                if(self.best > 0):
                    self.screen.blit(self.best_score, self.best_score_rect)
    
            pygame.display.update()
            self.clock.tick(60)
            

if __name__ == "__main__":
    game = Game()
    game.run()
