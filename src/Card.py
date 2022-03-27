import enum
from turtle import update
import pygame
from math import cos, fabs, radians, degrees

ASSETS_PATH = "./assets/"


class Card:
    def __init__(self, x, y, personnage):
        self.frontImage = pygame.image.load(ASSETS_PATH + "card.png")
        self.frontImage = pygame.transform.scale(self.frontImage, (120, 163))

        self.backImage = pygame.image.load(ASSETS_PATH + "card_backside.png")
        self.backImage = pygame.transform.scale(self.backImage, (120, 163))

        self.perImage = pygame.image.load(
            ASSETS_PATH + 'personnage/' + personnage + ".png")
        self.perImage = pygame.transform.scale(self.perImage, (60, 81))

        self.cardRect = self.frontImage.get_rect(x=x, y=y)
        self.persRect = self.perImage.get_rect(x=x + 35, y=y + 10)

        self.name = personnage


        if len(self.name) > 8:
            self.font = pygame.font.SysFont("arial", 11)
        else:
            self.font = pygame.font.SysFont("arial", 18)
        self.nameText = self.font.render(self.name, True, 'white')
        self.nameRect = self.nameText.get_rect(
            x=self.cardRect.centerx - self.nameText.get_width()/2, y=y + 110)



        self.speed = 5
        self.velocity = [0, 0]
        self.isFront = True
        self.isWin = False
        self.angle = 1
        self.wantedPosition = [0, 0]
        self.sec = 0
        self.waitToTurn = False
        self.isStarted = False



    def getWidth(self):
        return self.frontImage.get_size()[0]



    def getHeight(self):
        return self.frontImage.get_size()[1]



    def update(self, x, y):

        self.cardRect.x = x
        self.cardRect.y = y
        self.persRect.x = x + 35
        self.persRect.y = y + 10
        self.nameRect.x = self.cardRect.centerx - self.nameText.get_width()/2
        self.nameRect.y = y + 110



    def move(self):
        if (self.waitToTurn == True):
            self.sec += 1

        if (self.sec == 60 * 1 and self.isWin == False):
            self.isFront = False
            self.sec = 0
            self.waitToTurn = False





        wantedX = self.wantedPosition[0]
        wantedY = self.wantedPosition[1]
        actX = self.cardRect.topleft[0]
        actY = self.cardRect.topleft[1]

        if wantedX != actX or wantedY != actY:

            if wantedY < actY:
                if (actY - self.speed) <= wantedY:
                    self.update(actX, wantedY)
                else:
                    self.update(actX, actY - self.speed)
            elif wantedY > actY:
                if (actY + self.speed) >= wantedY:
                    self.update(actX, wantedY)
                else:
                    self.update(actX, actY + self.speed)
            if wantedX < actX:
                if (actX - self.speed) <= wantedX:
                    self.update(wantedX, actY)
                else:
                    self.update(actX - self.speed, actY)
            elif wantedX > actX:
                if (actX + self.speed) >= wantedX:
                    self.update(wantedX, actY)
                else:
                    self.update(actX + self.speed, actY)
        elif self.isStarted == False:
                self.isStarted = True
                self.waitToTurn = True


    def draw(self, screen):

        if (self.isFront == True):
            screen.blit(self.frontImage, self.cardRect)
            screen.blit(self.perImage, self.persRect)
            screen.blit(self.nameText, self.nameRect)
        else:
            screen.blit(self.backImage, self.cardRect)
