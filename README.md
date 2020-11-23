# Project_GUI
- 專題 : 魚眼鏡頭照片的車輛偵測及追蹤，使用python opencv為主，GUI介面使用pyqt呈現。
- [data set link](https://drive.google.com/drive/folders/10VRH7mm2EMXI10Yi6VELsfOvRtMJge1V?usp=sharing)
- 執行前先手動將im0資料夾(包含圖片)放到和main.py同一層的位置
- 之後執行 python main.py 即可
- 有設定.gitignore 執行後增加的"__pycache__"資料夾及"im0"資料夾不會被加到git中
# 修改 interface 設計
1. 使用 qt designer [參考連結](https://www.itread01.com/content/1547572153.html) 打開GUI_template.ui
 (anaconda 似乎有內建。[參考連結](http://elmer-storage.blogspot.com/2018/04/pyqt.html))
2. 更改好設計後儲存(盡量不要刪除已經存在的物件和改動已經存在的物件名稱，改變位置、大小隨意)
3. 執行 pyuic5 -x GUI_template.ui -o GUI_template.py 
4. 打開GUI_template.py import Class/image.py 中的 MyLabel class
5. 將GUI_template.py self.img_label1 的 constructor 改成 MyLabel(Dialog)
6. 執行 python main.py 應該可以看到新設計的頁面
# 資料夾說明
- Class資料夾放header file(EX. main.py 要import 的 module 放在image.py中)
- create_data資料夾放用來產生 data file的module，從 main.py call 進去，寫的時候路徑以main.py的位置當作root
- data資料夾放 data file
- result_data資料夾放各種車輛偵測、實驗的結果
- im0資料夾放圖片(資料夾內檔名任意皆可，以有序的編號為佳)
