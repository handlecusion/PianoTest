from bangtal import *
from pynput.keyboard import Listener, Key, KeyCode
import winsound as ws
import threading
import time

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

pos_musicpaper_1 = 300
pos_musicpaper_2 = 500

mode = 0
#0은 메인메뉴, 1은 자유모드, 2는 곰세마리

class Note:
    def __init__(self, position, length, line, pitch):
        self.position = position
        self.length = length
        self.line = line
        self.posx = 0
        self.posy = 0
        self.source = 'Images/note/note_'
        
        self.posy += pitch * 10
        self.posx += 150 + position * 40 + position // 8 * 40
        if length == 1:
            self.source += '1'
            if pitch >= 12 or pitch <= 0:
                self.source += '_line'
            self.posy += 50
        elif length == 2:
            if pitch >= 12:
                self.source += 'up_2_line'
                self.posy -= 40
            elif pitch >= 7:
                self.source += 'up_2'
                self.posy -= 40
            elif pitch <= 0:
                self.source += 'down_2_line'
                self.posy += 20
            else:
                self.source += 'down_2'
                self.posy += 20
        elif length == 4:
            if pitch >= 12:
                self.source += 'up_4_line'
                self.posy -= 40
            elif pitch >= 7:
                self.source += 'up_4'
                self.posy -= 40
            elif pitch <= 0:
                self.source += 'down_4_line'
                self.posy += 20
            else:
                self.source += 'down_4'
                self.posy += 20
        elif length == 8:
            if pitch >= 7:
                self.source += 'up_8'
                self.posy -= 40
            if pitch >= 12:
                self.source += 'up_8_line'
                self.posy -= 40
            elif pitch <= 0:
                self.source += 'down_8_line'
                self.posy += 20
            else:
                self.source += 'down_8'
                self.posy += 20
        else:
            showMessage("error in create object")

        if line == 1:
            self.posy += pos_musicpaper_1
            self.source += '.png'
        elif line ==2:
            self.posy += pos_musicpaper_2
            self.source += '_gray.png'
        
        self.note = Object(self.source)
        if mode == 1:
            self.note.locate(scene_free, self.posx, self.posy)
        elif mode == 2:
            self.note.locate(scene_main, self.posx, self.posy)
        self.note.show()

    def hide(self):
        self.note.hide()

    def getLine(self):
        return self.line

    def __del__(self):
        #pass
        self.note.hide()


def barpos2pos(bar, pos):
    result = bar * 8 + pos
    line = bar//3
    return result, line

class MusicPaper:
    def __init__(self, list):
        self.note = []
        self.progress = 0
        self.now_play_index = 4
        self.now_play_line = 0
        self.list = list
        for n in self.list:
            self.note.append(Note((n[0]*8 + n[1]) % 24, n[2], n[0]//3 + 1, n[3]))


    def played(self):
        self.now_play_index += 1
        if self.note[self.now_play_index].getLine() == self.now_play_line + 1:
            self.now_play_line += 1
            self.note.clear()
            for n in self.list:
                self.note.append(Note((n[0]*8 + n[1]) % 24, n[2], n[0]//3 + 1 - self.now_play_line, n[3]))


def sound_onCompleted(object):
    print(object)
      
class SoundPiano:
    def __init__(self, src):
        self.sound = Sound(src)
        self.bool_play = False

    def is_play(self):
        return self.play
    
    def play(self):
        self.sound.play()
        self.bool_play = True
        return

    def stop(self):
        self.sound.stop()
        self.bool_play = False
        return

class SoundBeep:
    def __init__(self, pitch):
        self.freq = 0
        self.dur = 500
        if pitch == 0:
            self.freq = 261
        elif pitch == 1:
            self.freq = 293
        elif pitch == 2:
            self.freq = 329
        elif pitch == 3:
            self.freq = 349
        elif pitch == 4:
            self.freq = 391
        elif pitch == 5:
            self.freq = 440
        elif pitch == 6:
            self.freq = 493
        else:
            self.freq = 523

    def play(self):
        ws.Beep(self.freq, self.dur)



scene_main = Scene("note", "Images/background/background_white.png")
scene_menu = Scene("menu", "Images/background/background_white.png")
scene_free = Scene("free", "Images/background/background_white.png")

button_free = Object("Images/button/freemode_white.png")
button_free.locate(scene_menu, 350, 400)
button_free.show()

button_threebear = Object("Images/button/threebear_white.png")
button_threebear.locate(scene_menu, 350, 200)
button_threebear.show()

music_paper_free = Object("Images/note/music_paper.png")
music_paper_free.locate(scene_free, 0, pos_musicpaper_1)
music_paper_free.show()



music_paper_2 = Object("Images/note/music_paper_gray.png")
music_paper_2.locate(scene_main, 0, pos_musicpaper_2)
music_paper_2.show()

music_paper_1 = Object("Images/note/music_paper.png")
music_paper_1.locate(scene_main, 0, pos_musicpaper_1)
music_paper_1.show()

sound = [
    SoundPiano('Sounds/sound1.mp3'),
    SoundPiano('Sounds/sound2.mp3'),
    SoundPiano('Sounds/sound3.mp3'),
    SoundPiano('Sounds/sound4.mp3'),
    SoundPiano('Sounds/sound5.mp3'),
    SoundPiano('Sounds/sound6.mp3'),
    SoundPiano('Sounds/sound7.mp3'),
    SoundPiano('Sounds/sound8.mp3'),

]

previus = KeyCode(char='0')
freenote = []
free_pos = 0
free_length = 4
free_line = 1

def handlePress(key):
    global previus
    global mode
    global free_pos
    if previus == key:
        return
    print( 'Press: {}'.format( key ) )
    if mode == 0:
        print("in if mode == 0")
        return
    elif mode == 1:
        print("in handlepress elif mode == 1")
        if key == KeyCode(char='a'):
            print("in if key == keycode")
            sound[0].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 0))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char='a')
        elif key == KeyCode(char='s'):
            sound[1].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 1))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char='s')
        elif key == KeyCode(char='d'):
            sound[2].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 2))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char='d')
        elif key == KeyCode(char='f'):
            sound[3].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 3))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char='f')
        elif key == KeyCode(char='j'):
            sound[4].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 4))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char='j')
        elif key == KeyCode(char='k'):
            sound[5].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 5))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char='k')
        elif key == KeyCode(char='l'):
            sound[6].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 6))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char='l')
        elif key == KeyCode(char=';'):
            sound[7].play()
            if free_pos < 24:
                freenote.append(Note(free_pos, free_length, free_line, 7))
            else:
                freenote.clear()
                free_pos = 0
                freenote.append(Note(free_pos, free_length, free_line, 0))
            previus = KeyCode(char=';')
        else:
            return
        free_pos += 2
    elif mode == 2:
        pass
    
    
