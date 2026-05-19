namespace SpriteKind {
    export const enemy = SpriteKind.create()
    export const bullet = SpriteKind.create()
}

//  =========================
//  BULLET KILLS PHANTOMS
//  =========================
sprites.onOverlap(SpriteKind.bullet, SpriteKind.enemy, function on_on_overlap2(bullet2: Sprite, phantom: Sprite) {
    sprites.destroy(phantom, effects.fire, 100)
    sprites.destroy(bullet2)
})
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
            `, SpriteKind.enemy)
    //  Try 20 random positions
    for (let index = 0; index < 20; index++) {
        x = randint(16, 300)
        y = randint(16, 300)
        phantom2.setPosition(x, y)
        overlap = false
        //  Check enemy overlap
        for (let enemy3 of sprites.allOfKind(SpriteKind.enemy)) {
            if (enemy3 != phantom2 && phantom2.overlapsWith(enemy3)) {
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
//  LEVEL TRANSITION
//  =========================
//  slower baseline in level 2
info.onCountdownEnd(function on_countdown_end() {
    
    current_level = 2
    tiles.setCurrentTilemap(tilemap`
        level2
        `)
    Ben_Clark.setPosition(30, 135)
    //  clear enemies
    for (let e of sprites.allOfKind(SpriteKind.enemy)) {
        sprites.destroy(e, effects.spray, 500)
    }
    //  restart timer + spawn system
    info.startCountdown(60)
    last_spawn_time = game.runtime()
    spawn_quantity = 1
    spawn_cooldown = 3000
})
//  =========================
//  HEALTH ITEM SPAWN
//  =========================
function spawn_health_item() {
    
    item = sprites.create(img`
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
            `, SpriteKind.Food)
    item.setPosition(randint(12, 300), randint(12, 300))
}

controller.right.onEvent(ControllerButtonEvent.Pressed, function on_right_pressed() {
    
    direction = 1
})
//  =========================
//  AUTO AIM SHOOT
//  =========================
controller.down.onEvent(ControllerButtonEvent.Pressed, function on_down_pressed() {
    
    direction = 4
})
function spawn_ammo_item() {
    
    item2 = sprites.create(img`
            . . . . 7 7 7 . . . .
            . . 7 7 7 7 7 7 7 . .
            . 7 7 7 7 7 7 7 7 7 .
            . 7 7 7 7 7 7 7 7 7 .
            . . 7 7 7 7 7 7 7 . .
            . . . . 7 7 7 . . . .
            `, SpriteKind.Food)
    item2.setPosition(randint(16, 300), randint(16, 300))
}

sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function on_on_overlap3(sprite: Sprite, otherSprite: Sprite) {
    //  =========================
    //  SPRITE TYPES
    //  =========================
    info.changeLifeBy(1)
    sprites.destroy(otherSprite)
})
function on_on_overlap(sprite2: Sprite, otherSprite2: Sprite) {
    info.changeLifeBy(-1)
    sprites.destroy(otherSprite2)
    pause(500)
}

let current_time3 = 0
let now = 0
let enemies2 : Sprite[] = []
let item2 : Sprite = null
let bullet22 : Sprite = null
let closest_distance = 0
let target : Sprite = null
let enemies : Sprite[] = []
let direction = 0
let phantom2 : Sprite = null
let ammo = 0
let last_spawn_time = 0
let spawn_quantity = 0
let spawn_cooldown = 0
let Ben_Clark : Sprite = null
let current_level = 0
let Health = 0
//  =========================
//  ENEMY DAMAGE
//  =========================
let damage_cooldown = false
let projectile2 = null
let item : Sprite = null
//  =========================
//  LEVEL TRACKER
//  =========================
current_level = 1
controller.A.onEvent(ControllerButtonEvent.Pressed, function shoot() {
    let distance: number;
    
    //  only works in level 2
    if (current_level != 2) {
        return
    }
    
    //  find all phantoms
    enemies = sprites.allOfKind(SpriteKind.enemy)
    //  no enemies = no shooting
    if (enemies.length == 0) {
        return
    }
    
    //  closest phantom
    target = enemies[0]
    closest_distance = 999999
    for (let enemy2 of enemies) {
        distance = Math.sqrt((enemy2.x - Ben_Clark.x) * (enemy2.x - Ben_Clark.x) + (enemy2.y - Ben_Clark.y) * (enemy2.y - Ben_Clark.y))
        if (distance < closest_distance) {
            closest_distance = distance
            target = enemy2
        }
        
    }
    //  create bullet
    bullet22 = sprites.create(img`
            . . 5 5 . .
            . 5 5 5 5 .
            . . 5 5 . .
            `, SpriteKind.bullet)
    bullet22.setPosition(Ben_Clark.x, Ben_Clark.y)
    //  bullet auto follows closest phantom
    bullet22.follow(target, 200)
    //  delete bullet after time
    bullet22.lifespan = 2000
})
current_level = 0
scene.setBackgroundColor(2)
//  =========================
//  PLAYER
//  =========================
Ben_Clark = sprites.create(assets.image`
    Ben Clark
    `, SpriteKind.Player)
controller.moveSprite(Ben_Clark, 150, 150)
scene.cameraFollowSprite(Ben_Clark)
tiles.setCurrentTilemap(tilemap`
    level1
    `)
info.startCountdown(60)
info.setLife(5)
Ben_Clark.setPosition(30, 135)
sprites.onOverlap(SpriteKind.Player, SpriteKind.enemy, on_on_overlap)
sprites.onOverlap(SpriteKind.Player, SpriteKind.enemy, on_on_overlap)
//  =========================
//  SPAWN SETTINGS
//  =========================
spawn_cooldown = 5000
spawn_quantity = 1
//  =========================
//  LEVEL TRACKER
//  =========================
current_level = 1
spawn_cooldown = 2000
spawn_quantity = 1
last_spawn_time = 0
game.onUpdate(function on_on_update() {
    
    enemies2 = sprites.allOfKind(SpriteKind.enemy)
    for (let a of enemies2) {
        for (let b of enemies2) {
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
//  =========================
//  SPAWN LOOP
//  =========================
game.onUpdate(function on_on_update2() {
    if (randint(0, 800) < 1) {
        spawn_health_item()
    }
    
})
//  =========================
//  SPAWN UPDATE LOOP
//  =========================
game.onUpdate(function on_on_update3() {
    let elapsed2: number;
    
    now = game.runtime()
    //  LEVEL 1 difficulty scaling
    if (current_level == 1) {
        elapsed2 = now / 1000
        spawn_cooldown = Math.max(800, 5000 - elapsed2 * 50)
        spawn_quantity = Math.min(5, 1 + Math.floor(elapsed2 / 12))
    } else if (current_level == 2) {
        //  LEVEL 2: slower, calmer, reduced pressure
        spawn_cooldown = 5000
        //  slower spawns
        spawn_quantity = 1
    }
    
    //  only 1 phantom per wave
    //  SPAWN CHECK
    if (now - last_spawn_time >= spawn_cooldown) {
        for (let index2 = 0; index2 < spawn_quantity; index2++) {
            spawn_phantom()
        }
        last_spawn_time = now
    }
    
})
//  =========================
//  GAME LOOP
//  =========================
game.onUpdate(function on_on_update4() {
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
        for (let index3 = 0; index3 < spawn_quantity; index3++) {
            spawn_phantom()
        }
        last_spawn_time = current_time3
    }
    
})
