from math import fabs
import pygame, random, enum
import os
from src.Card import Card

ASSETS_PATH = "./assets/"

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

DIFFICULTY = 10

class GameState(enum.Enum):
    PLAYING = 0
    WIN = 1
    LOOSE = 2

class Status(enum.Enum):
    MENU = 1
    GAME = 2
    SETTINGS = 3


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.selectCard = []
        self.winCard = [[], []]
        self.status = Status.GAME
        self.gameState = GameState.PLAYING
        self.errorLeft = DIFFICULTY
        self.changeDifficultyInt = DIFFICULTY
        self.score = 0
        self.changeDifficulty = False
        self.audioLevel = 10
        self.changeAudioLevel = 10


        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(ASSETS_PATH + "bg.jpeg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.backgroundRect = self.background.get_rect()
        self.youWinText = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 100)
        self.youWinTextSurface = self.youWinText.render("You Win", True, (0, 255, 0))
        self.youWinTextRect = self.youWinTextSurface.get_rect()
        self.youWinTextRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)

        self.youLooseText = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 100)
        self.youLooseTextSurface = self.youLooseText.render("You Loose", True, (255, 0, 0))
        self.youLooseTextRect = self.youLooseTextSurface.get_rect()
        self.youLooseTextRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.clickText = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 50)
        self.clickTextSurface = self.clickText.render("Click on the pile of cards to restart", True, (255, 255, 255))
        self.clickTextRect = self.clickTextSurface.get_rect()
        self.clickTextRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)

        self.clickTextWin = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 50)
        self.clickTextSurfaceWin = self.clickTextWin.render("Click on one of the win card to restart", True, (255, 255, 255))
        self.clickTextRectWin = self.clickTextSurfaceWin.get_rect()
        self.clickTextRectWin.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.goutte = pygame.image.load(ASSETS_PATH + "goutte.png")
        self.goutte = pygame.transform.scale(self.goutte, (100, 100))
        self.goutteRect = self.goutte.get_rect()
        self.goutteRect.center = (SCREEN_WIDTH - 100, SCREEN_HEIGHT / 2)

        self.error = pygame.image.load(ASSETS_PATH + "error.png")
        self.error = pygame.transform.scale(self.error, (100, 100))
        self.errorRect = self.error.get_rect()
        self.errorRect.center = (100, SCREEN_HEIGHT / 2)

        self.scoreText = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 50)
        self.scoreTextSurface = self.scoreText.render(str(self.score), True, (255, 255, 255))
        self.scoreTextRect = self.scoreTextSurface.get_rect()
        self.scoreTextRect.center = (SCREEN_WIDTH - 95, SCREEN_HEIGHT / 2 + 10)

        self.errorText = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 50)
        self.errorTextSurface = self.errorText.render(str(self.errorLeft), True, (255, 255, 255))
        self.errorTextRect = self.errorTextSurface.get_rect()
        self.errorTextRect.center = (95, SCREEN_HEIGHT / 2 + 5)

        self.settings = pygame.image.load(ASSETS_PATH + "setting.png")
        self.settings = pygame.transform.scale(self.settings, (30, 30))
        self.settingsRect = self.settings.get_rect(x = (SCREEN_WIDTH - 40), y = 10)

        self.restartLogo = pygame.image.load(ASSETS_PATH + "restart.png")
        self.restartLogo = pygame.transform.scale(self.restartLogo, (30, 30))
        self.restartLogoRect = self.restartLogo.get_rect(x = 10, y = 10)

        self.settingMenu = pygame.image.load(ASSETS_PATH + "setting-menu.png")
        self.settingMenu = pygame.transform.scale(self.settingMenu, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.settingMenuRect = self.settingMenu.get_rect()
        self.settingMenuRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)




        self.settingTextDifficulty = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 50)
        self.settingTextDifficultySurface = self.settingTextDifficulty.render(str(self.changeDifficultyInt), True, (255, 255, 255))
        self.settingTextDifficultyRect = self.settingTextDifficultySurface.get_rect()
        self.settingTextDifficultyRect.center = (852, 396)

        self.diffiPlus = pygame.image.load(ASSETS_PATH + "+.png")
        self.diffiPlus = pygame.transform.scale(self.diffiPlus, (25, 25))
        self.diffiPlusRect = self.diffiPlus.get_rect(x = self.settingTextDifficultyRect.x + self.settingTextDifficultyRect.width + 30, y = self.settingTextDifficultyRect.y + 15)

        self.diffiMinus = pygame.image.load(ASSETS_PATH + "-.png")
        self.diffiMinus = pygame.transform.scale(self.diffiMinus, (25, 10))
        self.diffiMinusRect = self.diffiMinus.get_rect(x = self.settingTextDifficultyRect.x - 50, y = self.settingTextDifficultyRect.y + 25)




        self.settingTextAudio = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 50)
        self.settingTextAudioSurface = self.settingTextAudio.render(str(self.changeAudioLevel), True, (255, 255, 255))
        self.settingTextAudioRect = self.settingTextAudioSurface.get_rect()
        self.settingTextAudioRect.center = (544, 392)

        self.audioPlus = pygame.image.load(ASSETS_PATH + "+.png")
        self.audioPlus = pygame.transform.scale(self.audioPlus, (25, 25))
        self.audioPlusRect = self.audioPlus.get_rect(x = self.settingTextAudioRect.x + self.settingTextAudioRect.width + 30, y = self.settingTextAudioRect.y + 15)

        self.audioMinus = pygame.image.load(ASSETS_PATH + "-.png")
        self.audioMinus = pygame.transform.scale(self.audioMinus, (25, 10))
        self.audioMinusRect = self.audioMinus.get_rect(x = self.settingTextAudioRect.x - 50, y = self.settingTextAudioRect.y + 25)




        self.settingChangeDiff = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 20)
        self.settingChangeDiffSurface = self.settingChangeDiff.render('You must restart the game if you change the difficulty', True, (255, 255, 255))
        self.settingChangeDiffRect = self.settingChangeDiffSurface.get_rect(x = 424, y = 520)

        self.settingSave = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 18)
        self.settingSaveSurface = self.settingSave.render('Save', True, (255, 255, 255))
        self.settingSaveRect = self.settingSaveSurface.get_rect(x = 820, y = 555)

        self.settingRestart = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 18)
        self.settingRestartSurface = self.settingRestart.render('Restart', True, (255, 255, 255))
        self.settingRestartRect = self.settingRestartSurface.get_rect(x = 820, y = 555)

        self.settingExit = pygame.font.Font(ASSETS_PATH + "Coffin-Stone.ttf", 18)
        self.settingExitSurface = self.settingExit.render('Exit', True, (255, 255, 255))
        self.settingExitRect = self.settingExitSurface.get_rect(x = 820, y = 595)



        self.audio = pygame.mixer.Sound(ASSETS_PATH + 'waves.mp3')
        self.audio.set_volume(self.audioLevel / 10)
        self.audio.play(-1)

        self.personnage_list = []
        for file in os.listdir(ASSETS_PATH + "personnage"):
            if file.endswith(".png"):
                self.personnage_list.append(os.path.splitext(file)[0])




        self.card_list = []
        for personnage in self.personnage_list:
            self.card_list.append(Card(SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 300, personnage))
            self.card_list.append(Card(SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 300, personnage))
        random.shuffle(self.card_list)




        self.nb_cards_per_line = int(SCREEN_WIDTH / self.card_list[0].getWidth())
        self.nb_cards_per_column = int(SCREEN_HEIGHT / self.card_list[0].getHeight())




        width = (SCREEN_WIDTH - self.nb_cards_per_line * self.card_list[0].getWidth()) / 2
        heaight = 10
        i = 0
        for card in self.card_list:
            if width + self.card_list[0].getWidth() > self.backgroundRect.width:
                heaight += self.card_list[0].getHeight() + 10
                # get the size of the card_list list
                if (len(self.card_list) - i) < self.nb_cards_per_line:
                    width = (SCREEN_WIDTH - (len(self.card_list) + 1 - i) * self.card_list[0].getWidth()) / 2 + 10
                else:
                    width = (SCREEN_WIDTH - self.nb_cards_per_line * self.card_list[0].getWidth()) / 2
            card.wantedPosition = [width, heaight]
            width += self.card_list[0].getWidth() + 10
            i += 1


    def restart(self, difficulty):
        self.gameState = GameState.PLAYING

        for card in self.winCard[0]:
            self.card_list.append(card[0])
            self.card_list.append(card[1])
        for card in self.winCard[1]:
            self.card_list.append(card[0])
            self.card_list.append(card[1])

        for card in self.card_list:
            del card

        self.card_list = []
        for personnage in self.personnage_list:
            self.card_list.append(Card(SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 300, personnage))
            self.card_list.append(Card(SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 300, personnage))
        random.shuffle(self.card_list)

        self.status = Status.GAME
        self.changeDifficulty = False
        self.winCard = [[], []]
        self.selectCard = []
        self.errorLeft = difficulty
        self.changeDifficulty = False
        self.score = 0
        self.errorTextSurface = self.errorText.render(str(self.errorLeft), True, (255, 255, 255))
        self.scoreTextSurface = self.scoreText.render(str(self.score), True, (255, 255, 255))

        width = (SCREEN_WIDTH - self.nb_cards_per_line * self.card_list[0].getWidth()) / 2
        heaight = 10
        i = 0
        for card in self.card_list:
            if width + self.card_list[0].getWidth() > self.backgroundRect.width:
                heaight += self.card_list[0].getHeight() + 10
                if (len(self.card_list) - i) < self.nb_cards_per_line:
                    width = (SCREEN_WIDTH - (len(self.card_list) + 1 - i) * self.card_list[0].getWidth()) / 2 + 10
                else:
                    width = (SCREEN_WIDTH - self.nb_cards_per_line * self.card_list[0].getWidth()) / 2
            card.wantedPosition = [width, heaight]
            card.isStart = False
            card.isFront = True
            width += self.card_list[0].getWidth() + 10
            i += 1



    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)


                if (self.restartLogoRect.collidepoint(mouse_pos)):
                    self.restart(self.changeDifficultyInt)

                if self.settingsRect.collidepoint(mouse_pos):
                    if (self.status == Status.SETTINGS): self.status = Status.GAME
                    else :
                        self.status = Status.SETTINGS
                        self.changeAudioLevel = self.audioLevel

                if (self.status == Status.SETTINGS):
                    if (self.diffiMinusRect.collidepoint(mouse_pos)):
                        if (self.changeDifficultyInt > 1):
                            self.changeDifficultyInt -= 1
                            self.settingTextDifficultySurface = self.settingTextDifficulty.render(str(self.changeDifficultyInt), True, (255, 255, 255))
                            self.changeDifficulty = True
                    elif (self.diffiPlusRect.collidepoint(mouse_pos)):
                        self.changeDifficultyInt += 1
                        self.settingTextDifficultySurface = self.settingTextDifficulty.render(str(self.changeDifficultyInt), True, (255, 255, 255))
                        self.changeDifficulty = True


                    if (self.audioMinusRect.collidepoint(mouse_pos)):
                        if (self.changeAudioLevel > 0):
                            self.changeAudioLevel -= 1
                            self.settingTextAudioSurface = self.settingTextAudio.render(str(self.changeAudioLevel), True, (255, 255, 255))
                    elif (self.audioPlusRect.collidepoint(mouse_pos)):
                        if (self.changeAudioLevel < 10):
                            self.changeAudioLevel += 1
                            self.settingTextAudioSurface = self.settingTextAudio.render(str(self.changeAudioLevel), True, (255, 255, 255))



                    if (self.settingRestartRect.collidepoint(mouse_pos) and self.changeDifficulty):
                        self.restart(self.changeDifficultyInt)
                    elif (self.settingRestartRect.collidepoint(mouse_pos)):
                        self.audioLevel = self.changeAudioLevel
                        self.audio.set_volume(self.audioLevel / 10)
                        self.status = Status.GAME
                    if (self.settingExitRect.collidepoint(mouse_pos)):
                        self.running = False
                    return


                if self.gameState == GameState.PLAYING:
                    for card in self.card_list:
                        if card.cardRect.collidepoint(mouse_pos):
                            if card in self.selectCard:
                                pass
                            else:
                                self.selectCard.append(card)
                                for actual in self.card_list:
                                    if actual not in self.selectCard and actual.isFront == True:
                                        actual.isFront = False
                                card.isFront = not card.isFront
                            break
                if (self.gameState == GameState.LOOSE) and self.card_list[0].cardRect.collidepoint(mouse_pos):
                    self.restart()
                if (self.gameState == GameState.WIN):
                    for line in self.winCard:
                        for pair in line:
                            for card in pair:
                                if card.cardRect.collidepoint(mouse_pos):
                                    self.restart()
                                    break

    def update(self):

        if (self.status == Status.SETTINGS):
            return

        for card in self.card_list:
            card.move()

        for line in self.winCard:
            for card in line:
                card[0].move()
                card[1].move()


        if len(self.selectCard) == 2:
            if self.selectCard[0].name == self.selectCard[1].name:
                self.selectCard[0].isWin = True
                self.selectCard[1].isWin = True
                if (len(self.winCard[0]) >= 8):
                    self.winCard[1].append([self.selectCard[0], self.selectCard[1]])
                else:
                    self.winCard[0].append([self.selectCard[0], self.selectCard[1]])
                self.card_list.remove(self.selectCard[0])
                self.card_list.remove(self.selectCard[1])
                self.selectCard = []
                self.score += 1
                self.scoreTextSurface = self.scoreText.render(str(self.score), True, (255, 255, 255))
            else:
                self.errorLeft -= 1
                self.errorTextSurface = self.errorText.render(str(self.errorLeft), True, (255, 255, 255))
                self.selectCard[0].waitToTurn = True
                self.selectCard[1].waitToTurn = True
                self.selectCard = []


        width = (SCREEN_WIDTH - len(self.winCard) * 120 + 40) / 2 + 10
        heaight = SCREEN_HEIGHT - 163 - 10

        for line in self.winCard:
            i = 0
            if len(line) == 0: break
            width = (SCREEN_WIDTH - (len(line) - i) * (line[0][0].getWidth() + 40)) / 2
            for cardPair in line:
                cardPair[0].wantedPosition = [width, heaight]
                cardPair[1].wantedPosition = [width + 30, heaight]
                width += cardPair[0].getWidth() + 40
                i += 1
            heaight -= cardPair[0].getHeight() + 10


        if (len(self.card_list) == 0):
            self.gameState = GameState.WIN
        if (self.errorLeft == 0):

            for line in self.winCard:
                for pair in line:
                    for card in pair:
                        card.wantedPosition = [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 300]
                        card.isFront = False


            for card in self.card_list:
                card.wantedPosition = [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 300]
                card.isFront = False
            self.gameState = GameState.LOOSE



    def display(self):
        self.screen.fill("white")
        screen.blit(self.background, self.backgroundRect)

        for card in self.card_list:
            card.draw(self.screen)
        for line in self.winCard:
            for card in line:
                card[0].draw(self.screen)
                card[1].draw(self.screen)
        screen.blit(self.goutte, self.goutteRect)
        screen.blit(self.error, self.errorRect)
        screen.blit(self.scoreTextSurface, self.scoreTextRect)
        screen.blit(self.errorTextSurface, self.errorTextRect)

        screen.blit(self.settings, self.settingsRect)

        screen.blit(self.restartLogo, self.restartLogoRect)

        if (self.gameState == GameState.WIN):
            self.screen.blit(self.youWinTextSurface, self.youWinTextRect)
            self.screen.blit(self.clickTextSurfaceWin, self.clickTextRectWin)
        elif (self.gameState == GameState.LOOSE):
            self.screen.blit(self.youLooseTextSurface, self.youLooseTextRect)
            self.screen.blit(self.clickTextSurface, self.clickTextRect)

        if (self.status == Status.SETTINGS):
            self.screen.blit(self.settingMenu, self.settingMenuRect)
            self.screen.blit(self.settingTextDifficultySurface, self.settingTextDifficultyRect)
            self.screen.blit(self.diffiMinus, self.diffiMinusRect)
            self.screen.blit(self.diffiPlus, self.diffiPlusRect)
            self.screen.blit(self.settingTextAudioSurface, self.settingTextAudioRect)
            self.screen.blit(self.audioMinus, self.audioMinusRect)
            self.screen.blit(self.audioPlus, self.audioPlusRect)
            if (self.changeDifficulty == True):
                self.screen.blit(self.settingChangeDiffSurface, self.settingChangeDiffRect)
            if (self.changeDifficulty == True):
                self.screen.blit(self.settingRestartSurface, self.settingRestartRect)
            else:
                self.screen.blit(self.settingSaveSurface, self.settingSaveRect)
            self.screen.blit(self.settingExitSurface, self.settingExitRect)


        pygame.display.flip()




    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game = Game(screen)
game.run()

pygame.quit()
