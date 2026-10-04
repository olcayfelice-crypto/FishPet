import tkinter as tk
import random
import math
import subprocess
import threading
import urllib.request
import webbrowser

WIDTH = 220
HEIGHT = 150

root = tk.Tk()
root.title("FishPet")
root.geometry(f"{WIDTH}x{HEIGHT}+300+300")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg="magenta")
root.wm_attributes("-transparentcolor", "magenta")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="magenta",
    highlightthickness=0
)
canvas.pack()

fish_x = 110
fish_y = 75
direction = 1
speed = 2
bubble_timer = 0
dragging = False
drag_offset_x = 0
drag_offset_y = 0

body = None
tail = None
eye = None
fin = None
bubble = None


def draw_fish():
    global body, tail, eye, fin

    canvas.delete("fish")

    body = canvas.create_oval(
        fish_x - 45,
        fish_y - 25,
        fish_x + 45,
        fish_y + 25,
        fill="orange",
        outline="black",
        width=2,
        tags="fish"
    )

    if direction == 1:
        tail = canvas.create_polygon(
            fish_x - 40, fish_y,
            fish_x - 70, fish_y - 25,
            fish_x - 70, fish_y + 25,
            fill="orange",
            outline="black",
            tags="fish"
        )

        eye = canvas.create_oval(
            fish_x + 20,
            fish_y - 12,
            fish_x + 30,
            fish_y - 2,
            fill="black",
            tags="fish"
        )

        fin = canvas.create_polygon(
            fish_x - 5, fish_y + 15,
            fish_x + 10, fish_y + 38,
            fish_x + 25, fish_y + 15,
            fill="gold",
            outline="black",
            tags="fish"
        )

    else:
        tail = canvas.create_polygon(
            fish_x + 40, fish_y,
            fish_x + 70, fish_y - 25,
            fish_x + 70, fish_y + 25,
            fill="orange",
            outline="black",
            tags="fish"
        )

        eye = canvas.create_oval(
            fish_x - 30,
            fish_y - 12,
            fish_x - 20,
            fish_y - 2,
            fill="black",
            tags="fish"
        )

        fin = canvas.create_polygon(
            fish_x - 25, fish_y + 15,
            fish_x - 10, fish_y + 38,
            fish_x + 5, fish_y + 15,
            fill="gold",
            outline="black",
            tags="fish"
        )


def move_fish():
    global fish_x, fish_y, direction

    if not dragging:
        fish_x += speed * direction

        fish_y += math.sin(fish_x / 35) * 0.8

        if fish_x > WIDTH - 70:
            direction = -1

        if fish_x < 70:
            direction = 1

        draw_fish()

    root.after(30, move_fish)


def make_bubble():
    x = fish_x + random.randint(-20, 20)
    y = fish_y - 25

    b = canvas.create_oval(
        x,
        y,
        x + 7,
        y + 7,
        outline="white",
        width=2
    )

    def rise(pos=0):
        if pos < 35:
            canvas.move(b, random.choice([-1, 0, 1]), -2)
            root.after(50, lambda: rise(pos + 1))
        else:
            canvas.delete(b)

    rise()


def bubble_loop():
    make_bubble()
    root.after(random.randint(1200, 2500), bubble_loop)


def speak(text):
    def run():
        safe_text = text.replace("'", "''")

        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"""
            Add-Type -AssemblyName System.Speech;
            $s = New-Object System.Speech.Synthesis.SpeechSynthesizer;
            $s.Speak('{safe_text}');
            """
        ]

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    threading.Thread(target=run, daemon=True).start()


def internet_test():
    try:
        urllib.request.urlopen(
            "https://www.google.com",
            timeout=5
        )
        speak("İnternete bağlanabiliyorum.")
    except:
        speak("İnternet bağlantısı yok.")


def open_browser():
    webbrowser.open("https://www.google.com")


def mouse_down(event):
    global dragging, drag_offset_x, drag_offset_y

    dragging = True
    drag_offset_x = event.x
    drag_offset_y = event.y


def mouse_move(event):
    if dragging:
        x = root.winfo_x() + event.x - drag_offset_x
        y = root.winfo_y() + event.y - drag_offset_y
        root.geometry(f"+{x}+{y}")


def mouse_up(event):
    global dragging
    dragging = False


def show_menu(event):
    menu = tk.Menu(
        root,
        tearoff=0
    )

    menu.add_command(
        label="🐟 Merhaba!",
        command=lambda: speak("Merhaba! Ben senin balığın.")
    )

    menu.add_command(
        label="🗣️ Konuş",
        command=lambda: speak("Blup blup! Ben FishPet!")
    )

    menu.add_command(
        label="🌐 İnterneti kontrol et",
        command=internet_test
    )

    menu.add_command(
        label="🔎 Tarayıcıyı aç",
        command=open_browser
    )

    menu.add_separator()

    menu.add_command(
        label="❌ Çıkış",
        command=root.destroy
    )

    menu.tk_popup(
        event.x_root,
        event.y_root
    )


canvas.bind("<Button-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_move)
canvas.bind("<ButtonRelease-1>", mouse_up)
canvas.bind("<Button-3>", show_menu)

draw_fish()
move_fish()
bubble_loop()

root.after(
    1000,
    lambda: speak("Merhaba! Ben FishPet.")
)

root.mainloop()