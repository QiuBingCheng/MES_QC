# MES_QC

## 簡介

**MES**（Manufacturing Execution System） 中文名稱為「製造執行系統」，能通過生產線的生產資訊的傳遞，從訂單下達到產品完成的整個生產過程的管理中獲得更有效的管理訊息。其中的核心模組包含 **WIP在製品管理系統**，**QC品質管理系統**，**MMS物料管理系統**。該repository展示的為其中的**QC品質管理系統**的介面雛形。

## 原理

以Django架設網站，撰寫前端統計監看頁面，當使用者填寫表單內容(產品編號、抽樣起始日等)，送出表單之際，觸發jQuery ajax call，後端判斷為POST請求，接受表單相關參數，提取sqlite資料庫產品數據，再使用controlchart module，計算出管制界限，繪製成管制圖表，最後將圖表參數打包成json格式，回傳到前端html，展示給使用者監看。

具備技能：<br>

+ Django架設網站
+ 基礎的html、css應用
+ 基礎的javascripts、jQuery、Ajax、Highchart應用
+ 熟稔SQL語法，清楚如何從資料庫提取資料。
+ 熟稔numpy套件，能夠有效梳理表單送出的數據。
+ 熟稔品質管制的觀念。

## 流程說明

### 範例一：平均管制圖

### 1.請使用者填入表單參數

![1](<https://github.com/vbjc5275/MES_QC/raw/master/image/1.jpg>)

###  2.展示管制圖

![2](<https://github.com/vbjc5275/MES_QC/raw/master/image/2.jpg>)

### 範例二：全距管制圖

### 1.請使用者輸入參數

![3](<https://github.com/vbjc5275/MES_QC/raw/master/image/3.jpg>)

### 2.請使用者輸入參數

![4](<https://github.com/vbjc5275/MES_QC/raw/master/image/4.jpg>)

## 附註

此MES系統會在近日正式部屬到實驗室伺服器，原先考慮先行使用Heroku，以展示此作品，但因為Heroku不支持Sqlite資料庫，倘若堅持整合，曠日廢時，唯恐趕不上履歷表期限，因此先以文字輔以圖片說明，造成不便，敬請見諒！

