# Project_GUI
- 執行前先手動將im0資料夾(包含圖片)放到和main.py同一層的位置
- 之後執行 python main.py 即可
- 有設定.gitignore 執行後增加的"__pycache__"資料夾及"im0"資料夾不會被加到git中
# 修改 interface 設計
1. 使用 qt designer [參考連結](https://www.itread01.com/content/1547572153.html) 打開GUI_template.ui
 (anaconda 似乎有內建。[參考連結](http://elmer-storage.blogspot.com/2018/04/pyqt.html))
2. 更改好設計後儲存(盡量不要刪除已經存在的物件和改動已經存在的物件名稱，改變位置、大小隨意)
3. 執行 pyuic5 -x GUI_template.ui -o GUI_template.py 
4. 執行 python main.py 應該可以看到新設計的頁面
