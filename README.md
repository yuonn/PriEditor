# PriEditor

プリチャン（プリパラ）の録画ファイルを縦に直したり，自動で顔をトリミングしたり，いい感じに編集を楽にしてくれるプログラムです．



## 実装済みの機能

* 横向きの動画を縦にする
* 20フレームごとに顔認識をしてトリミング





## 基本的な使い方

1. フォルダ内に編集したい横向きの動画を```./movies```に保存する
2. ```PriEditor.py```を実行
3. ```./images```にキャラをトリミングした画像が保存される
4. ```./outputs```に縦になった動画が保存される




### imagesに生成される無駄な画像の選別

デフォルトの状態だと，ロード中の画像からトリミングしたりするので無駄な画像が保存されてしまいます．そこで，パターンマッチングによって類似画像を保存しないようにすることができます．この機能は，**既に生成されたいらない画像を```./templates```に保存する**だけで使用することができます．ただし，追加した分だけ処理は重くなるので生成される画像のバランスを見ながら使用すると良いでしょう．




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