from pico2d import *
import gfw
import gobj
import menu_state

canvas_width = menu_state.canvas_width
canvas_height = menu_state.canvas_height

def build_world():
    gfw.world.init(['bg', 'ui'])

    center = (canvas_width//2, canvas_height//2)
    bg = gobj.ImageObject('logo.png', center,canvas_width,canvas_height)
    gfw.world.add(gfw.layer.bg, bg)

    # Button(l, b, w, h, font, text, callback, btnClass=None):
    font = gfw.font.load(gobj.res('Tekton-Bold.otf'), 40)

    global lobby_sound, select_sound
    lobby_sound = load_wav('res/wav/lobbydrum.wav')
    lobby_sound.set_volume(20)
    lobby_sound.play()
    select_sound = load_wav('res/wav/menu_enter.wav')

def enter():
    build_world()

def update():
    gfw.world.update()

def draw():
    gfw.world.draw()
    
def handle_event(e):
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        return gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            return gfw.pop()
        elif e.key == SDLK_a:
            gfw.change(menu_state)

def exit():
    global lobby_sound, select_sound

    del lobby_sound
    del select_sound

def pause():
    pass

def resume():
    build_world()

if __name__ == '__main__':
    gfw.run_main()
