# 學習人臉識別
## 參考資料
[人臉辨識模型-google-facenet-介紹與使用](https://chtseng.wordpress.com/2018/12/09/%E7%95%B6%E7%B4%85%E7%9A%84%E4%BA%BA%E8%87%89%E8%BE%A8%E8%AD%98%E6%A8%A1%E5%9E%8B-google-facenet-%E4%BB%8B%E7%B4%B9%E8%88%87%E4%BD%BF%E7%94%A8/)
## 本作品介紹
  為了記錄學習研究內容，分享研究內容和充實作品集而打此篇GitHub。此作品功能為
1. 拍攝一張照片後，從資料庫中比對人臉，辨識圖片中的人並印出資料庫此人的名字。`picture_face_recognize.py`
2. 即時影像辨識人臉，但太多人同框會導致計算複雜而幀數降低，也許待優化。`video_face_recognize.py`
3. 可先匯入圖片進資料庫。`start_database_input.py`
 - 確保資料庫中至少有一張人臉資料供比對
## 使用工具
| 工具 | 簡介 |
| --- | --- |
| [ANACONDA](https://www.anaconda.com/products/individual) | 虛擬環境 |
| [VS CODE](https://code.visualstudio.com/) | 程式碼編輯器 |
| [WAMPSERVER](https://www.wampserver.com/) | 方便連接phpmyadmin，MYSQL資料庫 |
## 本作品使用步驟
1. 在虛擬環境中下載所需套件程式庫，`requirement.txt`此檔案裡有寫需要哪些東西。
2. 建立MYSQL資料庫並建好表單以及欄位，本作品資料庫名稱設為facenet、表單設為face_name_images、欄位則設為Name與Image兩個，一個放名字一個放照片檔。
3. 確保資料庫中至少有一張人臉資料供比對。
4. 照使用者需求在環境中執行作品介紹裡的各個python檔。
# :bowtie::laughing:謝謝閱讀:laughing::bowtie:
### P.S. 程式碼內有些註解，但沒有全部每一行都註解說明，也許之後有時間再更新:relieved:。
