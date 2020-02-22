# This is a Pong Game!

import pygame, sys, random
from math import pi, sin, cos, radians

# 初始化隨機種子
random.seed()

# 球餅
class Puck:
    def __init__(self):
        self.x = width/2         # 球餅水平座標
        self.y = height/2        # 球餅垂直座標
        self.r = 10              # 球餅半徑
        self.mag = 5             # 球餅移動速率
        self.reset()             # 初始化球餅狀態
    def update(self):
        self.x += self.x_speed   # 速度->位置
        self.y += self.y_speed
    def show(self):              # 劃出球餅 (圓形)
        pygame.draw.circle(playSurface, white, (int(self.x), int(self.y)), self.r)
    def edges(self):
        global leftscore, rightscore   # 呼叫全域變數
        if (self.y < 0 or self.y > height):
            self.y_speed *= -1         # 撞到上下邊界反彈
        if (self.x-self.r < 0):        # 進入左邊邊界
            rightscore += 1            # 右方加一分
            sound_score.play()         # 得分音效
            self.reset()               # 初始化球餅狀態
        if (self.x+self.r > width):    # 進入右邊邊界
            leftscore += 1             # 左方加一分
            sound_score.play()         # 得分音效
            self.reset()            
    def reset(self):
        self.x = width/2        # 回到初始水平位置
        self.y = height/2       # 回到初始垂直位置
        self.mag = 5            # 回到初始速率
        angle = random.uniform(-pi/4, pi/4)     # 隨機選擇角度 (水平上下45度角)
        self.x_speed = self.mag * cos(angle)    # 水平速度
        self.y_speed = self.mag * sin(angle)    # 垂直速度
        if (random.uniform(0, 1) > 0.5):        # 一半的機率朝另一方向飛 (原本都往右飛)
            self.x_speed *= -1
    ### https://github.com/NITDgpOS/AirHockey/issues/39  <- 反彈角度設計理念
    def checkPaddleLeft(self, p):
        # 如果在板子的上下界內，且碰到板子
        if (self.x-self.r < p.x+p.w/2 and self.y > p.y-p.h/2 and self.y < p.y+p.h/2):
            # 避免卡球的bug, 故增設此比較條件 (以此避免球在板子後卻還要反彈的情況)
            if (self.x > p.x):
                # self.x_speed *= -1
                self.mag += 0.5                       # 強度增強 (球餅的速率加大)
                diff = self.y-(p.y-p.h/2)             # 和板子上方之距離
                rad = radians(45)                     # 將角度轉為弧度
                angle = map(diff, 0, p.h, -rad, rad)  # 等比例轉換角度 (詳見上方網站內有示意圖)
                self.x_speed = self.mag * cos(angle)  # 調整水平速度
                self.y_speed = self.mag * sin(angle)  # 調整垂直速度
                sound_ping.play()                     # 播放撞擊音效
    def checkPaddleRight(self, p):
        # 和上方概念大致相同
        if (self.x+self.r > p.x-p.w/2 and self.y > p.y-p.h/2 and self.y < p.y+p.h/2):
            if (self.x < p.x):
                # self.x_speed *= -1
                self.mag += 0.5
                diff = self.y-(p.y-p.h/2)
                rad = radians(45)
                # 這裡角度轉換比較特別 因為開角範圍是(-135~-180)、(135~180)
                # 所以不能直接寫(-135~135)，會產生錯誤
                # 將等比例範圍顛倒(45~-45)後 再做旋轉(pi) 就可以得到正確張角
                angle = map(diff, 0, p.h, rad, -rad) + pi
                self.x_speed = self.mag * cos(angle)
                self.y_speed = self.mag * sin(angle)
                sound_ping.play()
