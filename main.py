import sys
import pygame
from collections import deque
from queue import PriorityQueue
from collections import defaultdict
import math
import random

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
RED = (200, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 51)
AQUA = (127, 255, 212)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
pygame.init()


class Idx:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val


class Board:
    def __init__(self, size):
        self.first=0
        self.size = size
        self.checkBFS = False
        self.checkDFS = False
        self.checkA = False
        self.checkBidirectional = False
        self.checkMaze = False
        self.queue = deque([])
        self.myset = {}
        self.came_from = {}
        self.came_from2 = {}
        self.board = [[[None, None] for __ in range(self.size)] for _ in range(self.size)]
        self.blockSize = 700 // size
        self.endDFS = False
        self.list_frames = []
        self.pq = PriorityQueue()
        for x in range(0, WINDOW_WIDTH, self.blockSize):
            for y in range(0, WINDOW_HEIGHT, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                self.board[y // self.blockSize][x // self.blockSize] = [rect, WHITE]

    def drawGrid(self):
        for lst in self.board:
            for rect, color in lst:
                if color == WHITE:
                    pygame.draw.rect(SCREEN, color, rect, 1)
                else:
                    pygame.draw.rect(SCREEN, color, rect)

    def checkMouseAndKey(self, startRow, startCol, endRow, endCol):
        start = False
        mousePosX, mousePosY = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()[0]  # ==1:Pressing mouse
        keyPressed = pygame.key.get_pressed()
        if mousePressed == 1:
            if self.first<10:
                self.first+=1
                return None,None,None,None,False
            row = mousePosY // self.blockSize
            col = mousePosX // self.blockSize
            if keyPressed[pygame.K_LCTRL]:
                self.board[row][col][1] = GREEN
                startRow = row
                startCol = col

            elif keyPressed[pygame.K_LSHIFT]:
                self.board[row][col][1] = PURPLE
                endRow = row
                endCol = col
            else:
                self.board[row][col][1] = RED

        if keyPressed[pygame.K_SPACE]:
            start = True
        if keyPressed[pygame.K_ESCAPE]:
            menu3()
        return startRow, startCol, endRow, endCol, start

    def checkRow(self, currRow):
        return currRow >= 0 and currRow <= self.size - 1

    def checkCol(self, currCol):
        return currCol >= 0 and currCol <= self.size - 1

    def generateMaze(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j][1] = RED

        x = random.randint(1, self.size - 2)
        y = random.randint(1, self.size - 2)

        def check(x, y):
            count = 0
            try:
                if self.board[x + 1][y][1] == RED:
                    count += 1
            except:
                pass

            try:
                if self.board[x - 1][y][1] == RED and x > 0:
                    count += 1
            except:
                pass

            try:
                if self.board[x][y + 1][1] == RED:
                    count += 1
            except:
                pass

            try:
                if self.board[x][y - 1][1] == RED and y > 0:
                    count += 1
            except:
                pass

            return True if (count >= 3) else False

        def recur(x, y):
            lst = [1, 2, 3, 4]
            while len(lst) > 0:
                rnd = random.choice(lst)
                lst.remove(rnd)
                if rnd == 1:

                    if check(x + 1, y):
                        self.board[x + 1][y][1] = WHITE
                        recur(x + 1, y)
                if rnd == 2:
                    if check(x - 1, y):
                        self.board[x - 1][y][1] = WHITE
                        recur(x - 1, y)
                if rnd == 3:
                    if check(x, y + 1):
                        self.board[x][y + 1][1] = WHITE
                        recur(x, y + 1)
                if rnd == 4:
                    if check(x, y - 1):
                        self.board[x][y - 1][1] = WHITE
                        recur(x, y - 1)

        recur(x, y)
        lst = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j][1] == RED:
                    self.board[i][j][1] = WHITE
                    lst.append((i, j))
        for row, col in lst:
            self.board[col][row][1] = RED
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            CLOCK.tick(60)

    def BFS(self, startRow, startCol, endRow, endCol):
        self.queue.append(Idx(startRow, startCol, 0))
        while len(self.queue) != 0:
            tmp = self.queue.popleft()
            currRow = tmp.row
            currCol = tmp.col
            val = tmp.val
            if currRow == endRow and currCol == endCol:
                for i in range(self.size):
                    for j in range(self.size):
                        if self.board[i][j][1] == YELLOW:
                            self.board[i][j][1] = BLUE
                            self.drawGrid()
                            pygame.display.update()
                            CLOCK.tick(120)
                self.checkBFS = False
                break
            elif (currRow, currCol) in self.myset:
                continue
            elif self.checkRow(currRow) and self.checkCol(currCol) and self.board[currRow][currCol][1] != RED:
                self.queue.append(Idx(currRow + 1, currCol, val + 1))
                self.queue.append(Idx(currRow - 1, currCol, val + 1))
                self.queue.append(Idx(currRow, currCol + 1, val + 1))
                self.queue.append(Idx(currRow, currCol - 1, val + 1))
                self.myset[(currRow, currCol)] = val
                if not (currRow == startRow and currCol == startCol):
                    self.board[currRow][currCol][1] = BLUE
                if (currRow + 1 != endRow or currCol != endCol) and self.checkRow(currRow + 1) and \
                        self.board[currRow + 1][currCol][
                            1] != RED and (currRow + 1, currCol) not in self.myset:
                    self.board[currRow + 1][currCol][1] = YELLOW
                if (currRow - 1 != endRow or currCol != endCol) and self.checkRow(currRow - 1) and \
                        self.board[currRow - 1][currCol][
                            1] != RED and (currRow - 1, currCol) not in self.myset:
                    self.board[currRow - 1][currCol][1] = YELLOW
                if (currRow != endRow or currCol + 1 != endCol) and self.checkCol(currCol + 1) and \
                        self.board[currRow][currCol + 1][
                            1] != RED and (currRow, currCol + 1) not in self.myset:
                    self.board[currRow][currCol + 1][1] = YELLOW
                if (currRow != endRow or currCol - 1 != endCol) and self.checkCol(currCol - 1) and \
                        self.board[currRow][currCol - 1][
                            1] != RED and (currRow, currCol - 1) not in self.myset:
                    self.board[currRow][currCol - 1][1] = YELLOW
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            CLOCK.tick(120)

    def backtrack(self, currRow, currCol, startRow, startCol, text):
        if (text == "BFS" and not self.checkBFS):
            currVal = max(self.myset.values()) + 1
            path = []
            while True:
                path.append((currRow, currCol))
                if currRow == startRow and currCol == startCol:
                    break
                if (currRow + 1, currCol) in self.myset and self.myset[(currRow + 1, currCol)] < currVal:
                    currRow += 1
                elif (currRow - 1, currCol) in self.myset and self.myset[(currRow - 1, currCol)] < currVal:
                    currRow -= 1
                elif (currRow, currCol + 1) in self.myset and self.myset[(currRow, currCol + 1)] < currVal:
                    currCol += 1
                else:
                    currCol -= 1
                currVal -= 1

            path = path[::-1]
            for row, col in path:
                if self.board[row][col][1] == BLUE:
                    self.board[row][col][1] = AQUA
                self.drawGrid()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                CLOCK.tick(30)
        elif text == "DFS" and not self.checkDFS:
            path = []
            while True:
                path.append((currRow, currCol))
                if currRow == startRow and currCol == startCol:
                    break
                tmp1 = self.myset.get((currRow + 1, currCol), 9999999)
                tmp2 = self.myset.get((currRow - 1, currCol), 9999999)
                tmp3 = self.myset.get((currRow, currCol + 1), 9999999)
                tmp4 = self.myset.get((currRow, currCol - 1), 9999999)
                minn = min(tmp1, tmp2, tmp3, tmp4)
                if minn == tmp1:
                    currRow += 1
                elif minn == tmp2:
                    currRow -= 1
                elif minn == tmp3:
                    currCol += 1
                else:
                    currCol -= 1
            path = path[::-1]
            for row, col in path:
                if self.board[row][col][1] == BLUE:
                    self.board[row][col][1] = AQUA
                self.drawGrid()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                CLOCK.tick(30)
        elif text == "AStar" and not self.checkA:
            path = []
            while True:
                path.append((currRow, currCol))
                currRow, currCol = self.came_from[(currRow, currCol)]
                if currRow == startRow and currCol == startCol:
                    break
            path = path[::-1]
            for row, col in path:
                if self.board[row][col][1] == BLUE:
                    self.board[row][col][1] = AQUA
                self.drawGrid()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                CLOCK.tick(30)

        self.checkBFS = False
        self.checkDFS = False
        self.checkA = False

    def DFS(self, currRow, currCol, val, startRow, startCol, endRow, endCol):
        if self.checkDFS:
            if currRow == endRow and currCol == endCol:
                self.checkDFS = False
                return True
            elif (currRow, currCol) in self.myset:
                return
            elif self.checkRow(currRow) and self.checkCol(currCol) and self.board[currRow][currCol][1] != RED:
                self.myset[(currRow, currCol)] = val
                if currRow != startRow or currCol != startCol:
                    self.board[currRow][currCol][1] = BLUE
                self.drawGrid()
                pygame.display.update()
                CLOCK.tick(60)

                self.DFS(currRow + 1, currCol, val + 1, startRow, startCol, endRow, endCol)
                self.DFS(currRow - 1, currCol, val + 1, startRow, startCol, endRow, endCol)
                self.DFS(currRow, currCol + 1, val + 1, startRow, startCol, endRow, endCol)
                self.DFS(currRow, currCol - 1, val + 1, startRow, startCol, endRow, endCol)

    def AStar(self, startRow, startCol, endRow, endCol):

        def calcDist(currRow, currCol, endRow, endCol):
            return abs(currRow - endRow) + abs(currCol - endCol)

        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, (startRow, startCol)))
        g_score = defaultdict(lambda: math.inf)
        g_score[(startRow, startCol)] = 0
        f_score = defaultdict(lambda: math.inf)
        f_score[(startRow, startCol)] = calcDist(startRow, startCol, endRow, endCol)
        open_set_hash = {(startRow, startCol)}
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            currRow, currCol = open_set.get()[2]
            open_set_hash.remove((currRow, currCol))
            if currRow == endRow and currCol == endCol:
                self.checkA = False
                return True
            temp_g_score = g_score[(currRow, currCol)] + 1
            if 0 <= currRow + 1 <= self.size - 1 and self.board[currRow + 1][currCol][1] != RED:
                if temp_g_score < g_score[(currRow + 1, currCol)]:
                    self.came_from[(currRow + 1, currCol)] = (currRow, currCol)
                    g_score[(currRow + 1, currCol)] = temp_g_score
                    f_score[(currRow + 1, currCol)] = temp_g_score + calcDist(currRow + 1, currCol, endRow, endCol)
                    if (currRow + 1, currCol) not in open_set_hash:
                        count += 1
                        open_set.put((f_score[(currRow + 1, currCol)], count, (currRow + 1, currCol)))
                        open_set_hash.add((currRow + 1, currCol))
            if 0 <= currRow - 1 <= self.size - 1 and self.board[currRow - 1][currCol][1] != RED:
                if temp_g_score < g_score[(currRow - 1, currCol)]:
                    self.came_from[(currRow - 1, currCol)] = (currRow, currCol)
                    g_score[(currRow - 1, currCol)] = temp_g_score
                    f_score[(currRow - 1, currCol)] = temp_g_score + calcDist(currRow - 1, currCol, endRow, endCol)
                    if (currRow - 1, currCol) not in open_set_hash:
                        count += 1
                        open_set.put((f_score[(currRow - 1, currCol)], count, (currRow - 1, currCol)))
                        open_set_hash.add((currRow - 1, currCol))
            if 0 <= currCol + 1 <= self.size - 1 and self.board[currRow][currCol + 1][1] != RED:
                if temp_g_score < g_score[(currRow, currCol + 1)]:
                    self.came_from[(currRow, currCol + 1)] = (currRow, currCol)
                    g_score[(currRow, currCol + 1)] = temp_g_score
                    f_score[(currRow, currCol + 1)] = temp_g_score + calcDist(currRow, currCol + 1, endRow, endCol)
                    if (currRow, currCol + 1) not in open_set_hash:
                        count += 1
                        open_set.put((f_score[(currRow, currCol + 1)], count, (currRow, currCol + 1)))
                        open_set_hash.add((currRow, currCol + 1))
            if 0 <= currCol - 1 <= self.size - 1 and self.board[currRow][currCol - 1][1] != RED:
                if temp_g_score < g_score[(currRow, currCol - 1)]:
                    self.came_from[(currRow, currCol - 1)] = (currRow, currCol)
                    g_score[(currRow, currCol - 1)] = temp_g_score
                    f_score[(currRow, currCol - 1)] = temp_g_score + calcDist(currRow, currCol - 1, endRow, endCol)
                    if (currRow, currCol - 1) not in open_set_hash:
                        count += 1
                        open_set.put((f_score[(currRow, currCol - 1)], count, (currRow, currCol - 1)))
                        open_set_hash.add((currRow, currCol - 1))
            self.drawGrid()
            pygame.display.update()
            if not (currRow == startRow and currCol == startCol):
                self.board[currRow][currCol][1] = BLUE
            CLOCK.tick(60)

    def BidirectionalSearch(self, startRow, startCol, endRow, endCol):
        self.queue.append(Idx(startRow, startCol, 0))
        self.queue2 = deque()
        self.queue2.append(Idx(endRow, endCol, 0))
        qset = set()
        qset2 = set()
        while not (len(self.queue) == 0 or len(self.queue2) == 0):
            if len(qset.intersection(qset2)) != 0:
                break
            if len(self.queue) < len(self.queue2):
                tmp = self.queue.popleft()
                currRow = tmp.row
                currCol = tmp.col
                val = tmp.val

                if (currRow, currCol) in self.myset:
                    continue

                elif self.checkRow(currRow) and self.checkCol(currCol) and self.board[currRow][currCol][1] != RED:
                    self.queue.append(Idx(currRow + 1, currCol, val + 1))
                    self.queue.append(Idx(currRow - 1, currCol, val + 1))
                    self.queue.append(Idx(currRow, currCol + 1, val + 1))
                    self.queue.append(Idx(currRow, currCol - 1, val + 1))
                    self.myset[(currRow, currCol)] = val
                    qset.add((currRow, currCol))

                    if not (currRow == startRow and currCol == startCol):
                        self.board[currRow][currCol][1] = BLUE
                    if (currRow + 1 != endRow or currCol != endCol) and self.checkRow(currRow + 1) and \
                            self.board[currRow + 1][currCol][
                                1] != RED and (currRow + 1, currCol) not in self.myset:
                        self.board[currRow + 1][currCol][1] = YELLOW
                        qset.add((currRow + 1, currCol))
                        self.came_from[(currRow + 1, currCol)] = (currRow, currCol)
                    if (currRow - 1 != endRow or currCol != endCol) and self.checkRow(currRow - 1) and \
                            self.board[currRow - 1][currCol][
                                1] != RED and (currRow - 1, currCol) not in self.myset:
                        self.board[currRow - 1][currCol][1] = YELLOW
                        qset.add((currRow - 1, currCol))
                        self.came_from[(currRow - 1, currCol)] = (currRow, currCol)
                    if (currRow != endRow or currCol + 1 != endCol) and self.checkCol(currCol + 1) and \
                            self.board[currRow][currCol + 1][
                                1] != RED and (currRow, currCol + 1) not in self.myset:
                        self.board[currRow][currCol + 1][1] = YELLOW
                        qset.add((currRow, currCol + 1))
                        self.came_from[(currRow, currCol + 1)] = (currRow, currCol)
                    if (currRow != endRow or currCol - 1 != endCol) and self.checkCol(currCol - 1) and \
                            self.board[currRow][currCol - 1][
                                1] != RED and (currRow, currCol - 1) not in self.myset:
                        self.board[currRow][currCol - 1][1] = YELLOW
                        qset.add((currRow, currCol - 1))
                        self.came_from[(currRow, currCol - 1)] = (currRow, currCol)
                    self.drawGrid()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()
                    CLOCK.tick(120)

            else:
                tmp = self.queue2.popleft()
                currRow = tmp.row
                currCol = tmp.col
                val = tmp.val
                if (currRow, currCol) in self.myset:
                    continue

                if self.checkRow(currRow) and self.checkCol(currCol) and self.board[currRow][currCol][1] != RED:
                    self.queue2.append(Idx(currRow + 1, currCol, val + 1))
                    self.queue2.append(Idx(currRow - 1, currCol, val + 1))
                    self.queue2.append(Idx(currRow, currCol + 1, val + 1))

                    self.queue2.append(Idx(currRow, currCol - 1, val + 1))
                    self.myset[(currRow, currCol)] = val
                    qset2.add((currRow, currCol))

                    if not (currRow == endRow and currCol == endCol):
                        self.board[currRow][currCol][1] = BLUE
                    if (currRow + 1 != startRow or currCol != startCol) and self.checkRow(currRow + 1) and \
                            self.board[currRow + 1][currCol][
                                1] != RED and (currRow + 1, currCol) not in self.myset:
                        self.board[currRow + 1][currCol][1] = YELLOW
                        qset2.add((currRow + 1, currCol))
                        self.came_from2[(currRow + 1, currCol)] = (currRow, currCol)
                    if (currRow - 1 != startRow or currCol != startCol) and self.checkRow(currRow - 1) and \
                            self.board[currRow - 1][currCol][
                                1] != RED and (currRow - 1, currCol) not in self.myset:
                        self.board[currRow - 1][currCol][1] = YELLOW
                        qset2.add((currRow - 1, currCol))
                        self.came_from2[(currRow - 1, currCol)] = (currRow, currCol)
                    if (currRow != startRow or currCol + 1 != startCol) and self.checkCol(currCol + 1) and \
                            self.board[currRow][currCol + 1][
                                1] != RED and (currRow, currCol + 1) not in self.myset:
                        self.board[currRow][currCol + 1][1] = YELLOW
                        qset2.add((currRow, currCol + 1))
                        self.came_from2[(currRow, currCol + 1)] = (currRow, currCol)
                    if (currRow != startRow or currCol - 1 != startCol) and self.checkCol(currCol - 1) and \
                            self.board[currRow][currCol - 1][
                                1] != RED and (currRow, currCol - 1) not in self.myset:
                        self.board[currRow][currCol - 1][1] = YELLOW
                        qset2.add((currRow, currCol - 1))
                        self.came_from2[(currRow, currCol - 1)] = (currRow, currCol)
                    self.drawGrid()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()
                    CLOCK.tick(120)

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j][1] == YELLOW:
                    self.board[i][j][1] = BLUE
                    self.drawGrid()
                    pygame.display.update()
                    CLOCK.tick(120)
        intersectRow, intersectCol = random.choice(list(qset.intersection(qset2)))
        intersectRow2, intersectCol2 = intersectRow, intersectCol
        path = []
        path2 = []
        while True:
            path.append((intersectRow, intersectCol))
            intersectRow, intersectCol = self.came_from[(intersectRow, intersectCol)]
            if intersectRow == startRow and intersectCol == startCol:
                break
        while True:
            path2.append((intersectRow2, intersectCol2))
            intersectRow2, intersectCol2 = self.came_from2[(intersectRow2, intersectCol2)]
            if intersectRow2 == endRow and intersectCol2 == endCol:
                break
        for coordinate1, coordinate2 in zip(path, path2):
            row, col = coordinate1
            if self.board[row][col][1] == BLUE:
                self.board[row][col][1] = AQUA
            row, col = coordinate2
            if self.board[row][col][1] == BLUE:
                self.board[row][col][1] = AQUA
            self.drawGrid()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            CLOCK.tick(30)
        if len(path) < len(path2):
            for i in range(len(path), len(path2)):
                row, col = path2[i]
                if self.board[row][col][1] == BLUE:
                    self.board[row][col][1] = AQUA
                self.drawGrid()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                CLOCK.tick(30)
        else:
            for i in range(len(path2), len(path)):
                row, col = path[i]
                if self.board[row][col][1] == BLUE:
                    self.board[row][col][1] = AQUA
                self.drawGrid()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                CLOCK.tick(30)

        pass


