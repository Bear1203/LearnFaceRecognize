import cv2
import sys


def TakeAPicture(camera_id, model_path):
    camera = cv2.VideoCapture(camera_id)  # 讀取網路攝影機
    finish = 0

    while(camera.isOpened()):
        ret, frame = camera.read()  # 讀取每一幀
        key = cv2.waitKey(10)  # 聽取有無按鍵指令
        if finish == 0:
            if ret:
                frame = cv2.flip(frame, 1, dst=None)  # 每一幀畫面水平鏡像
                model = cv2.CascadeClassifier(model_path)  # 讀取人臉辨識模型
                face = model.detectMultiScale(
                    frame, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))  # 框出每一幀畫面中人臉
                if len(face) > 0:
                    text = "SMILE -- ('S'key to take a picture)"  # 文字提示有偵測到人臉
                    cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_TRIPLEX,
                                1, (0, 255, 0), 2, cv2.LINE_AA)  # 文字美編與座標
                    if key == ord('s') or key == ord('S'):
                        finish = 1
                        # 按下鍵盤S鍵拍一張照片並儲存於Image資料夾後退出拍照視窗
                        cv2.imwrite("YourPicture.jpg", frame)
                        print("Thank you")
                else:
                    text = "NO FACE -- ('Q'key to quit)"  # 文字提示沒有偵測到人臉
                    cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_TRIPLEX,
                                1, (0, 0, 255), 2, cv2.LINE_AA)  # 文字美編與座標
                    if key == ord('q') or key == ord('Q'):
                        finish = 1
                        print("Can't find your face")  # 無法偵測到人臉，按下鍵盤Q鍵退出拍照視窗
            else:
                sys.exit("Can't receive your frame")
        else:
            break
        cv2.imshow("Please Take A Picture", frame)  # 拍照視窗名稱

    if not camera.isOpened():
        sys.exit("Your webcamera can't open")

    camera.release()  # 關掉網路攝影機
    cv2.destroyAllWindows()  # 關掉拍照視窗
