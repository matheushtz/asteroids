# Projeto: Space Raiders com Pygame - Aula Interativa

# Instalação do Pygame (instalar usando o CMD caso não tenha em seu pc)
#!pip install pygame

# Importação das bibliotecas
import pygame        # biblioteca principal para jogos 2D
import random        # para gerar posições e velocidades aleatórias
import sys           # para sair do programa corretamente
import os            # para verificar arquivos

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1366, 768                            # largura e altura da janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # cria a janela do jogo
pygame.display.set_caption("Space Raiders")        # define o nome da janela

# Definindo algumas cores RGB para usar no jogo
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock para controlar os frames por segundo (FPS)
clock = pygame.time.Clock()
FPS = 60  # o jogo será atualizado 60 vezes por segundo

# Carrega sprites das naves
ship_sprites = []
for i in range(1, 6):
    ship_path = f"ships/ship{i}.png"
    if os.path.exists(ship_path):
        ship_sprites.append(pygame.image.load(ship_path))
    else:
        # Fallback para sprite simples se a imagem não existir
        fallback = pygame.Surface((40, 40))
        fallback.fill(WHITE)
        pygame.draw.polygon(fallback, RED, [(0, 40), (20, 0), (40, 40)])
        ship_sprites.append(fallback)

# Carrega sprites da vida
health_powerup_sprite = None
health_full_sprite = None
health_empty_sprite = None

if os.path.exists("health/health.png"):
    health_powerup_sprite = pygame.image.load("health/health.png")
else:
    # Fallback para sprite de vida
    health_powerup_sprite = pygame.Surface((20, 20))
    health_powerup_sprite.fill((0, 255, 0))  # Verde
    pygame.draw.circle(health_powerup_sprite, WHITE, (10, 10), 8)

if os.path.exists("health/healthbar-full.png"):
    health_full_sprite = pygame.image.load("health/healthbar-full.png")
else:
    # Fallback para barra de vida cheia
    health_full_sprite = pygame.Surface((20, 20))
    health_full_sprite.fill((255, 0, 0))  # Vermelho

if os.path.exists("health/healthbar-empty.png"):
    health_empty_sprite = pygame.image.load("health/healthbar-empty.png")
else:
    # Fallback para barra de vida vazia
    health_empty_sprite = pygame.Surface((20, 20))
    health_empty_sprite.fill((100, 100, 100))  # Cinza

# Carrega sprite da bomba
bomb_powerup_sprite = None
if os.path.exists("powerups/bomb.png"):
    bomb_powerup_sprite = pygame.image.load("powerups/bomb.png")
else:
    # Fallback para sprite de bomba
    bomb_powerup_sprite = pygame.Surface((20, 20))
    bomb_powerup_sprite.fill((255, 255, 0))  # Amarelo
    pygame.draw.circle(bomb_powerup_sprite, RED, (10, 10), 8)
    pygame.draw.circle(bomb_powerup_sprite, WHITE, (10, 10), 4)


