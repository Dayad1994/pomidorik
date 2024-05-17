'''
Convert .py to .exe:

pip install Pyinstaller
pyinstaller --onefile -w simple.py

where -w  - without consol

'''
from tkinter import Button, Label, Frame, Tk, RIGHT, BOTH
from winsound import PlaySound, SND_FILENAME


# main vars
MODES = {'pomodoro': 1500, 'short break': 300, 'long break': 900}  # timers
CUR_MODE = 'pomodoro'  # current mode of timer
SECONDS = MODES[CUR_MODE]  # current count of timer's seconds
STATUS_TIMER = 1  # 0 - start; 1 - stop; 2 - running
POMODORO = 0  # the number of finished pomodoro

# main window
window = Tk()
window.overrideredirect(True)  # title bar off
scr_width = window.winfo_screenwidth() - 150
scr_height = window.winfo_screenheight() - 250
window.geometry(f'{150}x{150}+{scr_width}+{scr_height}')
window.attributes('-topmost', True,
                  '-alpha', 0.5)  # above all windows and transparency
window.config(bg='black')


def get_pos(event):
    '''moving a window by clicking on lmb in title bar'''
    x_win = window.winfo_x()
    y_win = window.winfo_y()
    start_x = event.x_root
    start_y = event.y_root

    y_win = y_win - start_y
    x_win = x_win - start_x

    def move_window(event):
        window_x = window.winfo_width()
        window_y = window.winfo_height()
        window.geometry(f"{window_x}x{window_y}" + '+{0}+{1}'.format(
            event.x_root + x_win, event.y_root + y_win))

    window.bind('<B1-Motion>', move_window)


def seconds_to_ftime(seconds):
    '''format seconds to timestring'''
    m = str(seconds // 60).rjust(2, "0")
    s = str(seconds % 60).rjust(2, "0")
    ftime = f'{m}:{s}'
    return ftime


def mode():
    '''change current mode of timer - MODE'''
    global SECONDS, CUR_MODE
    if STATUS_TIMER < 2:
        if CUR_MODE == 'pomodoro':
            CUR_MODE = 'short break'
        elif CUR_MODE == 'short break':
            CUR_MODE = 'long break'
        else:
            CUR_MODE = 'pomodoro'
        SECONDS = MODES[CUR_MODE]
        time_lbl.configure(text=seconds_to_ftime(SECONDS))
        mode_btn.configure(text=CUR_MODE)


def timer():
    '''timer'''
    global SECONDS, CUR_MODE, STATUS_TIMER, POMODORO
    if not STATUS_TIMER:
        return
    if SECONDS == 0:
        PlaySound('sound.wav', SND_FILENAME)
        STATUS_TIMER = 1
        if CUR_MODE == 'pomodoro':
            POMODORO += 1
            # after 4 pomodoro - long break
            CUR_MODE = 'long break' if POMODORO % 4 == 0 else 'short break'
            SECONDS = MODES[CUR_MODE]

            pomodoro_lbl.configure(text=f'pomodoros: {POMODORO}')
            mode_btn.configure(text=CUR_MODE)
            window.state('zoom')  # window zommed

            STATUS_TIMER = 2
            timer()  # break timer after pomodoro
        elif CUR_MODE in ('short break', 'long break'):
            CUR_MODE = 'pomodoro'
            SECONDS = MODES[CUR_MODE]

            mode_btn.configure(text=CUR_MODE)
            start_stop_btn.configure(text='Start', command=stop, fg='green')
            time_lbl.configure(text=seconds_to_ftime(SECONDS))
    else:
        SECONDS -= 1
        time_lbl.configure(text=seconds_to_ftime(SECONDS))
        window.after(1000, timer)


def stop():
    '''stop timer'''
    global STATUS_TIMER
    STATUS_TIMER = 0
    start_stop_btn.configure(text='Start', command=start, fg='green')


def start():
    window.state('normal')  # return to normal size of window
    '''start timer'''
    global STATUS_TIMER
    STATUS_TIMER = 2
    start_stop_btn.configure(text='Stop', command=stop, fg='red')
    timer()


# new title bar
title_bar = Frame(window, bg='black')
title_bar.pack(fill=BOTH)
title_bar.bind('<Button-1>', get_pos)

# labels, buttons
close_btn = Button(title_bar, text='X', command=window.destroy, fg='red',
                   bg='black', activebackground='red', borderwidth=0,
                   activeforeground='black')
time_lbl = Label(window, bg='black', font=('Helvetica', 15), fg='green',
                 text=seconds_to_ftime(SECONDS))
start_stop_btn = Button(window, bg='black', fg='green', text='Start',
                        command=start)
mode_btn = Button(bg='black', fg='green', text=CUR_MODE, command=mode)
pomodoro_lbl = Label(window, bg='black', font=('Helvetica', 15), fg='green',
                     text=f'pomodoro: {POMODORO}')
close_btn.pack(side=RIGHT)
time_lbl.pack()
start_stop_btn.pack()
mode_btn.pack()
pomodoro_lbl.pack()

window.mainloop()
