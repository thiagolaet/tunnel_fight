from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from life import *
import globals

#class Enemys():


class Enemy1():
    def __init__(self, janela, player, x, y):
        self.janela = janela
        self.player = player
        self.teclado = janela.get_keyboard()

        self.enemy = Animation("assets/enemy1-medium.png", 36)
        self.enemy.set_position(x, y)
        self._set_seq_time()

        #sistema de vida
        self.life = Life()

        
        #1 = direita / 2 = esquerda
        self.direcao = 2

        #1 - idleRight / 1.5 - idleLeft / 2 - walkRight / 2.5 - walkLeft / 3 3.5 - attack1 / 4 4.5 - attack2 / 5 5.5 - attack3 / 6 6.5 - attack4  
        self.enemy_state = 1
        self.contadorAnimacao = 0
        self.contadorAtaque = 0
        self.enemy.set_sequence(0, 4)

        self.atacando = False

        self.tomouDano = False
        #pode andar
        self.canWalk = True


    def _set_seq_time(self):
        self.enemy.set_sequence_time(0, 4, 130) #IDLE
        self.enemy.set_sequence_time(4, 8, 130) #IDLE
        self.enemy.set_sequence_time(8, 14, 100) #WALK
        self.enemy.set_sequence_time(14, 20, 100) #WALK
        self.enemy.set_sequence_time(20, 25, 220) #attack1
        self.enemy.set_sequence_time(25, 30, 220) #attack1
        self.enemy.set_sequence_time(30, 33, 100) #hit 1
        self.enemy.set_sequence_time(33, 36, 100) #hit 1
        self.enemy.set_sequence_time(36, 39, 200) #hit 2
        self.enemy.set_sequence_time(39, 42, 200) #hit 2
        self.enemy.set_sequence_time(42, 56, 200) #die
        self.enemy.set_sequence_time(56, 69, 200) #die

    def idleRight(self):
        if self.enemy_state != 1:
            self.enemy.set_sequence(0, 4)
            self.enemy_state = 1

    def idleLeft(self):
        if self.enemy_state != 1.5:
            self.enemy.set_sequence(4, 8)
            self.enemy_state = 1.5

    def walkRight(self):
        if self.enemy_state != 2: 
            self.enemy.set_sequence(8, 14)
            self.enemy_state = 2
            self.enemy.y -= 0.1
            self.enemy.y += 0.1
        self.enemy.x += 1 * self.janela.delta_time() * globals.frame_per_SECOND
        self.direcao = 1

    def walkRightUp(self):
        if self.enemy_state != 2: 
            self.enemy.set_sequence(8, 14)
            self.enemy_state = 2
        self.enemy.y -= 0.1
        self.enemy.x += 1 * self.janela.delta_time() * globals.frame_per_SECOND
        self.direcao = 1

    def walkRightDown(self):
        if self.enemy_state != 2: 
            self.enemy.set_sequence(8, 14)
            self.enemy_state = 2
        self.enemy.y += 0.1
        self.enemy.x += 1 * self.janela.delta_time() * globals.frame_per_SECOND
        self.direcao = 1

    def walkLeft(self):
        if self.enemy_state != 2.5:
            self.enemy.set_sequence(14, 20)
            self.enemy_state = 2.5
        self.enemy.x -= 1 * self.janela.delta_time() * globals.frame_per_SECOND
        self.direcao = 2
    
    def walkLeftUp(self):
        if self.enemy_state != 2.5:
            self.enemy.set_sequence(14, 20)
            self.enemy_state = 2.5
        self.enemy.y -= 0.1
        self.enemy.x -= 1 * self.janela.delta_time() * globals.frame_per_SECOND
        self.direcao = 2

    def walkLeftDown(self):
        if self.enemy_state != 2.5:
            self.enemy.set_sequence(14, 20)
            self.enemy_state = 2.5
        self.enemy.y += 0.1
        self.enemy.x -= 1 * self.janela.delta_time() * globals.frame_per_SECOND
        self.direcao = 2

    def walkUp(self):
        if self.direcao == 1:
            self.enemy.y -= 0.1
            if self.enemy_state != 2: 
                self.enemy.set_sequence(8, 14)
                self.enemy_state = 2
        if self.direcao == 2:
            self.enemy.y -= 0.1
            if self.enemy_state != 2.5: 
                self.enemy.set_sequence(14, 20)
                self.enemy_state = 2.5

    def walkDown(self):
        if self.direcao == 1:
            self.enemy.y += 0.1
            if self.enemy_state != 2: 
                self.enemy.set_sequence(8, 14)
                self.enemy_state = 2
        if self.direcao == 2:
            self.enemy.y += 0.1
            if self.enemy_state != 2.5: 
                self.enemy.set_sequence(14, 20)
                self.enemy_state = 2.5

    def tomandoHit(self):
        if self.direcao == 1:
            self.enemy.set_sequence(30, 33)
        if self.direcao == 2:
            self.enemy.set_sequence(33, 36)
        self.enemy_state = 10
        self.contadorAnimacao = 0
        self.contadorAtaque = 1.5


    def attack(self, player):
        if self.direcao == 1:
            if self.enemy_state != 3:
                self.enemy.set_sequence(20, 25)
                self.enemy.set_curr_frame(20)
                self.enemy_state = 3
        elif self.direcao == 2:
            if self.enemy_state != 3.5:
                self.enemy.set_sequence(25, 30)
                self.enemy.set_curr_frame(25)
                self.enemy_state = 3.5
        self.contadorAtaque = 0
        self.contadorAnimacao = 0
        self.atacando = True
        player.atacado = True
        player.life.receive_damage(10)

    def follow_target(self, target):
        if not self.atacando:
            if self.tomouDano == True: 
                self.tomandoHit()
                self.tomouDano = False
        
        tempoContadorAnimacao = self.checarContadorAnimacao()  
        if target.hitbox.x + target.hitbox.width < self.enemy.x:
            self.direcao = 2
        elif target.hitbox.x - 50 > self.enemy.x:
            self.direcao = 1
        if(self.contadorAnimacao > tempoContadorAnimacao):
            self.atacando = False
            self.canWalk = True
            if self.enemy.collided(target.hitbox) and self.player.player.y < self.enemy.y and self.player.player.y + self.player.player.height > self.enemy.y + self.enemy.height:
                self.canWalk = False
            if self.canWalk:
                if self.direcao == 2:
                    self.walkLeft()
                elif self.direcao == 1:
                    self.walkRight()

                if target.hitbox.y < self.enemy.y:
                    self.walkUp()
                elif target.hitbox.y > self.enemy.y:
                    self.walkDown()
            else:
                if self.contadorAtaque > 3:
                        self.attack(target)
                else:
                    if self.direcao == 1:
                        self.idleRight()
                    elif self.direcao == 2:
                        self.idleLeft()

    def checarContadorAnimacao(self):
        if self.enemy_state == 3 or self.enemy_state == 3.5:
            return 1
        elif self.enemy_state == 10:
            return 0.2
        return 0

    def run(self, player):
        #self.enemy.draw()
        self.enemy.update()
        if self.life.alive:
            self.follow_target(self.player)
        self.contadorAtaque += self.janela.delta_time()
        self.contadorAnimacao += self.janela.delta_time()
