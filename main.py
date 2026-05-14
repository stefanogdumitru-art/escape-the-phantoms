@namespace
class SpriteKind:
    p = SpriteKind.create()


current_time3 = 0
phantom = None
global Ben_Clark = None

scene.set_background_color(2)

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


# =========================
# PLAYER ANIMATION
# =========================

def on_down_pressed():
    animation.run_image_animation(
        Ben_Clark,
        [
            img("""
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
            """),
            img("""
                . . . . . . . . . . . . .
                . . . . . e e e e . . . .
                . . . e e e e e e e e . .
                . . e e e e e e e e e e .
                e e e e e e e e e e e e e
                e e e e e e e e e e e e e
                . e e e e e e d d e e e e
                . e e e f f d d f f e e e
                . e e e b f d d f b e e e
                . e e d 1 f d d f 1 d e f
                . . f d d d d d d f f f f
                . f b f b b b b f d d d f
                . d d f b b b b f d d f .
                . . . f b b b b b f f . .
                . . . f f f f f f f . . .
                . . . f f f . . . . . . .
            """),
            img("""
                . . . . . . . . . . . . .
                . . . . e e e e . . . . .
                . . e e e e e e e e . . .
                . e e e e e e e e e e . .
                e e e e e e e e e e e e e
                e e e e e e e e e e e e e
                e e e e d d e e e e e e .
                e e e f f d d f f e e e .
                e e e b f d d f b e e e .
                e e d 1 f d d f 1 d e e .
                f f f f d d d d d d f . .
                f d d d f b b b b f b f .
                . f d d f b b b b f d d .
                . . f f b b b b b f . . .
                . . . f f f f f f f . . .
                . . . . . . . f f f . . .
            """)
        ],
        100,
        True
    )

controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)


# =========================
# ENEMY DAMAGE
# =========================

def on_on_overlap(sprite, otherSprite):
    info.change_life_by(-1)
    pause(500)
    sprites.destroy(otherSprite)

sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)


# =========================
# SPAWN SETTINGS
# =========================

spawn_cooldown = 5000
spawn_quantity = 1
last_spawn_time = 0


# =========================
# SPAWN FUNCTION
# =========================

def spawn_phantom():

    global phantom

    phantom = sprites.create(img("""
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
    """), SpriteKind.enemy)

    placed = False

    while not placed:

        x = randint(16, 300)
        y = randint(16, 300)

        phantom.set_position(x, y)

        overlap = False

        # Check overlap with other enemies
        for enemy in sprites.all_of_kind(SpriteKind.enemy):

            if enemy != phantom and phantom.overlaps_with(enemy):
                overlap = True

        # Prevent spawning too close to player
        if abs(phantom.x - Ben_Clark.x) < 40 and abs(phantom.y - Ben_Clark.y) < 40:
            overlap = True

        if not overlap:
            placed = True

    # Enemy chase AI
    phantom.follow(Ben_Clark, 40)


# =========================
# GAME UPDATE LOOP
# =========================

def on_on_update():

    global current_time3
    global spawn_cooldown
    global spawn_quantity
    global last_spawn_time

    current_time3 = game.runtime()

    # Difficulty scaling after 10 seconds
    if current_time3 > 10000:

        elapsed = (current_time3 - 10000) / 1000

        # Spawn faster slowly
        spawn_cooldown = max(
            1000,
            5000 - elapsed * 50
        )

        # Spawn more enemies slowly
        spawn_quantity = min(
            5,
            1 + Math.floor(elapsed / 12)
        )

    # Spawn check
    if current_time3 - last_spawn_time >= spawn_cooldown:

        for index in range(spawn_quantity):
            spawn_phantom()

        last_spawn_time = current_time3


game.on_update(on_on_update)
