@namespace
class SpriteKind:
    p = SpriteKind.create()
"""

=========================

"""
"""

VARIABLES

"""
"""

=========================

"""


# =========================
def spawn_phantom():
    global phantom2
    phantom2 = sprites.create(img("""
            . . . . . . f f f f . . . . . .
            . . . . f f f f f f f f . . . .
            . . . f f f f f f f f f f . . .
            . . f f 1 1 f f f f 1 1 f f . .
            . . f f 1 1 f f f f 1 1 f f . .
            . . f f f f f f f f f f f f . .
            . . f b 1 1 1 1 1 1 1 1 b f . .
            . f f 1 b 1 1 1 1 1 b b 1 f f .
            . f f f 1 b b 1 1 b 1 1 f f f .
            . . f f f f 1 b b 1 f f f f . .
            . . . f f f f f f f f f f . . .
            . . f f f f f f f f f f f f . .
            . . f f f f f f f f f f f f . .
            . . f f f f f f f f f f f f . .
            . . . . . f f f f f f . . . . .
            . . . . . f f . . f f . . . . .
            """),
        SpriteKind.enemy)
    # Try 20 random positions
    for index in range(20):
        x = randint(16, 300)
        y = randint(16, 300)
        phantom2.set_position(x, y)
        overlap = False
        # Check enemy overlap
        for enemy in sprites.all_of_kind(SpriteKind.enemy):
            if enemy != phantom2 and phantom2.overlaps_with(enemy):
                overlap = True
        # Don't spawn on player
        if abs(phantom2.x - Ben_Clark.x) < 40 and abs(phantom2.y - Ben_Clark.y) < 40:
            overlap = True
        # Good position found
        if not (overlap):
            break
    # Chase player
    phantom2.follow(Ben_Clark, 40)
# =========================
# LEVEL TRANSITION
# =========================
# slower baseline in level 2

def on_countdown_end():
    global current_level, last_spawn_time, spawn_quantity, spawn_cooldown
    current_level = 2
    tiles.set_current_tilemap(tilemap("""
        level2
        """))
    Ben_Clark.set_position(30, 135)
    # clear enemies
    for e in sprites.all_of_kind(SpriteKind.enemy):
        sprites.destroy(e, effects.spray, 500)
    # restart timer + spawn system
    info.start_countdown(60)
    last_spawn_time = game.runtime()
    spawn_quantity = 1
    spawn_cooldown = 3000
info.on_countdown_end(on_countdown_end)

# =========================
# HEALTH ITEM SPAWN
# =========================
def spawn_health_item():
    global item
    item = sprites.create(img("""
            . . . . . . . . . . . . . . . .
            . . . . 9 9 9 . . . 9 9 9 . . .
            . . . 9 2 2 2 9 . 9 2 2 2 9 . .
            . . 9 2 2 2 2 2 9 2 2 2 2 2 9 .
            . 9 2 2 2 2 2 2 2 2 2 2 2 2 2 9
            . 9 2 2 2 2 2 2 2 2 2 2 2 2 2 9
            . 9 2 2 2 2 2 2 2 2 2 2 2 2 2 9
            . . 9 2 2 2 2 2 2 2 2 2 2 2 9 .
            . . . 9 2 2 2 2 2 2 2 2 2 9 . .
            . . . . 9 2 2 2 2 2 2 2 9 . . .
            . . . . . 9 2 2 2 2 2 9 . . . .
            . . . . . . 9 2 2 2 9 . . . . .
            . . . . . . . 9 2 9 . . . . . .
            . . . . . . . . 9 . . . . . . .
            """),
        SpriteKind.food)
    item.set_position(randint(12, 300), randint(12, 300))

def on_right_pressed():
    global direction
    direction = 1
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_down_pressed():
    global direction
    direction = 4
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def on_on_overlap2(sprite, otherSprite):
    # =========================
    # SPRITE TYPES
    # =========================
    info.change_life_by(1)
    sprites.destroy(otherSprite)
sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_on_overlap2)

def on_on_overlap(sprite2: Sprite, otherSprite2: Sprite):
    info.change_life_by(-1)
    sprites.destroy(otherSprite2)
    pause(500)
