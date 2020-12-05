import pickle
from pico2d import *
import gobj
import time
import gfw

FILENAME = 'data.pickle'
scores = []
MAX_SCORE_COUNT = 5
last_rank = -1

backimage = None

class Entry:
    def __init__(self, score):
        self.score = score
        self.time = time.time()

def load():
    global font, image, backimage
    font = gfw.font.load(gobj.res('Tekton-Bold.otf'), 40)

    backimage = gfw.image.load(gobj.res('ui_back.png'))
    global scores
    try:
        f = open(FILENAME, "rb")
        scores = pickle.load(f)
        f.close()
        # print("Scores:", scores)
    except:
        print("No highscore file")

def save():
    f = open(FILENAME, "wb")
    pickle.dump(scores, f)
    f.close()

def add(score):
    global scores, last_rank
    entry = Entry(score)
    inserted = False
    for i in range(len(scores)):
        e = scores[i]
        if e.score < entry.score:
            scores.insert(i, entry)
            inserted = True
            last_rank = i + 1
            break
    if not inserted:
        scores.append(entry)
        last_rank = len(scores)

    if (len(scores) > MAX_SCORE_COUNT):
        scores.pop(-1)
    if last_rank <= MAX_SCORE_COUNT:
        save()

def draw():
    global font, last_rank
    no = 1
    y = 250
    backimage.draw(450, 150, 1050,350)
    for e in scores:
        str = "{:2d} {:7.0f}".format(no, e.score)
        color = (255, 255, 128) if no == last_rank else (0, 0, 0)
        font.draw(70, y, str, color)
        font.draw(320, y, time.asctime(time.localtime(e.time)), color)
        y -= 50
        no += 1



def update():
    pass