# Função para escolher o número de jogadores (1 ou 2)
def select_num_players():
    selecting = True
    selected = 1
    font = pygame.font.SysFont(None, 48)
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    selected = 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    selected = 2
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selecting = False
        screen.fill(BLACK)
        title = font.render("Space Raiders", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 120))
        screen.blit(title, title_rect)
        instr = pygame.font.SysFont(None, 36).render("Escolha o número de jogadores", True, WHITE)
        instr_rect = instr.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(instr, instr_rect)
        one_color = (0,255,0) if selected == 1 else WHITE
        two_color = (0,255,0) if selected == 2 else WHITE
        one = font.render("1 Jogador", True, one_color)
        two = font.render("2 Jogadores", True, two_color)
        one_rect = one.get_rect(center=(WIDTH//2 - 150, HEIGHT//2 + 20))
        two_rect = two.get_rect(center=(WIDTH//2 + 150, HEIGHT//2 + 20))
        screen.blit(one, one_rect)
        screen.blit(two, two_rect)
        hint = pygame.font.SysFont(None, 28).render("←/A ou →/D para alternar, ENTER/ESPAÇO para confirmar", True, WHITE)
        hint_rect = hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(hint, hint_rect)
        pygame.display.flip()
        clock.tick(FPS)
    return selected

# Função para escolher a nave (agora recebe o número do jogador)
def select_ship(player_num=1, controls=None, exclude_ships=None):
    selecting = True
    selected_ship = 0
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)
    if exclude_ships is None:
        exclude_ships = []
    if controls is None:
        # Default to arrow keys and space/enter
        controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'select': [pygame.K_RETURN, pygame.K_SPACE]}
    else:
        # Add select keys if not present
        if 'select' not in controls:
            controls['select'] = [pygame.K_RETURN, pygame.K_SPACE]
    # Start at first non-excluded ship
    available_ships = [i for i in range(len(ship_sprites)) if i not in exclude_ships]
    if not available_ships:
        return None
    selected_ship = available_ships[0]
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == controls['left']:
                    # Move to previous available ship
                    idx = available_ships.index(selected_ship)
                    selected_ship = available_ships[(idx - 1) % len(available_ships)]
                elif event.key == controls['right']:
                    idx = available_ships.index(selected_ship)
                    selected_ship = available_ships[(idx + 1) % len(available_ships)]
                elif event.key in controls['select']:
                    selecting = False
        screen.fill(BLACK)
        title_text = title_font.render(f"Jogador {player_num}: Escolha sua nave", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, 100))
        screen.blit(title_text, title_rect)
        instructions = font.render("Use as setas ← → para escolher, ENTER ou ESPAÇO para confirmar", True, WHITE)
        inst_rect = instructions.get_rect(center=(WIDTH//2, HEIGHT - 50))
        screen.blit(instructions, inst_rect)
        for i, ship in enumerate(ship_sprites):
            x = WIDTH//2 - (len(ship_sprites) * 60)//2 + i * 60
            y = HEIGHT//2
            if i == selected_ship:
                pygame.draw.rect(screen, WHITE, (x-5, y-5, 50, 50), 2)
            if i in exclude_ships:
                # Draw excluded ships faded
                faded = pygame.transform.scale(ship, (40, 40)).copy()
                faded.set_alpha(80)
                ship_rect = faded.get_rect(center=(x + 20, y + 20))
                screen.blit(faded, ship_rect)
            else:
                scaled_ship = pygame.transform.scale(ship, (40, 40))
                ship_rect = scaled_ship.get_rect(center=(x + 20, y + 20))
                screen.blit(scaled_ship, ship_rect)
            number_text = font.render(str(i+1), True, WHITE)
            number_rect = number_text.get_rect(center=(x + 20, y + 60))
            screen.blit(number_text, number_rect)
        pygame.display.flip()
        clock.tick(FPS)
    return selected_ship

# Função para desenhar a barra de vida (agora suporta múltiplos jogadores)
def draw_health_bar(screen, player, idx=0):
    # idx: 0 para player 1 (direita), 1 para player 2 (esquerda)
    if idx == 0:
        health_x = WIDTH - 370
        health_y = 0
    else:
        health_x = 10
        health_y = 0
    for i in range(player.max_health):
        if i < player.health:
            health_sprite = pygame.transform.scale(health_full_sprite, (64, 64))
        else:
            health_sprite = pygame.transform.scale(health_empty_sprite, (64, 64))
        screen.blit(health_sprite, (health_x + i * 70, health_y))

# Classe da Nave do Jogador (agora suporta controles diferentes)
class Player(pygame.sprite.Sprite):
    def __init__(self, ship_index, controls, start_pos=None):
        super().__init__()
        self.original_image = pygame.transform.scale(ship_sprites[ship_index], (64, 64))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        if start_pos:
            self.rect.centerx, self.rect.bottom = start_pos
        else:
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.health = 5
        self.max_health = 5
        self.invulnerable_timer = 0
        self.invulnerable_duration = 120
        self.controls = controls  # Dict with movement/shoot keys
        self.shoot_pressed = False  # To prevent autofire

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        # Movement
        if keys[self.controls['left']]:
            dx -= 1
        if keys[self.controls['right']]:
            dx += 1
        if keys[self.controls['up']]:
            dy -= 1
        if keys[self.controls['down']]:
            dy += 1
        if dx != 0 or dy != 0:
            length = (dx ** 2 + dy ** 2) ** 0.5
            dx = dx / length
            dy = dy / length
            self.rect.x += int(dx * self.speed)
            self.rect.y += int(dy * self.speed)
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))
        # Invulnerability effect
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer % 10 < 5:
                self.image = self.original_image.copy()
            else:
                self.image = self.original_image.copy()
                self.image.set_alpha(100)
        else:
            self.image = self.original_image.copy()

    def take_damage(self):
        if self.invulnerable_timer <= 0:
            self.health -= 1
            self.invulnerable_timer = self.invulnerable_duration
            return True
        return False

    def heal(self):
        if self.health < self.max_health:
            self.health += 1

# Classe dos Inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_ship_index):
        super().__init__()
        # Escolhe uma nave diferente da do jogador
        available_ships = [i for i in range(len(ship_sprites)) if i != player_ship_index]
        ship_index = random.choice(available_ships)
        
        # Usa o sprite da nave escolhida, rotacionado 180 graus
        original_ship = pygame.transform.scale(ship_sprites[ship_index], (64, 64))
        self.image = pygame.transform.rotate(original_ship, 180)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)  # posição aleatória na horizontal
        self.rect.y = -30                            # começa acima da tela
        self.speed = random.randint(2, 6)            # velocidade aleatória

    def update(self):
        self.rect.y += self.speed  # move o inimigo para baixo
        # Quando sai da tela, reinicia na parte superior com nova posição
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 30)
            self.rect.y = -30
            self.speed = random.randint(2, 6)

