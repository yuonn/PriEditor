import cv2
import os
import glob
import re
import numpy as np


def ScreenShot(movie_path, output_path):
    temp_dir = os.listdir('./matcher')
    temp_list = []
    for temp_path in temp_dir:
        temp_list.append(cv2.imread('./matcher/' + temp_path, cv2.IMREAD_GRAYSCALE))
    
    cap = cv2.VideoCapture(movie_path)
    
    frame_count = 0
    YTM_count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            if frame_count%20 == 0:
                if FlagOfSimilarity(frame, temp_list):
                    image_path = output_path + '/' + str(YTM_count) + '.png'
                    cv2.imwrite(image_path, frame)
                    YTM_count += 1
        except:
            break
        if YTM_count >= 50:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()


def FlagOfSimilarity(image, temp_list):
    
    image = image[1500:1900, :]
    
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    for temp in temp_list:
        match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
        min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
        print(max_value)
        if max_value > 0.3:
            return True
    
    return False


def RenameFiles(path, extension):
    movie_dir = glob.glob(path + '/*')
    
    for i, file_name in enumerate(movie_dir):
        movie_path = path + '/' + str(i) + extension
        if not os.path.exists(movie_path):
            os.rename(file_name, os.path.join(path, str(i) + extension))


def main(movies_path, images_path):
    RenameFiles(movies_path, '.mp4')

    movies = os.listdir(movies_path)
    count = 0
    for f in movies:
        index = re.search('.mp4', f)
        if index:
            count += 1

    for i in range(count):
        movie_path = movies_path + '/' + str(i) + '.mp4'
        image_path = images_path + '/' + str(i)
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        ScreenShot(movie_path, image_path)


if __name__ == '__main__':
    movies_path = './outputs'
    outputs_path = './screenshot'

    main(movies_path, outputs_path)
