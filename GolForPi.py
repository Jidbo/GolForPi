#!/usr/local/bin/python

# Copyright (c) 2017 Jan All Rights Reserved.

import sys
from random import randint
import pygame
import time


class Board:

    cells = []
    width = 0
    height = 0

    def __init__(self, height, width, screen, modifier):
        self.width = width
        self.height = height
        self.screen = screen
        self.modifier = modifier

        for i in range(0, height):
            row = []
            for j in range(0, width):
                cell = Cell(j, i)
                row.append(cell)
            self.cells.append(row)

    def printBoardFlags(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                row = self.cells[i]
                if row[j].flag == 0:
                    print("0 ")
                else:
                    print("1 ")

            print("")

    def __str__(self):
        str = ""
        for i in range(0, self.height):
            for j in range(0, self.width):
                row = self.cells[i]
                if row[j].flag == 0:
                    str += "0"
                else:
                    str += "1"

        return str

    def printBoardStatus(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                row = self.cells[i]
                if row[j].status == 0:
                    print("0 ")
                else:
                    print(bcolors.FAIL + "0 " + bcolors.END)

            print("")

    def getSurroundingCellsCoords(self, cell):
        coords = []

        coords.append((cell.x - 1, cell.y - 1))
        coords.append((cell.x, cell.y - 1))
        coords.append((cell.x + 1, cell.y - 1))
        coords.append((cell.x - 1, cell.y))
        coords.append((cell.x + 1, cell.y))
        coords.append((cell.x - 1, cell.y + 1))
        coords.append((cell.x, cell.y + 1))
        coords.append((cell.x + 1, cell.y + 1))

        return coords

    def getCellByCoord(self, x, y):
        if (x < 0) | (x >= self.width) | (y < 0) | (y >= self.height):
            return None
        else:
            row = self.cells[y]
            return row[x]

    def updateFlags(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                cell = self.getCellByCoord(j, i)
                cells = self.getSurroundingCellsCoords(cell)
                cellActiveNextCells = 0
                for x in cells:
                    nextCell = self.getCellByCoord(x[0], x[1])
                    if nextCell != None:
                        cellActiveNextCells += nextCell.status

                if (cell.status == 0) & (cellActiveNextCells == 3):
                    cell.flag = 1
                elif (cell.status == 1) & (cellActiveNextCells >= 2) & (cellActiveNextCells <= 3):
                    cell.flag = 1
                elif (cell.status == 1) & (cellActiveNextCells > 3):
                    cell.flag = 0
                elif (cell.status == 1) & (cellActiveNextCells < 2):
                    cell.flag = 0

    def updateCells(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                cell = self.getCellByCoord(j, i)
                if cell.flag == 1:
                    cell.status = 1
                    pygame.draw.rect(screen, (63, 216, 188, 1),
                                     (1 + (20 * modifier) * j, 1 + (20 * modifier) * i, 20*modifier - 2, 20*modifier - 2))
                    # pygame.draw.rect(screen, (116, 204, 108, 1),
                    #                  (1 + 20 * j, 1 + 20 * i, 18, 18))
                else:
                    cell.status = 0
                    # pygame.draw.rect(screen, (32, 36, 104, 1),
                    #                  (1 + 10 * j, 1 + 10 * i, 8, 8))
                    pygame.draw.rect(screen, (41, 42, 48, 1),
                                     (1 + (20 * modifier) * j, 1 + (20 * modifier) * i, 20*modifier - 2, 20*modifier - 2))
                    #  rgb(59, 61, 70)


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0
        self.flag = 0

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " status: " + str(self.status)


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'


def getRandBin(length):
    s = ""
    for i in range(0, length):
        rand = randint(0, 1)
        s += str(rand)

    return s


def randomizeBoard(b):
    for i in range(0, b.height):
        rand = getRandBin(b.width + 1)
        for j in range(0, b.width):
            cell = b.getCellByCoord(j, i)
            if rand[j] == "1":
                cell.status = 1
            else:
                cell.status = 0

width = 40
height = 24
delay = 0.2
modifier = 1

try:
    if len(sys.argv) == 5:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        delay = float(sys.argv[3])
        modifier = float(sys.argv[4])
    elif len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        delay = float(sys.argv[3])
    elif len(sys.argv) == 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    elif len(sys.argv) == 2:
        delay = float(sys.argv[1])

except TypeError:
    print("Wrong Arguments")

pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Game Of Life")
screen = pygame.display.set_mode((int(round(width * 20 * modifier, 0)), int(round(height * 20 * modifier, 0))))

board = Board(height, width, screen, modifier)

randomizeBoard(board)
counterSinceLastCheck = 0
counter = 0
running = True
boardState = ""
screen.fill((0, 0, 0))
isFullscreen = False
lock = False
try:
    while running:
        t = time.time()

        if counterSinceLastCheck > 1:
            if boardState == str(board):
                randomizeBoard(board)
                print(counter)
                counter = 0

            boardState = str(board)
            counterSinceLastCheck = 0

        counterSinceLastCheck += 1
        counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                xCoord = int(round(x / (20*modifier), 0))
                yCoord = int(round(y / (20*modifier), 0))
                if (xCoord == 0) & (yCoord == 0):
                    if lock == False:
                        lock = True
                    else:
                        lock = False
                if lock == False:
                    if (xCoord == board.width-1) & (yCoord == 1):
                        running = False
                    elif (xCoord == board.width-2) & (yCoord == 1):
                        if isFullscreen == False:
                            try:
                                screen = pygame.display.set_mode((int(round(width * 20 * modifier, 0)), int(round(height * 20 * modifier, 0))), pygame.FULLSCREEN)
                            except:
                                pass
                            isFullscreen = True
                        else:
                            pass
                    elif (xCoord == 1) & (yCoord == 0):
                        randomizeBoard(board)
                    elif (xCoord == 2) & (yCoord == 0):
                        board = Board(24, 40, screen, 1)
                        modifier = 1
                        randomizeBoard(board)
                        screen.fill((0, 0, 0))
                    elif (xCoord == 3) & (yCoord == 0):
                        board = Board(12, 20, screen, 2)
                        modifier = 2
                        randomizeBoard(board)
                        screen.fill((0, 0, 0))
                    elif (xCoord == 4) & (yCoord == 0):
                        board = Board(6, 10, screen, 4)
                        modifier = 4
                        randomizeBoard(board)
                        screen.fill((0, 0, 0))
                    elif (xCoord == 5) & (yCoord == 0):
                        board = Board(3, 5, screen, 8)
                        modifier = 8
                        randomizeBoard(board)
                        screen.fill((0, 0, 0))
                    elif (xCoord == 0) & (yCoord == 2):
                        delay = 0
                    elif (xCoord == 1) & (yCoord == 2):
                        delay = 0.2
                    elif (xCoord == 2) & (yCoord == 2):
                        delay = 0.3
                    elif (xCoord == 3) & (yCoord == 2):
                        delay = 0.5
                    elif (xCoord == 4) & (yCoord == 2):
                        delay = 1.0
                    else:
                        cell = board.getCellByCoord(xCoord, yCoord)
                        if cell.status == 1:
                            cell.status = 0
                            pygame.draw.rect(screen, (41, 42, 48, 1), (1 + (20 * modifier) * xCoord, 1 + (20 * modifier) * yCoord, 20*modifier - 2, 20*modifier - 2))
                        else:
                            cell.status = 1
                            pygame.draw.rect(screen, (63, 216, 188, 1), (1 + (20 * modifier) * xCoord, 1 + (20 * modifier) * yCoord, 20*modifier - 2, 20*modifier - 2))


        board.updateFlags()
        board.updateCells()
        if lock == True:
            pygame.draw.rect(screen, (163, 39, 45, 1), (1, 1, 20*modifier - 2, 20*modifier - 2))
        pygame.display.flip()
        print(t-time.time())

        if delay > 0:
            time.sleep(delay)

    else:
        print(bcolors.FAIL + "\b\bExeting!!!" + bcolors.END)
        sys.exit(0)

except KeyboardInterrupt:
    print(bcolors.FAIL + "\b\bQuitting!!!" + bcolors.END)
    sys.exit(0)
