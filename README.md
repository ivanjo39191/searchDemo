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
主要分為三種模式：精確模式、全模式、搜尋引擎模式  
這邊採用搜尋引擎模式

##  配置流程 
###  1.安裝套件  
`pip3 install whoosh haystack jieba `
### 2.配置haystack  
#### 在APP註冊haystack  
``` 
INSTALLED_APPS = [
    ...
    'haystack',
]
 ```
#### 在<settings.py>配置對應的搜索框架  
``` 
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine', #_cn在沒設置好jieba時可以先拿掉
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'   # 索引自動更新
 ```
### 3.配置url路徑  
 `path('search/',include('haystack.urls')),`
### 4.在APP中創建文檔search_indexes.py  
在haystack創建索引時會從應用所在的文檔夾中去尋找這個文檔  
以 類 的形式進行溝通，要創建對於模型的索引，通常取名為 模型名稱+index
類會繼承haystack的信息  
有兩個參數 (創建索引、是否可以創建索引)
後面加上text字段設置模板信息、使用模板傳遞創建字段索引的信息給模型
最後會有兩個方法：  
指名模型類(從哪張表創建索引)、指名字段(從表的哪個數據創建索引)

以下為範例：
```
from haystack import indexes
from Yourapp.models import Yourappmodel


class YourappmodelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Yourappmodel

    def index_queryset(self, using=None):        
        return self.get_model().objects.all()
```
### 5.設置取出的資料欄位
在應用目錄下的templates創建search/indexes/Yourapp/yourappmodel_text.text
取出models中資料表的欄位名稱
以下為範例：  

`{{ object.欄位名稱 }}`  

以下為我使用到的欄位： 
```
{{ object.goodname }}
{{ object.goodprice }}
{{ object.goodshop }}
{{ object.goodtype }}
{{ object.goodlink }}
{{ object.goodimglink }}

```
### 6.設置whoosh搜尋引擎、導入jieba中文分詞  

在該專案虛擬環境的目錄找到\Lib\site-packages\haystack\backends\whoosh_backend.py  
開啟並導入中文分析套件，修改後改名為whoosh_cn_backend.py(若settings的設置原先拿掉_cn須補回)  
以下為範例：  
```
#導入，不可放在第一行  
from jieba.analyse import ChineseAnalyzer
#找到
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=StemmingAnalyzer(), field_boost=field_class.boost, sortable=True)
#修改為
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=ChineseAnalyzer(), field_boost=field_class.boost, sortable=True)
```
### 7.前端頁面配置

這邊只做個基礎的展示

搜尋框：
```
<form role="search" method="get" id="searchform" action="{% url 'haystack_search' %}">
  <input type="search" name="q" placeholder="搜索" required>
  <button type="submit"><span class="ion-ios-search-strong"></span></button>
</form>
```
在search目錄創建search.html：
```
{% extends 'base.html' %}
{% load staticfiles %}
 {% load highlight %}
{% block title %}
商品目錄
{% endblock %}
{% block css %}
<style>
    span.highlighted{
        color: red;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <div>
        <h1>目前查詢的關鍵字為：{% highlight query with query %}</h1>
    </div>
    <div class="row" id="equalheight">
        <div class="col-sm-12 col-md-8 col-md-offset-2">
            {% for result in page %}
            <div class="col-sm-4 col-md-4">
                <div class="ehdiv">
                <div class="thumbnail">
                    <img class="img-responsive" src="{{ result.object.goodimglink }}" alt="{{ good.name }}">
                        <div class="caption">
                        <p>{% highlight result.object.goodname with query %}</p>
                        <p>價格：{{ result.object.goodprice }}</p>
                        <p>類別：<a href="#">{{ result.object.goodtype }}</a></p>
                        <p>賣場：{{ result.object.goodshop }}</p>
                        <p><a href="{{ result.object.goodlink }}" target="_blank" class="btn btn-primary" role="button">前往購買</a> <a href="#" class="btn btn-default" role="button">加入追蹤</a></p>
                    </div>
                </div>
            </div>
            </div>
            {% empty %}
                <div class="no-post"><h2>沒有搜索到相關內容，請重新搜尋</h2></div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```
### 8.建立索引

在專案虛擬環境命令輸入：

python manage.py rebuild_index

建立好後runserver即可成功搜索