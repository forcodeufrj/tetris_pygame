import pygame
import random

# Inicializando o Pygame
pygame.init()

# Configurações da janela
largura_janela = 800
altura_janela = 720
largura_jogo = 300
altura_jogo = 600
bloco_tamanho = 30

# Configurações da grade
jogo_topo_esquerdo_x = (largura_janela - largura_jogo) // 2
jogo_topo_esquerdo_y = altura_janela - altura_jogo - 50

# Formatos das peças
formatos = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],
    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],
    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],
    [['.....',
      '.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....']],
    [['.....',
      '..0..',
      '.000.',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..'],
     ['.....',
      '.....',
      '.000.',
      '..0..'],
     ['.....',
      '..0..',
      '.00..',
      '..0..']],
    [['.....',
      '.0...',
      '.000.',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..'],
     ['.....',
      '.....',
      '.000.',
      '...0.'],
     ['.....',
      '..0..',
      '..0..',
      '.00..']],
    [['.....',
      '...0.',
      '.000.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.'],
     ['.....',
      '.....',
      '.000.',
      '.0...'],
     ['.....',
      '.00..',
      '..0..',
      '..0..']]
]

# Cores das peças
cores = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 255, 255),
    (128, 0, 128)
]

class Peça:
    def __init__(self, x, y, formato):
        self.x = x
        self.y = y
        self.formato = formato
        self.cor = cores[formatos.index(formato)]
        self.rotacao = 0

def criar_grid(travada_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in travada_pos:
                c = travada_pos[(j, i)]
                grid[i][j] = c
    return grid

def converter_formato_forma(peca):
    posicoes = []
    formato = peca.formato[peca.rotacao % len(peca.formato)]

    for i, linha in enumerate(formato):
        fila = list(linha)
        for j, coluna in enumerate(fila):
            if coluna == '0':
                posicoes.append((peca.x + j, peca.y + i))

    for i, pos in enumerate(posicoes):
        posicoes[i] = (pos[0] - 2, pos[1] - 4)
    return posicoes

def peça_valida(peca, grid):
    posicoes_aceitaveis = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    posicoes_aceitaveis = [j for sub in posicoes_aceitaveis for j in sub]
    formatado = converter_formato_forma(peca)

    for pos in formatado:
        if pos not in posicoes_aceitaveis:
            if pos[1] >= 0:
                return False
    return True

def obter_forma():
    return Peça(5, 0, random.choice(formatos))

def desenhar_grid(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (j * bloco_tamanho + jogo_topo_esquerdo_x, i * bloco_tamanho + jogo_topo_esquerdo_y, bloco_tamanho, bloco_tamanho), 0)
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (jogo_topo_esquerdo_x, jogo_topo_esquerdo_y + i * bloco_tamanho), (jogo_topo_esquerdo_x + largura_jogo, jogo_topo_esquerdo_y + i * bloco_tamanho))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (jogo_topo_esquerdo_x + j * bloco_tamanho, jogo_topo_esquerdo_y), (jogo_topo_esquerdo_x + j * bloco_tamanho, jogo_topo_esquerdo_y + altura_jogo))

def limpar_linhas(grid, travada_pos):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        linha = grid[i]
        if (0, 0, 0) not in linha:
            inc += 1
            ind = i
            for j in range(len(linha)):
                try:
                    del travada_pos[(j, i)]
                except:
                    continue

    if inc > 0:
        for chave in sorted(list(travada_pos), key=lambda x: x[1])[::-1]:
            x, y = chave
            if y < ind:
                nova_chave = (x, y + inc)
                travada_pos[nova_chave] = travada_pos.pop(chave)
    return inc

def desenhar_proxima_forma(peca, surface):
    fonte = pygame.font.SysFont('', 30)
    label = fonte.render('Próxima Forma', 1, (255, 255, 255))

    sx = jogo_topo_esquerdo_x + largura_jogo + 50
    sy = jogo_topo_esquerdo_y + altura_jogo//2 - 130
    formato = peca.formato[peca.rotacao % len(peca.formato)]

    for i, linha in enumerate(formato):
        fila = list(linha)
        for j, coluna in enumerate(fila):
            if coluna == '0':
                pygame.draw.rect(surface, peca.cor, (sx + j*bloco_tamanho, sy + i*bloco_tamanho, bloco_tamanho, bloco_tamanho), 0)

    surface.blit(label, (sx + 10, sy))

