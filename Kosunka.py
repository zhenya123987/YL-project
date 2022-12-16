import pygame

pygame.init()
size = width, height = 500, 300
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color(0, 100, 100))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
