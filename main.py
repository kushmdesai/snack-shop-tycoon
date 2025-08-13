import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

character_img = pygame.image.load("tycoon_character.png").convert_alpha()
player_rect = character_img.get_rect(topleft=(100, 100))
background_img = pygame.image.load("background.jpg").convert_alpha()

fence_img = pygame.image.load("fence.png").convert_alpha()
fence_rect = fence_img.get_rect(topleft=(300, 200))
fence_positions = [(0,0), (170,0), (340, 0),(510, 0), (680, 0)]

rot_fence  = pygame.transform.rotate(fence_img, 90)
rot_fence_rect = rot_fence.get_rect(topleft=(300,200))
rot_fence_positions = [(0, 30), (770, 30), (0, 120), (770, 120)]

fences = []
rot_fences = []

for pos in fence_positions:
        rect = fence_img.get_rect(topleft=pos)
        fences.append(rect)

for pos in rot_fence_positions:
    rect = rot_fence.get_rect(topleft=pos)
    rot_fences.append(rect)

dt = 0
x, y = 100, 100
speed = 5


running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame

    keys = pygame.key.get_pressed()
    old_pos = player_rect.topleft

    for fence_rect in fences + rot_fences:
        if player_rect.colliderect(fence_rect):
            player_rect.topleft = old_pos
            break


    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_rect.y -= 300 * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_rect.y += 300 * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= 300 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += 300 * dt

    if player_rect.colliderect(fence_rect):
        player_rect.topleft = old_pos

    screen.blit(background_img, (0, 0))
    screen.blit(character_img, player_rect)
    for fence_rect in fences:
        screen.blit(fence_img, fence_rect)
    
    for rot_fence_rect in rot_fences:
        screen.blit(rot_fence, rot_fence_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()


    dt = clock.tick(60) / 1000

pygame.quit()