# 板子
class Paddle:
    # 板子位置是以矩形中心為座標
    def __init__(self, left):
        self.y = height/2    # 板子垂直高度
        self.y_change = 0    # 垂直高度變化率
        self.w = 20          # 板子寬
        self.h = 100         # 板子長
        if (left):
            self.x = self.w  # 板子水平座標
        else:
            self.x = width - self.w
    def update(self):
        self.y += self.y_change             # 更新垂直位置
        self.y = Constrain(self.y, self.h)  # 限制板子移動範圍
    def show(self):
        # 畫出板子 (長方形)
        rect = pygame.Rect(0, 0, self.w, self.h)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(playSurface, white, rect)
    def move(self, steps):
        self.y_change = steps  # 變化率更動 (一旦更動後，若未設回0則板子會持續移動)

def showScore():
    sFont = pygame.font.SysFont('monaco', 32)                   # 選擇字體字型大小
    Ssurf = sFont.render('{0}'.format(leftscore), True, white)  # 選擇文字和顏色
    Srect = Ssurf.get_rect()                                    # 取得文字方塊區域
    Srect.midtop = (50, 25)                                     # 調整方塊位置
    playSurface.blit(Ssurf, Srect)                              # 將文字以該方塊位置貼上
    Ssurf = sFont.render('{0}'.format(rightscore), True, white)
    Srect = Ssurf.get_rect()
    Srect.midtop = (width-50, 25)
    playSurface.blit(Ssurf, Srect)


def Constrain(y, h):
    down_limit = h/2       # 板子移動下限
    up_limit = height-h/2  # 板子移動上限
    if (y < down_limit):
        return down_limit  # 小於下限->回傳下限值
    elif (y > up_limit):
        return up_limit    # 大於上限->回傳上限值
    else:
        return y           # 一般情況回傳原值

step_w = 5  # 步寬
def KeyPressed():
    for event in pygame.event.get():         # 取得所有pygame事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)
        elif event.type == pygame.KEYDOWN:   # 有按鍵壓下
            if event.key == pygame.K_UP:
                right.move(-step_w)          # 右板子向上
            if event.key == pygame.K_DOWN:
                right.move(step_w)           # 右板子向下
            if event.key == ord('w'):
                left.move(-step_w)           # 左板子向上
            if event.key == ord('s'):
                left.move(step_w)            # 左板子向下
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif event.type == pygame.KEYUP:     # 有按鍵放開
            if event.key == pygame.K_UP:
                right.move(0)                # 右板子停止運動
            if event.key == pygame.K_DOWN:
                right.move(0)                # 停止原理->步寬訂為0
            if event.key == ord('w'):
                left.move(0)                 # 左板子停止運動
            if event.key == ord('s'):
                left.move(0)

# 等比例換算函式
def map(n, start1, stop1, start2, stop2):
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

# 確認pygame初始化有無錯誤
check_errors = pygame.init()
if (check_errors[1] > 0):
    print("(!) Had {0} initializing errors,exiting... ".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) Pygame successfully initialized!")

# 音樂功能初始化
pygame.mixer.init()

# 回擊 音效
sound_ping = pygame.mixer.Sound('PongSound.wav')
sound_ping.set_volume(0.8)
# 得分 音效
sound_score = pygame.mixer.Sound('cash.wav')
sound_score.set_volume(0.6)

# 主畫面大小參數
width = 600
height = 400

# 主畫面
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

# 設定顏色
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

# 幀數控制器
fpsController = pygame.time.Clock()
# 幀率
frame_rate = 50

# 球餅
puck = Puck()
# 板子
left = Paddle(True)
right = Paddle(False)

# 計分
leftscore = 0
rightscore = 0

while True:
	# 填充背景顏色
    playSurface.fill(black)

    # 檢測球餅是否碰到板子
    puck.checkPaddleLeft(left)
    puck.checkPaddleRight(right)
    # 球餅位置調整+顯示
    puck.update()
    puck.edges()   # 球餅撞擊上下邊界運算
    puck.show()

    # 按鍵控制
    KeyPressed()

    # 左右板子移動
    left.update()
    right.update()
    left.show()
    right.show()

    # 顯示分數
    showScore()

    pygame.display.flip()           # 更新視窗
    fpsController.tick(frame_rate)  # 控制幀數