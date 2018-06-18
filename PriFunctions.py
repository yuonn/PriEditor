import ffmpy
import os
import glob
import re
import cv2
import numpy as np

class PriFunctions:
    def __init__(self):
        self.recmovie_dir = './movies'
        self.movie_dir = './outputs'
        self.face_dir = './faces'
        self.YTM_dir = './YTMshot'
        self.face_interval = 50
    

    def set_recmovie_dir(self, path):
        self.recmovie_dir = path

    def set_movie_dir(self, path):
        self.movie_dir = path
    
    def set_face_dir(self, path):
        self.face_dir = path
    
    def set_YTM_dir(self, path):
        self.YTM_dir = path

    def set_face_interval(self, value):
        self.face_interval = int(value)


    def __rename_files(self, path, extension):
        directory = glob.glob(path + '/*')
        
        for i, file_name in enumerate(directory):
            item_path = path + '/' + str(i) + extension
            if not os.path.exists(item_path):
                os.rename(file_name, os.path.join(path, str(i) + extension))


    # Rotate movie
    def make_rotate_movie(self):
        self.__rename_files(self.recmovie_dir, '.mp4')

        movies = os.listdir(self.recmovie_dir)
        count = 0
        for f in movies:
            index = re.search('.mp4', f)
            if index:
                count += 1

        for i in range(count):
            movie_path = self.recmovie_dir + '/' + str(i) + '.mp4'
            output_path = self.movie_dir + '/' + str(i) + '.mp4'
            self.__rot_movie(movie_path, output_path)


    def __rot_movie(self, movie_path, output_path):
        if os.path.exists(output_path):
            os.remove(output_path)
        
        pass1 = ffmpy.FFmpeg(
            inputs={movie_path : None},
            outputs={output_path : '-b:v 11264k -s 1080x1920 -pass 1 -passlogfile "passlog" -vf "transpose=2" -y -vsync 1 -an'}
        )
        print(pass1.cmd)
        pass1.run()

        pass2 = ffmpy.FFmpeg(
            inputs={movie_path : None},
            outputs={output_path : '-b:v 11264k -s 1080x1920 -pass 2 -passlogfile "passlog" -vf "transpose=2" -y -vsync 1'}
        )
        print(pass2.cmd)
        pass2.run()


    # YTM_shot
    def capture_YTM(self):
        self.__rename_files(self.movie_dir, '.mp4')

        movies = os.listdir(self.movie_dir)
        count = 0
        for f in movies:
            index = re.search('.mp4', f)
            if index:
                count += 1

        for i in range(count):
            movie_path = self.movie_dir + '/' + str(i) + '.mp4'
            images_path = self.YTM_dir + '/' + str(i)
            if not os.path.exists(images_path):
                os.makedirs(images_path)
            self.__YTM_shot(movie_path, images_path)


    def __YTM_shot(self, movie_path, images_path):
        temp_dir = os.listdir('./matcher')
        temp_list = []
        for temp_path in temp_dir:
            temp_list.append(cv2.imread('./matcher/' + temp_path, cv2.IMREAD_GRAYSCALE))
        
        cap = cv2.VideoCapture(movie_path)
        
        frame_count = 0
        YTM_count = 0
        while(YTM_count < 4):
            frame_count += 1
            ret, frame = cap.read()
            if ret == False or frame_count%20 != 0:
                continue
            try:
                if ret and frame_count%20 == 0 and self.__flag_of_similarity(frame, temp_list):
                    image_path = images_path + '/' + str(YTM_count) + '.png'
                    cv2.imwrite(image_path, frame)
                    YTM_count += 1
            except:
                break

        for interval in range(500):
            cap.read()
        
        while(YTM_count < 8):
            frame_count += 1
            ret, frame = cap.read()
            if ret == False or frame_count%20 != 0:
                continue
            try:
                if ret and frame_count%20 == 0 and self.__flag_of_similarity(frame, temp_list):
                    image_path = images_path + '/' + str(YTM_count) + '.png'
                    cv2.imwrite(image_path, frame)
                    YTM_count += 1
            except:
                break

        for interval in range(500):
            cap.read()

        while(YTM_count < 12):
            frame_count += 1
            ret, frame = cap.read()
            if ret == False or frame_count%20 != 0:
                continue
            try:
                if ret and frame_count%20 == 0 and self.__flag_of_similarity(frame, temp_list):
                    image_path = images_path + '/' + str(YTM_count) + '.png'
                    cv2.imwrite(image_path, frame)
                    YTM_count += 1
            except:
                break
        

        cap.release()
        cv2.destroyAllWindows()


    def __flag_of_similarity(self, image, temp_list):
        image = image[1500:1900, 0:300]
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        for temp in temp_list:
            match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
            min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
            print(max_value)
            if max_value > 0.85:
                return True

        return False

    #Trim faces
    def trim_faces(self):
        self.__rename_files(self.movie_dir, '.mp4')

        movies = os.listdir(self.movie_dir)
        count = 0
        for f in movies:
            index = re.search('.mp4', f)
            if index:
                count += 1

        for i in range(count):
            movie_path = self.movie_dir + '/' + str(i) + '.mp4'
            image_path = self.face_dir + '/' + str(i)
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            self.__face_trim(movie_path, image_path)


    def __face_trim(self, movie_path, image_path):
        temp_dir = os.listdir('./templates')
        temp_list = []
        for temp_path in temp_dir:
            temp_list.append(cv2.imread('./templates/' + temp_path, cv2.IMREAD_GRAYSCALE))
        
        cap = cv2.VideoCapture(movie_path)
        frame_count = 0
        while(cap.isOpened()):
            frame_count += 1
            ret, frame = cap.read()
            if frame_count%self.face_interval != 0:
                continue
            try:
                faces = self.__face_detect(frame)
                for i, (x,y,w,h) in enumerate(faces):
                    y1 = max(0, y-int(0.4*h))
                    y2 = min(1920, y+h+int(1.3*h))
                    x1 = max(0, x-int(0.5*w))
                    x2 = min(1080, x+w+int(0.5*w))
                    face_image = frame[y1:y2, x1:x2]
                    if h > 200 and self.__trim_flag(face_image, temp_list):
                        face_path = image_path + '/' + str(frame_count) + '_' + str(i) + '.png'
                        cv2.imwrite(face_path, face_image)
            except:
                break
        cap.release()
        cv2.destroyAllWindows()


    def __face_detect(self, image):
        face_cascade = cv2.CascadeClassifier('lbpcascade_animeface.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        return faces


    def __trim_flag(self, image, temp_list):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        for temp in temp_list:
            temp = temp[30:temp.shape[0]-30, 30:temp.shape[1]-30]
            if gray.shape[0] >= temp.shape[0] and gray.shape[1] >= temp.shape[1]:
                if self.__degree_of_similarity(gray, temp) > 0.8:
                    return False
        return True


    def __degree_of_similarity(self, image, temp):
        match = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)
        min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
        return min_value
