#Text Editor

import tkinter as tk
from tkinter import filedialog,messagebox
from tkinter.scrolledtext import ScrolledText

#Global varible to track currently opended file
current_file = None

#file operations
def new_file(event=None):
    global current_file
    if text_area.edit_modified():
        if not confirm_save_changes():
            return
        text_area.delete(1.0,tk.END)
        current_file = None
        root.title("Untitled - Text Editor")
        status_bar.config(text="New File Created")

def open_file(event=None):
    global current_file
    file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Document","*.txt")])
    if file:
        if text_area.edit_modified():
            if not confirm_save_changes():
                return
        text_area.delete(1.0,tk.END)
        with open(file,"r") as f:
            text_area.insert(tk.END,f.read())
        current_file=file
        root.title(f"{file} - Text Editor")
        status_bar.config(text=f"Opended: {file}")

def save_file(event=None):
    global current_file
    if current_file:
        with open(current_file,'w') as f:
            f.write(text_area.get(1.0,tk.END))
        status_bar.config(text=f"Saved: {current_file}")
    else:
        save_as()

def save_as():
    global current_file
    file = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Document","*.txt")])
    if file:
        with open(file,"w") as f:
            f.write(text_area.get(1.0,tk.END))
        root.title(f"{file} - Text Editor")
        status_bar.config(text=f"Saved As: {file}")

def exit_app():
    if text_area.edit_modified():
        if not confirm_save_changes():
            return
    if messagebox.askokcancel("Exit","Do you want to quit"):
        root.destroy()

def confirm_save_changes():
    result = messagebox.askyesnocancel("Save Changes","Do you want to save changes?")
    if result:
        save_file()
        return True
    elif result is None:
        return False
    else:
        return True

#GUI setup

root = tk.Tk()
root.title("Text Editor")
root.geometry("700x500")

text_area=ScrolledText(root,wrap=tk.WORD,font=("Arial",12),undo=True)
text_area.pack(fill=tk.BOTH,expand=1)

#Menu Bar
menu_bar = tk.Menu(root)

#File Menu
file_menu = tk.Menu(menu_bar,tearoff=0)
file_menu.add_command(label="New",accelerator="Ctrl+N",command=new_file)
file_menu.add_command(label="Open",accelerator="Ctrl+O",command=open_file)
file_menu.add_command(label="Save",accelerator="Ctrl+S",command=save_file)
file_menu.add_command(label="Save As",command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=exit_app)

menu_bar.add_cascade(label="File",menu=file_menu)

#Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=text_area.edit_undo)
edit_menu.add_command(label="Redo", command=text_area.edit_redo)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)

#Status Bar
status_bar = tk.Label(root,text="Ready",anchor='w')
status_bar.pack(side=tk.BOTTOM,fill=tk.X)

#Keyboard Shortcuts
root.bind("<Control-n>", new_file)
root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)

#main loop
root.mainloop()


