from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import GoodsType, GoodsDetail
import json
import time

millis = int(round(time.time() * 1000))


def good_common_data(request, good_all_list):
    # 將資料進行分頁
    paginator = Paginator(good_all_list, 9)
    # 獲取url頁面參數
    page_num = request.GET.get('page', 1)
    # 自動識別頁碼
    page_of_goods = paginator.get_page(page_num)
    # 當前頁碼
    current_page_num = page_of_goods.number
    # 當前頁碼的資料
    currnt_good_list = page_of_goods.object_list
    # 頁碼範圍
    page_range = list(range(max(1, current_page_num - 2), current_page_num)) + \
                 list(range(current_page_num, min(paginator.num_pages, current_page_num + 2) + 1))
    # 加入省略符號
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if page_range[-1] + 2 <= paginator.num_pages:
        page_range.append('...')
    # 加入首頁末頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    goodtypes = GoodsType.objects.all()
    context = {}
    context['goods'] = currnt_good_list
    context['goodtypes'] = goodtypes
    context['page_range'] = page_range
    context['page_of_goods'] = page_of_goods
    return context
def good_list(request,order=None):


    good_all_list = GoodsDetail.objects.all()

    context = {}
    context = good_common_data(request, good_all_list)

    return render(request, "good_list.html", context)



def pcgood(pccid, page, pcclname):
    url = 'https://ecapi.pchome.com.tw/mall/prodapi/v1/newarrival/prod&region=' + str(pccid) + '&offset=' + str(
        page) + '&limit=50&_callback=jsonpcb_newarrival'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'  # 偽裝使用者
    headers = {'User-Agent': user_agent,
               'server': 'PChome/1.0.4',
               'Referer': 'https://mall.pchome.com.tw/newarrival/'}
    res = requests.get(url=url, headers=headers)  # 分析得出的網址
    res_text = res.text
    res_text_format = res_text.replace('try{jsonpcb_newarrival(', '').replace(
        ');}catch(e){if(window.console){console.log(e);}}', '')
    jd = json.loads(res_text_format)
    if jd['Rows'] != []:
        pcgoods = (jd['Rows'][:])
        for pcgood in pcgoods:
            pcname = pcgood['Name']
            pcimg = 'https://b.ecimg.tw' + pcgood['Pic']['S']
            pcprice = pcgood['Price']['P']
            pclink = 'https://mall.pchome.com.tw/prod/' + pcgood['Id']
            pcshop = 'PChome購物中心'
            if pcclname == '運動戶外':
                pcclname = '運動休閒'
            if pcclname == '生活':
                pcclname = '居家生活'
            if pcclname == '時尚':
                pcclname = '鞋包配飾'
            print(pcname)
            print(pcimg)
            print(pcprice)
            print(pclink)
            print('分類：' + pcclname)
            pchomesql(pcname, pcprice, pcclname, pcshop, pcimg, pclink)
    else:
        status = 'no_data'
        return status


def pchomesql(pcname, pcprice, pcclname, pcshop, pcimg, pclink):
    goodname = pcname
    goodprice = pcprice
    goodshop = pcshop
    goodtype = pcclname
    goodlink = pclink
    goodimglink = pcimg

    try:
        typename = GoodsType.objects.get(type_name=goodtype)
        print('存入分類')
    except:
        typename = GoodsType.objects.create(type_name=goodtype)
        print('創建分類')
    typename.save()

    try:
        pcdb = GoodsDetail.objects.get(goodlink=goodlink)
        pcdb.goodname = goodname
        pcdb.goodprice = goodprice
        pcdb.goodshop = goodshop
        pcdb.goodtype = typename
        pcdb.goodlink = goodlink
        pcdb.goodimglink = goodimglink
        pcdb.save()
        print('更新資料')
    except:
        momodb = GoodsDetail.objects.create(goodname=goodname, goodprice=goodprice, goodshop=goodshop,
                                            goodtype=typename, goodlink=goodlink, goodimglink=goodimglink)
        momodb.save()
        print('成功存入一筆資料')


# 分類、頁數遍歷
# 分析後，網址結尾需加上13位unix時間戳記

def pchomecrawler(request):
    url = 'https://ecapi.pchome.com.tw/mall/cateapi/v1/sign&tag=newarrival&fields=Id,Name,Sort,Nodes&_callback=jsonpcb_newarrival&' + str(
        millis)
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'  # 偽裝使用者
    headers = {'User-Agent': user_agent,
               'server': 'PChome/1.0.4',
               'Referer': 'https://mall.pchome.com.tw/newarrival/'}
    res = requests.get(url=url, headers=headers)  # 分析得出的網址
    res_text = res.text
    res_text_format = res_text.replace('try{jsonpcb_newarrival(', '').replace(
        ');}catch(e){if(window.console){console.log(e);}}', '')
    jd = json.loads(res_text_format)
    pcclass = jd[0:1]
    # print(pc)
    for pc in pcclass:
        pcclname = pc['Name']
        print(pc['Name'])
        for pccl in pc['Nodes']:
            pccid = pccl['Id']
            pageid = 1
            for page in range(10):
                print(page)
                if pcgood(pccid, pageid, pcclname) != 'no_data':
                    pcgood(pccid, pageid, pcclname)
                    pageid = pageid + 50
                    time.sleep(8)
                else:
                    break