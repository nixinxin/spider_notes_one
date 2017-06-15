# !/usr/bin/env python
#  -*- coding;utf-8 -*-
"""
    网络爬虫类型：1、通用网络爬虫。2、聚焦网络爬虫（主题网络爬虫）。3、增量式网络爬虫。4、深层网络爬虫
    1、通用网络爬虫
        通用网络爬虫首先我们来看通用网络爬虫的实现原理。通用网络爬虫的实现原理及过程可以简要概括如下（见图3-1）。
            1）获取初始的URL。初始的URL地址可以由用户人为地指定，也可以由用户指定的某个或某几个初始爬取网页决定。
            2）根据初始的URL爬取页面并获得新的URL。获得初始的URL地址之后，首先需要爬取对应URL地址中的网页，爬取了
               对应的URL地址中的网页后，将网页存储到原始数据库中， 并且在爬取网页的同时，发现新的URL地址，同时将已爬
               取的URL地址存放到一个URL列表中，用于去重及判断爬取的进程。
            3）将新的URL放到URL队列中。在第2步中，获取了下一个新的URL地址之后，会将新的URL地址放到URL队列中。
            4）从URL队列中读取新的URL，并依据新的URL爬取网页，同时从新网页中获取新URL，并重复上述的爬取过程。
            5）满足爬虫系统设置的停止条件时，停止爬取。在编写爬虫的时候，一般会设置相应的停止条件。如果没有设置停止条件，
               爬虫则会一直爬取下去，一直到无法获取新的URL地址为止，若设置了停止条件，爬虫则会在停止条件满足时停止爬取。
    2、聚焦网络爬虫（主题网络爬虫）
        聚焦网络爬虫，由于其需要有目的地进行爬取，所以对于通用网络爬虫来说，必须要增加目标的定义和过滤机制，具体来说，
        此时，其执行原理和过程需要比通用网络爬虫多出三步，即目标的定义、无关链接的过滤、下一步要爬取的URL地址的选取等，
        如图3-2所示。
            1）对爬取目标的定义和描述。首先要依据爬取需求定义好该聚焦网络爬虫爬取的目标，以及进行相关的描述。
            2）获取初始的URL。
            3）根据初始的URL爬取页面，并获得新的URL。
            4）从新的URL中过滤掉与爬取目标无关的链接。因为聚焦网络爬虫对网页的爬取是有目的性的，所以与目标无关的网页将会
               被过滤掉。同时，也需要将已爬取的URL地址存放到一个URL列表中，用于去重和判断爬取的进程。
            5）将过滤后的链接放到URL队列中。
            6）从URL队列中，根据搜索算法，确定URL的优先级，并确定下一步要爬取的URL地址。在通用网络爬虫中，下一步爬取哪些
               URL地址，是不太重要的，但是在聚焦网络爬虫中，由于其具有目的性，故而下一步爬取哪些URL地址相对来说是比较重要
               的。对于聚焦网络爬虫来说，不同的爬取顺序，可能导致爬虫的执行效率不同，所以，我们需要依据搜索策略来确定
               下一步需要爬取哪些URL地址。
            7）从下一步要爬取的URL地址中，读取新的URL，然后依据新的URL地址爬取网页，并重复上述爬取过程。
            8）满足系统中设置的停止条件时，或无法获取新的URL地址时，停止爬行。
    3、爬行策略：深度优先爬行策略、广度优先爬行策略、大站优先爬行策略、反链策略、其他策略。
    4、网页更新策略：用户体验策略、历史数据策略、聚类分析策略
    5、网页分析算法
        1）基于用户行为的网页分析算法
        2）基于网络拓扑的网页分析算法
            （1）基于网页粒度的分析算法，pageRank，谷歌搜索引擎的核心算法
            （2）基于网页块粒度的分析算法
            （3）基于网站粒度的分析算法
        3、基于网页内容的网页分析算法
        
    网络爬虫由控制节点（中央控制器）、爬虫节点、资源库组成。
            
    Urllib是python提供的用于操作URL的模块：
        import urllib.request
        file  =  urllib.request.urlopen("网址")
        data  =  file.read() 读取文件的全部内容，read会把读取到的内容赋给一个字符串变量。
        dataline  =  file.readline()  读取文件的一行内容
        dataline  =  file.readlines()  读取文件的全部内容，readlines会把读取到的内容赋给一个列表变量(推荐使用这种方式)
            
        我们还可以使用urllib.request里面的urlretrieve（）函数直接将对应信息写入本地文件，格式为：
            urllib.request.urlretrieve（url，filename = 本地文件地址）。
            urllib在使用中会造成一定的缓存，可用该语句清理：urllib.request.urlcleanup()
        
        url编码：urllib.request.quote()
            urllib.request.quote("http:// www.sina.com.cn")      >>> 'http%3A// www.sina.com.cn'
        url解码：
            urllib.request.unquote("http%3A// www.sina.com.cn")  >>>  'http:// www.sina.com.cn'

            
    模拟浏览器登录：
        1、使用build_opener()修改报头
            import urllib.request
            url =  "http:// blog.csdn.net/weiwei_pig/article/details/51178226"
            headers = ("User-Agent",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
                Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
            opener  =  urllib.request.build_opener()
            opener.addheaders  =  [headers]
            data  =  opener.open(url).read()
            fhandle  =  open("D:/Python35/myweb/part4/3.html","wb")
            fhandle.write(data)
            fhandle.close()
            
            1中使用的是addheaders（）方法。
            2中使用的是add_header（）方法，注意末尾有无s以及有无下划线的区别。
            
        2：使用add_header（）添加报头
            import urllib.request
            url =  "http:// blog.csdn.net/weiwei_pig/article/details/51178226"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/ 537.36 (KHTML, like Gecko)
                Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
            data = urllib.request.urlopen(req).read()
            
    超时设置：file = urllib.request.urlopen("http:// yum.iqianyue.com",timeout = 1)
    
    Http请求协议：
        (1）GET请求：直接在URL中写上要传递的信息，也可以由表单进行传递。如果使用表单进行传递，这表单中的信息会自动转为URL地址中的数据，通过URL地址传递。
            1）构建对应的URL地址，地址包含GET请求的字段名和字段内容等信息，并且URL地址满足GET请求的格式，即“http://网址？字段名1 = 字段内容1&字段名2 = 字段内容2”。
            2）以对应的URL为参数，构建Request对象。
            3）通过urlopen（）打开构建的Request对象。
            4）按需求进行后续的处理操作，比如读取网页的内容、将内容写入文件等。
                import urllib.request
                url = "http:// www.baidu.com/s?wd = " key = "百度"
                key_code = urllib.request.quote(key)   #  注意对非ascii网址内容编码
                url_all = url+key_code
                req = urllib.request.Request(url_all)
                data = urllib.request.urlopen(req).read()
                fh = open("D:/Python35/myweb/part4/5.html","wb")
                fh.write(data)
                fh.close()
        (2）POST请求：可以向服务器提交数据，是一种比较主流也比较安全的数据传递方式，比如在登录时，经常使用POST请求发送数据。
            1）设置好URL网址。
            2）构建表单数据，并使用urllib.parse.urlencode对数据进行编码处理。
            3）创建Request对象，参数包括URL地址和要传递的数据。
            4）使用add_header（）添加头信息，模拟浏览器进行爬取。
            5）使用urllib.request.urlopen（）打开对应的Request对象，完成信息的传递。
            6）后续处理，比如读取网页内容、将内容写入文件等。
                import urllib.request
                import urllib.parse
                url  =  "http:// www.iqianyue.com/mypost/"
                #  将表单数据进行urlencode编码处理后，使用encode()设置为utf-8编码
                postdata  = urllib.parse.urlencode({ "name":"nideshengri", "pass":"783211aa" }).encode('utf-8')
                req  =  urllib.request.Request(url,postdata)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/ 537.36
                (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
                data = urllib.request.urlopen(req).read()
                fhandle = open("D:/Python35/myweb/part4/6.html","wb")
                fhandle.write(data) fhandle.close()
                
        (3）PUT请求：请求服务器存储一个资源，通常要指定存储的位置。
        (4）DELETE请求：请求服务器删除一个资源。
        (5）HEAD请求：请求获取对应的HTTP报头信息。
        (6）OPTIONS请求：可以获得当前URL所支持的请求类型。
        除此之外，还有TRACE请求与CONNECT请求等，TRACE请求主要用于测试或诊断。
        
    代理IP地址：
        def use_proxy(proxy_addr,url):
            import urllib.request
            proxy =  urllib.request.ProxyHandler({'http':proxy_addr})
            opener  =  urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            #  创建全局默认的opener对象，那么，在使用urlopen()时亦会使用我们安装的opener对象
            urllib.request.install_opener(opener)
            data  =  urllib.request.urlopen(url).read().decode('utf-8')
            return data
            
        proxy_addr = "202.75.210.45:7777"
        data = use_proxy(proxy_addr,"http:// www.baidu.com")
        print(len(data))
            
    在程序运行的过程中，边运行边打印调试日志：
        1）分别使用urllib.request.HTTPHandler（）和urllib.request.HTTPSHandler（）将debuglevel设置为1。
        2）使用urllib.request.build_opener（）创建自定义的opener对象，并使用1）中设置的值作为参数。
        3）用urllib.request.install_opener（）创建全局默认的opener对象，这样，在使用urlopen（）时，也会使用我们安装的opener对象。
        4）进行后续相应的操作，比如urlopen（）等。
            
            import urllib.request
            httphd = urllib.request.HTTPHandler(debuglevel = 1)
            httpshd = urllib.request.HTTPSHandler(debuglevel = 1)
            opener = urllib.request.build_opener(httphd,httpshd)
            urllib.request.install_opener(opener)
            data = urllib.request.urlopen("http:// edu.51cto.com")
            
    UrlError异常处理：
        第一个类是URLError类。
        第二个类是URLError类的一个字类 -- HTTPError类。
        
        一般来说，产生URLError的原因有如下几种可能：
            1）连接不上服务器
            2）远程URL不存在
            3）无网络
            4）触发了HTTPError
        
        import urllib.request
        import urllib.error
        try:
            urllib.request.urlopen("http:// blog.csdn.net")
        except urllib.error.HTTPError as e:
            #  前三个异常没有状态码
            if hasattr(e,"code"):
                print(e.code)
            if hasattr(e,"reason"):
                print(e.reason)
                
    常见的状态码及含义：
        200 OK     一切正常
        301 Moved Permanently     重定向到新的URL，永久性
        302 Found     重定向到临时的URL，非永久性
        304 Not Modified     请求的资源未更新
        400 Bad Request     非法请求
        401 Unauthorized     请求未经授权
        403 Forbidden     禁止访问
        404 Not Found     没有找到对应页面
        500 Internal Server Error     服务器内部出现错误
        501 Not Implemented     服务器不支持实现请求所需要的功能
            
    正则表达式基础知识：
        1.原子，是正则表达式中最基本的组成单位，每个正则表达式中至少要包含一个原子，常见的原子有以下几类：
            1）普通字符作为原子(字母、数字、下划线)。
            
            2）非打印字符作为原子。
                在一些字符串中用于格式控制的符号，、\n(匹配一个换行符)、\t(匹配一个制表符)
                
            3）通用字符作为原子，一个原子可以匹配一类字符。
                \w  匹配任意一个字母、数字或下划线 \W 否
                \d  匹配任意一个十进制数           \D 否
                \s  匹配任意一个空白字符           \S 否
            
            4）原子表。
                定义一组地位平等的原子，然后匹配的时候会取该原子表中的任意一个原子进行匹配，在Python中，原子表由[]表示。
                [xyz]表示匹配里面任一个字符
                [^]代表的是除了中括号里面的原子均可以匹配，比如“[^xyz]py”能匹配“apy”，但是却不能匹配“xpy
            
        2、元字符，就是正则表达式中具有一些特殊含义的字符，比如重复N次前面的字符等。
            .  匹配除换行符以外的任一字符     任意匹配元字符
            ^  匹配字符串的开始位置           边界限制元字符
            $  匹配字符串的结束位置           边界限制元字符
            *  匹配前面的原子 > = 0 次          限定符
            ?  匹配前面的原子 0或1 次         限定符
            +  匹配前面的原子 > = 1 次          限定符
            {n, m} 匹配前面的原子 n = < 匹配原子  = < m 限定符
            |  模式选择符                     任选一个匹配
            () 模式单元符                     括号内的部分被当做整体使用
            
        3、模式修正符
            在不改变正则表达式的情况下，通过模式修正符改变正则表达式的含义，从而实现一些匹配结果的调整等功能。
            re.I  匹配时忽略大小写
            re.M  多行匹配
            re.L  本地化识别匹配
            re.U  根据Unicode字符及解析字符
            re.S  让"."匹配任一字符，包括换行符
                import re
                pattern1 = "python"
                pattern2 = "python"
                string = "abcdfphp345Pythony_py"
                result1 = re.search(pattern1,string)
                result2 = re.search(pattern2,string,re.I)
                print(result1) None
                print(result2) python
                
        4、贪婪模式与懒惰模式
            贪婪模式的核心点就是尽可能多地匹配，而懒惰模式的核心点就是尽可能少地匹配。
                import re
                pattern1 = "p.*y"# 贪婪模式
                pattern2 = "p.*?y"# 懒惰模式
                string = "abcdfphp345pythony_py"
                result1 = re.search(pattern1,string)
                result2 = re.search(pattern2,string)
                print(result1)  php345pythony_py
                print(result2)  php345py
                
                默认贪婪模式转化为懒惰模式方法：p.*y >>> p.*?y  加一个问号
                
        5、正则表达式函数
            (1) re.match(pattern,string,flag) 从原字符串起始位置匹配，只返回一个结果
                第一个参数代表对应的正确表达式
                第二个参数代表对应的源字符
                第三个参数是可选参数，代表对应的标志位，可以放模式修正符
                    import re
                    string = "apythonhellomypythonhispythonourpythonend"
                    pattern = ".python."
                    result = re.match(pattern,string)
                    result2 = re.match(pattern,string).span()
                    print(result)   返回匹配详细信息
                    print(result2)  返回匹配字符的位置
                
            (2) re.search() 扫描整个字符串进行匹配，只返回一个结果
            
            (3) 全局匹配函数，输出一个列表
                1）使用re.compile（）对正则表达式进行预编译。
                2）编译后，使用findall（）根据正则表达式从源字符串中将匹配的结果全部找出。
                    import re
                    string = "hellomypythonhispythonourpythonend"
                    pattern = re.compile(".python.") #  预编译
                    result = pattern.findall(string) #  找出符合模式的所有结果
                    #  result = re.compile(pattern).findall(string)
                    print(result)
            (4) re.sub()函数
                re.sub(pattern, rep, string, max)
                    第一个参数为对应的正则表达式，
                    第二个参数为要替换成的字符串，
                    第三个参数为源字符串，
                    第四个参数为可选项，代表最多替换的次数，如果忽略不写，则会将符合模式的结果全部替换。
                        import re
                        string = "hellomypythonhispythonourpythonend"
                        pattern = "python."
                        result1 = re.sub(pattern,"php",string)
                        #  全部替换
                        result2 = re.sub(pattern,"php",string,2)
                        #  最多替换两次
                        print(result1)
                        print(result2)
    Coolie与Session:
        如果是通过Cookie保存会话信息，此时会将所有的会话信息保存在客户端.
        如果是通过Session保存会话信息，会将对应的会话信息保存在服务器端.
        使用Session的方式来保存会话信息，大部分的时候，还是会到Cookie.
        
        使用Python处理Cookie，在Python3中可以使用Cookiejar库进行处理，而在Python2则可以使用Cookielib库进行处理。
        进行Cookie处理的一种常用思路如下：
            1）导入Cookie处理模块http.cookiejar。
            2）使用http.cookiejar.CookieJar（）创建CookieJar对象。
            3）使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象。
            4）创建全局默认的opener对象。
                import urllib.request
                import urllib.parse
                import http.cookiejar
                url = "http:// bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash = L768q"
                postdata = urllib.parse.urlencode({ "username":"weisuen", "password":"aA123456" }).encode('utf-8')
                req  =  urllib.request.Request(url,postdata)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/ 537.36
                    (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
                #  使用http.cookiejar.CookieJar()创建CookieJar对象
                cjar = http.cookiejar.CookieJar()
                #  使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
                #  将opener安装为全局
                urllib.request.install_opener(opener)
                file = opener.open(req)
                data = file.read()
                file = open("D:/Python35/myweb/part5/3.html","wb")
                file.write(data) file.close()
                url2 = "http:// bbs.chinaunix.net/"
                data2 = urllib.request.urlopen(url2).read()
                fhandle = open("D:/Python35/myweb/part5/4.html","wb")
                fhandle.write(data2)
                fhandle.close()
        链接爬虫实例：
            import re
            import urllib.request
            def getlink(url):
                # 模拟成浏览器
                headers = ("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/ 537.36 (KHTML, like Gecko)
                    Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
                opener = urllib.request.build_opener()
                opener.addheaders  =  [headers]
                # 将opener安装为全局
                urllib.request.install_opener(opener)
                file = urllib.request.urlopen(url)
                data = str(file.read())
                # 根据需求构建好链接表达式
                pat = '(https?:// [^\s)";]+\.(\w|/)*)'
                link = re.compile(pat).findall(data)
                # 去除重复元素
                link = list(set(link))
                return link
                
            # 要爬取的网页链接
            url = "http:// blog.csdn.net/"
            # 获取对应网页中包含的链接地址
            linklist = getlink(url)
            # 通过for循环分别遍历输出获取到的链接地址到屏幕上
            for link in linklist:
                print(link[0])
        
    队列：
        import queue
        a = queue.Queue()
        a.put('python')
        a.task_done()
        a.get()
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
        
    浏览器伪装技术：
        常见的反爬机制：
           1）通过分析用户请求的Headers信息进行反爬虫。
           2）通过检测用户行为进行反爬虫，比如通过判断同一个IP在短时间内是否频繁访问对应网站等进行分析。
           3）通过动态页面增加爬虫爬取的难度，达到反爬虫的目的。
        
        针对的破解方法：
            1）构造请求头，模拟浏览器登录
            2）使用代理服务器并经常借还代理服务器。
            3）利用工具：selenium + plantomJS 。
        常见头信息中的字段：
            常见字段1
                Accept：·Accept字段主要用来表示浏览器能够支持的内容类型有哪些。
                    text/html，·text/html表示HTML文档。
                    application/xhtml+xml，·application/xhtml+xml表示XHTML文档。
                    application/xml；·application/xml表示XML文档。
                    q=0.9，*/*；q=0.8·q代表权重系数，值介于0和1之间。
                所以这一行字段信息表示浏览器可以支持text/html、application/xhtml+xml、application/xml、*/*等内容类型，
                支持的优先顺序从左到右依次排列。
            常见字段2
                Accept-Encoding：·Accept-Encoding字段主要用来表示浏览器支持的压缩编码有哪些。
                gzip，·gzip是压缩编码的一种。
                deflate·deflate是一种无损数据压缩算法。
                这一行字段信息表示浏览器可以支持gzip、deflate等压缩编码。
            常见字段3
                Accept-Language：·Accept-Language主要用来表示浏览器所支持的语言类型。
                zh-CN，zh；·zh-CN表示简体中文语言，zh表示中文，CN表示简体。
                q=0.8，en-US；·en-US表示英语（美国）语言。
                q=0.5，en；·en表示英语语言。
                q=0.3
                所以之一行字段表示浏览器可以支持zh-CN、zh、en-US、en等语言。
            常见字段4
                User-Agent：Mozilla/5.0（Windows NT 6.1；WOW64；rv：47.0）Gecko/20100101 Firefox/47.0
                User-Agent字段主要表示用户代理，服务器可以通过该字段识别出客户端的浏览器类型、浏览器版本号、客户端的
                操作系统及版本号，网页排版引擎等客户端信息。所以我们之前要模拟浏览器登录，主要以伪造该字段进行。
                ·Mozilla/5.0表示浏览器名及版本信息。
                ·Windows NT 6.1；WOW64；rv：47.0表示客户端操作系统对应信息。
                ·Gecko表示网页排版引擎对应信息。
                ·firefox自然表示火狐浏览器。
                所以这一行字段表示的信息为对应的用户代理信息是Mozilla/5.0（Windows NT 6.1；WOW64；rv：47.0）Gecko/
                20100101 Firefox/47.0。
            常见字段5
                Connection：keep-alive·Connection表示客户端与服务器的连接类型，对应的字段值主要有两种：
                    ·keep-alive表示持久性连接。
                    ·close表示单方面关闭连接，让连接断开。
                所以此时，这一行字段表示客户端与服务器的连接是持久性连接。
            常见字段6
                Host：www.youku.com·Host字段表示请求的服务器网址是什么，此时这一行字段表示请求的服务器网址是www.youku.com。
            常见字段7
                Referer：网址·Referer字段主要表示来源网址地址，比如我们从http://www.youku.com网址中访问了该网址下的子
                    页面http://tv.youku.com/?spm=0.0.topNav.5～1～3！2～A.QnQOEf，那么此时来源网址为http://www.youku.com，
                    即此时Referer字段的值为http://www.youku.com。
            
            import urllib.request
            import http.cookiejar
            #注意，如果要通过fiddler调试，则下方网址要设置为"http:// www.baidu.com/"
            url= "http:// www.baidu.com"
            headers={ "Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Encoding":" gb2312,utf-8",
                        "Accept-Language":" zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                        User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36
                                (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/ 537.36 SE 2.X MetaSr 1.0",
                        "Connection": "keep-alive",
                        "referer":"baidu.com"}
            cjar=http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
            headall=[]
            for key,value in headers.items():
                item=(key,value)
                headall.append(item)
            opener.addheaders = headall
            urllib.request.install_opener(opener)
            data=urllib.request.urlopen(url).read()
            fhandle=open("D:/Python35/myweb/part8/3.html","wb")
            fhandle.write(data)
            fhandle.close()
                
    定向爬虫步骤与策略
        爬取步骤：
            (1)理清爬取目标
            (2)设置网址过滤规则
            (3)设置内容采集规则
            (4)规划采集任务
            (5)将采集结果进行相应的修正
            (6)对结果进行进一步处理
    
        信息筛选策略：
            (1)通过正则表达式筛选
            (2)通过Xpath表达式筛选
            (3)通筛选过xslt
    
    常用python爬虫框架：
        (1)scrapy框架
        (2)crawley框架
            crawlspider链接提取器：
                rules= （Rule(Linktractor(allow=r'Items/', deny='', restrice_xpaths='', allow_domains=('...')...), callback='prse_item）, follow=True),)
            链接提取器主要负责将response响应中符合条件的链接提取出来LinkEtractor：
                allow: 提取符合对应正则表达式的链接
                deny : 不提取符合对应正则表达式的链接
                restrict_xpaths: 使用Xpath表达式与allow共同作用提取出同时符合对应Xpath表达式和正则表达式的链接
                allow_domains: 应许提取的域名，从某个域名下提取链接
                deny_domains: 禁止提取的域名，从某个域名下提取链接
                
        (3)portia框架（可视化）
        (4)newspaper框架
        (5)python-goose框架
                
    scrapy架构：
        1）Scrapy引擎
            Scrapy引擎是整个Scrapy架构的核心，负责控制整个数据处理流程，以及触发一些事务处理。Scrapy引擎与调度器、实体管
            道、中间件、下载器、蜘蛛等组件都有关系，Scrapy引擎处于整个Scrapy框架的中心的位置，对各项组件进行控制及协调。
            
        2）调度器
            调度器主要实现存储待爬取的网址，并确定这些网址的优先级，决定下一次爬取哪个网址等。我们可以把调度器的存储结构
            看成一个优先队列，调度器会从引擎中接收request请求并存入优先队列中，在队列中可能会有多个待爬取的网址，但是这些
            网址各自具有一定的优先级，同时调度器也会过滤掉一些重复的网址，避免重复爬取。当引擎发出请求之后，调度器将优先
            队列中的下一次要爬取的网址返回给引擎，以供引擎进行进一步处理。
            
        3）下载器
            下载器主要实现对网络上要爬取的网页资源进行高速下载，由于该组件需要通过网络进行大量数据的传输，所以该组件的压
            力负担一般会比其他的组件重。下载器下载了对应的网页资源后，会将这些数据传递给Scrapy引擎，再由Scrapy引擎传递给
            对应的爬虫进行处理。
            
        4）下载中间件
            下载中间件是处于下载器和Scrapy引擎之间的一个特定的组件，主要用于对下载器和Scrapy引擎之间的通信进行处理，在下
            载中间件中，可以加入自定义代码，轻松地实现Scrapy功能的扩展，我们在下载中间件中加入的自定义代码，会在Scrapy引
            擎与下载器通信的时候调用。上一章中我们已经具体的使用过下载中间件来实现IP池和用户代理池的相关功能。

        5）蜘蛛（也叫作爬虫，一个Scrapy项目下可能会有多个Spiders爬虫文件）
            蜘蛛（Spider）组件，也叫作爬虫组件，该组件是Scrapy框架中爬虫实现的核心。在一个Scrapy项目中，可以有多个蜘蛛，
            每个蜘蛛可以负责一个或多个特定的网站。蜘蛛组件主要负责接收Scrapy引擎中的response响应（这些响应具体是下载器从
            互联网中得到的响应然后传递到Scrapy引擎中的），在接收了response响应之后，蜘蛛会对这些response响应进行分析处理，
            然后可以提取出对应的关注的数据，也可以提取出接下来需要处理的新网址等信息。

        6）爬虫中间件
            爬虫中间件是处于Scrapy引擎与爬虫组件之间的一个特定的组件，主要用于对爬虫组件和Scrapy引擎之间的通信进行处理。
            同样，在爬虫中间件中可以加入一些自定义代码，很轻松地实现Scrapy功能的扩展。在爬虫中间件中加入的自定义代码，会
            在Scrapy引擎与爬虫组件之间进行通信的时候调用。

        7）实体管道
            实体管道主要用于接收从蜘蛛组件中提取出来的项目（item），接收后，会对这些item进行对应的处理，常见的处理主要有：
            清洗、验证、存储到数据库中等。

    scrapy常用命令：
        1、全局命令：scrapy -h
            1) fetch :scrapy fetch http://www.baidu.com. 显示爬虫爬取的过程
                help : scrapy fetch -h
                scrapy fetch --headers --nolog http:?/news.sina.com.cn/
            2) runspider : scrapy runspider --loglevel=INFO first.py 在不依托scrapy的爬虫项目，直接运行一个爬虫文件
            3) setting ：通过命令查看配置信息scrapy settings --配置名
            4）shell : 启动scrapy交互终端，用于开发调试， scrapy shell http://www.baidu.com --nolog
            5) startproject
            6) version ： 获取scrapy版本信息
            7）view ：下载某个网页并用浏览器打开 scrapy view  网址
        2、项目命令：
            1)bench : 可以测试本地硬件的性能
            2）gensider : scrapy genspider -l 创建爬虫文件 可用的爬虫模板basic、crawl、csvfeed、xmldeed
                命令格式： scrapy genspider -t 模板  爬虫名 爬取网站域名
            3）check : 对爬虫进行测试  进入到项目目录 scrapy check mysite
            4)crawl : 启动爬虫命令 scrapy crawl 爬虫名  （要进入到爬虫项目）
            5)list : 列出当前项目可使用的爬虫文件
            6)edit : 爬虫编辑命令
            7)parse : 使用默认爬虫和处理函数对指定网站进行爬取 scrapy parse url
            
    Xath表达式语法
        /  : 从根节点选取，绝对定位。
        // : 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
        .  ：选取当前节点
        .. : 选取当前节点的父节点
        @  ： 选取属性
        
        /bookstore/book[1]	                选取属于 bookstore 子元素的第一个 book 元素。
        /bookstore/book[last()]	            选取属于 bookstore 子元素的最后一个 book 元素。
        /bookstore/book[last()-1]	        选取属于 bookstore 子元素的倒数第二个 book 元素。
        /bookstore/book[position()<3]	    选取最前面的两个属于 bookstore 元素的子元素的 book 元素。
        //title[@lang]	                    选取所有拥有名为 lang 的属性的 title 元素。
        //title[@lang='eng']	            选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。
        /bookstore/book[price>35.00]	    选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。
        /bookstore/book[price>35.00]/title	选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。
        
       选取未知节点
        XPath 通配符可用来选取未知的 XML 元素。
            通配符	描述
            *	匹配任何元素节点。
            @*	匹配任何属性节点。
            node()	匹配任何类型的节点。
            
            /bookstore/*	选取 bookstore 元素的所有子元素。
            //*	            选取文档中的所有元素。
            //title[@*]	    选取所有带有属性的 title 元素。
            
            //book/title | //book/price	选取 book 元素的所有 title 和 price 元素。
            //title | //price	选取文档中的所有 title 和 price 元素。
            /bookstore/book/title | //price	选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。

    scrapy爬虫避免被禁止：
        (1）禁止Cookie；
            打开对应的Scrapy爬虫项目中的settings.py文件，可以发现文件中有以下两行代码,去掉注释：
            # Disable cookies (enabled by default)
            COOKIES_ENABLED = False

        (2）设置下载延时；
            # Configure a delay for requests for the same website (default: 0)
            # See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
            # See also autothrottle settings and docs DOWNLOAD_DELAY = 0.7
            DOWNLOAD_DELAY = 3  # 下载延迟，单位秒

        (3）使用IP池；
            具体方法：
                1）获取代理服务器的IP信息；
                2）在setting.py文件中增加IP池
                    IPPOOL = [
                        {"ipaddr" : "host:port"},
                    ]
                3)在项目核心目录创建middleware.py
                    # middlewares下载中间件
                    # 导入随机数模块，目的是随机挑选一个IP池中的IP
                    import random
                    # 从settings文件（myfirstpjt.settings为settings文件的地址）中导入设置好的IPPOOL
                    from myfirstpjt.settings import IPPOOL
                    # 导入官方文档中HttpProxyMiddleware对应的模块
                    from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
                    
                    class IPPOOLS(HttpProxyMiddleware):
                        # 初始化方法
                        def __init__(self,ip=''):
                            self.ip=ip
                        # process_request()方法，主要进行请求处理
                        def process_request(self,request,spider):
                            # 先随机选择一个IP
                            thisip=random.choice(IPPOOL)
                            # 输出当前选择的IP，便于调试观察
                            print("当前使用的IP是："+thisip["ipaddr"])
                            # 将对应的IP实际添加为具体的代理，用该IP进行爬取
                            request.meta["proxy"]="http://"+thisip["ipaddr"]
                4)配置中间件到settings.py
                    在settings.py文件中，与下载中间件相关的配置信息默认如下：
                        # DOWNLOADER_MIDDLEWARES = { 'myfirstpjt.middlewares.MyCustomDownloaderMiddleware': 543, }
                    所以现在需要对这一部分配置信息进行如下修改：
                        DOWNLOADER_MIDDLEWARES = { 'myfirstpjt.middlewares.MyCustomDownloaderMiddleware': 543,
                                    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':123,
                                    'myfirstpjt.middlewares.IPPOOLS':125 }

        (4）使用用户代理池；
            具体方法：
                1）收集多种浏览器的信息；
                
                2）在setting.py文件中增加用户代理池。
                    # 用户代理（user-agent）池设置
                    UAPOOL = [ "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"\
                             Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0", \
                            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",\
                            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5" ]
                            
                3)在项目核心目录创建user_agent_middleware.py
                    # middlewares下载中间件
                    # 导入随机数模块，目的是随机挑选一个IP池中的IP
                    import random
                    # 从settings文件（myfirstpjt.settings为settings文件的地址）中导入设置好的UAPOOL
                    from myfirstpjt.settings import UAPOOL
                    # 导入官方文档中HttpProxyMiddleware对应的模块
                    from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
                    
                    class UAmid(UserAgentMiddleware):
                        # 初始化方法
                        def __init__(self, ua=''):
                            self.ua = ua
                        # process_request()方法，主要进行请求处理
                        def process_request(self,request,spider):
                            # 先随机选择一个UA
                            thisua = random.choice(UAPOOL)
                            # 输出当前选择的UA，便于调试观察
                            print("当前使用的user_agent是：" + thisua)
                            # 将对应的UA实际添加为具体的代理，用该UA进行爬取
                            request.headers.setdefault("User-Agent", thisua)
                            
                4)配置中间件到settings.py
                    在settings.py文件中，与下载中间件相关的配置信息默认如下：
                        # Enable or disable downloader middlewares
                        # See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
                        DOWNLOADER_MIDDLEWARES = {'mysite.middlewares.MyCustomDownloaderMiddleware': 543,
                                                 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':2,
                                                 'mysite.user_agent_middleware.UAmid':1 }

                
                
                
                
                
                
                
"""













