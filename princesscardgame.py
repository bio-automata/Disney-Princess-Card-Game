import pygame, random, sys, time
from pygame.locals import*

#constants

#screen constants
SCREEN_WIDTH = 1280
SCREEN_HEIGTH = 680

#cards constants
BACKCARD_IMAGE = pygame.image.load('resources/image/backcard.png')
CARDS_FILENAME = ('resources/image/anna.png' ,'resources/image/ariel.png','resources/image/belle.png' ,'resources/image/brave.png' ,'resources/image/cinderela.png' ,'resources/image/elsa.png' ,'resources/image/jade.png' ,'resources/image/pocahontas.png' ,'resources/image/rapunzel.png' ,'resources/image/sleepy.png' ,'resources/image/tiana.png' ,'resources/image/white.png')


NUMBER_OF_CARDS = len(CARDS_FILENAME)
DECK_SIZE = 2*NUMBER_OF_CARDS
CARD_WIDTH = 150
CARD_HEIGHT = 200
CARDS_SPACEMENT = 5

LINE_LENGTH = 8
TOP_BORDER = 60
LEFT_BORDER = 20


#game variables
BACKGROUND_IMAGE = pygame.image.load('resources/image/background.png')
PRESS_ANY_KEY_IMAGE = pygame.image.load('resources/image/pressanykey.png')
MENU_MUSIC = 'resources/music/happy.mp3'

GAMEOVER_IMAGE_FILENAME = ('resources/image/cinderelaending.png' ,'resources/image/elsaending.png' ,'resources/image/pocahontasending.png' ,'resources/image/rapunzelending.png' ,'resources/image/whiteending.png')
MUSICS_FILENAME = ('resources/music/cinderela.mp3','resources/music/rapunzel.mp3','resources/music/anna.mp3','resources/music/elsa.mp3','resources/music/brave.mp3')
NUMBER_OF_MUSICS = len(MUSICS_FILENAME)

class Card(object):
  def __init__(self, number):
    self.__number = number
    self.__image = pygame.image.load(CARDS_FILENAME[self.__number])
    self.__covered = True
    self.__veiled = True
    
  def setImage(self, imageAddress):
    self.image = pygame.image.load(imageAddress)
  
  def number(self):
    return self.__number
  
  def image(self):
    return self.__image
  
  def covered(self):
    return self.__covered
  
  
  def veiled(self):
    return self.__veiled
    
  def flip(self):
    if(self.__veiled):
      self.__covered = not self.__covered
    else:
      self.__covered = False
  
  def unveil(self):
    self.__veiled = False


