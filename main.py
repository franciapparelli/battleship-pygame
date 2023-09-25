import pygame
from sys import exit
from funciones import * 

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naval Battle")

LIGHT_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

FPS = 60
CREW_IMG = pygame.image.load('images/x.png')
rect = CREW_IMG.get_rect()
rect.center = 1280 // 2, 720 // 2 


def draw_window():
    SCREEN.fill(LIGHT_BLUE)
    pygame.draw.rect(SCREEN, (255, 0, 0), [WIDTH / 2, 0, 2, 1280])

matrix = inicializar_matriz()
# we use the sizes to draw as well as to do our "steps" in the loops. 
grid_node_width = 60  
grid_node_height = 60

def createCrew(x, y, color):
    pygame.draw.rect(SCREEN, color, [x, y, grid_node_width, grid_node_height], 2)

def visualizeGrid(matrix):
    y = 115  # we start at the top of the screen
    x = 100
    myfont = pygame.font.SysFont("monospace", 30)
    for letter in LETTERS:
        label = myfont.render(letter, 2, BLACK)
        SCREEN.blit(label, (x, y - 30))
        x += grid_node_width
    counter = 0
    for row in matrix:
        x = 80 # for every row we start at the left of the screen again
        label = myfont.render(str(counter), 1, BLACK)
        counter += 1
        SCREEN.blit(label, (x, y))
        x = 100
        for item in row:
            if item == "-":
                createCrew(x, y, (255, 255, 255))
            elif item == "H":
                createCrew(x, y, (0, 255, 0))
            else:
                createCrew(x, y, (0, 0, 0))

            x += grid_node_width # for ever item/number in that row we move one "step" to the right
        y += grid_node_height   # for every new row we move one "step" downwards

def main():
    moving = False
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 representa el clic izquierdo del mouse
                    # Obtener la posición del clic del mouse
                    x, y = pygame.mouse.get_pos()
                    # Calcular la celda en la que se hizo clic
                    column_click = x // 60 - 6
                    row_click = y // 60 - 4
                    print(f"Se hizo clic en la celda ({row_click}, {column_click})")
                    if row_click <= 8 and row_click >= 0 and column_click <= 8 and column_click >= 0:
                        matrix[row_click][column_click] = "T"
                    if rect.collidepoint(event.pos):
                        moving = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                moving = False
                first_pos_x , first_pos_y = rect.topleft 
                second_pos_x , second_pos_y = rect.bottomright
                first_node_x = first_pos_x // 60 - 1
                first_node_y = first_pos_y // 60 - 2
                second_node_x = second_pos_x // 60 - 2
                second_node_y = second_pos_y // 60 - 2
                print(f"{first_node_x} {first_node_y} | {second_node_x} {second_node_y}")
 
        # Make your image move continuously
            elif event.type == pygame.MOUSEMOTION and moving:
                rect.move_ip(event.rel)
                first_pos_x , first_pos_y = rect.topleft 
                second_pos_x , second_pos_y = rect.bottomright
                first_node_x = first_pos_x // 60 - 1
                first_node_y = first_pos_y // 60 - 2
                second_node_x = second_pos_x // 60 - 2
                second_node_y = second_pos_y // 60 - 2
                for row in range(8):
                    for item in range(8):
                        if first_node_x <= 8 and first_node_x >= 0 and first_node_y <= 8 and first_node_y >= 0 and second_node_x <= 8 and second_node_x >= 0 and second_node_y <= 8 and second_node_y >= 0:
                            if (row == first_node_y and item == first_node_x) or (row == second_node_y and item == second_node_x):
                                matrix[row][item] = "H"
                            else:
                                matrix[row][item] = "-"
                
                    
        draw_window()            
        visualizeGrid(matrix)
        SCREEN.blit(CREW_IMG, rect)
        pygame.draw.rect(SCREEN, BLACK, rect, 2)
        pygame.display.update()

    

if __name__ == '__main__':
    main()


    