# Classe dos Tiros
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Usa a textura do projétil se existir, senão fallback
        projectile_path = os.path.join("projectiles", "projectile.png")
        if os.path.exists(projectile_path):
            img = pygame.image.load(projectile_path).convert_alpha()
            self.image = pygame.transform.scale(img, (12, 12))
        else:
            self.image = pygame.Surface((12, 12))
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # o tiro sobe para cima

    def update(self):
        self.rect.y += self.speed
        # Remove o tiro se ele sair da tela
        if self.rect.bottom < 0:
            self.kill()

# Classe do Power-up de Vida
class HealthPowerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Usa o sprite de vida ou fallback
        self.image = pygame.transform.scale(health_powerup_sprite, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 25)
        self.rect.y = -25
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        # Remove o power-up se ele sair da tela
        if self.rect.top > HEIGHT:
            self.kill()

# Classe do Power-up de Bomba
class BombPowerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Usa o sprite de bomba ou fallback
        self.image = pygame.transform.scale(bomb_powerup_sprite, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 64)
        self.rect.y = -64
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        # Remove o power-up se ele sair da tela
        if self.rect.top > HEIGHT:
            self.kill()

# Classe da Explosão com efeito ripple
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = 300
        self.speed = 8
        self.alpha = 255
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2))
        self.image.set_colorkey(BLACK)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.radius += self.speed
        self.alpha = max(0, 255 - (self.radius / self.max_radius * 255))
        
        if self.radius > self.max_radius:
            self.kill()
        else:
            # Cria a imagem da explosão ripple
            self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2))
            self.image.set_colorkey(BLACK)
            self.image.set_alpha(self.alpha)
            
            # Desenha círculos concêntricos para efeito ripple
            for i in range(3):
                ripple_radius = self.radius - (i * 20)
                if ripple_radius > 0:
                    color_intensity = max(0, self.alpha - (i * 50))
                    color = (255, min(255, 200 + color_intensity), 0)  # Amarelo-laranja
                    pygame.draw.circle(self.image, color, (self.max_radius, self.max_radius), int(ripple_radius), 3)
            
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)


