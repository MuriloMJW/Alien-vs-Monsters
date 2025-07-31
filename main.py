import pgzrun
import math
import random

WIDTH = 1280
HEIGHT = 720

scene = 'main_menu'

# --- Globals --- #
player = Actor("player")
bg = Actor('bg')
bullets = []
enemies = []
spawned_items = []


enemy_spawn_cooldown = 1.0
enemy_spawn_timer = 0

music_enabled = True


# --- Funções do Player --- #
def player_move():

    dx, dy = 0, 0

   # Verifica se alguma tecla de movimento está pressionada
    player.is_walking = keyboard.a or keyboard.d or keyboard.w or keyboard.s

    if player.is_walking:
        if keyboard.a:
            dx = -1
            player.is_looking_right = False
        if keyboard.d:
            dx = 1
            player.is_looking_right = True
        if keyboard.w:
            dy = -1
        if keyboard.s:
            dy = 1


        # Move o player
        player.x += dx * player.speed
        player.y += dy * player.speed
        # Salva a última direção para o tiro continuar na direção certa
        player.last_direction = [dx, dy]

        # Impedir o player de sair da tela
        if player.x < 0: player.x = 0
        elif player.x > WIDTH: player.x = WIDTH
        if player.y < 0: player.y = 0
        elif player.y > HEIGHT: player.y = HEIGHT

    else:
        player.is_walking = False


def player_animate(delta_time):

    # Animação de dano
    if player.is_hurt:
        player.hurt_animation_timer += delta_time

        if player.hurt_animation_timer >= player.hurt_animation_duration:
            player.hurt_animation_timer = 0.0 # Reseta o timer
            player.is_hurt = False

        if player.is_looking_right:
            player.image = 'player_hurt'
        else:
            player.image = 'player_hurt_flipped'

        return

    # Animação de andar
    elif player.is_walking:
        player.walk_animation_timer += delta_time

        if  player.walk_animation_timer >= player.walk_animation_duration:
            player.walk_animation_timer = 0.0 # Reseta o timer

            # Alterna entre os dois frames de walk e
            # de acordo com o lado em que player está olhando
            if player.is_looking_right:
                if player.walk_frame == 1:
                    player.image = 'player_walk2'
                    player.walk_frame = 2
                else:
                    player.image = 'player_walk1'
                    player.walk_frame = 1
            else:
                if player.walk_frame == 1:
                    player.image = 'player_walk2_flipped'
                    player.walk_frame = 2
                else:
                    player.image = 'player_walk1_flipped'
                    player.walk_frame = 1
    # Player parado
    else:
        player.image = 'player' if player.is_looking_right else 'player_flipped'

# --- Funções do Tiro --- #

def shoot(delta_time):

    # Verifica se já pode atirar de acordo com o tempo de cooldown
    if player.last_shoot_timer <= player.shoot_cooldown:
        player.last_shoot_timer += delta_time
        return

    player.last_shoot_timer = 0 # Reseta o timer

    bullet = Actor("bullet")
    bullet.pos = player.pos
    bullet.speed = 13

    # Atira na mesma direção do player
    dir_x, dir_y = player.last_direction
    bullet.dir_x = dir_x
    bullet.dir_y = dir_y

    bullets.append(bullet)

def bullet_move():
    # Move os tiros
    for bullet in bullets[:]:
        bullet.x += bullet.dir_x * bullet.speed
        bullet.y += bullet.dir_y * bullet.speed

        # Remove o tiro da memória caso saia da tela
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)


# --- Funções do Enemy --- #

def spawn_enemy(delta_time):
    global enemy_spawn_cooldown, enemy_spawn_timer

    # Verifica se pode spawnar o inimigo, de acordo com o cooldown do spawner
    if enemy_spawn_timer <= enemy_spawn_cooldown:
        enemy_spawn_timer += delta_time
        return

    enemy_spawn_timer = 0.0 # Reseta o timer

    enemy = Actor("enemy_1_walk1")
    enemy.speed = 0.5
    enemy.walk_frame = 1

    # Sorteia a posição do inimigo, acima ou abaixo da tela
    enemy_spawn_choice = random.choice(['top', 'bottom'])

    # Eixo x aleatorio
    if(enemy_spawn_choice == 'top'):
        enemy.x = random.randint(0, WIDTH)
        enemy.y = -20
    else:
        enemy.x = random.randint(0, WIDTH)
        enemy.y = HEIGHT + 20

    enemies.append(enemy)