current_time3 = 0
now = 0
enemies: List[Sprite] = []
item: Sprite = None
phantom2: Sprite = None
projectile: Sprite = None
direction = 0
last_spawn_time = 0
current_level = 0
spawn_quantity = 0
spawn_cooldown = 0
Ben_Clark: Sprite = None
Health = 0
# =========================
# ENEMY DAMAGE
# =========================
damage_cooldown = False
phantom = None
scene.set_background_color(2)
# =========================
# PLAYER
# =========================
Ben_Clark = sprites.create(assets.image("""
    Ben Clark
    """), SpriteKind.player)
controller.move_sprite(Ben_Clark, 150, 150)
scene.camera_follow_sprite(Ben_Clark)
tiles.set_current_tilemap(tilemap("""
    level1
    """))
info.start_countdown(60)
info.set_life(5)
Ben_Clark.set_position(30, 135)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)
# =========================
# SPAWN SETTINGS
# =========================
spawn_cooldown = 5000
spawn_quantity = 1
# =========================
# LEVEL TRACKER
# =========================
current_level = 1
spawn_cooldown = 2000
spawn_quantity = 1
last_spawn_time = 0

def on_on_update():
    global enemies
    enemies = sprites.all_of_kind(SpriteKind.enemy)
    for a in enemies:
        for b in enemies:
            if a != b and a.overlaps_with(b):
                if a.x < b.x:
                    a.x -= 2
                else:
                    a.x += 2
                if a.y < b.y:
                    a.y -= 2
                else:
                    a.y += 2
game.on_update(on_on_update)

# =========================
# SPAWN LOOP
# =========================

def on_on_update2():
    if randint(0, 800) < 1:
        spawn_health_item()
game.on_update(on_on_update2)

# =========================
# SPAWN UPDATE LOOP
# =========================

def on_on_update3():
    global now, spawn_cooldown, spawn_quantity, last_spawn_time
    now = game.runtime()
    # LEVEL 1 difficulty scaling
    if current_level == 1:
        elapsed2 = now / 1000
        spawn_cooldown = max(800, 5000 - elapsed2 * 50)
        spawn_quantity = min(5, 1 + Math.floor(elapsed2 / 12))
    elif current_level == 2:
        # LEVEL 2: slower, calmer, reduced pressure
        spawn_cooldown = 5000
        # slower spawns
        spawn_quantity = 1
    # only 1 phantom per wave
    # SPAWN CHECK
    if now - last_spawn_time >= spawn_cooldown:
        for index2 in range(spawn_quantity):
            spawn_phantom()
        last_spawn_time = now
game.on_update(on_on_update3)

# =========================
# GAME LOOP
# =========================

def on_on_update4():
    global current_time3, spawn_cooldown, spawn_quantity, last_spawn_time
    current_time3 = game.runtime()
    # Difficulty scaling
    if current_time3 > 10000:
        elapsed = (current_time3 - 10000) / 1000
        # Faster spawning over time
        spawn_cooldown = max(1000, 5000 - elapsed * 50)
        # More enemies over time
        spawn_quantity = min(5, 1 + Math.floor(elapsed / 12))
    # Spawn enemies
    if current_time3 - last_spawn_time >= spawn_cooldown:
        for index3 in range(spawn_quantity):
            spawn_phantom()
        last_spawn_time = current_time3
game.on_update(on_on_update4)

def on_up_pressed():
    global direction
    direction = 3
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def on_a_pressed():
    global projectile
    if projectile == 1:
        projectile = sprites.create_projectile_from_sprite(img("""
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                """),
            Ben_Clark,
            100,
            0)
    elif projectile == 2:
        projectile = sprites.create_projectile_from_sprite(img("""
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                """),
            Ben_Clark,
            -100,
            0)
    elif projectile == 3:
        projectile = sprites.create_projectile_from_sprite(img("""
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                """),
            Ben_Clark,
            0,
            -100)
    elif projectile == 4:
        projectile = sprites.create_projectile_from_sprite(img("""
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . f f f f f . . . . . .
                . . . . . . f f f . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                """),
            Ben_Clark,
            0,
            100)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_left_pressed():
    global direction
    direction = 2
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

# =========================
# SPAWN FUNCTION