board = Board(35)


def menu():
    bg = pygame.image.load(r"images\game-background-g00c04c352_1920.jpg")
    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
        SCREEN.fill((WHITE))
        SCREEN.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        createButton("BFS", BLUE, GREEN, 250, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 100, 40)
        createButton("A Star", BLUE, GREEN, 250, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2), 40)
        createButton("DFS", BLUE, GREEN, 250, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + 100, 40)
        createButton("Bidirectional", BLUE, GREEN, 250, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + 200, 40)
        pygame.display.update()
        CLOCK.tick(60)


def menu2():
    bg = pygame.image.load(r"images\game-background-g00c04c352_1920.jpg")
    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
        SCREEN.fill((WHITE))
        SCREEN.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        createButton("Maze", BLUE, GREEN, 200, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 50, 40)
        createButton("No Maze", BLUE, GREEN, 200, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + 50, 40)
        pygame.display.update()
        CLOCK.tick(60)


def menu3():
    while True:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        createButton("New Game", BLUE, AQUA, 200, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + 100, 40)
        check = createButton("Continue", BLUE, AQUA, 200, 50, WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 100, 40)
        if check:
            break
        pygame.display.update()
        CLOCK.tick(60)
    SCREEN.fill(BLACK)
    return


def main():
    SCREEN.fill(BLACK)
    startRow = None
    startCol = None
    endRow = None
    endCol = None
    if board.checkMaze:
        board.generateMaze()
    while True:
        startRow, startCol, endRow, endCol, start = board.checkMouseAndKey(startRow, startCol, endRow, endCol)
        board.drawGrid()
        if start and board.checkBFS:
            board.BFS(startRow, startCol, endRow, endCol)
            board.backtrack(endRow, endCol, startRow, startCol, "BFS")
        elif start and board.checkDFS:
            board.DFS(startRow, startCol, 0, startRow, startCol, endRow, endCol)
            board.backtrack(endRow, endCol, startRow, startCol, "DFS")
        elif start and board.checkA:
            board.AStar(startRow, startCol, endRow, endCol)
            board.backtrack(endRow, endCol, startRow, startCol, "AStar")
        elif start and board.checkBidirectional:
            board.BidirectionalSearch(startRow, startCol, endRow, endCol)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(60)


