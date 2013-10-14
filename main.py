import sfml as sf
import collision
from random import randint

# TO-DO LIST #
# TODO: Get proper art from 0creds #
# TODO: Force Josh to make promo art #

w = sf.RenderWindow(sf.VideoMode(640, 480), "INSERT YOUR TITLE HERE", sf.Style.TITLEBAR)

# A game where you hug people - exactly what it says on the tin
hug_sound = sf.Sound(sf.SoundBuffer.from_file("hug.wav"))

player = sf.Sprite(sf.Texture.from_file("player.png"))
textures = [sf.Texture.from_file("person1.png"), sf.Texture.from_file("person2.png"), sf.Texture.from_file("person3.png"), sf.Texture.from_file("person4.png"), sf.Texture.from_file("person5.png")]

title1 = sf.Sprite(sf.Texture.from_file("title1.png"))
title1.position = sf.Vector2(320, 10)
title2 = sf.Sprite(sf.Texture.from_file("title2.png"))
title2.position = sf.Vector2(320, 138)
title3 = sf.Sprite(sf.Texture.from_file("title3.png"))
title3.position = sf.Vector2(320, 266)

people = []
for i in range(0, 20):
    people.append(sf.Sprite(textures[randint(0, 4)]))

for i in people:
    i.position = sf.Vector2(randint(0, 640), randint(0, 480))

player.position = sf.Vector2(randint(0, 640), randint(0, 480))

ai_clock = sf.Clock()
breathing_clock = sf.Clock()
a = 0
hugging = False
title_screen = True
score = 0

keyboard_dict = {sf.Keyboard.UP:sf.Vector2(0, -7), sf.Keyboard.LEFT:sf.Vector2(-7, 0), sf.Keyboard.RIGHT:sf.Vector2(7, 0), sf.Keyboard.DOWN:sf.Vector2(0, 7)}

randclock = sf.Clock()
taxiclock = sf.Clock()
refresh_clock = sf.Clock()

taxi_vis = False
taxi = sf.Sprite(sf.Texture.from_file("taxi.png"))
taxi.move(sf.Vector2(0, 10))

while w.is_open:
    for e in w.events:
        if not title_screen:
            if type(e) == sf.KeyEvent and e.pressed:
                try:
                    player.move(keyboard_dict[e.code])
                except KeyError:
                    if e.code is sf.Keyboard.ESCAPE:
                        w.close()
                    elif e.code is sf.Keyboard.SPACE or e.code is sf.Keyboard.R_CONTROL or e.code is sf.Keyboard.NUMPAD0:
                        hugging = True
                    else:
                        pass
        elif title_screen:
            if type(e) == sf.MouseButtonEvent and e.pressed:
                if title2.global_bounds.contains(e.position):
                    title_screen = False
                elif title3.global_bounds.contains(e.position):
                    w.close()
                else:
                    pass
            elif type(e) == sf.KeyEvent and e.pressed:
                if e.code is sf.Keyboard.ESCAPE:
                    w.close()
                else:
                    pass
            else:
                pass
    
    if breathing_clock.elapsed_time.seconds >= 10:
        # YOU DEAD
        w.close()

    if hugging:
        # Hugging handler
        for i in people:
            if collision.collides(player.global_bounds, i.global_bounds):
                people.remove(i)
                hug_sound.play()
                breathing_clock.restart()
                score += 10
            else:
                pass
        hugging = False

    if randclock.elapsed_time.seconds >= randint(10, 20) and not taxi_vis:
        taxi_vis = True
        randclock.restart()
    
    if taxi_vis and refresh_clock.elapsed_time.seconds >= 1 and len(people) < 25:
        a = len(people)
        for i in range(0, randint(0, 5)):
            people.append(sf.Sprite(textures[randint(0, 4)]))
        for i in people[a:]:
            i.position = sf.Vector2(randint(0, 640), randint(0, 480))
        taxiclock.restart()
        refresh_clock.restart()

    if taxiclock.elapsed_time.seconds >= 5 and taxi_vis:
        taxi_vis = False
        taxi.position = sf.Vector2(0, 10)

    blargh = sf.Text(str(10 - int(breathing_clock.elapsed_time.seconds)))
    blargh.position = sf.Vector2(290, 0)

    score_text = sf.Text(str(score))
    score_text.position = sf.Vector2(340, 0)

    w.clear()
    if title_screen:
        w.draw(title1)
        w.draw(title2)
        w.draw(title3)
    elif not title_screen:
        w.draw(player)
        for i in people:
            w.draw(i)
        if taxi_vis:
            taxi.move(sf.Vector2(2.5, 0))
            w.draw(taxi)
        w.draw(blargh)
        w.draw(score_text)
    else:
        pass

    for i in people:
        if i.position.x < 0 or i.position.y < 0 or i.position.x > 640 or i.position.y > 480:
            i.position = sf.Vector2(randint(0,640), randint(0,480))

    if player.position.x < 0 or player.position.y < 0 or player.position.x > 640 or player.position.y > 480:
        player.position = sf.Vector2(randint(0, 640), randint(0, 480))
    
    if ai_clock.elapsed_time.seconds >= randint(0, 3):
        ai_clock.restart()
        people[randint(0, 4)].move(sf.Vector2(randint(-1, 1)*randint(-18, -5), randint(-1, 1)*randint(5, 18)))
    
    w.display()