# Classe para partículas de estrelas de fundo
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH-1)
        self.y = random.randint(0, HEIGHT-1)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.choice([1, 2])
        self.color = (random.randint(180,255), random.randint(180,255), random.randint(180,255))

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.x = random.randint(0, WIDTH-1)
            self.y = 0
            self.speed = random.uniform(0.5, 2.0)
            self.size = random.choice([1, 2])
            self.color = (random.randint(180,255), random.randint(180,255), random.randint(180,255))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, int(self.y), self.size, self.size))

# Função principal do jogo com suporte a multiplayer
def main():
    while True:
        # Home screen: escolha 1 ou 2 jogadores
        num_players = select_num_players()

        # Controles para cada jogador
        controls1 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'select': [pygame.K_RETURN, pygame.K_SPACE]}
        controls2 = {'left': pygame.K_a, 'right': pygame.K_d, 'select': [pygame.K_LSHIFT, pygame.K_RSHIFT]}

        # Seleção de naves para cada jogador
        if num_players == 2:
            player1_ship_index = select_ship(1, controls1)
            player2_ship_index = select_ship(2, controls2, exclude_ships=[player1_ship_index])
        else:
            player1_ship_index = select_ship(1, controls1)
            player2_ship_index = None


        # Adiciona controles de movimento e tiro
        controls1.update({'up': pygame.K_UP, 'down': pygame.K_DOWN, 'shoot': pygame.K_SPACE})
        controls2.update({'up': pygame.K_w, 'down': pygame.K_s, 'shoot': pygame.K_LSHIFT})

        # Cria jogadores
        player1 = Player(player1_ship_index, controls1, start_pos=(WIDTH//2 - 80, HEIGHT - 10))
        if num_players == 2:
            player2 = Player(player2_ship_index, controls2, start_pos=(WIDTH//2 + 80, HEIGHT - 10))
        else:
            player2 = None

        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        health_powerups = pygame.sprite.Group()
        bomb_powerups = pygame.sprite.Group()
        explosions = pygame.sprite.Group()

        all_sprites.add(player1)
        if player2:
            all_sprites.add(player2)

        for _ in range(5):
            a = Enemy(player1_ship_index)
            all_sprites.add(a)
            enemies.add(a)
        score = 0
        font = pygame.font.SysFont(None, 36)
        health_spawn_timer = 0
        bomb_spawn_timer = 0
        stars = [Star() for _ in range(80)]

        running = True
        while running:
            clock.tick(FPS)
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Player 1 shoot (only if alive)
                    if player1.alive() and player1.health > 0:
                        if event.key == controls1['shoot'] and not player1.shoot_pressed:
                            bullet = Bullet(player1.rect.centerx, player1.rect.top)
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            player1.shoot_pressed = True
                        if event.key == controls1['shoot']:
                            player1.shoot_pressed = True
                    if player2 and player2.alive() and player2.health > 0:
                        # Player 2 shoot (only if alive)
                        if event.key == controls2['shoot'] and not player2.shoot_pressed:
                            bullet = Bullet(player2.rect.centerx, player2.rect.top)
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            player2.shoot_pressed = True
                        if event.key == controls2['shoot']:
                            player2.shoot_pressed = True
                if event.type == pygame.KEYUP:
                    if player1.alive() and event.key == controls1['shoot']:
                        player1.shoot_pressed = False
                    if player2 and player2.alive() and event.key == controls2['shoot']:
                        player2.shoot_pressed = False

            # Atualiza estrelas
            for star in stars:
                star.update()
            all_sprites.update()
            explosions.update()

            # Spawna power-ups de vida ocasionalmente
            health_spawn_timer += 1
            if health_spawn_timer >= 600:
                if random.randint(1, 100) <= 30:
                    health_powerup = HealthPowerup()
                    all_sprites.add(health_powerup)
                    health_powerups.add(health_powerup)
                health_spawn_timer = 0

            # Spawna power-ups de bomba ocasionalmente
            bomb_spawn_timer += 1
            if bomb_spawn_timer >= 900:
                if random.randint(1, 100) <= 15:
                    bomb_powerup = BombPowerup()
                    all_sprites.add(bomb_powerup)
                    bomb_powerups.add(bomb_powerup)
                bomb_spawn_timer = 0

            # Colisões de tiros com inimigos
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 1
                new_enemy = Enemy(player1_ship_index)
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

            # Colisão inimigos com jogadores
            for idx, player in enumerate([player1, player2] if player2 else [player1]):
                if player is None:
                    continue
                enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
                for enemy in enemy_hits:
                    if player.take_damage():
                        if player.health <= 0:
                            # Remove player from all sprite groups so he disappears
                            player.kill()

            # Check if all players are dead to end the game
            if player2:
                if player1.health <= 0 and player2.health <= 0:
                    running = False

            # Colisão com power-ups de vida (aplica para todos os jogadores)
            for idx, player in enumerate([player1, player2] if player2 else [player1]):
                if player is None:
                    continue
                health_hits = pygame.sprite.spritecollide(player, health_powerups, True)
                for health_powerup in health_hits:
                    # Revive friend if possible
                    if num_players == 2 and player.health == player.max_health:
                        friend = player2 if player is player1 else player1
                        if friend and (not friend.alive() or friend.health <= 0):
                            friend.health = 1
                            if not friend.alive():
                                all_sprites.add(friend)
                            if friend is player1:
                                friend.rect.centerx, friend.rect.bottom = (WIDTH//2 - 80, HEIGHT - 10)
                            else:
                                friend.rect.centerx, friend.rect.bottom = (WIDTH//2 + 80, HEIGHT - 10)
                    else:
                        player.heal()

            # Colisão com power-ups de bomba (aplica para todos os jogadores)
            for idx, player in enumerate([player1, player2] if player2 else [player1]):
                if player is None:
                    continue
                bomb_hits = pygame.sprite.spritecollide(player, bomb_powerups, True)
                for bomb_powerup in bomb_hits:
                    explosion = Explosion(WIDTH // 2, HEIGHT // 2)
                    explosions.add(explosion)
                    all_sprites.add(explosion)
                    enemies_killed = len(enemies)
                    for enemy in enemies:
                        enemy.kill()
                        score += 2
                    for _ in range(5):
                        new_enemy = Enemy(player1_ship_index)
                        all_sprites.add(new_enemy)
                        enemies.add(new_enemy)

            # Desenha a tela
            screen.fill(BLACK)
            for star in stars:
                star.draw(screen)
            all_sprites.draw(screen)
            explosions.draw(screen)
            # Mostra a pontuação
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (650, 10))
            draw_health_bar(screen, player1, idx=0)
            if player2:
                draw_health_bar(screen, player2, idx=1)
            pygame.display.flip()

        # GAME OVER SCREEN
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_over = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            screen.fill(BLACK)
            for star in stars:
                star.update()
                star.draw(screen)
            over_font = pygame.font.SysFont(None, 96)
            over_text = over_font.render("GAME OVER", True, RED)
            over_rect = over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
            screen.blit(over_text, over_rect)
            score_font = pygame.font.SysFont(None, 60)
            score_text = score_font.render(f"Score: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(score_text, score_rect)
            info_font = pygame.font.SysFont(None, 40)
            info_text = info_font.render("Pressione ENTER ou ESPAÇO para jogar novamente", True, WHITE)
            info_rect = info_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
            screen.blit(info_text, info_rect)
            esc_text = info_font.render("Pressione ESC para sair", True, WHITE)
            esc_rect = esc_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 130))
            screen.blit(esc_text, esc_rect)
            pygame.display.flip()

# Executa o jogo
main()