class Game(object):
  def __init__(self):
    self.__screen = None
    self.__cards = None
    self.__state = None
    self.__messageTurn = None
    self.__uncoveredCards = []
    self.__numberOfUnveiledCards = 0
    
    self.__mousex  = 0
    self.__mousey  = 0
  
  #variables management
  def raffleCards (self):
    self.__cards = []
    for i in range(0, NUMBER_OF_CARDS):
      for j in range(0, 2):
        card = Card(i)
        if(self.__cards==[]):
          self.__cards.append(card)
        else:
          self.__cards.insert(random.randrange(len(self.__cards)+1), card)
  
  def increaseUnveiledCards(self):
    self.__numberOfUnveiledCards = self.__numberOfUnveiledCards+1  
  
  def addUncoveredCard(self, card):
    self.__uncoveredCards.append(card)
  
  def resetUncoveredCards(self):
    self.__uncoveredCards = []
    
  
  #game
  def initialize(self):
    pygame.init()
    pygame.display.set_caption('Disney Princess Card Game')
    self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
  
  def menu(self):
    self.__state = 'menu'
    pygame.mixer.music.load(MENU_MUSIC)
    pygame.mixer.music.play(-1, 0.0)
    self.__messageTurn = True
    while(self.__state=='menu'):
      self.drawMenu()
      self.sensoring()
      time.sleep(0.5)
      self.__messageTurn = not self.__messageTurn
  
  def start(self):
    #initializing variables
    self.raffleCards()
    self.__uncoveredCards = []
    self.__numberOfUnveiledCards = 0
    pygame.mixer.music.load(MUSICS_FILENAME[random.randrange(NUMBER_OF_MUSICS)])
    pygame.mixer.music.play(-1, 0.0)
    
    #playing loop
    self.__state = 'playing'
    while(self.__state=='playing'):
      self.drawGame()
      self.monitoring()
      self.sensoring()
    
  def gameOver(self):
    self.__state='gameover'
    
    time.sleep(2)
    gameoverImage = pygame.image.load(GAMEOVER_IMAGE_FILENAME[random.randrange(len(GAMEOVER_IMAGE_FILENAME))])
    self.__screen.blit(gameoverImage, (0,0))
    pygame.display.update()
    time.sleep(3)
    self.menu()
    
  #game logic
  def monitoring(self):
    if(len(self.__uncoveredCards)==2):
      if(self.__cards[self.__uncoveredCards[0]].number()==self.__cards[self.__uncoveredCards[1]].number()):
        self.__cards[self.__uncoveredCards[0]].unveil()
        self.__cards[self.__uncoveredCards[1]].unveil()
        self.increaseUnveiledCards()
        
      else:
        self.__cards[self.__uncoveredCards[0]].flip()
        self.__cards[self.__uncoveredCards[1]].flip()
      self.resetUncoveredCards()
      time.sleep(0.5)
        
    if(self.__numberOfUnveiledCards==NUMBER_OF_CARDS):
      self.gameOver()
    


  #event traetement
  def sensoring(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONDOWN:
        self.__mousex, self.__mousey = event.pos        
        self.onClick()

  def onClick(self):
    if(self.__state=='menu'):
      self.start()
    elif(self.__state=='playing'):
      for i in range(0, DECK_SIZE):
        x = LEFT_BORDER+(i%LINE_LENGTH)*CARD_WIDTH+CARDS_SPACEMENT*(i%LINE_LENGTH)
        y = TOP_BORDER+int(i/LINE_LENGTH)*CARD_HEIGHT+CARDS_SPACEMENT*int(i/LINE_LENGTH)
        
        if((self.__mousex>x and self.__mousex<x+CARD_WIDTH) and (self.__mousey>y and self.__mousey<y+CARD_HEIGHT)):
          if((self.__cards[i].covered())):
            self.__cards[i].flip()
            self.addUncoveredCard(i)
                        
    elif(self.__state=='gameover'):
      self.Menu()
    

  #drawing
  def drawMenu(self):
    self.__screen.blit(BACKGROUND_IMAGE, (0,0))
    if(self.__messageTurn):
      self.__screen.blit(PRESS_ANY_KEY_IMAGE, (380,350))
    pygame.display.update()

  def drawGame(self):  
    self.__screen.blit(BACKGROUND_IMAGE, (0,0))
    for i in range(0, DECK_SIZE):
      x = LEFT_BORDER+(i%LINE_LENGTH)*CARD_WIDTH+CARDS_SPACEMENT*(i%LINE_LENGTH)
      y = TOP_BORDER+int(i/LINE_LENGTH)*CARD_HEIGHT+CARDS_SPACEMENT*int(i/LINE_LENGTH)
            
      if(self.__cards[i].covered()):
        self.__screen.blit(BACKCARD_IMAGE, (x,y))
      else:
        self.__screen.blit(self.__cards[i].image(), (x,y))      
    
    pygame.display.update()  
    
    
  def drawGameOver(self):
    self.__screen.blit(BACKGROUND_IMAGE, (0,0))
    self.__screen.blit(PRESS_ANY_KEY_IMAGE, (200,0))
    
    
    pygame.display.update()


game = Game()
game.initialize()
game.menu()

