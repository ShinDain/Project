from pico2d import *
import gfw
import gobj
import main_state

canvas_width = main_state.canvas_width
canvas_height = main_state.canvas_height

buttonimage = None
button_pressimage = None
blackimage = None

index = 0

def build_world():
    gfw.world.init(['bg', 'ui'])

    center = (canvas_width//2, canvas_height//2)
    logo_pos = (canvas_width//2, canvas_height//2 + 250)
    logo = gobj.ImageObject('title.png', logo_pos, canvas_width, 375)
    bg = gobj.ImageObject('Background.png', center, canvas_width, canvas_height)

    gfw.world.add(gfw.layer.bg, bg)
    gfw.world.add(gfw.layer.ui, logo)

    global buttonimage,button_pressimage,font, blackimage

    buttonimage = gfw.image.load(gobj.res('ui_back.png'))
    button_pressimage = gfw.image.load(gobj.res('ui_back_pressed.png'))
    blackimage = gfw.image.load(gobj.res('black.png'))
    
    # Button(l, b, w, h, font, text, callback, btnClass=None):
    font = gfw.font.load(gobj.res('Tekton-Bold.otf'), 100)

    global select_sound, menu_swipe_sound
    select_sound = load_wav('res/wav/menu_enter.wav')
    menu_swipe_sound = load_wav('res/wav/menu_swipe.wav')

    global black_pos
    black_pos = canvas_width // 2, canvas_height + canvas_height // 2

    global start_check
    start_check = False

def enter():
    build_world()

def update():
    gfw.world.update()
    if start_check == True:
        fade_in_out()

def draw():
    gfw.world.draw()

    for i in range(2):
        button_pos = (canvas_width//2, canvas_height//2 - (250 * i))
        button_size = (500, 230)
        if i == index:
            button_pressimage.draw(*button_pos, *button_size)
        else:
            buttonimage.draw(*button_pos, *button_size)

        font_pos = (canvas_width//2 - 150 + (50 * i), canvas_height//2 - (250 * i))
        if i == 0:
            font.draw(*font_pos, "START")
        else:
            font.draw(*font_pos, "EXIT")

    blackimage.draw(*black_pos, canvas_width, canvas_height)

def handle_event(e):
    # prev_dx = boy.dx
    global index, start_check

    if e.type == SDL_QUIT:
        return gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            return gfw.pop()
        elif e.key == SDLK_UP:
            menu_swipe_sound.play()
            index += 1
            index = index % 2
        elif e.key == SDLK_DOWN:
            menu_swipe_sound.play()
            index += 1
            index = index % 2
        elif e.key == SDLK_a:
            select_sound.play()
            if index == 1:
                return gfw.pop()
            else:
                start_check = True

def exit():
    print("menu_state exits")
    pass

def pause():
    pass

def resume():
    build_world()

def fade_in_out():
    global black_pos
    b_x, b_y = black_pos
    
    if b_y > canvas_height // 2:
        b_y -= 1
    else:
        gfw.push(main_state)

    black_pos = b_x,b_y

if __name__ == '__main__':
    gfw.run_main()



