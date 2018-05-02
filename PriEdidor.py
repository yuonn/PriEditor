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


def RotMovie(movie_path, output_path, faces_path):
    cap = cv2.VideoCapture(movie_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter(output_path, fourcc, fps, (1080, 1920))

    frame_count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            frame = Rot90(frame)
            output.write(frame)
            if frame_count%20 == 0:
                FaceTrim(frame_count, frame, faces_path)
        except AttributeError:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

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


def DegreeOfSimilarity(image, temp):
    match = cv2.matchTemplate(image, temp, cv2.TM_SQDIFF)
    min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
    return min_value


def TrimFlag(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    temp_list = os.listdir('./templates')
    for temp_path in temp_list:
        temp = cv2.imread('./templates/' + temp_path)
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = temp[30:temp.shape[0]-30, 30:temp.shape[1]-30]
        if gray.shape[0] >= temp.shape[0] and gray.shape[1] >= temp.shape[1]:
            if DegreeOfSimilarity(gray, temp) < 50000000:
                return False
    return True


def FaceDetect(image):
    face_cascade = cv2.CascadeClassifier('lbpcascade_animeface.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return faces


def FaceTrim(image_num, image, faces_path):
    if not os.path.exists(faces_path):
        os.makedirs(faces_path)

    faces = FaceDetect(image)

    for i, (x,y,w,h) in enumerate(faces):
        if h > 100:
            y1 = max(0, y-int(0.4*h))
            y2 = min(1920, y+h+int(1.3*h))
            x1 = max(0, x-int(0.5*w))
            x2 = min(1920, x+w+int(0.5*w))
            face_image = image[y1:y2, x1:x2]
            if TrimFlag(face_image):
                face_path = faces_path + '/' + str(image_num) + '_' + str(i) + '.png'
                cv2.imwrite(face_path, face_image)


def RenameFiles(path, extension):
    movie_dir = glob.glob(path + '/*')
    
    for i, file_name in enumerate(movie_dir):
        movie_path = path + '/' + str(i) + extension
        if not os.path.exists(movie_path):
            os.rename(file_name, os.path.join(path, str(i) + extension))


def main(movies_path, rotated_movie_path, audio_path, outputs_path, images_path):
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
        RotMovie(movie_path, rotated_movie_path, image_path)
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
    images_path = './images'

    main(movies_path, rotated_movie_path, audio_path, outputs_path, images_path)
