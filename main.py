from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from player import Player
import globals

janela = Window(globals.WIDTH, globals.HEIGHT)
teclado = janela.get_keyboard()
janela.set_title("Daft Drunk")    

fase = 1

background = Sprite("assets/bg-1.png", 1)
player = Player(janela)

while True:
    background.draw()
    
    #checarLimitesJogador()
    player.run()

    janela.update()