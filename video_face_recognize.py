from ProgramCode.DatabaseIO import phpMyAdminoutput
from keras.models import load_model
from ProgramCode.ImageProcess import image_process
import cv2
import numpy as np
from scipy.spatial import distance


try:
    db_names, db_images = phpMyAdminoutput.database_output()
    # 框住人臉的矩形邊框顏色
    color = (0, 255, 0)

    # 捕獲指定攝像頭的實時視訊流
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.ocl.setUseOpenCL(False)

    # 人臉識別分類器本地儲存路徑
    face_model_path = "./Model/Opencv/haarcascade_frontalface_alt2.xml"
    keras_model = load_model("./Model/Keras/facenet_keras.h5")
    # 迴圈檢測識別人臉
    while True:
        ret, frame = cap.read()  # 讀取一幀視訊
        frame = cv2.flip(frame, 1)

        if ret is True:

            # 影象灰化，降低計算複雜度
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            continue
        # 使用人臉識別分類器，讀入分類器
        model = cv2.CascadeClassifier(face_model_path)

        # 利用分類器識別出哪個區域為人臉
        faceRects = model.detectMultiScale(
            frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:
            for faceRect in faceRects:
                (x, y, w, h) = faceRect
                your_picture = frame[y:y+h, x:x+w]
                cv2.rectangle(frame, (x - 10, y - 10),
                              (x + w + 10, y + h + 10), color, thickness=2)
                similar = []
                n = 0
                for image in db_images:
                    alignedfs = image_process.align_image(
                        image, 6, face_model_path)
                    if alignedfs is None:
                        print("Cannot find any face in database: {}".format(
                            db_names[n]))
                        n += 1
                    else:
                        for alignedf in alignedfs:
                            face_dbimage = image_process.preProcess(alignedf)
                            embs_dbface = image_process.l2_normalize(
                                np.concatenate(keras_model.predict(face_dbimage)))
                            alignedys = image_process.align_image(
                                your_picture, 6, face_model_path)
                            if alignedys is None:
                                print("Cannot find any face in video: {}".format(
                                    db_names[n]))
                                n += 1
                            else:
                                for alignedy in alignedys:
                                    face_yimage = image_process.preProcess(
                                        alignedy)
                                    embs_yface = image_process.l2_normalize(
                                        np.concatenate(keras_model.predict(face_yimage)))
                                    distanceNum = distance.euclidean(
                                        embs_dbface, embs_yface)
                                    if(distanceNum < 0.6):
                                        similar.append("%f,%s" %
                                                       (distanceNum, db_names[n]))
                                        print(db_names[n] +
                                              "=" + str(distanceNum))
                                    n += 1
                if(similar):
                    best = min(similar)
                    best = best.split(',')
                    print(best)
                    print(best[1])
                    final = str(best[1])
                    cv2.putText(frame, final,
                                (x + 30, y + 30),  # 座標
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字型
                                1,  # 字號
                                (255, 0, 255),  # 顏色
                                2)  # 字的線寬
                    similar.clear()
                else:
                    # 文字提示是誰
                    cv2.putText(frame, 'Unknown',
                                (x + 30, y + 30),  # 座標
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字型
                                1,  # 字號
                                (255, 0, 255),  # 顏色
                                2)  # 字的線寬
                    similar.clear()

        cv2.imshow("FaceTest", frame)

        # 等待10毫秒看是否有按鍵輸入
        k = cv2.waitKey(10)
        # 如果輸入q則退出迴圈
        if k & 0xFF == ord('q'):
            break

    # 釋放攝像頭並銷燬所有視窗
    cap.release()
    cv2.destroyAllWindows()

except:
    print('SHARKSHARKSHARKSHARKSHARKSHARK')
