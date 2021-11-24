# HTTP_SERVER
实现http服务器，支持文件夹/文件上传和下载


# 简介
本文主要讨论如何实现远程文件的上传和下载功能。

由于本人好久不写代码，手有些生了，功能还算是实现了，有需要的人可以参考一下~


## 功能
1. 本地上传文件夹（单个文件夹，文件夹内部支持多级嵌套）
2. 本地上传文件（多个任意类型的文件）
3. 展示文件目录（以当前目录为根目录，层层展开显示其中所有文件），属性（文件路径，大小和最后修改时间）
4. 实时生成目录树和文件列表写入文件，支持下载导出
5. 文件下载

### 代码：
该模块通过以相当简单的方式实现标准`GET`和`HEAD`请求，构建在`BaseHTTPServer`上，基于`BaseHTTPRequestHandler`实现，具体细节请看代码和注释。


#本地测试启动 python simple_http_server.py 8000
#linux服务器启动时，注意选择python3环境
#忽略挂断信号
#nohup python3 HTTP_SERVER.py >> ../HTTP_SERVER.log 2>&1 &

__version__ = "0.3.0"
__author__ = "antrn CSDN: https://blog.csdn.net/qq_38232598"
__all__ = ["MyHTTPRequestHandler"]


"""带有GET/HEAD/POST命令的简单HTTP请求处理程序。
提供来自当前目录及其任何子目录的文件,可以接收客户端上传的文件和文件夹。
GET/HEAD/POST请求完全相同，只是HEAD请求忽略了文件的实际内容。
"""
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
 
构建目录树，存入列表
def p(self, url):

获取文件列表
def getAllFilesList(self):

写入文件
def writeList(self,url):

处理GET请求
def do_GET(self):

Serve a HEAD request.
def do_HEAD(self):

Serve a POST request.
def do_POST(self):

处理post数据
def deal_post_data(self):
        
发送head
Common code for GET and HEAD commands.
This sends the response code and MIME headers.
Return value is either a file object (which has to be copied
to the output file by the caller unless the command was HEAD,
and must be closed by the caller under all circumstances), or
None, in which case the caller has nothing further to do.
def send_head(self):


Helper to produce a directory listing (absent index.html).
Return value is either a file object, or None (indicating an
error).  In either case, the headers are sent, making the
interface the same as for send_head().
def list_directory(self, path):
        
Guess the type of a file.
Argument is a PATH (a filename).
Return value is a string of the form type/subtype,
usable for a MIME Content-type header.
The default implementation looks the file's extension
up in the table self.extensions_map, using application/octet-stream
as a default; however it would be permissible (if
slow) to look inside the data to make a better guess.
def guess_type(self, path):
       
Translate a /-separated PATH to the local filename syntax.
Components that mean special things to the local file system
(e.g. drive or directory names) are ignored.  (XXX They should
probably be diagnosed.)
def translate_path(path):
    
提示关闭，退出
def signal_handler(signal, frame):

主函数
def main():
   
入口
if __name__ == '__main__':
    
    
## 版本更新记录

 - 0.0.8.基于BaseHTTPRequestHandler实现目录列表功能，原来是只显示一级文件或目录，修改为walk遍历所有文件
 - 0.1.0.实现上传文件夹功能
 - 0.1.4.实现列表属性查看
 - 0.2.0.实现展示目录树和列表，并提供下载
 - 0.2.7.实现支持上传文件和文件夹功能
 - 0.2.8.美化界面
 - 0.2.9.写入文件字符乱码问题，增加目录列表排序
 - 0.3.0.最后规整发布

该代码目前在`windows`和`Linux`平台均已测试通过，有兴趣的小伙伴可以运行试一下。

## 运行步骤：

 - 打开`Terminal/CMD`窗口，进入要共享的文件目录，注意使用`python3`运行代码：
```python
python http_server.py [port]
```
 - `[port]` 端口为可选参数，默认8001。
 - 如果需要放在服务器运行，则使用远程连接工具登录到服务器控制台，需要使用`nohup`来支持关闭`shell`之后，让他保持后台运行，
 - 执行：
```python
 nohup python3 HTTP_SERVER.py >> HTTP_SERVER.log 2>&1 &
 ```
 - 这里我们将日志保存到`HTTP_SERVER.log`中，便于调试查看，优化程序。

## 效果图
请按照上述命令启动，打开浏览器输入`IP:port`即可。
### 主页面
![在这里插入图片描述](https://img-blog.csdnimg.cn/f5bf04f1f390401bbbf65bd29cb44eeb.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAQW50cm4=,size_16,color_FFFFFF,t_70,g_se,x_16)

### dirtree 目录树+列表
在地址栏输入`127.0.0.1:8000/dirtree.txt`，或者直接点击列表中的`dirtree.txt`文件，跳转到显示文件内容的页面，如下图，这两个列表默认都是按照英文字母和数字的顺序排序（小写字母），两种方式方便不同查看目录结构的需求。
![在这里插入图片描述](https://img-blog.csdnimg.cn/e80d55675706461a949b0324ef0a7922.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAQW50cm4=,size_20,color_FFFFFF,t_70,g_se,x_16)
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

好了，本次探索到此为止，有兴趣的小伙伴赶紧去玩一下吧！GitHub仓库：

## 参考资料

 - 参考https://www.jianshu.com/p/2147b7e7cf38
 - 参考https://github.com/freelamb/simple_http_server
 - 参考https://blog.csdn.net/dirful/article/details/4374953
 - 参考https://blog.csdn.net/qq_35038500/article/details/87943004
