import cv2
import ffmpy
import os
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
        if h>100:
            face_image = image[y-int(0.3*h):y+h+int(0.2*h), x:x+w]
            face_path = faces_path + '/' + str(image_num) + '_' + str(i) + '.png'
            cv2.imwrite(face_path, face_image)


if __name__ == '__main__':
    original_path = 'original.mp4'
    rotated_movie_path = 'rotated.mp4'
    audio_path = 'audio.mp4'
    output_path = 'output.mp4'
    faces_path = './faces'

    RotMovie(original_path, rotated_movie_path, faces_path)
    print('Rotated!')
    MakeAudio(original_path, audio_path)
    print('make audio!')
    MakeMovie(rotated_movie_path, audio_path, output_path)
    print('make movie!')
    
    print('start final process')
    if os.path.exists(rotated_movie_path):
        os.remove(rotated_movie_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)
    print('finish all process!!')
    
    