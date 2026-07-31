from matplotlib import animation
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt

def make_bw_anim(frame_gen_func, num_frames):
#    fig,ax = plt.subplots()
    data = frame_gen_func(0)
    H = len(data)
    W = len(data[0])
    fig, ax = plt.subplots(figsize=(12, 12 * (H / W)), facecolor='black', frameon=True)
    ax.set_axis_off()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
    h = ax.imshow(data, vmin=0, vmax=1, cmap=get_cmap('binary').reversed())
    plt.close()

    def make_frame(n):
        data = frame_gen_func(n)
        h.set_data(data)
        return [h]

    return animation.FuncAnimation(fig, make_frame,
                                   frames=num_frames,
                                   blit=True)

from threading import Event, Thread
from ipywidgets import Label, HTML, Button, HBox


def canvas_animation(canvas, steps, callback, interval = 0.2):
    stopped = Event()
    step = 0
    max_step = steps -1
    reverse = False
    progression = 1
    rng = range(steps)
    stopped.set()

    def update(new_step):
        nonlocal step
        step = max(0, min(new_step, max_step))

        if stopped.isSet():
            callback(canvas, step)

    def start():
        stopped.clear()
        Thread(target=loop).start()

    def loop():
        nonlocal step

        while not stopped.wait(interval):  # the first call is in `interval` secs
            callback(canvas, step)

            if step + progression in rng:
                step += progression
            else:
                stop()


    start()  # Start it by default

    def play_pause(btn=None):
        nonlocal step, progression

        if stopped.isSet() or progression != 1:
            need_start = stopped.isSet()
            play_btn.icon = "pause lg"
            progression = 1

            if step == max_step:
                step = 0

            if need_start:
                start()
        else:
            stop()

    play_btn = Button(icon="pause lg")
    play_btn.on_click(play_pause)

    def backward_pause(btn=None):
        nonlocal step, progression

        if stopped.isSet() or progression != -1:
            need_start = stopped.isSet()
            backward_btn.icon = "pause  lg"
            progression = -1

            if step == 0:
                step = max_step

            if need_start:
                start()
        else:
            stop()

    backward_btn = Button(icon="backward lg")
    backward_btn.on_click(backward_pause)


    def stop_and_update(new_step):
        stop()
        update(new_step)

    def stop():
        if not stopped.isSet():
            stopped.set()
            play_btn.icon = "play lg"
            backward_btn.icon = "backward lg"


    first_btn = Button(icon="fast-backward lg")
    first_btn.on_click(lambda btn: update(0))


    last_btn = Button(icon="fast-forward lg")
    last_btn.on_click(lambda btn: update(max_step))


    next_btn = Button(icon="step-forward lg")
    next_btn.on_click(lambda btn: stop_and_update(step + 1))

    prev_btn = Button(icon="step-backward lg")
    prev_btn.on_click(lambda btn: stop_and_update(step - 1))

        # icons are fontawesome icons
        # can also include classes like
        # spin, pulse,
        # lg, 2x, 3x, 3x, 4x, 5x
        # rotate-90, flip-horizontal
        # inverse
        # https://fontawesome.com/v4/examples/#animated
#    gear_btn = Button(icon="gear spin")


    display(canvas, HBox([first_btn, prev_btn, backward_btn, play_btn, next_btn, last_btn]))

