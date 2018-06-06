import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()
root.title('PriEditor')
root.geometry('400x300')

#ラベル
label1 = tk.Label(text='フォルダを選択してください')
label1.pack()

dir_entry = tk.Entry()
dir_entry.insert(tk.END,'./movies')
dir_entry.pack()

def select_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    dir = tk.filedialog.askdirectory(initialdir = iDir)
    dir_entry.delete(0, tk.END)
    dir_entry.insert(tk.END, dir)

dir_entry_button = tk.Button(text='選択')
dir_entry_button.bind('<Button-1>', select_dir) 
dir_entry_button.pack()

label2 = tk.Label(text='＊＊＊＊＊＊＊＊設定＊＊＊＊＊＊＊＊')
label2.pack()

#実行ボタン
def run(event):
    #実行ボタンが押されたときの処理
    global rot_flag
    global YTM_flag
    global face_flag
    if rot_flag.get():
        pass
    messagebox.showinfo('info','実行中です')

rot_flag = tk.BooleanVar()
rot_flag.set(True)
rot_button = tk.Checkbutton(text='動画の回転', variable=rot_flag)
rot_button.pack()

YTM_flag = tk.BooleanVar()
YTM_flag.set(True)
YTM_button = tk.Checkbutton(text='やってみた', variable=YTM_flag)
YTM_button.pack()

face_flag = tk.BooleanVar()
face_flag.set(False)
face_button = tk.Checkbutton(text='顔画像', variable=face_flag)
face_button.pack()

run_button = tk.Button(text='実行！')
run_button.bind('<Button-1>', run)
run_button.pack()

root.mainloop()