import os
import subprocess
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import time

root = Tk()
root.geometry('500x300')
root.title("Batch Python actions executor in Blender")
progress_var = DoubleVar()
progressbar = ttk.Progressbar(root, variable=progress_var, length=490, maximum=100)
progressbar.place(x=5, y=280)
progressbar.step(0)
style = ttk.Style()
style.theme_use("alt")
style.configure("Convert.TButton", foreground="white", background="#1EA7DF")
style.configure("Blender.TButton", foreground="white", background="#FFA800")
style.configure("Folder.TButton", foreground="white", background="#55006D")
style.configure("Actions.TButton", foreground="white", background="#323232")

blender_instance = ""
selected_dir = ""
actions_file = ""
converted_files = 0


def select_blender_exe():
    global blender_instance
    blender_instance = askopenfilename(initialdir="C:/Program Files")
    blend_exe_txt_box.configure(state='normal')
    blend_exe_txt_box.insert(END, blender_instance)
    blend_exe_txt_box.configure(state='disabled')
    if selected_dir:
        convert_btn.config(state=NORMAL)


def select_input_dir():
    global selected_dir
    selected_dir = askdirectory(title='Select Folder With .blend Files')
    sel_inpt_fold_txt_box.configure(state='normal')
    sel_inpt_fold_txt_box.insert(END, selected_dir)
    sel_inpt_fold_txt_box.configure(state='disabled')
    if blender_instance:
        convert_btn.config(state=NORMAL)


def select_actions_file():
    global actions_file
    actions_file = askopenfilename(initialdir="./actions")

    if actions_file:
        btn3.configure(text=os.path.basename(actions_file))
        convert_btn.config(state=NORMAL)


def convert_to_gltf():
    files = os.listdir(selected_dir)

    filtered_files = []

    for f in files:
        extension = os.path.splitext(f)[1]
        if extension == ".blend":
            filtered_files.append(f)

    for file in filtered_files:
        file_path = os.path.join(selected_dir, file)
        subprocess.call([blender_instance, "-b", file_path, "--python", actions_file])
        global converted_files
        converted_files += 1
        processed_percent = (converted_files * 100) / len(filtered_files)
        progress_var.set(processed_percent)
        time.sleep(0.02)
        root.update_idletasks()


btn = Button(root, text='Select Blender .exe', command=lambda: select_blender_exe(), style="Blender.TButton", padding=5)
btn2 = Button(root, text='Select Input Folder', command=lambda: select_input_dir(), style="Folder.TButton", padding=5)
btn3 = Button(root, text='Select Actions', command=lambda: select_actions_file(), width=200,
              style="Actions.TButton", padding=5)
convert_btn = Button(root, text='Convert Files', command=lambda: convert_to_gltf(), width=225, style="Convert.TButton",
                     padding=5)
blend_exe_lbl = Label(text="Selected Blender executable file:")
sel_inpt_fold_lbl = Label(text="Selected input folder:")
blend_exe_txt_box = Text(root, height=3,
                         width=100,
                         bg="light grey")
sel_inpt_fold_txt_box = Text(root, height=3,
                             width=100,
                             bg="light grey")

blend_exe_lbl.pack()
blend_exe_txt_box.pack()
sel_inpt_fold_lbl.pack()
sel_inpt_fold_txt_box.pack()
btn.pack(side=LEFT, pady=5, padx=20)
btn2.pack(side=RIGHT, pady=5, padx=20)
btn3.pack(side=TOP, pady=5, padx=20)
convert_btn.pack(side=BOTTOM, pady=25)

if not blender_instance and not selected_dir and not actions_file:
    convert_btn.config(state=DISABLED)
else:
    convert_btn.config(state=NORMAL)
mainloop()