def createButton(mytext, color, colorOnHover, width, height, x, y, textsize, action=None):
    mousePosX, mousePosY = pygame.mouse.get_pos()

    myRect = pygame.Rect(0, 0, width, height)
    myRect.center = (x, y)
    if myRect.x <= mousePosX <= myRect.x + width and myRect.y <= mousePosY <= myRect.y + height:
        color, colorOnHover = colorOnHover, color
        if pygame.mouse.get_pressed()[0] == 1:

            if mytext == "New Game":
                board.__init__(35)
                menu()
            elif mytext == "Continue":
                return True
            elif mytext == "BFS":
                board.checkBFS = True
                menu2()
            elif mytext == "DFS":
                board.checkDFS = True
                menu2()
            elif mytext == "A Star":
                board.checkA = True
                menu2()
            elif mytext == "Bidirectional":
                board.checkBidirectional = True
                menu2()
            elif mytext == "Maze":
                board.checkMaze = True
                main()
            elif mytext == "No Maze":
                board.checkMaze = False
                main()
    pygame.draw.rect(SCREEN, color, myRect)
    f = pygame.font.Font(r"Elianto\Elianto-Regular.ttf", textsize)
    textSurface = f.render(mytext, True, BLACK)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    SCREEN.blit(textSurface, textRect)


menu()
