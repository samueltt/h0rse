## h0rse是什么

h0rse是一个更现代化的Web漏洞扫描器，它与其他同类黑客工具相比最大的优势在于性能！要快！

同类的工具大多采用python编写，因为丰富的第三方模块简化了开发过程。但目前突出问题在于:

1. 检测方法老旧，似乎自动化测试到了一个瓶颈，再想精准貌似只能通过人工；
2. 常规套路的多进程、多线程的模式受制于GIL，效率并不是很高；
3. Web2.0时代，越来越多的数据通过XHR请求，使得单个URL请求网页难以拿到有用数据。

针对问题一，作者目前的技术功底还不够；针对问题二，引入基于协程的asyncio应该能大幅度提高效率；针对问题三，业界常规套路是使用无头浏览器处理。

## Good Readings:

1. [https://www.anquanke.com/post/id/178339]()


## 一点感悟和想法

最开始写这个项目，是因为看某大佬的实习面经里提到了他写的扫描器，而自己之前又
看过刘璇写的《白帽子讲Web扫描》，于是想效法炮制一个。所以一开始的意图是很模
糊的，只是觉得该有这个功能点，就开始往上加。最近的挖洞经历使我意识到——**大而
全的扫描器在单个功能的准确性与性能上绝逼比不了小而专的工具**。开发这玩意的价值
在于省力，通过自动化测试来缩短人工排查的时间，所以它其实是人工渗透经验的总结，
误报、漏报都太正常。不如把它当成脚手架，自己挖累了就让它去做。

另一点感悟便是写一个工具和写好一个工具是两回事，后者要考虑很多（直观地将代码
量相差很大）。一直在纠结要不要直接上pyppeteer对付XHR，坦白的将要写好这个
软件早晚要做这一点。但目前已经写出了1.0版本的雏形，现在掉头去搞2.0有点可惜，
而且有很多功能点是写2.0不可避免地。比如去重（REST结构的怎么判断）、页面比较
算法、注入|分析的通用模式，爬去策略等。这些都值得在1.0时候就去试水。因为只有
写入第一代后反复测试，才能理解下一代的优化点在哪里。

*** 

### 想法

有个自己感觉不错的idea。既然写一个大而全的自动化扫描器有诸多弊端：要处理千奇百怪的容错，出现异常难以恢复现场等。
不如高度解耦，将扫描器功能拆分，例如做成如下的菜单选项：

>   1 -->高级爬虫（提取有用信息：公开信息、Url、接口等）可采取静态爬虫或基于无头浏览器的动态爬虫
>   2 -->XSS检测
>   3 -->SQLi检测
>   4 -->SSRF检测
>   5 -->XXE检测
>   6 -->API接口Fuzz等
>   n -->全自动化Batch 

每条在测试前可通过文件或输入url，以此来保证对burpsuite等工具数据的兼容性。

## h0rse特性构想

第一个版本开发完之后，它应该具备以下特性：

1. 基于aiohttp实现，可以设置爬虫的协程数，爬取+解析大型网站在数秒之内；
2. 广度+深度优先策略：首页用广度获取最多的子域名，然后依次分析每个子域名下的目录；
3. 跟进前、后端URL跳转，使爬虫继续下去；(到底该跟不跟)
4. 识别404错误，避免爬虫宕机；
5. URL去重、去似、去含，从而提取出值得注入分析的端点；
6. 检测表单并自动填写，检测Ajax事件（暂未想好怎么做）；
7. 断连重试机制（包括有一定道理的策略）；
8. Payload的生成、注入、输出分析功能（Fuzzer）；
9. 简单的报告输出功能（控制台输出）。

## h0rse功能构想

在我看来，当前黑客们惯用的扫描器都是依据自己的渗透经验开发，我的这款也不例外。就按照正常的流程走吧：

1. 登入某公益SRC首页，爬取页面并解析获取其子域名
2. 爬取每个子站页面，分析其功能，找到合适的注入点
3. 输出可疑url，有些功能还是得人工审查，哈哈！

## 进度安排：

那现在开始吧，第一个版本跑通主要流程，第二个版本再去弥补健壮性。

Period-2

* 5.10-5.12，相应分析，主要是页面相似算法
* 5.12-5.14，Payload注入
* 可以把页面相似、URL去重等功能单独拎出来，优化、研究