def desenhar_janela(surface, grid, score=0):
    surface.fill((30, 22, 71))
    fonte = pygame.font.SysFont('', 50)
    label = fonte.render('FOR_TETRIS', 1, (255, 255, 255))

    surface.blit(label, (jogo_topo_esquerdo_x + largura_jogo // 2 - (label.get_width() // 2), 30))

    fonte = pygame.font.SysFont('', 30)
    label = fonte.render('Pontos: ' + str(score), 1, (255, 255, 255))

    sx = jogo_topo_esquerdo_x + largura_jogo + 50
    sy = jogo_topo_esquerdo_y + altura_jogo // 2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (j * bloco_tamanho + jogo_topo_esquerdo_x, i * bloco_tamanho + jogo_topo_esquerdo_y, bloco_tamanho, bloco_tamanho), 0)
    desenhar_grid(surface, grid)

def main():
    travada_pos = {}
    grid = criar_grid(travada_pos)

    troca_peca = False
    rodada = 0
    corrente_peca = obter_forma()
    próxima_peca = obter_forma()
    clock = pygame.time.Clock()
    queda_tempo = 0
    score = 0

    run = True
    while run:
        grid = criar_grid(travada_pos)
        queda_tempo += clock.get_rawtime()
        clock.tick()

        if queda_tempo / 1000 > 0.27:
            queda_tempo = 0
            corrente_peca.y += 1
            if not (peça_valida(corrente_peca, grid)) and corrente_peca.y > 0:
                corrente_peca.y -= 1
                troca_peca = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    corrente_peca.x -= 1
                    if not peça_valida(corrente_peca, grid):
                        corrente_peca.x += 1
                if event.key == pygame.K_RIGHT:
                    corrente_peca.x += 1
                    if not peça_valida(corrente_peca, grid):
                        corrente_peca.x -= 1
                if event.key == pygame.K_DOWN:
                    corrente_peca.y += 1
                    if not peça_valida(corrente_peca, grid):
                        corrente_peca.y -= 1
                if event.key == pygame.K_UP:
                    corrente_peca.rotacao = corrente_peca.rotacao + 1 % len(corrente_peca.formato)
                    if not peça_valida(corrente_peca, grid):
                        corrente_peca.rotacao = corrente_peca.rotacao - 1 % len(corrente_peca.formato)

        forma_pos = converter_formato_forma(corrente_peca)

        for i in range(len(forma_pos)):
            x, y = forma_pos[i]
            if y > -1:
                grid[y][x] = corrente_peca.cor

        if troca_peca:
            for pos in forma_pos:
                p = (pos[0], pos[1])
                travada_pos[p] = corrente_peca.cor
            corrente_peca = próxima_peca
            próxima_peca = obter_forma()
            troca_peca = False
            score += limpar_linhas(grid, travada_pos) * 10

        desenhar_janela(janela, grid, score)
        desenhar_proxima_forma(próxima_peca, janela)
        pygame.display.update()

        if any(y < 1 for (x, y) in travada_pos):
            run = False
            draw_text_middle("Você Perdeu", 80, (255, 255, 255), janela)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

def main_menu():
    run = True
    while run:
        janela.fill((30, 22, 71))
        draw_text_middle('FOR_TETRIS', 60, (255, 255, 255), janela)
        draw_text_middle('\n\n\n\n\n\nPressione qualquer\ntecla para começar', 25, (255, 255, 255), janela)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.display.quit()

def draw_text_middle(text, size, color, surface):
    fonte = pygame.font.SysFont('', size, bold=True)
    label = fonte.render(text, 1, color)

    surface.blit(label, (jogo_topo_esquerdo_x + largura_jogo / 2 - (label.get_width() / 2), jogo_topo_esquerdo_y + altura_jogo / 2 - (label.get_height() / 2)))

janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption('for_tetris')

main_menu()
