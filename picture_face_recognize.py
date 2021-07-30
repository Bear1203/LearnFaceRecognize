from ProgramCode.Camera import take_a_picture
from ProgramCode.DatabaseIO import phpMyAdminoutput
from keras.models import load_model
from ProgramCode.ImageProcess import image_process
import cv2
import numpy as np
from scipy.spatial import distance
from ProgramCode.Answer import answer_name
import os


face_model_path = "./Model/Opencv/haarcascade_frontalface_alt2.xml"
keras_model = load_model("./Model/Keras/facenet_keras.h5")
webcamera_id = 0

take_a_picture.TakeAPicture(webcamera_id, face_model_path)

db_names, db_images = phpMyAdminoutput.database_output()
n = 0
your_picture = cv2.imread("YourPicture.jpg")
similar = []

for image in db_images:
    alignedf = image_process.align_image(image, 6, face_model_path)
    if alignedf is None:
        print("Cannot find any face in database: {}".format(db_names[n]))
        n += 1
    else:
        face_dbimage = image_process.preProcess(alignedf)
        embs_dbface = image_process.l2_normalize(
            np.concatenate(keras_model.predict(face_dbimage)))
        alignedy = image_process.align_image(your_picture, 6, face_model_path)
        face_yimage = image_process.preProcess(alignedy)
        embs_yface = image_process.l2_normalize(
            np.concatenate(keras_model.predict(face_yimage)))
        distanceNum = distance.euclidean(embs_dbface, embs_yface)
        if(distanceNum < 0.65):
            similar.append("%f,%s" % (distanceNum, db_names[n]))
            print(db_names[n] + "=" + str(distanceNum))
        n += 1

answer_name.answer(similar)
