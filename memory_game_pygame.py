import pygame
import sys
import os
import random
import time
from tkinter import messagebox
from tkinter import *

# Arma la matriz de memoria
def set_matrix_memory(columns = 4):
    images_folder = os.listdir("images/pairs")
    images_folder = random.sample(images_folder, len(images_folder))[:columns**2//2]
    matrix = []
    images_list = [(image, i) for image, i in enumerate(images_folder)] * 2
    for i in range(0, columns):
        matrix.append([])
        for j in range(0, columns):
            index = random.randint(0, len(images_list) - 1)
            matrix[i].append((images_list[index][0], images_list[index][1], False))
            images_list.remove(images_list[index])
    return matrix

def draw_matrix(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[j][i][0] != None and not matrix[j][i][2]:
                pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(i * 100 + 10, j * 100 + 10, 100, 100), 1)
            else:
                image = pygame.image.load(os.path.join("images/pairs", matrix[j][i][1])).convert()
                image = pygame.transform.scale(image, (100, 100))
                rect = image.get_rect()
                rect.x = i * 100 + 10
                rect.y = j * 100 + 10
                rect.w = 100
                rect.h = 100
                surface.blit(image, rect)
                pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(i * 100 + 10, j * 100 + 10, 100, 100), 1)

# Muestra la matriz en consola
def view_matrix(matrix):
    for i in range(0, len(matrix)):
        print(matrix[i])

# Eleccion del cuadro/imagen en la matriz de memoria
def choose_image(columns):
    error_input = True
    while error_input:
        try:
            row = int(input("Ingresa fila: "))
            column = int(input("Ingresa columna: "))
        except ValueError:
            print("Error, no ingreso un numero")
            continue
        if (row < columns and column < columns and row >= 0 and column >= 0):
            error_input = False
        else:
            print("Error en el ingreso de fila o columna")
    return row, column

# Valida que se haya terminado el juego
def check_game(matrix):
    for i in range(0, len(matrix)):
        for j in range(i, len(matrix[i])):
            if matrix[i][j][0] != None:
                return False
    return True

# Juego
def main_game(matrix_memory):
    pygame.display.set_caption("Memory Game")
    icon = pygame.image.load(os.path.join("images/other", "question_icon.png"))
    pygame.display.set_icon(icon)
    # Variables de inicio
    game_start = True
    pairs = []
    next_step = None
    pause_count = 0
    tries = 0
    # Inicio de juego
    while game_start:
        # Rellenar de negro la pantalla
        surface.fill((0, 0, 0))
        # Drawing Rectangle
        draw_matrix(matrix_memory)
        # Tiempo entre frame
        time.sleep(0.1)
        # Pausa para ver las figuras
        if pause_count > 0:
            pause_count -=1
            continue
        # Eventos
        for event in pygame.event.get():
            # Quitar juego
            if event.type == pygame.QUIT:
                game_start = False
                sys.exit()
            # Eleccion de cuadros
            if event.type == pygame.MOUSEBUTTONDOWN:
                posX, posY = pygame.mouse.get_pos()
                if len(pairs) < 2:
                    col = (posX - 10) // 100
                    row = (posY - 10) // 100
                    if (row, col) not in pairs and row < columns and col < columns:
                        pairs.append((row, col))
                        matrix_memory[row][col] = (matrix_memory[row][col][0], matrix_memory[row][col][1], True)
        # Validacion de igualidades y ganador
        if len(pairs) == 2 and next_step:
            # Cuadros iguales
            if matrix_memory[pairs[0][0]][pairs[0][1]][0] == matrix_memory[pairs[1][0]][pairs[1][1]][0] and matrix_memory[pairs[0][0]][pairs[0][1]][0] != None and matrix_memory[pairs[1][0]][pairs[1][1]][0] != None:
                #print("Los dos cuadros son iguales")
                matrix_memory[pairs[0][0]][pairs[0][1]] = (None, matrix_memory[pairs[0][0]][pairs[0][1]][1], False)
                matrix_memory[pairs[1][0]][pairs[1][1]] = (None, matrix_memory[pairs[1][0]][pairs[1][1]][1], False)
                tries += 1
                pygame.display.set_caption(f"Memory Game | Intentos {tries}")
                if check_game(matrix_memory):
                    game_start = False
            else:
                tries += 1
                pygame.display.set_caption(f"Memory Game | Intentos {tries}")
                pause_count = 4
            for pair in pairs:
                matrix_memory[pair[0]][pair[1]] = (matrix_memory[pair[0]][pair[1]][0], matrix_memory[pair[0]][pair[1]][1], False)
            pairs = []
            next_step = False
        elif len(pairs) == 2 and not next_step:
            next_step = True
        pygame.display.flip()
    return "finished"

# Main
if __name__ == "__main__":
    Tk().wm_withdraw()
    # Columnas y filas de la matriz
    columns = 4
    if columns**2 % 2 != 0:
        sys.exit(1)
    # Creacion de la ventana pygame
    pygame.init()
    surface = pygame.display.set_mode((420, 420))
    while True:
        matrix_memory = set_matrix_memory(columns)
        game_status = main_game(matrix_memory)
        if game_status == "finished":
            messagebox.showinfo("Ganaste", "Ganaste el juego")
        if not messagebox.askokcancel("Nuevo Juego", "Deseas comenzar otra partida"):
            break
    os._exit(0)