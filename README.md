# PriEditor

プリチャン（プリパラ）の録画ファイルを縦に直したり，自動で顔をトリミングしたり，いい感じに編集を楽にしてくれるプログラムです．



## 実装済みの機能

* 横向きの動画を縦にする
* 20フレームごとに顔認識をして顔をトリミング



## 使い方

1. フォルダ内に編集したい動画を```original.mp4```として保存する
2. ```PriEditor.py```を実行
3. 実行結果が```output.mp4```として出力される





## 実行環境

* Python3
* opencv-python
* ffmpy
* FFMPEG



opencv-pythonは下記URLを参照してください．（pipで入ります）

https://pypi.org/project/opencv-python/



FFMPEGは下記URLからダウンロードして，PATH通して使えるようにしてください．

https://www.ffmpeg.org/download.html



ffmpyは下記URLを参照してください．（pipで入ります）

http://ffmpy.readthedocs.io/en/latest/



## 顔認識について

本プログラムの顔認識は[nagadomi様のlbpcascade_animeface.xml](https://github.com/nagadomi/lbpcascade_animeface)を使用しています．関係者各位に感謝いたします．