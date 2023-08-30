import pygame as pg
import sys
import time
# VARIABLES------------------------------------------------------------------
TimePeriod = 1 / 10
# ---------------------------------------------------------------------------
# CLASSES--------------------------------------------------------------------
class Cell:
    WIDTH = 20

    def __init__(
        self,
        x,
        y,
    ):
        self.x = x
        self.y = y
        self.rect = pg.Rect(
            self.x * Cell.WIDTH, self.y * Cell.WIDTH, Cell.WIDTH, Cell.WIDTH
        )
        self.aliveColor = (0, 0, 0)
        self.deadColor = (255, 255, 255)
        self.alive = False

    def draw(self, screen):
        if self.alive:
            pg.draw.rect(screen, self.aliveColor, self.rect)
        else:
            pg.draw.rect(screen, self.deadColor, self.rect)

    def get_live_neighbours(self, CELLS):
        count = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                try:
                    if CELLS[self.x - x][self.y - y].alive:
                        count += 1
                except IndexError:
                    pass
        return count

    def update(self, CELLS):
        if self.alive:
            if self.get_live_neighbours(CELLS) < 2:
                self.alive = False
            elif self.get_live_neighbours(CELLS) > 3:
                self.alive = False
        else:
            if self.get_live_neighbours(CELLS) == 3:
                self.alive = True
# ---------------------------------------------------------------------------
# INITIALIZATION-------------------------------------------------------------
CELLS = [[Cell(x, y) for y in range(38)] for x in range(38)]
pg.init()
screen = pg.display.set_mode((760, 800))
pg.display.set_caption("Conway's Game of Life")
font = pg.font.Font("Comfortaa.ttf", 30)
clock = pg.time.Clock()
# ---------------------------------------------------------------------------
# FUNCTIONS------------------------------------------------------------------
def draw_grid():
    for x in range(38):
        pg.draw.line(
            screen, "#dddddd", (x * Cell.WIDTH, 0), (x * Cell.WIDTH, 38 * Cell.WIDTH), 2
        )
        pg.draw.line(
            screen, "#dddddd", (0, x * Cell.WIDTH), (38 * Cell.WIDTH, x * Cell.WIDTH), 2
        )

    pg.draw.rect(screen, "#dddddd", pg.Rect(0, 0, 761, 761), 2)
# ---------------------------------------------------------------------------
def create():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                x = x // Cell.WIDTH
                y = y // Cell.WIDTH
                try:
                    CELLS[x][y].alive = not CELLS[x][y].alive
                except IndexError:
                    pass
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return run

        screen.fill((0, 0, 0))
        for row in CELLS:
            for cell in row:
                cell.draw(screen)
        draw_grid()

        label = font.render(f"Edit mode... FPS : {clock.get_fps():.0f}", 1, "#ffffff")

        screen.blit(label, label.get_rect(center=(380, 780)))
        clock.tick(60)
        pg.display.update()
# ---------------------------------------------------------------------------
def run():
    global CELLS
    C = 0
    prevTime = time.time()
    while True:
        screen.fill((0, 0, 0))

        deltaTime = time.time() - prevTime
        prevTime = time.time()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return create

        CELLS_COPY = [[Cell(x, y) for y in range(38)] for x in range(38)]
        for row in CELLS:
            for cell in row:
                CELLS_COPY[cell.x][cell.y].alive = cell.alive

        for row in CELLS:
            for cell in row:
                cell.draw(screen)

        draw_grid()

        label = font.render(
            f"Simulation Active. FPS : {clock.get_fps():.0f}", 1, "#ffffff"
        )
        C += deltaTime
        if C >= TimePeriod:
            C = 0
            # print('updating....')
            for row in CELLS_COPY:
                for cell in row:
                    cell.update(CELLS)

            # p = pg.mouse.get_pos()
            # print(CELLS[p[0]//Cell.WIDTH][p[1]//Cell.WIDTH].get_live_neighbours(CELLS))

            CELLS = CELLS_COPY

        screen.blit(label, label.get_rect(center=(380, 780)))
        clock.tick(60)
        pg.display.update()
# ---------------------------------------------------------------------------
# ENTRY-POINT----------------------------------------------------------------
if __name__ == "__main__":
    func = create
    while True:
        func = func()
# ---------------------------------------------------------------------------