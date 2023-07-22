import tkinter

from func import seconds_to_ftime


root = tkinter.Tk()
root.title('Timer')
root.geometry('300x300')


# dict of timer's mode
MODES = {'pomodoro': 6,
         'short break': 5,
         'long break': 15}

# mode of timer
MODE = 'pomodoro'

# current count of timer's seconds
SECONDS = MODES[MODE]

# status of timer (0 - start; 1 - stop; 2 - running)
STATUS_TIMER = 1

# pomodoro
POMODORO = 0


# function for change timer's mode
def mode():
    global SECONDS, MODE
    if STATUS_TIMER < 2:
        if MODE == 'pomodoro':
            MODE = 'short break'
        elif MODE == 'short break':
            MODE = 'long break'
        else:
            MODE = 'pomodoro'
        SECONDS = MODES[MODE]
        time_label.configure(text=seconds_to_ftime(SECONDS))
        mode_label.configure(text=MODE)


# function of timer
def timer():
    global SECONDS, MODE, STATUS_TIMER, POMODORO
    if not STATUS_TIMER:
        return
    if SECONDS == 0:
        STATUS_TIMER = 1
        if MODE == 'pomodoro':
            POMODORO += 1
            pomodoro_label.configure(text=f'pomodoros: {POMODORO}')
            if POMODORO % 4 == 0:
                MODE = 'long break'
            else:
                MODE = 'short break'
            mode_label.configure(text=MODE)
            SECONDS = MODES[MODE]

            # break timer after pomodoro
            STATUS_TIMER = 2
            timer()
        elif MODE in ('short break', 'long break'):
            MODE = 'pomodoro'
            mode_label.configure(text=MODE)
            SECONDS = MODES[MODE]
            time_label.configure(text=seconds_to_ftime(SECONDS))
        return
    SECONDS -= 1
    time_label.configure(text=seconds_to_ftime(SECONDS))
    root.after(1000, timer)


# function for stop timer
def stop():
    global STATUS_TIMER
    STATUS_TIMER = 0


# function for start timer
def start():
    global STATUS_TIMER
    STATUS_TIMER = 2
    timer()


time_label = tkinter.Label(root, fg='green', font=('Helvetica', 15),
                           text=seconds_to_ftime(SECONDS))
time_label.pack()

start_button = tkinter.Button(root, text='Start', command=start)
start_button.pack()

stop_button = tkinter.Button(root, text='Stop', command=stop)
stop_button.pack()

mode_button = tkinter.Button(text='Mode', command=mode)
mode_button.pack()

mode_label = tkinter.Label(root, fg='green', font=('Helvetica', 15),
                           text=MODE)
mode_label.pack()

pomodoro_label = tkinter.Label(root, fg='red', font=('Helvetica', 15),
                               text=f'pomodoros: {POMODORO}')
pomodoro_label.pack()

root.mainloop()
