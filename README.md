# HTTP_SERVER

实现 http 服务器，支持文件夹/文件上传和下载

## 简介

本文主要讨论如何实现远程文件的上传和下载功能。

由于本人好久不写代码，手有些生了，功能还算是实现了，有需要的人可以参考一下~

## 版本更新记录

- 0.0.8.基于 BaseHTTPRequestHandler 实现目录列表功能，原来是只显示一级文件或目录，修改为 walk 遍历所有文件
- 0.1.0.实现上传文件夹功能
- 0.1.4.实现列表属性查看
- 0.2.0.实现展示目录树和列表，并提供下载
- 0.2.7.实现支持上传文件和文件夹功能
- 0.2.8.美化界面
- 0.2.9.写入文件字符乱码问题，增加目录列表排序
- 0.3.0.最后规整发布
- 0.3.5.支持上传中文文件
- 0.3.9.支持删除远程文件
- 0.4.0.解决各种中文字符编码问题
- 0.5.4.解决无法删除内层文件的 bug
- 0.5.6.解决上传文件夹内层文件内容丢失的 bug
- 0.5.8.增加删除空目录的功能
- 0.5.9.批量更新
  - 优化代码和文档注释；
  - 取消显示隐藏文件和目录，保持界面清爽整洁；
  - 修复删除文件时跳转页面报错的 bug；
  - 修复文件树文件内容累积的 bug。
- 0.6.0.对较多内容进行更新
  - 修复中文文件显示内容乱码的问题。
  - 优化显示文件大小，支持动态转化单位。
  - 修复写入目录树中文乱码的问题。
  - 取消显示所有文件，增加分层显示文件夹的功能，避免显示文件过多显得杂乱。
  - 修复删除目录报错的问题。
  - 修复删除子目录中文件报错的问题。
  - 修复上传中文目录文件跳转报错的问题。
  - 取消自动删除空目录的功能。
  - 增加删除目录按钮的红框警示。
  - 增加显示文件类型的条目，便于看清当前类型。
- 0.6.1.修复目录树文件内容不完整的问题；优化页面表格显示，增加警示效果。
- 0.6.2.累积更新
  - 修复文件夹大小计算为0的问题。
  - 修复目录树文件大小计算为0的问题。
  - 修复目录树累积的问题。
  - 更新readme文档。


## 功能

### 已完成

1. 本地上传文件夹（单个文件夹，文件夹内部支持多级嵌套）
2. 本地上传文件（多个任意类型的文件）
3. 展示文件目录（以当前目录为根目录，层层展开显示其中所有文件），属性（文件路径，大小和最后修改时间）
4. 实时生成目录树和文件列表写入文件，支持下载导出
5. 文件下载
6. 文件删除和删除目录

### 未完成

暂无。

