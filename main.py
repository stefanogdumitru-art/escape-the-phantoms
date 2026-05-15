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
# SPAWN FUNCTION
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
# PLAYER ANIMATION
# =========================

def on_down_pressed():
    animation.run_image_animation(Ben_Clark,
        [img("""
            . . . . e e e e . . . . .
            . . e e e e e e e e . . .
            . e e e e e e e e e e . .
            e e e e e e e e e e e e .
            e e e e e e e e e e e e .
            e e e e e e d d e e e e .
            e e e f f d d f f e e e .
            e e e b f d d f b e e e .
            . f d 1 f d d f 1 d f . .
            . f d d d d d d d d f . .
            . f f f d d d d f f f . .
            f b f b b b b b b f b f .
            d d f b b b b b b f d d .
            d d f b b b b b b f d d .
            . . . f f f f f f . . . .
            . . . f f . . f f . . . .
            """)],
        100,
        True)
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def on_on_overlap2(sprite, otherSprite):

# =========================
# SPRITE TYPES
# =========================

def on_on_overlap2(sprite, otherSprite):
    info.change_life_by(1)
    sprites.destroy(otherSprite)

sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_on_overlap2)


# =========================
# HEALTH ITEM SPAWN
# =========================

def spawn_health_item():
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
    """), SpriteKind.food)

    item.set_position(randint(16, 300), randint(16, 300))


# =========================
# PICKUP LOGIC
# =========================

def on_health_overlap(player, item):
    info.change_life_by(1)
    sprites.destroy(item)

sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_health_overlap)


# =========================
# SPAWN LOOP
# =========================

def on_update():
    if randint(0, 500) < 3:
        spawn_health_item()

game.on_update(on_update)

def on_on_overlap(sprite2: Sprite, otherSprite2: Sprite):
    info.change_life_by(-1)
    sprites.destroy(otherSprite2)
    pause(500)
enemies: List[Sprite] = []
last_spawn_time = 0
current_time3 = 0
Health = 0
phantom2: Sprite = None
Ben_Clark: Sprite = None
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
tiles.set_current_tilemap(tilemap("""
    level1
    """))
scene.camera_follow_sprite(Ben_Clark)
info.set_life(5)
info.start_countdown(60)
Ben_Clark.set_position(30, 150)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)
# =========================
# SPAWN SETTINGS
# =========================
spawn_cooldown = 5000
spawn_quantity = 1
# =========================
# GAME LOOP
# =========================

def on_on_update():
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
        for index2 in range(spawn_quantity):
            spawn_phantom()
        last_spawn_time = current_time3
game.on_update(on_on_update)

def on_on_update2():
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
game.on_update(on_on_update2)
