import cv2
import ffmpy
import os
import glob
import re
import numpy as np


def Rot90(image):
    size_before = tuple([image.shape[1], image.shape[0]])
    size_after  = tuple([image.shape[0], image.shape[1]])
    center = tuple([int(size_before[0]/2), int(size_after[1]/2)])
    angle = 90.0
    R = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_image = cv2.warpAffine(image, R, size_after, flags=cv2.INTER_CUBIC)

    return rotated_image


def RotMovie(movie_path, output_path):
    cap = cv2.VideoCapture(movie_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter(output_path, fourcc, fps, (1080, 1920))

    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            frame = Rot90(frame)
            output.write(frame)
        except AttributeError:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    output.release()
    cv2.destroyAllWindows()


def MakeAudio(movie_path, audio_path):
    if os.path.exists(audio_path):
        os.remove(audio_path)

    ff = ffmpy.FFmpeg(
        inputs={movie_path : None},
        outputs={audio_path : ['-map', '0:a', '-c:a', 'copy', '-f', 'mp4']}
    )
    ff.run()


def MakeMovie(movie_path, audio_path, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    
    ff = ffmpy.FFmpeg(
        inputs={movie_path : None, audio_path : None},
        outputs={output_path : '-c:v h264 -c:a ac3'}
    )
    ff.run()


def RenameFiles(path, extension):
    movie_dir = glob.glob(path + '/*')
    
    for i, file_name in enumerate(movie_dir):
        movie_path = path + '/' + str(i) + extension
        if not os.path.exists(movie_path):
            os.rename(file_name, os.path.join(path, str(i) + extension))


def main(movies_path, rotated_movie_path, audio_path, outputs_path):
    RenameFiles(movies_path, '.mp4')

    movies = os.listdir(movies_path)
    count = 0
    for f in movies:
        index = re.search('.mp4', f)
        if index:
            count += 1

    for i in range(count):
        movie_path = movies_path + '/' + str(i) + '.mp4'
        RotMovie(movie_path, rotated_movie_path)
        print('Rotated!')
        
        MakeAudio(movie_path, audio_path)
        print('made audio!')
        
        output_path = outputs_path + '/' + str(i) + '.mp4'
        MakeMovie(rotated_movie_path, audio_path, output_path)
        print('made movie!')
        
        print('start final process')
        if os.path.exists(rotated_movie_path):
            os.remove(rotated_movie_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        print('finish all process!!')


if __name__ == '__main__':
    movies_path = './movies'
    rotated_movie_path = 'rotated.mp4'
    audio_path = 'audio.mp4'
    outputs_path = './outputs'

    main(movies_path, rotated_movie_path, audio_path, outputs_path)