def enemy_move():
    # Movimenta os inimigos na direção do player
    for enemy in enemies:
        # Move no eixo X (horizontal)
        if enemy.x < player.x:
            enemy.x += enemy.speed
        elif enemy.x > player.x:
            enemy.x -= enemy.speed

        # Move no eixo Y (vertical)
        if enemy.y < player.y:
            enemy.y += enemy.speed
        elif enemy.y > player.y:
            enemy.y -= enemy.speed


def animate_all_enemies():
    for enemy in enemies:
        if enemy.walk_frame == 1:
            enemy.image = 'enemy_1_walk2'
            enemy.walk_frame = 2
        else:
            enemy.image = 'enemy_1_walk1'
            enemy.walk_frame = 1


# --- Funções dos Itens --- #

def spawn_item(pos):

    # 70% de chance de dropar moeda
    # 10% de chance de dropar +hp, +speed ou -cooldown

    num = random.randint(1, 100)
    if (num <= 70):
        item = Actor('item_coin')
    elif(num <= 80):
        item = Actor('item_hp')
    elif(num <= 90):
        item = Actor('item_speed')
    else:
        item = Actor('item_cooldown')

    item.pos = pos
    spawned_items.append(item)

def grab_item(item):
    # Coleta os itens, emite o som do respectivo item
    # e verifica se já coletou a quantidade máxima de
    # determinado item
    player.score += 100

    if item.image == 'item_coin':
        play_sound(sounds.grab_coin)
    elif item.image == 'item_hp':
        player.hp += 1
        play_sound(sounds.grab_item)
    elif item.image == 'item_speed':
        if(player.speed <= 16):
            player.speed += 0.25
            play_sound(sounds.grab_item)
    elif item.image == 'item_cooldown':
        if player.shoot_cooldown > 0.2:
            player.shoot_cooldown -= 0.1
            play_sound(sounds.grab_item)


def set_set_difficulty():
    global enemy_spawn_cooldown

    # Nível de dificuldade de acordo com a quantidade de inimigos que o player matou.
    # Quanto mais inimigos ele matou, mais inimigos irão surgir (menor o cooldown do spawner)

    if (player.enemies_killed <= 20):
        enemy_spawn_cooldown = 1.0
        player.level = 'Easy'
    elif (player.enemies_killed <= 50):
        enemy_spawn_cooldown = 0.8
        player.level = 'Medium'
    elif(player.enemies_killed <= 80):
        enemy_spawn_cooldown = 0.5
        player.level= 'Hard'
    elif(player.enemies_killed <= 300):
        enemy_spawn_cooldown = 0.1
        player.level = 'Pro Player'
    else:
        player.level = 'HARDCORE'
        enemy_spawn_cooldown = 0.05

# Emite som caso o som esteja ativado
def play_sound(sound):
    if(music_enabled):
        sound.play()

# Botões do menu principal
btn_play = Actor('btn_play')
btn_music = Actor('btn_music_on') if music_enabled else Actor('btn_music_off')
btn_quit = Actor('btn_quit')
instructions = Actor('instructions')

# Função de clique do mouse
def on_mouse_down(pos):

    if scene != 'main_menu':
        return

    global music_enabled, btn_music
    if btn_play.collidepoint(pos):
        start_game()
    if btn_music.collidepoint(pos):
        music_enabled = not music_enabled
        # Atualiza a aparencia do botão
        btn_music.image = 'btn_music_on' if music_enabled else 'btn_music_off'
    if btn_quit.collidepoint(pos):
        exit()


