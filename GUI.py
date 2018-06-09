import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox
import PriFunctions

root = tk.Tk()
root.title('PriEditor')
root.geometry('300x400')

#ラベル
def select_recmovie_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    recmovie_entry.delete(0, tk.END)
    recmovie_entry.insert(tk.END, directory)
recmovie_label = tk.Label(text='録画（横）のフォルダ')
recmovie_label.pack()
recmovie_entry = tk.Entry()
recmovie_entry.insert(tk.END,'./movies')
recmovie_entry.pack()
recmovie_entry_button = tk.Button(text='選択')
recmovie_entry_button.bind('<Button-1>', select_recmovie_dir)
recmovie_entry_button.pack()

def select_movie_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    movie_entry.delete(0, tk.END)
    movie_entry.insert(tk.END, directory)
movie_label = tk.Label(text='動画の出力先および動画（縦）のフォルダ')
movie_label.pack()
movie_entry = tk.Entry()
movie_entry.insert(tk.END,'./outputs')
movie_entry.pack()
movie_entry_button = tk.Button(text='選択')
movie_entry_button.bind('<Button-1>', select_movie_dir) 
movie_entry_button.pack()

def select_YTM_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    YTM_entry.delete(0, tk.END)
    YTM_entry.insert(tk.END, directory)
YTM_label = tk.Label(text='やってみた！のキャプチャを保存フォルダ')
YTM_label.pack()
YTM_entry = tk.Entry()
YTM_entry.insert(tk.END,'./YTMshot')
YTM_entry.pack()
YTM_entry_button = tk.Button(text='選択')
YTM_entry_button.bind('<Button-1>', select_YTM_dir) 
YTM_entry_button.pack()

def select_face_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    face_entry.delete(0, tk.END)
    face_entry.insert(tk.END, directory)
face_label = tk.Label(text='顔画像を保存するフォルダ')
face_label.pack()
face_entry = tk.Entry()
face_entry.insert(tk.END,'./faces')
face_entry.pack()
face_entry_button = tk.Button(text='選択')
face_entry_button.bind('<Button-1>', select_face_dir) 
face_entry_button.pack()


label2 = tk.Label(text='＊＊＊＊＊＊＊＊＊＊＊設定＊＊＊＊＊＊＊＊＊＊＊')
label2.pack()

#実行ボタン
def run(event):
    #実行ボタンが押されたときの処理
    global rot_flag
    global YTM_flag
    global face_flag

    messagebox.showinfo('info','処理を開始しました')
    pri = PriFunctions.PriFunctions()
    
    pri.set_recmovie_dir(str(recmovie_entry.get()))
    pri.set_movie_dir(str(movie_entry.get()))
    pri.set_YTM_dir(str(YTM_entry.get()))
    pri.set_face_dir(str(face_entry.get()))
    
    if rot_flag.get():
        pri.make_rotate_movie()
        #messagebox.showinfo('info','動画の回転が終了しました')
    if YTM_flag.get():
        pri.capture_YTM()
        #messagebox.showinfo('info','やってみた！のキャプチャが終了しました')
    if face_flag.get():
        pri.trim_faces()
        #messagebox.showinfo('info','顔画像のトリミングが終了しました')

    messagebox.showinfo('info','全ての処理が終了しました')

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
