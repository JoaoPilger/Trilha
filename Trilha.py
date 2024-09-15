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
player1 = pygame.image.load("img/azul.webp").convert_alpha()
player1 = pygame.transform.scale(player1, (38,38))
player1_rect = player1.get_rect()

#imagem que representa o player2
player2 = pygame.image.load("img/verde.webp").convert_alpha()
player2 = pygame.transform.scale(player2, (39,38))
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

    def dicionarioCasa(self):
        return {
            'id': self.id,
            'ocupado': self.ocupado,
            'peca': self.peca,
            'vizinhos': self.vizinhos,
            'camada_id': self.camada_id,
            'coordenadas': self.coordenadas
        }
    
class imgJogador:
    def __init__(self,imgCoord,imagem):
        self.imgCoord = imgCoord
        self.imagem = imagem

    def dicionarioImg(self):
        return{
            "coordenadas" : self.imgCoord,
            "cor" : self.imagem
        }

#define o jogador inicial
jogador = player1

#variável para quantidade de peças
pecas = [[],[]]
pecaJogador = 0
pecaEstado = True

#para armazenar informações passadas(usado na troca de peças)
aTrocarCoord= []
aTrocarPeca = []
aTrocarOcup = []
aTrocarVizi = []
aTrocarCamada = []

#registra quantos eventos aconteceram (usado na troca de peças)
QuantEvents = 0

subtraiEvents = 0

#registra se o clique de escolha de peça já aconteceu
cliqueState = False

#variável para carregar as imagens que representam os jogadores
imagens = []

#define os valores para o parâmetro vizinho da classe Casa e o dicionário dicionarioCasa
def vizinhos(i):
        if i == 0:
            return [1, 7]
        elif i == 7:
            return [0, 6, i]
        elif i % 2 != 0:
            return [i + 1, i -1, i]
        else:
            return [i + 1, i - 1]


#cria os retângulos clicáveis
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
            tabuleiro[idx].append(novaCasa.dicionarioCasa())
        if idx < 2:
            left += 115
            top += 115
            salto -= 114   


#escolha inicial das casas
def escolhaInicial(pecas,pecaJogador):
    mouse_pos = event.pos
    for i in tabuleiro:
        for e in i:
            if len(pecas[pecaJogador]) < 9:
                escolhaCasa(e['coordenadas'], mouse_pos, pecas,pecaEstado,pecaJogador,e)
                # verificarTrios(tabuleiro,idx,e)


def escolhaCasa(casa, mouse_pos, pecas,pecaEstado,pecaJogador,e):
    if casa.collidepoint(mouse_pos):
        global jogador
        if e['ocupado'] == False:
            e['ocupado'] = True
            e['peca'] = jogador
            pecas[pecaJogador].append(pecaEstado) #posso alterar para False quando retirar a peca do jogo sem quebrar o loop d repetição
            novoJogador = imgJogador(e['coordenadas'],jogador)
            imagens.append(novoJogador.dicionarioImg())
            jogador = player1 if jogador == player2 else player2


            print("ocupado")
        else:
            print('Escolha outra casa')


#escolhe a peça a ser trocada
def escolhaTroca(posicaoInicial,mouse_pos, e):
    if posicaoInicial.collidepoint(mouse_pos):
        if e['ocupado'] == True and e['peca'] == jogador:
            aTrocarCoord.append(e['coordenadas'])
            aTrocarPeca.append(e['peca'])
            aTrocarOcup.append(e['ocupado'])
            aTrocarVizi.append(e['vizinhos'])
            aTrocarCamada.append(e['camada_id'])


def trocaPosicao(i,obj,idx):
    global jogador
    for e in i:
        if e['ocupado'] == aTrocarOcup[idx - 1] and e['peca'] == aTrocarPeca[idx - 1]:
            e['ocupado'] = False
            e['peca'] = None
            for imagem in imagens:
                if aTrocarCoord[idx - 1] == imagem['coordenadas']:
                        imagem['coordenadas'] = obj['coordenadas']
            obj['ocupado'] = True
            obj['peca'] = jogador
            print("trocado")
            jogador = player1 if jogador == player2 else player2
            break

                #criar elif para caso seja a mesma casa em camadas diferentes



def trocaCasa(idx):
    mouse_pos = event.pos
    global cliqueState

    if cliqueState == True:
        for i in tabuleiro:
            for obj in i:
                if obj['ocupado'] == False and aTrocarCoord[idx - 1] != obj['coordenadas']: #ta tendo problema no idx que não troca d 0!!!
                    if obj['coordenadas'].collidepoint(mouse_pos) and obj['id'] in aTrocarVizi[idx - 1]:
                        trocaPosicao(i,obj,idx)
                        cliqueState = 1
    
    if cliqueState == False:
        for i in tabuleiro:
            for e in i:
                if e['ocupado'] == True and e['coordenadas'].collidepoint(mouse_pos) and e['peca'] == jogador:
                    escolhaTroca(e['coordenadas'], mouse_pos, e)
                    cliqueState = True
                    idx += 1
                    break
            if cliqueState == True:
                print('escolha uma casa vizinha vazia para trocar de lugar')
                return cliqueState
            
    if cliqueState == 1:
        cliqueState = False


#loop de funcionamento
criarPosicoes()

#desenha as imagens após cada update de tela
def desenhaImagem():
    idx = 0
    for imgObj in imagens:
        screen.blit(imgObj['cor'],imgObj['coordenadas'])
        idx += 1
    
#loop para o jogo rodar e atualizar
while rodando:

    for event in pygame.event.get(): #verifica eventos que ocorrem no jogo    
        if event.type == pygame.QUIT: #verifica se a aba foi fechada para encerrar o loop
            rodando = False

        if len(pecas[pecaJogador]) == 9 and event.type == pygame.MOUSEBUTTONDOWN:
            trocaCasa(QuantEvents)

        if len(pecas[pecaJogador]) < 9 and event.type == pygame.MOUSEBUTTONDOWN: #Verifica a posição do clique e executa a função cliqueCasa
            if pecaJogador == 0:
                imagem = pygame.transform.scale(player1, (50,50))
            elif pecaJogador == 1:
                imagem = pygame.transform.scale(player2, (40,40))
            escolhaInicial(pecas,pecaJogador)

        if jogador == player1:
            pecaJogador = 0
        elif jogador == player2:
            pecaJogador = 1

    screen.blit(background, (0,0))
    desenhaImagem()
    pygame.display.flip()
    