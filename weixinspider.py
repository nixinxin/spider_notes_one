#!/usr/bin/env python
# -*- coding;utf-8 -*-
"""
    多线程加队列微信网络爬虫：
    1）总体规划好程序执行的流程，并规划好各线程的关系与作用。本项目中将划分为3个线程。
    2）线程1专门获取对应网址并处理为真实网址，然后将网址写入队列urlqueue中，该队列专门用来存放具体文章的网址。
    3）线程2与线程1并行执行，从线程1提供的文章网址中依次爬取对应文章信息并处理，处理后将我们需要的结果写入对应的本地文件中。
    4）线程3主要用于判断程序是否完成。因为在此若没有一个总体控制的线程，即使线程1、2执行完，也不会退出程序，这不是
       我们想要的结果，所以我们可以建立一个新的线程，专门用来实现总体控制，每次延时60秒，延时后且存放网址的队列
       urlqueue中没有了网址数据，说明线程2已经GET完全部的网址了（不考虑线程1首次无法将网址写入队列的特殊情况，如果爬
       取没问题，60秒的时间完全足够执行完第一次爬取与写入的操作。也不考虑线程2爬取完网址但线程1尚未执行完下一次写入网
       址的操作的情况，因为线程1会比线程2快很多，即使线程1延时较长时间等待线程2的执行，正常情况下，线程1速度仍会比
       线程2快。），即此时已经爬取完所有的文章信息，所以此时可以由线程3控制退出程序。
    5）在正规的项目设计的时候，我们会希望并行执行的线程执行的时间相近，因为这样整个程序才能达到更好的平衡，如果并行
       执行的线程执行时间相差较大，会发生某一个线程早早执行完成，而另一些线程迟迟未完成的情况，这样显然程序不够平衡，
       自然效率以及线程设计有待改进。从这一点来说，本项目仍然有完善的空间。
    6）建立合理的延时机制，比如在发生异常之后，进行相应的延时处理。再比如也可以通过延时机制让执行较快的线程进行延时，
       等待一下执行较慢的线程。
    7）建立合理的异常处理机制。
"""
import threading
import queue
import re
import urllib.request
import time
import urllib.error

urlqueue = queue.Queue()
# 模拟成浏览器
headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko)Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
# 将opener安装为全局
urllib.request.install_opener(opener)
listurl = []


# 使用代理服务器的函数
def use_proxy(proxy_addr, url):
    try:
        proxy = urllib.request.ProxyHandler({'http': proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print("exception:" + str(e))
        time.sleep(1)


# 线程1，专门获取对应网址并处理为真实网址
class geturl(threading.Thread):
    def __init__(self, key, pagestart, pageend, proxy, urlqueue):
        threading.Thread.__init__(self)
        self.pagestart = pagestart
        self.pageend = pageend
        self.proxy = proxy
        self.urlqueue = urlqueue
        self.key = key
    
    def run(self):
        page = self.pagestart
        # 编码关键词key
        keycode = urllib.request.quote(key)
        # 编码"&page"
        pagecode = urllib.request.quote("&page")
        for page in range(self.pagestart, self.pageend + 1):
            url = "http:// weixin.sogou.com/weixin?type = 2&query = " + keycode + pagecode + str(page)
            # 用代理服务器爬取，解决IP被封杀问题
            data1 = use_proxy(self.proxy, url)
            # 列表页url正则
            listurlpat = '<div class = "txt-box">.*?(http:// .*?)"'
            listurl.append(re.compile(listurlpat, re.S).findall(data1))
        # 便于调试
        print("获取到" + str(len(listurl)) + "页")
        for i in range(0, len(listurl)):
            # 等一等线程2，合理分配资源
            time.sleep(7)
            for j in range(0, len(listurl[i])):
                try:
                    url = listurl[i][j]
                    # 处理成真实url，读者亦可以观察对应网址的关系自行分析，采集网址比真实网址多了一串amp
                    url = url.replace("amp;", "")
                    print("第" + str(i) + "i" + str(j) + "j次入队")
                    self.urlqueue.put(url)
                    self.urlqueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e, "code"):
                        print(e.code)
                    if hasattr(e, "reason"):
                        print(e.reason)
                        time.sleep(10)
                except Exception as e:
                    print("exception:" + str(e))
                    time.sleep(1)


# 线程2，与线程1并行执行，从线程1提供的文章网址中依次爬取对应文章信息并处理
class getcontent(threading.Thread):
    def __init__(self, urlqueue, proxy):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
        self.proxy = proxy
    
    def run(self):
        html1 = '''<!DOCTYPE html PUBLIC "-// W3C// DTD XHTML 1.0 Transitional// EN"  "http:// www.w3.org/TR/xhtm
            l1/DTD/xhtml1-transitional.dtd"> <html xmlns = "http:// www.w3.org/1999/xhtml"> <head> <meta http-equi
            v = "Content-Type" content = "text/html; charset = utf-8" /> <title>微信文章页面</title> </head> <body>'''
        fh = open("F:\Python课程\PycharmProjects\spider_notes/2.html", "wb")
        fh.write(html1.encode("utf-8"))
        fh.close()
        fh = open("F:\Python课程\PycharmProjects\spider_notes/2.html", "ab")
        i = 1
        while True:
            url = ''
            try:
                url = self.urlqueue.get()
                data = use_proxy(self.proxy, url)
                titlepat = "<title>(.*?)</title>"
                contentpat = 'id = "js_content">(.*?)id = "js_sg_bar"'
                title = re.compile(titlepat).findall(data)
                content = re.compile(contentpat, re.S).findall(data)
                thistitle = "此次没有获取到"
                thiscontent = "此次没有获取到"
                if title:
                    thistitle = title[0]
                if content:
                    thiscontent = content[0]
                dataall = "<p>标题为:" + thistitle + "</p><p>内容为:" + thiscontent + "</p><br>"
                fh.write(dataall.encode("utf-8"))
                print("第" + str(i) + "个网页处理")  # 便于调试
                i += 1
            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
                    time.sleep(10)
            except Exception as e:
                print("exception:" + str(e))
                time.sleep(1)
            if url is None:
                break
        fh.close()
        html2 = '''</body> </html>         '''
        fh = open("F:\Python课程\PycharmProjects\spider_notes/2.html", "ab")
        fh.write(html2.encode("utf-8"))
        fh.close()


# 并行控制程序，若60秒未响应，并且存url的队列已空，则判断为执行成功
class conrl(threading.Thread):
    def __init__(self, urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
    
    def run(self):
        while True:
            print("程序执行中")
            time.sleep(60)
            if self.urlqueue.empty():
                print("程序执行完毕！")
                exit()


if __name__ == "__main__":
    key = "人工智能"
    proxy = "119.6.136.122:80"
    proxy2 = ""
    pagestart = 1  # 起始页
    pageend = 2  # 爬取到哪页
    # 创建线程1对象，随后启动线程1
    t1 = geturl(key, pagestart, pageend, proxy, urlqueue)
    t1.start()
    # 创建线程2对象，随后启动线程2
    t2 = getcontent(urlqueue, proxy)
    t2.start()
    # 创建线程3对象，随后启动线程3
    t3 = conrl(urlqueue)
    t3.start()