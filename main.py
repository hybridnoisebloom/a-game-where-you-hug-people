import sfml as sf
import collision
from random import randint

# TO-DO LIST #
# TODO: Integrate random people appearances into gameplay #
# TODO: Get proper art from 0creds #
# TODO: Force Josh to make promo art #
# TODO: use SFXR to get some sound effects going #

w = sf.RenderWindow(sf.VideoMode(640, 480), "INSERT YOUR TITLE HERE", sf.Style.TITLEBAR)

# A game where you hug people - exactly what it says on the tin

player = sf.Sprite(sf.Texture.from_file("player.png"))
textures = [sf.Texture.from_file("person1.png"), sf.Texture.from_file("person2.png"), sf.Texture.from_file("person3.png"), sf.Texture.from_file("person4.png"), sf.Texture.from_file("person5.png")]

people = []
for i in range(0, 20):
    people.append(sf.Sprite(textures[randint(0, 4)]))

for i in people:
    i.position = sf.Vector2(randint(0, 640), randint(0, 480))

player.position = sf.Vector2(randint(0, 640), randint(0, 480))

ai_clock = sf.Clock()
breathing_clock = sf.Clock()
breath_limit = 10
a = 0
hugging = False
title_screen = False

keyboard_dict = {sf.Keyboard.UP:sf.Vector2(0, -7), sf.Keyboard.LEFT:sf.Vector2(-7, 0), sf.Keyboard.RIGHT:sf.Vector2(7, 0), sf.Keyboard.DOWN:sf.Vector2(0, 7)}

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
                    elif e.code is sf.Keyboard.L_BRACKET:
                        for i in range(0, 5):
                            people.pop()
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
                breathing_clock.restart()
            else:
                pass
        hugging = False

    if len(people) < 15+a:
        a = len(people)
        for i in range(0, 20):
            people.append(sf.Sprite(textures[randint(0, 4)]))
        for i in people[a:]:
            i.position = sf.Vector2(randint(0, 640), randint(0, 480))

    w.clear()
    w.draw(player)
    for i in people:
        w.draw(i)

    for i in people:
        if i.position.x < 0 or i.position.y < 0 or i.position.x > 640 or i.position.y > 480:
            i.position = sf.Vector2(randint(0,640), randint(0,480))

    if player.position.x < 0 or player.position.y < 0 or player.position.x > 640 or player.position.y > 480:
        player.position = sf.Vector2(randint(0, 640), randint(0, 480))
    
    if ai_clock.elapsed_time.seconds >= randint(0, 3):
        ai_clock.restart()
        people[randint(0, 4)].move(sf.Vector2(randint(-1, 1)*randint(-18, -5), randint(-1, 1)*randint(5, 18)))
    
    print len(people)
    print hugging
    print breathing_clock.elapsed_time.seconds

    w.display()
