from datetime import datetime
import tensorflow as tf
from imutils.video import VideoStream
from PyQt5.QtWidgets import *


import facenet
import imutils
import align.detect_face
import numpy as np
import cv2
import os

def main(name):

    MINSIZE = 20
    THRESHOLD = [0.6, 0.7, 0.7]
    FACTOR = 0.709
    ROOT_PATH = "//"
    FACENET_MODEL_PATH = ROOT_PATH+'Models/20180402-114759.pb'
    MARGIN_IMG = 20
    USR_PATH = ROOT_PATH+"Dataset/"+name+"/"
    if(os.path.isdir(USR_PATH)==False):
        os.mkdir(USR_PATH)

    count = 50
    SIZE_IMG = (320, 320)
    with tf.Graph().as_default():

        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))

        with sess.as_default():

            # Load the model
            print('Loading feature extraction model')
            facenet.load_model(FACENET_MODEL_PATH)

            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, "align")
            cap  = VideoStream(src=0).start()

            while count:
                frame = cap.read()
                frame = imutils.resize(frame, width=600)
                frame = cv2.flip(frame, 1)

                bounding_boxes, _ = align.detect_face.detect_face(frame, MINSIZE, pnet, rnet, onet, THRESHOLD, FACTOR)

                faces_found = bounding_boxes.shape[0]
                try:
                    if faces_found > 1:
                        cv2.putText(frame, "Only one face", (0, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1, (255, 255, 255), thickness=1, lineType=2)
                    elif faces_found > 0:
                        det = bounding_boxes[:, 0:4]
                        bb = np.zeros((faces_found, 4), dtype=np.int32)
                        for i in range(faces_found):
                            bb[i][0] = det[i][0]
                            bb[i][1] = det[i][1]
                            bb[i][2] = det[i][2]
                            bb[i][3] = det[i][3]
                            if (bb[i][3]-bb[i][1])/frame.shape[0]>0.25:
                                cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (255, 0, 0), 2)
                                img = frame[bb[i][1]-MARGIN_IMG:bb[i][3]+MARGIN_IMG, bb[i][0]-MARGIN_IMG: bb[i][2]+MARGIN_IMG]
                                img = cv2.resize(img, SIZE_IMG)

                                print("img", img)
                                c = 1
                                while (c <= 30):
                                    path = str(USR_PATH +  str(c) + '{}.jpg'.format(
                                        str(datetime.now())[:-7].replace(":", "-").replace(" ", "-") + str(count)))

                                    print(path)
                                    cv2.imwrite(path, img)
                                    print('ok')
                                    c += 1
                                count-=1
                except:
                    pass

                cv2.imshow('Face Recognition', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
