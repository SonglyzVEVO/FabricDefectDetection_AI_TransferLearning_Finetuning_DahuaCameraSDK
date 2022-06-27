from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

# import camera_control
import camera_control_DeeplearningEmbeded

#x = camera_control.ThreadCamera()
x = camera_control_DeeplearningEmbeded.ThreadCamera_ver2()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def info_button():
    messagebox.showinfo("Info",
                        "Textile industrials in Thailand have a total value proportion of approximately 2.2 % from all products. We are therefore interested and aware of the benefits of replacing automation in the fabric inspection process which was originally used humans for inspection and often have an error. This research designed and search for making fabric defect detecting systems.")


def start_button():
    print("test_start")
    x.start_program()


def stop_button():
    print("test_stop")
    x.stop_program()


window = Tk()
window.geometry("551x487")
window.configure(bg="#C4C4C4")

canvas = Canvas(
    window,
    bg="#C4C4C4",
    height=487,
    width=551,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

# info button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: info_button(),
    relief="flat"
)
button_1.place(
    x=355.0,
    y=385.0,
    width=120.0,
    height=60.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: stop_button(),
    relief="flat"
)
button_2.place(
    x=223.0,
    y=385.0,
    width=120.0,
    height=60.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: start_button(),
    relief="flat"
)
button_3.place(
    x=91.0,
    y=385.0,
    width=120.0,
    height=60.0
)

canvas.create_rectangle(
    57.1036376953125,
    104.21800231933594,
    507.92181396484375,
    347.7179870605469,
    fill="#E5D64B",
    outline="")

canvas.create_text(
    73.0,
    122.0,
    anchor="nw",
    text="Welcome to Fabric Detection program.\nAll you have to do is connecting a Daheng\ncolor camera to your pc and press start.\nIf you want to stop program,press stop \nthen close the program to stop its progress\nand open again.",
    fill="#000000",
    font=("UbuntuMono Regular", 21 * -1)
)

canvas.create_text(
    57.1036376953125,
    50.64801025390625,
    anchor="nw",
    text="Fabric Inspection System\n",
    fill="#000000",
    font=("UbuntuMono Regular", 36 * -1)
)
window.resizable(False, False)
window.mainloop()
