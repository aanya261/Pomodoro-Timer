
import tkinter as tk
from tkinter import messagebox
import winsound

root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry("500x550")
root.configure(bg="#707575")
root.resizable(False, False)

session = 0
break_time = 0
remaining = 0
mode = "SESSION"
running = False
after_id = None


def display():
    m, s = divmod(remaining, 60)
    timer.config(text=f"{m:02d}:{s:02d}")
    mode_label.config(text=mode)


def countdown():
    global remaining, running, after_id, mode

    after_id = None

    if not running:
        return

    if remaining > 0:
        remaining -= 1
        display()
        after_id = root.after(1000, countdown)
    else:
        running = False
        winsound.Beep(1000, 1000)
        messagebox.showinfo("Pomodoro", "Time is up!")

        mode = "BREAK" if mode == "SESSION" else "SESSION"
        remaining = break_time if mode == "BREAK" else session
        display()


def start():
    global running
    if remaining == 0:
        messagebox.showwarning("Timer", "Set your time first!")
    elif not running:
        running = True
        countdown()


def pause():
    global running, after_id
    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None


def reset():
    global remaining
    pause()
    remaining = session if mode == "SESSION" else break_time
    display()


def apply_time():
    global session, break_time, remaining

    try:
        sh, sm = int(session_h.get()), int(session_m.get())
        bh, bm = int(break_h.get()), int(break_m.get())

        if min(sh, sm, bh, bm) < 0 or sh*60+sm == 0 or bh*60+bm == 0:
            raise ValueError

        session = (sh*60 + sm) * 60
        break_time = (bh*60 + bm) * 60

        pause()
        remaining = session if mode == "SESSION" else break_time
        display()

    except ValueError:
        messagebox.showerror("Error", "Enter valid time values!")


# Heading
tk.Label(root, text="POMODORO TIMER",
         font=("Arial", 23, "bold"),
         bg="#707575", fg="white").pack(pady=22)

# Main box
card = tk.Frame(root, bg="#C5CECE", bd=2,
                relief="solid", padx=30, pady=25)
card.pack(padx=35, pady=5)

inner = tk.Frame(card, bg="white", bd=2,
                 relief="solid", padx=25, pady=15)
inner.pack()

mode_label = tk.Label(inner, text=mode,
                      font=("Arial", 13, "bold"), bg="white")
mode_label.pack()

timer = tk.Label(inner, text="00:00",
                 font=("Arial", 48, "bold"), bg="white")
timer.pack(pady=10)

# Buttons
buttons = tk.Frame(inner, bg="white")
buttons.pack()

tk.Button(buttons, text="Start", width=7,
          command=start).pack(side="left", padx=4)

tk.Button(buttons, text="Pause", width=7,
          command=pause).pack(side="left", padx=4)

tk.Button(buttons, text="Reset", width=7,
          command=reset).pack(side="left", padx=4)


# Setting boxes
settings = tk.Frame(card, bg="#C5CECE")
settings.pack(pady=25)


def setting_box(title):
    box = tk.Frame(settings, bg="#333333", padx=10, pady=10)
    tk.Label(box, text=title, bg="#333333",
             fg="white", font=("Arial", 12, "bold")).pack()
    fields = tk.Frame(box, bg="#333333")
    fields.pack(pady=8)
    return box, fields


def time_input(parent):
    h = tk.Entry(parent, width=4, justify="center")
    h.insert(0, "00")
    h.pack(side="left")

    tk.Label(parent, text="H", bg="#333333",
             fg="white").pack(side="left")

    m = tk.Entry(parent, width=4, justify="center")
    m.insert(0, "00")
    m.pack(side="left")

    tk.Label(parent, text="M", bg="#333333",
             fg="white").pack(side="left")

    return h, m


# Session
box1, fields1 = setting_box("Session Length")
box1.pack(side="left", padx=8)
session_h, session_m = time_input(fields1)

# Break
box2, fields2 = setting_box("Break Length")
box2.pack(side="left", padx=8)
break_h, break_m = time_input(fields2)

tk.Button(card, text="Apply Settings",
          font=("Arial", 11, "bold"),
          command=apply_time).pack()

display()
root.mainloop()
