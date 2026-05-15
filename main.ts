namespace SpriteKind {
    export const p = SpriteKind.create()
}

/** ========================= */
/** VARIABLES */
/** ========================= */
//  =========================
//  SPAWN FUNCTION
//  =========================
function spawn_phantom() {
    let x: number;
    let y: number;
    let overlap: boolean;
    
    phantom2 = sprites.create(img`
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
            `, SpriteKind.Enemy)
    //  Try 20 random positions
    for (let index = 0; index < 20; index++) {
        x = randint(16, 300)
        y = randint(16, 300)
        phantom2.setPosition(x, y)
        overlap = false
        //  Check enemy overlap
        for (let enemy of sprites.allOfKind(SpriteKind.Enemy)) {
            if (enemy != phantom2 && phantom2.overlapsWith(enemy)) {
                overlap = true
            }
            
        }
        //  Don't spawn on player
        if (Math.abs(phantom2.x - Ben_Clark.x) < 40 && Math.abs(phantom2.y - Ben_Clark.y) < 40) {
            overlap = true
        }
        
        //  Good position found
        if (!overlap) {
            break
        }
        
    }
    //  Chase player
    phantom2.follow(Ben_Clark, 40)
}

//  =========================
//  PLAYER ANIMATION
//  =========================
controller.down.onEvent(ControllerButtonEvent.Pressed, function on_down_pressed() {
    animation.runImageAnimation(Ben_Clark, [img`
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
            `], 100, true)
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function on_on_overlap2(sprite: Sprite, otherSprite: Sprite) {
    //  increase player life
    info.changeLifeBy(1)
    //  create health item (THIS is the sprite)
    let health_item = sprites.create(img`
        . . . . . . . . . . . . . . . .
        . . . . 9 9 9 . . . 9 9 9 . . .
        . . . 9 2 2 2 9 . 9 2 2 2 9 . .
        . . 9 2 2 2 2 2 9 2 2 2 2 2 9 .
        . 9 2 2 2 2 2 2 2 2 2 2 2 2 2 9
        . 9 2 2 2 2 2 2 2 2 2 2 2 2 2 9
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
    `, SpriteKind.Food)
    //  put it somewhere random (NUMBERS ONLY)
    health_item.setPosition(randint(16, 300), randint(16, 300))
})
function on_on_overlap(sprite2: Sprite, otherSprite2: Sprite) {
    info.changeLifeBy(-1)
    sprites.destroy(otherSprite2)
    pause(500)
}

let enemies : Sprite[] = []
let last_spawn_time = 0
let current_time3 = 0
let Health = 0
let phantom2 : Sprite = null
let Ben_Clark : Sprite = null
//  =========================
//  ENEMY DAMAGE
//  =========================
let damage_cooldown = false
let phantom = null
scene.setBackgroundColor(2)
//  =========================
//  PLAYER
//  =========================
Ben_Clark = sprites.create(assets.image`
    Ben Clark
    `, SpriteKind.Player)
controller.moveSprite(Ben_Clark, 150, 150)
tiles.setCurrentTilemap(tilemap`
    level1
    `)
scene.cameraFollowSprite(Ben_Clark)
info.setLife(5)
info.startCountdown(60)
Ben_Clark.setPosition(30, 150)
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, on_on_overlap)
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, on_on_overlap)
//  =========================
//  SPAWN SETTINGS
//  =========================
let spawn_cooldown = 5000
let spawn_quantity = 1
//  =========================
//  GAME LOOP
//  =========================
game.onUpdate(function on_on_update() {
    let elapsed: number;
    
    current_time3 = game.runtime()
    //  Difficulty scaling
    if (current_time3 > 10000) {
        elapsed = (current_time3 - 10000) / 1000
        //  Faster spawning over time
        spawn_cooldown = Math.max(1000, 5000 - elapsed * 50)
        //  More enemies over time
        spawn_quantity = Math.min(5, 1 + Math.floor(elapsed / 12))
    }
    
    //  Spawn enemies
    if (current_time3 - last_spawn_time >= spawn_cooldown) {
        for (let index2 = 0; index2 < spawn_quantity; index2++) {
            spawn_phantom()
        }
        last_spawn_time = current_time3
    }
    
})
game.onUpdate(function on_on_update2() {
    
    enemies = sprites.allOfKind(SpriteKind.Enemy)
    for (let a of enemies) {
        for (let b of enemies) {
            if (a != b && a.overlapsWith(b)) {
                if (a.x < b.x) {
                    a.x -= 2
                } else {
                    a.x += 2
                }
                
                if (a.y < b.y) {
                    a.y -= 2
                } else {
                    a.y += 2
                }
                
            }
            
        }
    }
})
