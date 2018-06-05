import cv2
import os
import glob
import re
import numpy as np


def face_trim(movie_path, output_path):
    temp_dir = os.listdir('./templates')
    temp_list = []
    for temp_path in temp_dir:
        temp_list.append(cv2.imread('./templates/' + temp_path, cv2.IMREAD_GRAYSCALE))
    
    cap = cv2.VideoCapture(movie_path)
    frame_count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            if frame_count%100 == 0:
                faces = face_detect(frame)
                for i, (x,y,w,h) in enumerate(faces):
                    y1 = max(0, y-int(0.4*h))
                    y2 = min(1920, y+h+int(1.3*h))
                    x1 = max(0, x-int(0.5*w))
                    x2 = min(1080, x+w+int(0.5*w))
                    face_image = frame[y1:y2, x1:x2]
                    if h > 200 and trim_flag(face_image, temp_list):
                        face_path = output_path + '/' + str(frame_count) + '_' + str(i) + '.png'
                        cv2.imwrite(face_path, face_image)
        except:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()


def face_detect(image):
    face_cascade = cv2.CascadeClassifier('lbpcascade_animeface.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return faces


def trim_flag(image, temp_list):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    for temp in temp_list:
        temp = temp[30:temp.shape[0]-30, 30:temp.shape[1]-30]
        if gray.shape[0] >= temp.shape[0] and gray.shape[1] >= temp.shape[1]:
            if degree_of_similarity(gray, temp) > 0.9:
                return False
    return True


def degree_of_similarity(image, temp):
    match = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)
    min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
    return min_value


def rename_files(path, extension):
    movie_dir = glob.glob(path + '/*')
    
    for i, file_name in enumerate(movie_dir):
        movie_path = path + '/' + str(i) + extension
        if not os.path.exists(movie_path):
            os.rename(file_name, os.path.join(path, str(i) + extension))


def main(movies_path, images_path):
    rename_files(movies_path, '.mp4')

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
        face_trim(movie_path, image_path)


if __name__ == '__main__':
    movies_path = './outputs'
    outputs_path = './images'

    main(movies_path, outputs_path)
