#-*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas
import threading
import sqlite3
import sqlite3 as db
import jieba
import time

def chushihua():
    
    global f
    f = 0   
    global fengebiao
    fengebiao = []   
    global p
    p = 1     
    global qqq
    qqq = 1     
    global qqqq
    qqqq = 1
    global thread
    thread = []   
    global u
    u = 0
    global w
    w = 200
    global hqlj
    hqlj = []
    global jishu    
    jishu = 1
    global huizong
    huizong = []
    global xinwenliebiao
    xinwenliebiao = []
    global x
    x = 0
    global y
    y = 0
    global z
    z = y - x
    global name
    name = ''
    global c
    c = 1
    global k
    k = 0
    global texthuizong
    texthuizong = ""
    global cp
    cp = 0
    
commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format\
=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8\
&page=1&page_size=20'
xinwenliebiaourl = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1486376361414'

def getpinglun(newsurl):
    #填入新闻链接
    m = re.search('doc-i(.+).shtml',newsurl)
    newsid = m.group(1)#获取新闻id
    comments = requests.get(commenturl.format(newsid))#组成新闻的评论链接并下载该页面
    pinglunshu = json.loads(comments.text.strip('var data='))#将页面由json处理
    return pinglunshu['result']['count']['total']

def getnewsdata(newsurl):
    
    global jishu
    result = {}
    global huizong
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    try:
        result['title'] = soup.select("#artibodyTitle")[0].text
    except:
        pass
    try:
        time = soup.select('.time-source')[0].contents[0].strip()   
        result['time'] =  datetime.strptime(time,'%Y年%m月%d日%H:%M')
        result['bianji'] = soup.select('.article-editor')[0].text.lstrip('责任编辑：')
        result['neirong'] = ' '.join([p.text.replace('\u3000','') for p in soup.select('#artibody p')[:-1]])
        result['pinglunshu'] = getpinglun(newsurl)
    except:
        pass
    try:
        soup.select('.time-source span a')[0].text
        result['laiyuan'] = soup.select('.time-source span a')[0].text       
    except:
        laiyuan1 = soup.select('.time-source span ')[0].text
        if len(laiyuan1) == 1:
            result['laiyuan'] = laiyuan1.strip()
        else:
            pass
    print("我获取了第%s条新闻！" % (jishu))

    jishu = jishu + 1
    huizong.append(result)

def getnewsurl(url):
    
    global xinwenliebiao
    res = requests.get(url)
    res.encoding = 'utf-8' 
    try:
        liebiao = json.loads(res.text.lstrip(' newsloadercallback(').rstrip(');'))
    except:
        pass

    else:
        for ent in liebiao['result']['data']:
            xinwenliebiao.append(ent['url'])
    print(liebiao)
    
def shuru():

    global x
    global y
    global name
    global z
    global cp
    
    try:                      
        x = int(input("请输入要抓取的起始页，每页22条新闻（整数，大于等于1）：\n"))   
        y = int(input("请输入要抓取的新闻结束页（整数，大于等于起始页）：\n"))
        cp = int(input("请输入要统计的前TOP几的词频（整数>0<50）：\n"))
        if (((x > 1) or (x == 1)) and (cp > 0) and ( cp < 50)):
            #x -= 1
            y += 1
            #name =  int(input("请输入保存新闻的数据库表名（只能为数字）：\n")):
            z = y - x
        else:
            print('！！！！！这是坠痛苦的！输入错误，请重新输入！！！！！\n')
            return shuru()

        try:
            name =  int(input("请输入保存新闻的数据库表名（只能为数字）：\n"))
            conntest = db.connect('xinwen.sqlite')
            curstest = conntest.cursor()
            sqltest = "select count(*) from sqlite_master where type='table' and name='%s'" % (name)
            curstest.execute(sqltest)
            tabletest = curstest.fetchall()
            if tabletest[0][0] == 1: 
    
                print('！！！！！这是坠痛苦的！数据表已存在，请重新输入！！！！！\n')
                return shuru()
        except:
            print('！！！！！这是坠痛苦的！输入错误，请重新输入！！！！！\n')
            return shuru()
    except:
        print('！！！！！这是坠痛苦的！输入错误，请重新输入！！！！！\n')
        return shuru()
    else:
        getlink()
        
def getlink():
    
    global c
    global hqlj
    global x
    global y 
    t = y
    global z 
    #z = y - u 
    print(x,y,z)
    for i in range(x-1,y):
        newsurl = xinwenliebiaourl.format(i)
        
        t = threading.Thread(target=getnewsurl,
                                 args=(newsurl,))       
        hqlj.append(t)
    print(len(hqlj))
        
