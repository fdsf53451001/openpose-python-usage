# openpose-python-usage

## 功能
對一段運動影片做骨架分析，往往會辨識到觀眾，或路過的其他人。所以我們設計了yolo模型專門區分運動員、評審和其他人物。本專案的目的在於結合兩者的輸出，將非運動員的骨架自openpose辨識的結果中刪除。

如果openpose辨識的人物在yolo的運動員辨識框時，保留骨架 ;
如果不在辨識框內，則視為路人，刪除骨架。

最後將檔案重新存回資料夾，及完成比對。

## 資料集格式
資料集來自 https://github.com/mostafa-saad/deep-activity-rec

![圖片](https://user-images.githubusercontent.com/35889113/169795826-995cdb30-0267-4416-9dad-5956c022ecdd.png)

## 資料格式
Openpose : json in txt file (格式可以參考：https://blog.csdn.net/qq_35649669/article/details/97786303)

Yolo : txt file (yolo format, xywh)

Openpose Result : json in txt file (the same format as origin one)

## 執行
* YOLO辨識

（1）將yolo_recognize/detect.py & yolo_recognize/yolo_detect_dataset.py 放到YOLO資料夾中

（2）修改路徑（yolo_detect_dataset.py）

![圖片](https://user-images.githubusercontent.com/35889113/169798993-c959d38c-ed18-43f8-9644-e2bb6ca830b9.png)

（3）執行
```
python detect_dataset.py
```
