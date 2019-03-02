# searchDemo


## 開發環境  
Ubuntu18.04  
Python3.6  
Django2.0  
## 使用whoosh、haystack、jieba中文分詞進行搜尋功能  
### 搜尋引擎：whoosh  
建立數據索引表  
進行分詞操作  
默認不支援中文分詞  
### 搜尋框架：haystack  
haystack搭載了用戶與搜索引擎之間的橋樑  
將與引擎的接口進行統一的封裝  
haystack的概念：搜索框輸入關鍵字→透過網路方式傳給haystack所對應的接口→查詢後返回值  
### 中文分詞工具：jieba  
