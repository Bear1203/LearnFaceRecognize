import numpy as np
import time
import cv2
from skimage.transform import resize


# 圖像白化（whitening）可用於對過度曝光或低曝光的圖片進行處理，處理的方式就是改變圖像的平均像素值為 0 ，改變圖像的方差為單位方差 1
def prewhiten(x):
    if x.ndim == 4:
        axis = (1, 2, 3)
        size = x[0].size

    elif x.ndim == 3:
        axis = (0, 1, 2)
        size = x.size

    else:
        raise ValueError("Dimension should be 3 or 4")

    mean = np.mean(x, axis=axis, keepdims=True)
    std = np.std(x, axis=axis, keepdims=True)
    std_adj = np.maximum(std, 1.0/np.sqrt(size))
    y = (x - mean) / std_adj

    return y


# 使用L1或L2標準化圖像，可強化其特徵
def l2_normalize(x, axis=-1, epsilon=1e-10):
    output = x / np.sqrt(np.maximum(np.sum(np.square(x),
                                           axis=axis, keepdims=True), epsilon))

    return output


# 偵測並取得臉孔area，接著再resize為模型要求的尺寸(下方例子並未作alignment)
def align_image(img, margin, cascade_path):
    cascade = cv2.CascadeClassifier(cascade_path)
    faces = cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=3)
    aligneds = []

    if(len(faces) > 0):
        for face in faces:
            (x, y, w, h) = face
            face = img[y:y+h, x:x+w]
            faceMargin = np.zeros((h+margin*2, w+margin*2, 3), dtype="uint8")
            faceMargin[margin:margin+h, margin:margin+w] = face
            aligned = resize(
                faceMargin, (160, 160), mode="reflect")
            aligneds.append(aligned)

        return aligneds

    else:

        return None


# 圖像的預處理(即前述的幾項步驟)
def preProcess(img):
    whitenImg = prewhiten(img)
    whitenImg = whitenImg[np.newaxis, :]

    return whitenImg
