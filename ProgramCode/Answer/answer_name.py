import cv2
from ProgramCode.DatabaseIO import phpMyAdmininput
import os


def answer(similars):
    if(similars):
        best = min(similars)
        best = best.split(',')
        print(best)
        print(best[1])
        final = str(best[1])
        similars.clear()
        while(True):
            img = cv2.imread("YourPicture.jpg")
            k = cv2.waitKey(1)
            # 裁切區域的 x 與 y 座標（左上角）
            x = 0
            y = 55
            # 裁切區域的長度與寬度
            w = 900
            h = 900
            # 裁切圖片
            crop_img = img[y:y+h, x:x+w]
            # 文字提示你是誰
            text = final+" ('E'key to exit)"
            # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色(B, G, R), 線條寬度, 線條種類)
            cv2.putText(img, text, (10, 80), cv2.FONT_HERSHEY_TRIPLEX,
                        1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow("Your Name", crop_img)
            if k == ord('e') or k == ord('E'):
                break
        # 關掉圖片視窗
        cv2.destroyAllWindows()
        os.remove("YourPicture.jpg")
    else:
        print("There is no matching face in the database")
        # 將前面拍的YourPicture照片存入phpMyAdmin資料庫並輸入該照片名稱
        new = input("Enter your name: ")
        os.rename("YourPicture.jpg", new + ".jpg")
        phpMyAdmininput.database_input(new)
