namespace SpriteKind {
    export const p = SpriteKind.create()
}

let current_time3 = 0
let phantom = null
let Ben_Clark = null
scene.setBackgroundColor(2)
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
            `, img`
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
            `, img`
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
            `], 100, true)
})
//  =========================
//  ENEMY DAMAGE
//  =========================
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_on_overlap(sprite: Sprite, otherSprite: Sprite) {
    info.changeLifeBy(-1)
    sprites.destroy(otherSprite)
})
//  =========================
//  SPAWN SETTINGS
//  =========================
let spawn_cooldown = 5000
let spawn_quantity = 1
let last_spawn_time = 0
//  =========================
//  SPAWN FUNCTION
//  =========================
function spawn_phantom() {
    let x: number;
    let y: number;
    let overlap: boolean;
    
    phantom = sprites.create(img`
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
    let placed = false
    while (!placed) {
        x = randint(16, 300)
        y = randint(16, 300)
        phantom.setPosition(x, y)
        overlap = false
        //  Check overlap with other enemies
        for (let enemy of sprites.allOfKind(SpriteKind.Enemy)) {
            if (enemy != phantom && phantom.overlapsWith(enemy)) {
                overlap = true
            }
            
        }
        //  Prevent spawning too close to player
        if (Math.abs(phantom.x - Ben_Clark.x) < 40 && Math.abs(phantom.y - Ben_Clark.y) < 40) {
            overlap = true
        }
        
        if (!overlap) {
            placed = true
        }
        
    }
    //  Enemy chase AI
    phantom.follow(Ben_Clark, 40)
}

//  =========================
//  GAME UPDATE LOOP
//  =========================
game.onUpdate(function on_on_update() {
    let elapsed: number;
    
    
    
    
    current_time3 = game.runtime()
    //  Difficulty scaling after 10 seconds
    if (current_time3 > 10000) {
        elapsed = (current_time3 - 10000) / 1000
        //  Spawn faster slowly
        spawn_cooldown = Math.max(1000, 5000 - elapsed * 50)
        //  Spawn more enemies slowly
        spawn_quantity = Math.min(5, 1 + Math.floor(elapsed / 12))
    }
    
    //  Spawn check
    if (current_time3 - last_spawn_time >= spawn_cooldown) {
        for (let index = 0; index < spawn_quantity; index++) {
            spawn_phantom()
        }
        last_spawn_time = current_time3
    }
    
})
