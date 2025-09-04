import pygame
import random
import os
pygame.init()

BASE_DIR = os.path.dirname(__file__)
character_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "tycoon_character.png"))
background_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "background.jpg"))
shack_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "storage_shack.png"))
truck_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "truck.png"))
fence_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "fence.png"))
farm_rot_fence = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "fence_farm.png"))
coin_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "coin.png"))
npc_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "npc.png"))
worker_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "npc.png"))
storage_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "storage.png"))
store_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "store.png"))
strawberry_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "strawberry.png"))
grape_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "grape.png"))
orange_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "orange.png"))
strawberry_store = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "strawberry-store.png"))
grape_store = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "grape-store.png"))
orange_store = pygame.image.load(os.path.join(BASE_DIR, "assets", "level1", "orange-store.png"))

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Character
player_rect = character_img.get_rect(topleft=(100, 100))

# Storage Shack
shack_rect = shack_img.get_rect(topleft=(630, 50))

# Truck
truck_rect = truck_img.get_rect(topleft=(630,350))
# Fences
fence_positions = [(0,0), (170,0), (340,0), (510,0), (680,0)]
rot_fence = pygame.transform.rotate(fence_img, 90)
rot_fence_positions = [(0,30), (770,30), (0,120), (770,120)]

fences = [fence_img.get_rect(topleft=pos) for pos in fence_positions]
rot_fences = [rot_fence.get_rect(topleft=pos) for pos in rot_fence_positions]

# Coin Farm Fences
farm_fence_positions = [(200, 100), (200, 200), (490, 160)]
farm_fence_img = pygame.transform.rotate(farm_rot_fence, 90)
farm_rot_fence_positions = [(200, 100), (200, 300), (300, 100), (300, 300), (400, 100), (400, 300)]

farm_fences = [farm_fence_img.get_rect(topleft=pos) for pos in farm_fence_positions]
farm_rot_fences = [farm_rot_fence.get_rect(topleft=pos) for pos in farm_rot_fence_positions]


# Coins
coin_positions = [(300,200), (250, 150), (400,250)]
coins = [coin_img.get_rect(topleft=pos) for pos in coin_positions]
farm_coin_spots = [
    (250, 180), (350, 180), (450, 180),
    (250, 250), (350, 250), (450, 250)
]

# NPCs
npc_positions = [(700, 300), (665, 300)]
npcs = [npc_img.get_rect(topleft=pos) for pos in npc_positions]

# Worker
worker_rect = worker_img.get_rect(topleft=(600, 100))

# Storage
storage_open = False
# Store
shop_open = False
interaction_text = ""
interaction_text_option = ""
player_cash = 0

# Fruits
strawberry_rect = strawberry_img.get_rect(topleft=(10 , 300))
strawberry_store_open = False

orange_rect = orange_img.get_rect(topleft=(150 , 310))
orange_store_open = False

grape_rect = grape_img.get_rect(topleft=(80 , 350))
grape_store_open = False

# Purchase cooldown
buy_delay = 300  # milliseconds
last_buy_time = -buy_delay
coin_spawn_delay = 60000  # 60 seconds in milliseconds
last_coin_spawn_time = 0
font = pygame.font.SysFont(None, 36)

# Snack prices
snacks = {"1": ("Chips", 50), "2": ("Cookies", 10), "3": ("Soda", 3)}
sell_prices = {"Chips": 75, "Cookies": 15, "Soda": 6}

# Stock - Fixed to include all special items properly
stock = {"Chips": 0, "Cookies": 0, "Soda": 0, "Golden Apples": 0, "Mystery Snack": 0}

# Special items system - Fixed with proper initialization
def create_mystery_snack():
    """Create a mystery snack with a random multiplier"""
    return {"name": "Mystery Snack", "multiplier": random.choice([2, 1.5, 1])}

def get_special_item():
    """Get a special item with 10% chance, otherwise return None"""
    if random.random() < 0.1:  # 10% chance for special item
        if random.random() < 0.5:  # 50/50 between Golden Apple and Mystery Snack
            return {"name": "Golden Apples", "multiplier": 3}
        else:
            return create_mystery_snack()
    return None

def calculate_sell_price(item_name, base_price):
    """Calculate the actual selling price including multipliers"""
    if item_name == "Golden Apples":
        return base_price * 3
    elif item_name == "Mystery Snack":
        # For simplicity, we'll use a fixed high multiplier for mystery snacks
        # In a more complex system, you'd track individual mystery snack multipliers
        return base_price * 2
    else:
        return base_price

running = True
millisecond_counter = 0

screen_rect = screen.get_rect()

