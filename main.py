import tkinter
import winsound

from func import seconds_to_ftime, create_db, write_db, read_db, today_pomodoro


# create 'pomodoro' table
create_db()

root = tkinter.Tk()
root.title('Timer')
root.geometry('300x300')
root.attributes('-topmost', False)


# dict of timer's mode
MODES = {'pomodoro': 1500,
         'short break': 300,
         'long break': 900}

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
        mode_button.configure(text=MODE)


# function of timer
def timer():
    global SECONDS, MODE, STATUS_TIMER, POMODORO
    if not STATUS_TIMER:
        return
    if SECONDS == 0:
        # sound
        winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        STATUS_TIMER = 1
        if MODE == 'pomodoro':
            POMODORO += 1
            # write 1 pomodoro to db
            count_pomodoro = write_db()
            # update label of pomodoros
            pomodoro_label.configure(text=f'pomodoros: {count_pomodoro}')
            if POMODORO % 4 == 0:
                MODE = 'long break'
            else:
                MODE = 'short break'
            mode_button.configure(text=MODE)
            SECONDS = MODES[MODE]

            # break timer after pomodoro
            STATUS_TIMER = 2
            # app window zommed
            root.state('zoom')
            # app window over all other windows
            root.attributes('-topmost', True)
            timer()
        elif MODE in ('short break', 'long break'):
            MODE = 'pomodoro'
            mode_button.configure(text=MODE)
            SECONDS = MODES[MODE]
            time_label.configure(text=seconds_to_ftime(SECONDS))
            # app window return to normal
            root.attributes('-topmost', False)
            # return to normal size of window
            root.state('normal')
        return
    SECONDS -= 1
    time_label.configure(text=seconds_to_ftime(SECONDS))
    root.after(1000, timer)


# function for stop timer
def stop():
    global STATUS_TIMER
    STATUS_TIMER = 0
    start_stop_button.configure(text='Start', command=start)


# function for start timer
def start():
    global STATUS_TIMER
    STATUS_TIMER = 2
    start_stop_button.configure(text='Stop', command=stop)
    timer()


time_label = tkinter.Label(root, fg='green', font=('Helvetica', 15),
                           text=seconds_to_ftime(SECONDS))
time_label.pack()

start_stop_button = tkinter.Button(root, text='Start', command=start)
start_stop_button.pack()

mode_button = tkinter.Button(text=MODE, command=mode)
mode_button.pack()

pomodoro_label = tkinter.Label(root, fg='red', font=('Helvetica', 15),
                               text=f'pomodoros: {today_pomodoro()}')
pomodoro_label.pack()

root.mainloop()