def draw():
    global music_enabled, btn_play, btn_music, btn_quit
    bg.draw()

    # Desenha o menu principal na tela
    if scene == 'main_menu':
        screen.draw.text("ALIEN VS MONSTERS", center=(WIDTH // 2, HEIGHT // 2 -150), fontsize=100, color="red")

        btn_play.pos = WIDTH // 2, HEIGHT // 2
        btn_play.draw()

        btn_music.pos = WIDTH // 2, HEIGHT // 2 + 80
        btn_music.draw()


        btn_quit.pos = WIDTH // 2, HEIGHT // 2 + 160
        btn_quit.draw()

        instructions.pos = 1090, 550
        instructions.draw()

        return

    # Desenha a tela de game over
    if scene == 'game_over':
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 -150), fontsize=100, color="red")
        screen.draw.text(f"Score: {player.score}", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="yellow")
        screen.draw.text(f"Enemies Killed: {player.enemies_killed}", center=(WIDTH // 2, HEIGHT // 2 + 80), fontsize=50, color="yellow")
        screen.draw.text(f"Press SPACE to return to Menu", center=(WIDTH // 2, HEIGHT // 2 + 160), fontsize=40, color="white")
        return

    # Tela do jogo
    if scene == 'game':

        # --- Desenha o jogador --- #
        player.draw()

        # --- Desenha os tiros --- #
        for bullet in bullets:
            bullet.draw()

        # --- Desenha os inimigos --- #
        for enemy in enemies:
            enemy.draw()

        # --- Desenha os itens --- #
        for item in spawned_items:
            item.draw()

        # --- Desenha as informações do jogador no topo da tela --- #
        screen.draw.text(f"Level: {player.level}", center=(WIDTH // 2 - 200, 30), fontsize=30, color="white")
        screen.draw.text(f"Score: {player.score}", center=(WIDTH // 2, 30), fontsize=30, color="yellow")
        screen.draw.text(f"HP: {player.hp}", center=(WIDTH // 2 + 150, 30), fontsize=30, color="red")
        screen.draw.text(f"Speed: {player.speed}", center=(WIDTH // 2 + 300, 30), fontsize=30, color="blue")
        screen.draw.text(f"Cooldown: {player.shoot_cooldown:.2f}", center=(WIDTH // 2 + 450, 30), fontsize=30, color="green")


def update(delta_time):
    global scene, enemy_spawn_cooldown

    if scene == 'game_over':
        music.stop()

        if keyboard.space:
            scene = 'main_menu'
        return

    if scene == 'game':
        player_move()
        player_animate(delta_time)

        shoot(delta_time)
        bullet_move()

        spawn_enemy(delta_time)
        enemy_move()

        # Verificação de colisão tiro com inimigo
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                # Se o tiro colidir com o inimigo
                if bullet.colliderect(enemy):

                    bullets.remove(bullet)
                    enemies.remove(enemy)

                    player.enemies_killed += 1

                    spawn_item(enemy.pos) # Dropa um item onde o inimigo morreu
                    play_sound(sounds.enemy_hurt)
                    set_set_difficulty()  # Atualiza a dificuldade
                    break

        # Verificação da colisão do inimigo com o player
        for enemy in enemies[:]:
            if enemy.colliderect(player):
                enemies.remove(enemy)
                player.hp -= 1

                player.is_hurt = True
                play_sound(sounds.hurt)

                if player.hp <= 0:
                    scene = 'game_over'

        # Verificação de colisão dos itens com o player
        for item in spawned_items[:]:
            if item.colliderect(player):
                spawned_items.remove(item)
                grab_item(item)


# Configurações padrões do player
def setup_player():
    global player

    # Começa no centro da tela
    player.pos = WIDTH // 2, HEIGHT // 2

    player.score = 0
    player.hp = 5
    player.speed = 5
    player.shoot_cooldown = 1.0
    player.last_shoot_timer = 0.0

    player.is_walking = False
    player.walk_frame = 1
    player.is_looking_right = True
    player.last_direction = [1, 0] # Inicia atirando para direita

    # Variaveis da animação de dano
    player.is_hurt = False
    player.hurt_animation_timer = 0.0
    player.hurt_animation_duration = 0.2

    # Variaveis da animação de walk
    player.walk_animation_timer = 0.0
    player.walk_animation_duration = 0.1

    player.enemies_killed = 0
    set_set_difficulty()

# Configurações iniciais da partida
def setup_stage():
    global bullets, enemies, spawned_items, enemy_spawn_cooldown, enemy_spawn_timer
    bullets = []
    enemies = []
    spawned_items = []

    enemy_spawn_cooldown = 1.0
    enemy_spawn_timer = 0

    # Animação do inimigo
    clock.unschedule(animate_all_enemies) # Para a animação dos inimigos caso esteja acontecendo
    clock.schedule_interval(animate_all_enemies, 0.15) # Chama a função de animação do inimigo a cada 0.15 segundos

def start_game():
    global scene

    print("Game starting")
    setup_stage()
    setup_player()
    scene = 'game'

    if(music_enabled):
        music.play('game_music')



pgzrun.go()
