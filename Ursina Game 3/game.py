from ursina import *

app = Ursina()

Sky(texture="BackgroundSky.jpeg")

# Create the player
player = Entity(model='sphere', texture="Player.jpeg", y=2)
player.y_speed = 0
# Rotate the player 90 degrees to the right
player.rotation_y = 90
player.gold = 100 # Give the player some gold to start with

# Create the ground
ground = Entity(model='plane', scale=(100, 1, 100), texture='grass')

# Create the house
house = Entity(model='cube', scale=(10, 10, 10), x=20, y=5, texture='brick')

# Make the house slightly transparent
house.color = color.color(1, 1, 1, 0.6)

# Create the NPC
npc = Entity(model='cube', scale=(1,2,1), x=20, y=1, color=color.yellow)

# Create the camera
camera = EditorCamera()
camera.position = (0, 5, -10)

# Create a variable to store whether the camera is following the player
camera_following_player = False

# Create the shop
shop = {
    'sword': 50,
    'shield': 75,
    'potion': 25
}

# Create a Text entity to display the player's gold
gold_text = Text(text=f'Gold: {player.gold}', y=0.45, origin=(0,0), background=True)

# Create a Text entity to display the controls
controls_text = Text(text='WASD to move, Space to jump, C to switch camera modes, E to open the shop', y=-0.45, origin=(0,0), background=True)

# Create a Text entity to display the shop items
shop_text = Text(text='', origin=(0,0), background=True)
shop_text.enabled = False # Disable the shop text by default






def update(): # update gets automatically called
    global camera_following_player # We need to use the global keyword to change the value of a global variable

    # Calculate the forward and right vectors of the camera
    forward = camera.forward * (held_keys['w'] - held_keys['s'])
    right = camera.right * (held_keys['d'] - held_keys['a'])
    direction = (forward + right).normalized() * 4

    # Update the player's position based on the calculated direction
    player.position += direction * time.dt

    # Rotate the camera based on the arrow keys
    if held_keys['left arrow']:
        camera.rotation_y += 2 # Adjust this value to change the rotation speed
    if held_keys['right arrow']:
        camera.rotation_y -= 2 # Adjust this value to change the rotation speed
    if held_keys['up arrow']:
        camera.rotation_x += 1 # Adjust this value to change the rotation speed
    if held_keys['down arrow']:
        camera.rotation_x -= 1 # Adjust this value to change the rotation speed

# Old movement code
#    if held_keys['a']:
#        player.x -= 4 * time.dt
#    if held_keys['d']:
#        player.x += 4 * time.dt
#    if held_keys['w']:
#        player.z += 4 * time.dt
#    if held_keys['s']:
#        player.z -= 4 * time.dt

    # Simple gravity
    player.y = player.y + player.y_speed * time.dt
    player.y_speed = player.y_speed - 0.1 # You can change this value to make the gravity stronger or weaker

    # Simple collision with the ground
    if player.y < ground.y + 0.5: # If the player is in the ground
        player.y = ground.y + 0.5 # Put it on top of the ground
        player.y_speed = 0 # And set its speed to 0

    if held_keys['space'] and player.y <= ground.y + 0.5: # If space is pressed and the player is on the ground
        player.y_speed = 4 # Make the player jump

    # Switch the camera mode when the 'c' key is pressed
    if held_keys['c']:
        camera_following_player = not camera_following_player

    # If the camera is following the player, set its position to the player's position
    if camera_following_player:
        camera.position = player.position + Vec3(0, 3, -10) # Adjust these values to change the camera position relative to the player


    # Open the shop when the 'e' key is pressed and the player is near the NPC
    if held_keys['e'] and distance(player.position, npc.position) < 2:
        shop_text.enabled = not shop_text.enabled # Enable/disable the shop text
        if shop_text.enabled: # If the shop text is enabled
            shop_text.text = f'Welcome to the shop! here are the items for sale: \n'
            for item, price in shop.items():
                shop_text.text += f'{item}: {price} gold\n'


app.run()