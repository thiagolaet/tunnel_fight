from enemy import*
from random import randrange
from food import*
from PPlay.animation import Animation

class Enemy_Controller():
    def __init__(self, janela, player):
        self.enemyList = []
        self.dieList = []
        self.player = player
        self.janela = janela
        self.food_list = []
        self.dead_enemies = 0

    def novaMorte(self, inimigo):
        self.dieList.append(Animation("assets/enemy_dying.png", 28))
        self.dieList[len(self.dieList)-1].set_position(inimigo.enemy.x, inimigo.enemy.y)
        self.dieList[len(self.dieList)-1].set_sequence_time(0, 14, 100)
        self.dieList[len(self.dieList)-1].set_sequence_time(14, 28, 100)
        self.dead_enemies += 1
        if inimigo.direcao == 1:
            self.dieList[len(self.dieList)-1].set_sequence(0, 14)
        elif inimigo.direcao == 2:
            self.dieList[len(self.dieList)-1].set_sequence(14, 28)

        if randrange(1, 3) == 2:
            index = randrange(0, 3)
            heal = 0
            if index == 0:
                food = Animation("assets/frango_assado.png", 4)
                heal = 100
            elif index == 1:
                food = Animation("assets/taco.png", 4)
                heal = 50
            elif index == 2:
                food = Animation("assets/sushi.png", 4)
                heal = 20
            food.set_position(inimigo.enemy.x, inimigo.enemy.y + inimigo.enemy.height - food.height)
            fd = Food(food, heal)
            self.food_list.append(fd)

    def food_control(self):
        for a in range(len(self.food_list)):
            self.food_list[a].timer += self.janela.delta_time()
            self.food_list[a].update()
            if self.food_list[a].sprite.collided(self.player.player) and self.food_list[a].timer >= 2:
                self.player.life.set_life(self.food_list[a].heal)
                self.food_list.pop(a)
                break

    def atualizaMorte(self):
        for i in range(len(self.dieList)):
            self.dieList[i].update()
            if self.dieList[i].get_curr_frame() == 13 or self.dieList[i].get_curr_frame() == 27:
                self.dieList.pop(i)
                break

    def list_control(self):
        for a in range(len(self.enemyList)):
            if not self.enemyList[a].life.alive:
                self.novaMorte(self.enemyList[a])
                self.enemyList.pop(a)
                break

    def start_a_wave(self, nmbr):
        if len(self.enemyList) == 0:
            for a in range(nmbr):
                pos = randrange(self.janela.height / 2, self.janela.height)
                if a % 2 == 0:
                    temp = Enemy1(self.janela, self.player, -100, pos)
                else:
                    temp = Enemy1(self.janela, self.player, self.janela.width, pos)
                self.enemyList.append(temp)

    def run(self):
        self.list_control()
        self.food_control()
        for a in self.enemyList:
            a.run(self.player)
