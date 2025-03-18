import pygame
import random

class DeleteSystem32:
    def delete(self):
        # Inicialização do Pygame
        pygame.init()

        # Configurações da tela
        WIDTH, HEIGHT = 400, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        # Cores
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        # Configurações do jogo
        gravity = 1
        jump = -10
        pipe_width = 70
        pipe_gap = 150
        bird_x = 50
        bird_y = HEIGHT // 2
        bird_radius = 15
        bird_velocity = 0
        pipes = []
        score = 0
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        # Função para criar novos canos
        def create_pipe():
            y = random.randint(100, 400)
            pipes.append({'x': WIDTH, 'y': y})

        # Loop principal
        game_over = False
        while not game_over:
            screen.fill(WHITE)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_velocity = jump

            # Atualizar posição do pássaro
            bird_velocity += gravity
            bird_y += bird_velocity

            # Criar novos canos
            if len(pipes) == 0 or pipes[-1]['x'] < WIDTH - 200:
                create_pipe()

            # Mover e desenhar canos
            for pipe in pipes[:]:
                pipe['x'] -= 5
                pygame.draw.rect(screen, GREEN, (pipe['x'], 0, pipe_width, pipe['y']))
                pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['y'] + pipe_gap, pipe_width, HEIGHT))

                # Verificar colisão
                if (bird_x + bird_radius > pipe['x'] and bird_x - bird_radius < pipe['x'] + pipe_width and
                    (bird_y - bird_radius < pipe['y'] or bird_y + bird_radius > pipe['y'] + pipe_gap)):
                    game_over = True

                # Atualizar pontuação
                if pipe['x'] + pipe_width == bird_x:
                    score += 1

                # Remover cano fora da tela
                if pipe['x'] < -pipe_width:
                    pipes.remove(pipe)

            # Desenhar pássaro
            pygame.draw.circle(screen, BLUE, (bird_x, int(bird_y)), bird_radius)

            # Exibir pontuação
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            # Verificar se o pássaro caiu
            if bird_y > HEIGHT or bird_y < 0:
                game_over = True

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
