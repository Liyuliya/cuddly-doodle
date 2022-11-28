import pygame
import os
import sys
import random
from time import sleep
from pygame import mixer

# 게임 스크린 전역변수
screen_width = 800
screen_height = 600

# 게임 화면 전역변수
block_size = 20 #size of block
block_width = screen_width / block_size
block_height= screen_height / block_size

# 방향 전역변수
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 색상 전역변수
WHITE = (255, 255, 255)
ORANGE = (250, 150, 0)
GRAY = (100, 100, 100)

# 뱀 객체
class Snake(object):
    def __init__(self):
        self.create()
        #self.head_right = pygame.image.load('assets/head_right.png').convert_alpha()
        #self.head_left = pygame.image.load('assets/head_left.png').convert_alpha()
        #self.head_up = pygame.image.load('assets/head_up.png').convert_alpha()
        #self.head_down = pygame.image.load('assets/head_down.png').convert_alpha()

      # 뱀 생성
    def create(self):
        self.length = 2
        # snake location in the start set in the middle
        self.positions = [(int(screen_width / 2), int(screen_height / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # 뱀 방향 조정
    def control(self, xy):
        #block opposite direction
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    # 뱀 이동
    def move_snake(self):
        cur = self.positions[0] #head
        x, y = self.direction
        new = (cur[0] + (x * block_size)), (cur[1] + (y * block_size))

        # 뱀이 자기 몸통에 닿았을 경우 뱀 처음부터 다시 생성
        if new in self.positions[2:]:
            sleep(1)
            self.create()
        # 뱀이 게임화면을 넘어갈 경우 뱀 처음부터 다시 생성
        elif new[0] < 0 or new[0] >= screen_width or \
                new[1] < 0 or new[1] >= screen_height:
            sleep(1)
            self.create()
        # 뱀이 정상적으로 이동하는 경우
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # 뱀이 먹이를 먹을 때 호출
    def eat(self):
        self.length += 3
        self.crunch_sound = pygame.mixer.Sound('assets/nyam_nyam.wav')
    
      
    # 뱀 그리기
    def draw_snake(self,screen):
        red, green, blue = 50 / (self.length -1), 150, 150/(self.length -1)
        #self.update_head_dir() #peack one of head dic
        for i, p in enumerate(self.positions):
            color = (100 +red * i, green, blue * i)
            block_rect = pygame.Rect((p[0], p[1]), (block_size, block_size))
            #pygame.draw.rect(screen, color, block_rect)
            if i == 0 :
                pygame.draw.rect(screen, color, block_rect)
                #screen.blit(self.head_down, block_rect)            
            else:
                pygame.draw.rect(screen, (150,100,100), block_rect)
    #def update_head_dir(self):
        #head_relation = self.positions[1]-self.positions[0]
        #and from this direction we are able to tell how the head relates to block that comes before it
        #if head_relation == RIGHT: self.head == self.head_right
        #elif head_relation ==LEFT:self.head == self.head_left
        #elif head_relation ==DOWN:self.head == self.head_down
        #elif head_relation ==UP:self.head == self.head_up

    def play_crunch_sound(self):
        self.crunch_sound.play()

# 먹이 객체
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    # 먹이 random 생성
    def create(self):
            x = random.randint(0, block_width - 1) 
            y = random.randint(0, block_height - 1) 
            self.position = x * block_size, y * block_size


    # 먹이 그리기
    def draw(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (block_size,block_size))
        grass = pygame.image.load('assets/grass.png').convert_alpha()
        grass = pygame.transform.scale(grass,(20,20))
        screen.blit(grass, rect) 
        #rect = pygame.Rect((self.position[0], self.position[1]), (block_size,block_size))
        #water_drop = pygame.image.load('assets/water_drop.png').convert_alpha()
        #water_drop = pygame.transform.scale(water_drop,(20,20))
        #screen.blit(water_drop, rect)
    
  
# 게임 객체
class Game(object):
    def __init__(self):
        self.snake = Snake()
        self.feed = Feed()
        self.speed = 25

    # 게임 이벤트 처리 및 조작
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
        return False

    # 게임 로직 수행
    def run_logic(self):
        self.snake.move_snake()
        self.check_eat(self.snake, self.feed)
        self.speed = (20 + self.snake.length) / 4

    # 뱀이 먹이를 먹었는지 체크
    def check_eat(self, snake, feed):
        if snake.positions[0] == feed.position:
            snake.eat()
            feed.create()
            snake.play_crunch_sound()
    

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # 게임 정보 출력n
    def draw_info(self, length, speed, screen):
        info = "Length: " + str(length) + "    " + "Speed: " + str(round(speed, 2))
        font_path = ("assets/NanumGothicCoding-Bold.ttf")
        font = pygame.font.SysFont(font_path, 30)
        text_obj = font.render (info, 1, GRAY) #text      
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj, text_rect) 


    # 게임 프레임 처리
    def display_frame(self, screen):
        bgi= pygame.image.load('assets/bgi.png')
        screen.blit(pygame.transform.scale(bgi,(800,600)), (0,0))
        self.draw_info(self.snake.length, self.speed, screen)
        self.snake.draw_snake(screen)
        self.feed.draw(screen)

# 리소스 경로 설정
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main(): 
    # 게임 초기화 및 환경 설정
    pygame.mixer.pre_init() 
    pygame.init()
    pygame.display.set_caption('Snake Game')
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    mixer.music.load('assets/bgm.mp3')
    mixer.music.play(-1)#-1 play on loop

    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit()

#main func
if __name__ == '__main__':
    main()