> 如您有好的意见或建议，请前往本项目的仓库[Github issue](https://github.com/JevenM/HTTP_SERVER/issues)提出问题，感谢您对项目的贡献和宝贵意见及支持。

## 代码

该模块通过以相当简单的方式实现标准`GET`和`HEAD`请求，构建在`BaseHTTPServer`上，基于`BaseHTTPRequestHandler`实现，具体细节请看代码和注释。

**version**：最新版本："0.6.0"

**content**：本文的 CSDN 博客地址：[使用 python 实现提供远程上传下载文件的 http 服务器](https://blog.csdn.net/qq_38232598/article/details/121520894?spm=1001.2014.3001.5501)

**author**：我的 CSDN 博客地址：[antrn](CSDN:%20https://blog.csdn.net/qq_38232598)

### 函数功能

| 类/函数                                             | 注释                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| class MyHTTPRequestHandler(BaseHTTPRequestHandler): | 带有 GET/HEAD/POST 命令的简单 HTTP 请求处理程序。提供来自当前目录及其任何子目录的文件,可以接收客户端上传的文件和文件夹。GET/HEAD/POST 请求完全相同，只是 HEAD 请求忽略了文件的实际内容。                                                                                                                                                                                            |
| def buildTree(self, url):                           | 构建目录树，存入列表                                                                                                                                                                                                                                                                                                                                                                |
| def getAllFilesList(self):                          | 获取文件列表                                                                                                                                                                                                                                                                                                                                                                        |
| def writeList(self,url):                            | 写入文件                                                                                                                                                                                                                                                                                                                                                                            |
| def do_GET(self):                                   | 处理 GET 请求                                                                                                                                                                                                                                                                                                                                                                       |
| def do_HEAD(self):                                  | Serve a HEAD request.                                                                                                                                                                                                                                                                                                                                                               |
| def do_POST(self):                                  | Serve a POST request.                                                                                                                                                                                                                                                                                                                                                               |
| def deal_post_data(self):                           | 处理 post 数据                                                                                                                                                                                                                                                                                                                                                                      |
| def send_head(self):                                | Common code for GET and HEAD commands.This sends the response code and MIME headers.Return value is either a file object (which has to be copied to the output file by the caller unless the command was HEAD,and must be closed by the caller under all circumstances), orNone, in which case the caller has nothing further to do.                                                |
| def list_directory(self, path):                     | Helper to produce a directory listing (absent index.html).Return value is either a file object, or None (indicating an error). In either case, the headers are sent, making the interface the same as for send_head().                                                                                                                                                              |
| def guess_type(self, path):                         | Guess the type of a file.Argument is a PATH (a filename).Return value is a string of the form type/subtype,usable for a MIME Content-type header. The default implementation looks the file's extension up in the table self.extensions_map, using application/octet-stream as a default; however it would be permissible (if slow) to look inside the data to make a better guess. |
| def translate_path(path):                           | Translate a /-separated PATH to the local filename syntax.Components that mean special things to the local file system (e.g. drive or directory names) are ignored. (XXX They should probably be diagnosed.)                                                                                                                                                                        |
| def str_to_chinese(self,var)                        | 将 16 进制字符串解析为中文字符                                                                                                                                                                                                                                                                                                                                                      |
| def signal_handler(signal, frame):                  | 提示关闭，退出                                                                                                                                                                                                                                                                                                                                                                      |
| def main():                                         | 主函数                                                                                                                                                                                                                                                                                                                                                                              |
| if **name** == '**main**':                          | 程序入口                                                                                                                                                                                                                                                                                                                                                             

该代码目前在`windows`和`Linux`平台均已测试通过，有兴趣的小伙伴可以运行体验一下操作。

## 运行步骤：

- 打开`Terminal/CMD`窗口，进入要共享的文件目录，注意使用`python3`运行代码（python2 也支持）：

```shell
python HTTP_SERVER.py [port]
```

- `[port]` 端口为可选参数，不填写默认为 1234。

### 本地测试启动

示例：修改服务端口为 8000。

```shell
python HTTP_SERVER.py 8000
```

- 注意，如果需要放在服务器运行，则使用远程连接工具登录到服务器控制台，需要使用`nohup`来支持关闭`shell`之后，让其保持后台运行，

执行：

```shell
 nohup python3 HTTP_SERVER.py >> HTTP_SERVER.log 2>&1 &
```

- 这里我们将日志保存到`HTTP_SERVER.log`中，便于调试查看，优化程序。

`linux`服务器启动时，注意选择`python3`环境

## 效果图

请按照上述命令启动，打开浏览器输入`IP:port`即可。

### 主页面

![在这里插入图片描述](https://img-blog.csdnimg.cn/8ca71a5821da432f922737636f8d4d1c.png)

这里注意，① 共享的目录就是主代码文件`HTTP_SERVER.py`所在的目录，代码中特意将其取消显示，避免误操作导致删库跑路；② 标红的删除按钮慎用。

### 子目录
点击`测试目录`，进入二级目录，同样支持各种文件操作：
![在这里插入图片描述](https://img-blog.csdnimg.cn/a608541820674dce8e00af884c6bd175.png)

### dirtree 目录树+列表

在地址栏输入`127.0.0.1:8000/dirtree.txt`，或者直接点击列表中的`dirtree.txt`文件，跳转到显示文件内容的页面，如下图，这默认按照英文字母和数字的顺序排序（小写字母）。两种方式方便不同查看目录结构的需求。

![在这里插入图片描述](https://img-blog.csdnimg.cn/9f1fe903c4fa42b1982525c7aecd8397.png)

## 上传

此模块包括上传（多个）文件和上传文件夹两种功能，针对不同的需求。

### 上传文件夹

点击`Directory Updating`下的`Choose Files`，在弹出窗口选择要上传的文件夹，点击`upload`，随后`chrome`浏览器会弹出页面，

![在这里插入图片描述](https://img-blog.csdnimg.cn/ec93063cf5fa436dad4027e12a6cb65d.png)

再次点击`upload`，此处显示文件夹中的文件总数量

![在这里插入图片描述](https://img-blog.csdnimg.cn/44efcae987fa434b9f9a0cb9f76dfa30.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAQW50cm4=,size_16,color_FFFFFF,t_70,g_se,x_16)

随后点击`uploadDir`，即可上传，成功页面如下

![在这里插入图片描述](https://img-blog.csdnimg.cn/bd16f9fb78164f9a957f5001efe497cf.jpg?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAQW50cm4=,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

点击`back`返回主页面

### 上传（多个）文件

上传文件功能，如上所述，相同步骤。

## 下载

找到需要的文件，右键选择另存为或者点击（浏览器解析不了的文件格式）进行下载。

## 结尾

好了，本次探索到此为止，有兴趣的小伙伴赶紧去玩一下吧！GitHub 仓库：[JevenM](https://github.com/JevenM/HTTP_SERVER)

如果您对此项目感兴趣，欢迎`star`☆ 或者`fork`，感谢您的支持！

## 参考资料

- 参考https://www.jianshu.com/p/2147b7e7cf38
- 参考https://github.com/freelamb/simple_http_server
- 参考https://blog.csdn.net/dirful/article/details/4374953
- 参考https://blog.csdn.net/qq_35038500/article/details/87943004