def handleRelease(key):
    global previus
    print( 'Released: {}'.format( key ) )
    
    if key == KeyCode(char='a'):
        sound[0].stop()
    elif key == KeyCode(char='s'):
        sound[1].stop()
    elif key == KeyCode(char='d'):
        sound[2].stop()
    elif key == KeyCode(char='f'):
        sound[3].stop()
    elif key == KeyCode(char='j'):
        sound[4].stop()
    elif key == KeyCode(char='k'):
        sound[5].stop()
    elif key == KeyCode(char='l'):
        sound[6].stop()
    elif key == KeyCode(char=';'):
        sound[7].stop()
    else:
        return
    previus = KeyCode(char='0')


def get_current_key():
    with Listener(on_press = handlePress, on_release = handleRelease) as listener:
         listener.join()

class ThreadIO:
    def __init__(self):
        self.t = threading.Thread(target = get_current_key)
        self.t.start()

    def __del__(self):
        self.t._stop()

t = ThreadIO()



button_bug = Object('Images/button/bug.png')
button_bug.locate(scene_main, 400, 150)
button_bug.show()

button_return = Object('Images/button/button_return.png')
button_return.setScale(0.25)
button_return.locate(scene_main, 1100, 100)
button_return.show()

button_bug_free = Object('Images/button/bug.png')
button_bug_free.locate(scene_free, 400, 150)
button_bug_free.show()

button_return_free = Object("images/button/button_return.png")
button_return_free.setScale(0.25)
button_return_free.locate(scene_free, 1100, 100)
button_return_free.show()

def button_bug_onMouseAction(x, y, action):
    
    global t
    if action == MouseAction.CLICK:
        try:
            del t
        except:
            print("cant del threadIO")
        t = ThreadIO()
   
        
def button_free_onMouseAction(x, y, action):
    global mode
    mode = 1
    startGame(scene_free)
    
button_free.onMouseAction = button_free_onMouseAction

def button_threebear_onMouseAction(x, y, action):
    global mode
    mode = 2
    arr = [
    [0, 0, 4, 0], [0, 2, 8, 0], [0, 3, 8, 0], [0, 4, 4, 0], [0, 6, 4, 0],
    [1, 0, 4, 2], [1, 2, 8, 4], [1, 3, 8, 4], [1, 4, 4, 2], [1, 6, 4, 0],
    [2, 0, 8, 4], [2, 1, 8, 4], [2, 2, 4, 2], [2, 4, 8, 4], [2, 5, 8, 4], [2, 6, 4, 2],
    [3, 0, 4, 0], [3, 2, 4, 0], [3, 4, 2, 0],
    [4, 0, 4, 4], [4, 2, 4, 4], [4, 4, 4, 2], [4, 6, 4, 0],
    [5, 0, 4, 4], [5, 2, 4, 4], [5, 4, 2, 4],
    [6, 0, 4, 4], [6, 2, 4, 4], [6, 4, 4, 2], [6, 6, 4, 0],
    [7, 0, 4, 4], [7, 2, 4, 4], [7, 4, 2, 4],
    [8, 0, 4, 4], [8, 2, 4, 4], [8, 4, 4, 2], [8, 6, 4, 0],
    [9, 0, 8, 4], [9, 1, 8, 4], [9, 2, 8, 4], [9, 3, 8, 5], [9, 4, 2, 4],
    [10, 0, 4, 7], [10, 2, 4, 4], [10, 4, 4, 7], [10, 6, 4, 4],
    [11, 0, 4, 2], [11, 2, 4, 1], [11, 4, 2, 0]
]

    musicpaper = MusicPaper(arr)
    startGame(scene_main)
    global t

button_threebear.onMouseAction = button_threebear_onMouseAction

button_bug.onMouseAction = button_bug_onMouseAction
button_bug_free.onMouseAction = button_bug_onMouseAction

def button_return_onMouseAction(x, y, action):
    global mode
    mode = 0
    startGame(scene_menu)

button_return.onMouseAction = button_return_onMouseAction
button_return_free.onMouseAction = button_return_onMouseAction

startGame(scene_menu)