while running:
    interaction_text_option = ""
    dt = clock.tick(60)
    millisecond_counter += dt

    old_pos = player_rect.topleft

    keys = pygame.key.get_pressed()
    # Movement
    if not (shop_open or storage_open or strawberry_store_open or orange_store_open or grape_store_open):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_rect.y -= 300 * dt / 1000
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_rect.y += 300 * dt / 1000
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_rect.x -= 300 * dt / 1000
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_rect.x += 300 * dt / 1000

    # Collisions with fences
    for fence in fences + rot_fences:
        if player_rect.colliderect(fence):
            player_rect.topleft = old_pos
            break

    for fence in farm_fences + farm_rot_fences:
        if player_rect.colliderect(fence):
            player_rect.topleft = old_pos
            break

    for npc in npcs:
        if player_rect.colliderect(npc):
            interaction_text_option = "Press E to interact"
            break

    if player_rect.colliderect(worker_rect):
        interaction_text_option = "Press E to interact"

    if player_rect.colliderect(strawberry_rect):
        interaction_text_option = "Press E to interact"

    if player_rect.colliderect(orange_rect):
        interaction_text_option = "Press E to interact"

    if player_rect.colliderect(grape_rect):
        interaction_text_option = "Press E to interact"

    if player_rect.colliderect(truck_rect):
        player_rect.topleft = old_pos
        
    if player_rect.colliderect(shack_rect):
        player_rect.topleft = old_pos

    # Collect coins
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            player_cash += 1
            coins.remove(coin)

    player_rect.clamp_ip(screen_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if shop_open:
            if event.type == pygame.KEYDOWN:
                # Check cooldown
                if millisecond_counter - last_buy_time >= buy_delay:
                    if event.key == pygame.K_1 and player_cash >= snacks["1"][1]:
                        player_cash -= snacks["1"][1]
                        last_buy_time = millisecond_counter
                        special_item = get_special_item()
                        if special_item:
                            stock[special_item["name"]] += 1
                            interaction_text = f"Lucky! You got {special_item['name']} (x{special_item['multiplier']} multiplier)!"
                        else:
                            stock["Chips"] += 1
                            interaction_text = f"You bought {snacks['1'][0]}"
                        
                    elif event.key == pygame.K_2 and player_cash >= snacks["2"][1]:
                        player_cash -= snacks["2"][1]
                        last_buy_time = millisecond_counter
                        special_item = get_special_item()
                        if special_item:
                            stock[special_item["name"]] += 1
                            interaction_text = f"Lucky! You got {special_item['name']} (x{special_item['multiplier']} multiplier)!"
                        else:
                            stock["Cookies"] += 1
                            interaction_text = f"You bought {snacks['2'][0]}"
                            
                    elif event.key == pygame.K_3 and player_cash >= snacks["3"][1]:
                        player_cash -= snacks["3"][1]
                        last_buy_time = millisecond_counter
                        special_item = get_special_item()
                        if special_item:
                            stock[special_item["name"]] += 1
                            interaction_text = f"Lucky! You got {special_item['name']} (x{special_item['multiplier']} multiplier)!"
                        else:
                            stock["Soda"] += 1
                            interaction_text = f"You bought {snacks['3'][0]}"
                            
                    elif event.key == pygame.K_ESCAPE:
                        shop_open = False
                        
        elif storage_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    storage_open = False
                    
        elif strawberry_store_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # Priority: Golden Apples > Mystery Snack > Regular Soda
                    if stock['Golden Apples'] > 0:
                        stock['Golden Apples'] -= 1
                        earned = calculate_sell_price("Golden Apples", sell_prices["Soda"])
                        player_cash += earned
                        interaction_text = f'Sold Golden Apple for ${earned}!'
                    elif stock["Mystery Snack"] > 0:
                        stock['Mystery Snack'] -= 1
                        earned = calculate_sell_price("Mystery Snack", sell_prices["Soda"])
                        player_cash += earned
                        interaction_text = f"Sold Mystery Snack for ${earned}!"
                    elif stock["Soda"] > 0:
                        stock["Soda"] -= 1
                        earned = sell_prices["Soda"]
                        player_cash += earned
                        interaction_text = f"Sold Soda for ${earned}"
                    else:
                        interaction_text = "No items to sell!"
                    last_buy_time = millisecond_counter
                elif event.key == pygame.K_ESCAPE:
                    strawberry_store_open = False
                    
        elif orange_store_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if stock["Cookies"] > 0:
                        stock["Cookies"] -= 1
                        earned = sell_prices["Cookies"]
                        player_cash += earned
                        interaction_text = f"Sold Cookies for ${earned}"
                        last_buy_time = millisecond_counter
                    else:
                        interaction_text = "No cookies to sell!"
                elif event.key == pygame.K_ESCAPE:
                    orange_store_open = False
                    
        elif grape_store_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if stock["Chips"] > 0:
                        stock["Chips"] -= 1
                        earned = sell_prices["Chips"]
                        player_cash += earned
                        interaction_text = f"Sold Chips for ${earned}"
                        last_buy_time = millisecond_counter
                    else:
                        interaction_text = "No chips to sell!"
                elif event.key == pygame.K_ESCAPE:
                    grape_store_open = False
        else:
            # Open shop if near NPC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if player_rect.colliderect(worker_rect):
                    storage_open = True
                elif player_rect.colliderect(strawberry_rect):
                    strawberry_store_open = True
                elif player_rect.colliderect(orange_rect):
                    orange_store_open = True
                elif player_rect.colliderect(grape_rect):
                    grape_store_open = True
                else:
                    for npc in npcs:
                        if player_rect.colliderect(npc):
                            shop_open = True
                            break

    # Coin farm spawns every minute
    if millisecond_counter - last_coin_spawn_time >= coin_spawn_delay:
        spawn_pos = random.choice(farm_coin_spots)
        coins.append(coin_img.get_rect(topleft=spawn_pos))
        last_coin_spawn_time = millisecond_counter

    # Draw
    screen.blit(background_img, (0,0))
    for fence in fences:
        screen.blit(fence_img, fence)
    for fence in rot_fences:
        screen.blit(rot_fence, fence)
    for fence in farm_fences:
        screen.blit(farm_fence_img, fence)
    for fence in farm_rot_fences:
        screen.blit(farm_rot_fence, fence)
    for coin in coins:
        screen.blit(coin_img, coin)
    for npc in npcs:
        screen.blit(npc_img, npc)
    screen.blit(character_img, player_rect)
    screen.blit(truck_img, truck_rect)
    screen.blit(shack_img, shack_rect)
    screen.blit(worker_img, worker_rect)
    
    # Cash
    cash_text = font.render(f"Cash: ${player_cash}", True, (255,255,0))
    screen.blit(cash_text, (10,10))

    # Static labels
    message_surface = font.render("Buy", True, (0, 0, 0))
    screen.blit(message_surface,(670, 370))
    message_surface = font.render("Storage", True, (0, 0, 0))
    screen.blit(message_surface,(640, 35))
    message_surface = font.render("Coin Farm", True, (0, 0, 0))
    screen.blit(message_surface,(300, 150))
    message_surface = font.render("Sell", True, (0, 0, 0))
    screen.blit(message_surface,( 75, 300))

    screen.blit(strawberry_img, strawberry_rect)
    screen.blit(orange_img, orange_rect)
    screen.blit(grape_img, grape_rect)

    # Store screen
    if shop_open:
        screen.blit(store_img, (100,100))

    if storage_open:
        screen.blit(storage_img, (100, 100))
        # Display regular items
        message_surface = font.render(str(stock["Chips"]), True, (0 , 0, 0))
        screen.blit(message_surface, (200, 340))
        message_surface = font.render(str(stock["Cookies"]), True, (0 , 0, 0))
        screen.blit(message_surface, (390, 340))
        message_surface = font.render(str(stock["Soda"]), True, (0 , 0, 0))
        screen.blit(message_surface, (580, 340))
        
        # Display special items
        special_y_offset = 380
        message_surface = font.render(f"Golden Apples: {stock['Golden Apples']}", True, (255, 215, 0))
        screen.blit(message_surface, (200, special_y_offset))
        message_surface = font.render(f"Mystery Snacks: {stock['Mystery Snack']}", True, (138, 43, 226))
        screen.blit(message_surface, (200, special_y_offset + 30))

    if strawberry_store_open:
        screen.blit(strawberry_store, (100, 100))
        message_surface = font.render(str(stock["Soda"]), True, (0 , 0, 0))
        screen.blit(message_surface, (390, 340))
        
        # Show special items available for sale
        special_y = 20
        if stock['Golden Apples'] > 0:
            message_surface = font.render(f"Golden Apples: {stock['Golden Apples']} (${calculate_sell_price('Golden Apples', sell_prices['Soda'])} each)", True, (255, 215, 0))
            screen.blit(message_surface, (270, special_y))
        if stock['Mystery Snack'] > 0:
            message_surface = font.render(f"Mystery Snacks: {stock['Mystery Snack']} (${calculate_sell_price('Mystery Snack', sell_prices['Soda'])} each)", True, (138, 43, 226))
            screen.blit(message_surface, (270, special_y + 25))

    if orange_store_open:
        screen.blit(orange_store, (100, 100))
        message_surface = font.render(str(stock["Cookies"]), True, (0 , 0, 0))
        screen.blit(message_surface, (390, 340))

    if grape_store_open:
        screen.blit(grape_store, (100, 100))
        message_surface = font.render(str(stock["Chips"]), True, (0 , 0, 0))
        screen.blit(message_surface, (390, 340))

    if interaction_text_option:
        message_surface = font.render(interaction_text_option, True, (255, 255, 255))
        screen.blit(message_surface, (10, 50))

    if interaction_text:
        message_surface = font.render("Last Action:", True, (255, 0, 0))
        screen.blit(message_surface, (10, 100))
        message_surface = font.render(interaction_text, True, (255, 0, 0))
        screen.blit(message_surface, (10, 130))

    pygame.display.flip()

pygame.quit()