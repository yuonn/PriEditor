import ffmpy
import os
import glob
import re


def rot_movie(movie_path, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    
    ff = ffmpy.FFmpeg(
        inputs={movie_path : None},
        outputs={output_path : '-vf "transpose=2"'}
    )
    ff.run()


def rename_files(path, extension):
    movie_dir = glob.glob(path + '/*')
    
    for i, file_name in enumerate(movie_dir):
        movie_path = path + '/' + str(i) + extension
        if not os.path.exists(movie_path):
            os.rename(file_name, os.path.join(path, str(i) + extension))


def main(movies_path, outputs_path):
    rename_files(movies_path, '.mp4')

    movies = os.listdir(movies_path)
    count = 0
    for f in movies:
        index = re.search('.mp4', f)
        if index:
            count += 1

    for i in range(count):
        movie_path = movies_path + '/' + str(i) + '.mp4'
        output_path = outputs_path + '/' + str(i) + '.mp4'
        rot_movie(movie_path, output_path)

if __name__ == '__main__':
    movies_path = './movies'
    outputs_path = './outputs'

    main(movies_path, outputs_path)