def liebiaoxunhuan():
    
    global c  
    global u     
    global w 
    global z
    global y
    global x
    global hqlj
    global b 
    z = y - x
    global k
    print(z)
    print(u,w)    
    if z >= 200:
        for i in range(u,w):
                #print(i)
            hqlj[i].start()
            print("excited！正在获取第%s页的新闻列表---！" %(c))
            c += 1
        print("等待获取新闻链接...")
            
        for i in range(u,w):
                
            hqlj[i].join()
            
        x += 200
        k += 200
        b = y - x

        if b >= 200:
            w += 200
            u += 200
        else:
            return liebiaoxunhuan()
       
        return liebiaoxunhuan()
        
    else:

        if (y - x) < 200:
            if k > 0:
                for i in range(w,w+b-1):
                    hqlj[i].start()
                    print("excited！正在获取第%s页的新闻列表！" %(c))
                    c += 1
            
                print("等待获取新闻链接!!!!!!!!!!")
                for i in range(w,w+b-1):
                    hqlj[i].join()
                return fengexiazai()
            else:
                
                for i in range(0,y-x):
                        #print(i)
                    hqlj[i].start()
                    print("excited！正在获取第%s页的新闻列表！" %(c))
                    c += 1
                
                print("等待获取新闻链接...")
                    
                for i in range(0,y-x):
                        
                    hqlj[i].join()
                return fengexiazai()

def fengexiazai():
    
    global f
    global zongshu
    global m
    global fengebiao
    global xinwenliebiao
    global p
    zongshu = len(xinwenliebiao)
    if zongshu > 300:
        print("分段获取内容")
        fengebiao = xinwenliebiao[0:300]
        f = len(fengebiao)
        xinwenliebiao = xinwenliebiao[300: ]
        xiazaixiancheng(fengebiao)
        print("第%s次获取!" %(p))
        p += 1
        return fengexiazai()

    else:
        print("即将获取完成！这是坠吼的！")
        f = len(xinwenliebiao)
        xiazaixiancheng(xinwenliebiao)
                 
def xiazaixiancheng(fengebiao):
    
    thread = [] 
    global w
    global qqq
    global qqqq
    for i in range(0,f):
        newsurl = fengebiao[i]
        print("线程已分配第%s条新闻链接，滋呲不滋呲啊？" %(qqq))

        xz1 = threading.Thread(target=getnewsdata,
                               args=(newsurl,))
        thread.append(xz1)
        qqq += 1
    for i in range(0,f):
        thread[i].start()
        print("我按照基本法启动了第%s个线程获取新闻内容！" %(qqqq))
        qqqq += 1
 
    for i in range(0,f):
        thread[i].join()
        
def cipin(texthuizong):
    
    global tongji
    texthuizong = re.sub("[A-Za-z0-9\[\`\~\！\@\#\$\^\&\*\（\）\=\|\{\}\'\：\；\原标题\-\'\，\[\]\.\<\>\/\?\~\！\@\、\#\\\&\*\%]", "", texthuizong)
    tongji = {}
    ShuiBa_word_list = []
    ShuiBa_word_set = set()
    texthuizong = texthuizong.replace(' ', '')
    texthuizong = texthuizong.strip('\n')
    word_list = jieba.lcut(texthuizong, cut_all=False) 
    word_set = set(word_list)
    ShuiBa_word_list = ShuiBa_word_list + word_list
    ShuiBa_word_set = ShuiBa_word_set.union(word_set)
    
    for word in ShuiBa_word_set:
        if len(word) > 1:
            fre = ShuiBa_word_list.count(word)
            tongji[word] = int(fre)
    tongji = sorted(tongji.items(), key=lambda d:d[1], reverse = True)
    #print(tongji)
    return(tongji)

def yunxing(): 
    
    global u 
    global w 
    global z 
    global x
    global k
    global b
    global texthuizong
    global cp
    texthuizong = ""
    print('-------------新浪新闻抓取程序，搞个大新闻！-------------\n')
    print('------请用管理员权限运行，否则将无法保存新闻，安姆安格瑞！------\n')
    chushihua()  
    shuru()
    u = 0
    w = 200
    z = y - x
    k = 0
    b = 1
    now = datetime.now()   
    liebiaoxunhuan()
    zongshu = len(huizong)
    
    print(zongshu) 
    df = pandas.DataFrame(huizong)
    name1 = str(name) 
    with sqlite3.connect('xinwen.sqlite') as db:
        df.to_sql(name1, con = db)
    db.close()
    name2 = name1 + "cipin"
    end = datetime.now()
    for i in huizong:
        texthuizong += i["neirong"]
    print("正在进行词频统计------------------------------")
    cipin(texthuizong)
    print("词频统计完成！！！！！！！！！！！！！！！！！！！！！！！！\n")
    cipinxieru = pandas.DataFrame(tongji[0:cp])
    with sqlite3.connect('xinwen.sqlite') as db2:
        cipinxieru.to_sql(name2, con = db2)
    db2.close()
    
    print(now)
    print(end)
    print("程序耗时： " + str(end-now) + "\n" + "\n新闻存放在本程序所在目录的xinwen sqlite数据库%s数据表中\n词频数据存放在%scipin数据表中\n" %(name1,name1))
    jieshu = input("输入r重新运行本程序，继续学习一个！输入其他字符结束程序！\n")
    if jieshu == "r":
        yunxing()
        

yunxing()




