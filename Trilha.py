#importação da biblioteca pygame após o pip install pygame
import pygame

#inicia o pygame
pygame.init()

#tamanho da tela
x = 700
y = 700

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("Trilha")

#imagem de fundo
background = pygame.image.load('img/tabuleiro.png').convert_alpha()
background = pygame.transform.scale(background, (x,y))

#imagem que representa o player1
player1 = pygame.image.load("img/vermelho.png").convert_alpha()
player1 = pygame.transform.scale(player1, (50,50))
player1_rect = player1.get_rect()

#imagem que representa o player2
player2 = pygame.image.load("img/verde.webp").convert_alpha()
player2 = pygame.transform.scale(player2, (40,40))
player2_rect = player2.get_rect()

#para manter o loop do jogo ativo
rodando = True

#definição da class Casa para criar objetos e dicionários
class Casa:
    def __init__(self,id,ocupado,peca,vizinhos,camada_id,coordenadas):
        self.id = id
        self.ocupado = ocupado
        self.peca = peca
        self.vizinhos = vizinhos
        self.camada_id = camada_id
        self.coordenadas = coordenadas

    def dictionaryCasa(self):
        return {
            'id': self.id,
            'ocupado': self.ocupado,
            'peca': self.peca,
            'vizinhos': self.vizinhos,
            'camada_id': self.camada_id,
            'coordenadas': self.coordenadas
        }

#define os valores para a lista vizinhos
def vizinhos(idx):
        if idx == 0:
            return [1, 7]
        elif idx == 7:
            return [0, 6]
        else:
            return [idx + 1, idx - 1]

#cria os retângulos interativo     
def criaRects(left,top,salto):
    global coords
    coords = [[],[],[]]
    idx = 0
    for lista in coords:
        for e in range(8):
            if e <= 1:
                casa = pygame.Rect(left,top,36,36)
                coords[coords.index(lista)].append(casa)
                left += salto
            elif e > 1 and e <= 3:
                casa = pygame.Rect(left,top,36,36)
                coords[coords.index(lista)].append(casa)
                top += salto
            elif e > 3 and e <= 5:
                casa = pygame.Rect(left,top,36,36)
                coords[coords.index(lista)].append(casa)
                left -= salto
            elif e > 5 and e <= 7:
                casa = pygame.Rect(left,top,36,36)
                coords[coords.index(lista)].append(casa)
                top -= salto
        idx +=1

    

#cria o tabuleiro e os objetos "Casa"
def criarPosicoes():
    global tabuleiro
    tabuleiro = [[],[],[]]

    left = 13
    top = 13
    salto = 318

    for idx in range(3):
        for i in range(8):
            criaRects(left,top,salto)
            novaCasa = Casa(i,False,None,vizinhos(i),idx,coords[idx][i])
            tabuleiro[idx].append(novaCasa.dictionaryCasa())
        if idx < 2:
            left += 115
            top += 115
            salto -= 114

#confere se o clique foi dentro de uma casa
def cliqueCasa(casa,mouse_pos):
    if casa.collidepoint(mouse_pos):
        e['ocupado'] = True
        print("ocupado")

#loop de funcionamento
criarPosicoes()
    
#loop para o jogo rodar e atualizar
while rodando:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            idx = 0
            for i in tabuleiro:
                for e in tabuleiro[idx]:
                    cliqueCasa(e['coordenadas'],mouse_pos)
                idx +=1

    screen.blit(background, (0,0))
    pygame.display.update()