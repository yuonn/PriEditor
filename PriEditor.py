import os
import time
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import PriFunctions


def main_loop():
    root = tk.Tk()
    root.title('PriEditor')
    root.geometry('295x425')

    #ラベル
    global label1 
    label1 = tk.Label(text='＊＊＊＊＊＊＊＊＊フォルダ選択＊＊＊＊＊＊＊＊＊')
    folder_row = 0
    label1.grid( column=0, row=folder_row, columnspan=2, pady=10)

    global recmovie_label 
    recmovie_label = tk.Label(text='録画（横）のフォルダ')
    recmovie_label.grid( column=0, row=folder_row+1, padx=5, sticky=tk.W+tk.S)
    global recmovie_entry
    recmovie_entry = tk.Entry()
    recmovie_entry.insert(tk.END,'./movies')
    recmovie_entry.grid( column=0, row=folder_row+2, padx=5, sticky=tk.W+tk.E+tk.N)
    global recmovie_entry_button
    recmovie_entry_button = tk.Button(text='選択')
    recmovie_entry_button.bind('<Button-1>', select_recmovie_dir)
    recmovie_entry_button.grid( column=1, row=folder_row+2, sticky=tk.N)

    global movie_label
    movie_label = tk.Label(text='動画の出力先および動画（縦）のフォルダ')
    movie_label.grid( column=0, row=folder_row+3, padx=5, sticky=tk.W+tk.S)
    global movie_entry
    movie_entry = tk.Entry()
    movie_entry.insert(tk.END,'./outputs')
    movie_entry.grid( column=0, row=folder_row+4, padx=5, sticky=tk.W+tk.E+tk.N)
    global movie_entry_button
    movie_entry_button = tk.Button(text='選択')
    movie_entry_button.bind('<Button-1>', select_movie_dir) 
    movie_entry_button.grid( column=1, row=folder_row+4, sticky=tk.N)

    global YTM_label
    YTM_label = tk.Label(text='やってみた！のキャプチャを保存フォルダ')
    YTM_label.grid( column=0, row=folder_row+5, padx=5, sticky=tk.W+tk.S)
    global YTM_entry
    YTM_entry = tk.Entry()
    YTM_entry.insert(tk.END,'./YTMshot')
    YTM_entry.grid( column=0, row=folder_row+6, padx=5, sticky=tk.W+tk.E+tk.N)
    global YTM_entry_button
    YTM_entry_button = tk.Button(text='選択')
    YTM_entry_button.bind('<Button-1>', select_YTM_dir) 
    YTM_entry_button.grid( column=1, row=folder_row+6, sticky=tk.N)

    global face_label
    face_label = tk.Label(text='顔画像を保存するフォルダ')
    face_label.grid( column=0, row=folder_row+7, padx=5, sticky=tk.W+tk.S)
    global face_entry
    face_entry = tk.Entry()
    face_entry.insert(tk.END,'./faces')
    face_entry.grid( column=0, row=folder_row+8, padx=5, sticky=tk.W+tk.E+tk.N)
    global face_entry_button
    face_entry_button = tk.Button(text='選択')
    face_entry_button.bind('<Button-1>', select_face_dir) 
    face_entry_button.grid( column=1, row=folder_row+8, sticky=tk.N)


    label2 = tk.Label(text='＊＊＊＊＊＊＊＊＊＊処理選択＊＊＊＊＊＊＊＊＊＊')
    process_row = folder_row + 9
    label2.grid( column=0, row=process_row,  columnspan=2, pady=10, sticky=tk.S)


    global rot_flag
    rot_flag = tk.BooleanVar()
    rot_flag.set(True)
    global rot_button
    rot_button = tk.Checkbutton(text='動画の回転', variable=rot_flag)
    rot_button.grid( column=0, row=process_row+1,  columnspan=2 )

    global YTM_flag
    YTM_flag = tk.BooleanVar()
    YTM_flag.set(True)
    global YTM_button
    YTM_button = tk.Checkbutton(text='やってみた', variable=YTM_flag)
    YTM_button.grid( column=0, row=process_row+2,  columnspan=2 )

    global face_flag
    face_flag = tk.BooleanVar()
    face_flag.set(False)
    global face_button
    face_button = tk.Checkbutton(text='顔画像', variable=face_flag)
    face_button.grid( column=0, row=process_row+3,  columnspan=2 )


    global run_button
    run_button = tk.Button(text='実行！')
    run_button.bind('<Button-1>', run)

    # プログレスバー
    global progress_bar
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate')
    
    run_row = process_row + 4
    run_button.grid( column=0, row=run_row, columnspan=2, pady=10, ipady=5, ipadx=5)
    progress_bar.grid( column=0, row=run_row+1, columnspan=2, sticky=tk.E+tk.W)


    root.mainloop()


def select_recmovie_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    recmovie_entry.delete(0, tk.END)
    recmovie_entry.insert(tk.END, directory)


def select_movie_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    movie_entry.delete(0, tk.END)
    movie_entry.insert(tk.END, directory)

def select_YTM_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    YTM_entry.delete(0, tk.END)
    YTM_entry.insert(tk.END, directory)


def select_face_dir(event):
    fTyp = [('','*')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    directory = tk.filedialog.askdirectory(initialdir = iDir)
    face_entry.delete(0, tk.END)
    face_entry.insert(tk.END, directory)


#実行ボタン
def run(event):
    #実行ボタンが押されたときの処理
    '''
    global rot_flag
    global YTM_flag
    global face_flag
    '''

    messagebox.showinfo('PriEditor','処理を開始します')
    progress_bar.start()
    
    t1 = threading.Thread(target=main_loop)
    t1.start()
    
    t = threading.Thread(target=main_process)
    t.start()
    

    progress_bar.stop()
    messagebox.showinfo('PriEditor','全ての処理が終了しました')


def main_process():
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
    

if __name__=='__main__':
    main_loop()