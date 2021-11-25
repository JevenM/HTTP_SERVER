#!/usr/bin/python
# -*- coding: UTF-8 -*-
#本地测试启动 python simple_http_server.py 8000
#linux服务器启动时，注意选择python3环境
#忽略挂断信号
#nohup python3 HTTP_SERVER.py >> ../HTTP_SERVER.log 2>&1 &

__version__ = "0.3.0"
__author__ = "antrn CSDN: https://blog.csdn.net/qq_38232598"
__all__ = ["MyHTTPRequestHandler"]

import os, time
import sys, socket
import posixpath
try:
    from html import escape
except ImportError:
    from cgi import escape
import shutil
import mimetypes
import re
import signal
from io import StringIO, BytesIO

if sys.version_info.major == 3:
    # Python3
    from urllib.parse import quote
    from urllib.parse import unquote
    from http.server import HTTPServer
    from http.server import BaseHTTPRequestHandler
else:
    # Python2
    from urllib import quote
    from urllib import unquote
    from BaseHTTPServer import HTTPServer
    from BaseHTTPServer import BaseHTTPRequestHandler

"""带有GET/HEAD/POST命令的简单HTTP请求处理程序。
提供来自当前目录及其任何子目录的文件,可以接收客户端上传的文件和文件夹。
GET/HEAD/POST请求完全相同，只是HEAD请求忽略了文件的实际内容。
"""
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
 
    server_version = "simple_http_server/" + __version__

    mylist = []
    myspace =""
    treefile = "dirtree.txt"
    IPAddress = socket.gethostbyname(socket.gethostname())

    def p(self, url):
        print("url:", url)
        files = os.listdir(r''+url)
        for file in files:           
            myfile = url + "//"+file
            size = os.path.getsize(myfile)
            if os.path.isfile(myfile):
                MyHTTPRequestHandler.mylist.append(str(MyHTTPRequestHandler.myspace)+"|____"+file +" "+ str(size)+"\n")
            
            if os.path.isdir(myfile) :
                MyHTTPRequestHandler.mylist.append(str(MyHTTPRequestHandler.myspace)+"|____"+file + "\n")
                #get into the sub-directory,add "|    "
                MyHTTPRequestHandler.myspace = MyHTTPRequestHandler.myspace+"|    "
                self.p(myfile)
                #when sub-directory of iteration is finished,reduce "|    "
                MyHTTPRequestHandler.myspace = MyHTTPRequestHandler.myspace[:-5]

    def getAllFilesList(self):
        listofme = []
        for root, dirs, files in os.walk(translate_path(self.path)):
            files.sort()
            for fi in files:
                display_name = os.path.join(root, fi)
                #删除前面的XXX个字符，取出相对当前目录的路径
                relativePath = display_name[len(os.getcwd()):].replace('\\','/')
                st = os.stat(display_name)
                fsize = st.st_size
                fmtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))
                listofme.append(relativePath+"\t")
                listofme.append(str(fsize)+"\t")
                listofme.append(str(fmtime)+"\t\n")
        return listofme

    def writeList(self,url):
        f = open(url,'w')
        f.write("http://"+str(MyHTTPRequestHandler.IPAddress)+":8001/ directory tree\n")
        MyHTTPRequestHandler.mylist.sort()
        f.writelines(MyHTTPRequestHandler.mylist)
        f.write("\nFile Path\tFile Size\tFile Modify Time\n")
        f.writelines(self.getAllFilesList())
        MyHTTPRequestHandler.mylist = []
        MyHTTPRequestHandler.myspace = ""
        print("ok")
        f.close()

    def do_GET(self):
        """Serve a GET request."""

        paths = unquote(self.path)
        path = str(paths)
        plist = path.split("/", 2)
        #result = urllib.parse.urlparse(paths).query
        #paralist = result.split("=")
        #if len(plist) > 1 and plist[1] == "delete" and len(paralist)>1:
            # result = paralist[1]
        # f = BytesIO()
        # f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        # f.write(b"<html>\n<title>Delete Result Page</title>\n")
        # f.write(b"<body>\n<h2>Delete Result Page</h2>\n")
        # f.write(b"<hr>\n")
        if len(plist) > 2 and plist[1] == "delete":
            result = plist[2]
            print("ready delete file===",result)
            if os.path.exists(result):
                print("delete file===",result)
                dirn = os.path.dirname(result)
                #删除完文件，检测是否为空，删除文件夹
                print("dirn", dirn)
                os.remove(result)
                if not os.listdir(dirn):
                    os.removedirs(dirn)
                time.sleep(0.5)
                # 0.5s后重定向
                self.send_response(302)
                self.send_header('Location', "/")
                self.end_headers()
                return


            #     f.write(b"delete successfully<br>")

            # f.write(b"not found<br>")

            # f.write(b"<br><a href=\"/\">back</a>")
            
            # f.write(b"</body>\n</html>\n")
            # length = f.tell()
            # f.seek(0)
            # self.send_response(200)
            # self.send_header("Content-type", "text/html;charset=utf-8")
            # self.send_header("Content-Length", str(length))
            # self.end_headers()
            # if f:
            #     print("############")
            #     shutil.copyfileobj(f, self.wfile)
            #     f.close()
            #     return
        # 这个一定要放在后面，否则，怎么都不会重定向，一直卡在默认的404页面
        fd = self.send_head()
        #查看当前的请求路径
        #参考https://blog.csdn.net/qq_35038500/article/details/87943004
        if fd:
            print("path===", path)
            shutil.copyfileobj(fd, self.wfile)
            #只有回到根目录下才更新写入目录文件，保持最新
            if path == "/":
                self.p(translate_path(self.path))
                self.writeList(MyHTTPRequestHandler.treefile)
            fd.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        fd = self.send_head()
        if fd:
            fd.close()

    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()
        
        f = BytesIO()
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title>Upload Result Page</title>\n")
        f.write(b"<body>\n<h2>Upload Result Page</h2>\n")
        f.write(b"<hr>\n")
        if r:
            f.write(b"<strong>Success:</strong><br>")
        else:
            f.write(b"<strong>Failed:</strong><br>")

        for i in info:
            print(r, i, "by: ", self.client_address)
            f.write(i.encode('utf-8')+b"<br>")
        f.write(b"<br><a href=\"%s\">back</a>" % self.headers['referer'].encode('ascii'))
        #f.write(b"<hr><small>Powered By: freelamb, check new version at ")
        #f.write(b"<a href=\"https://github.com/freelamb/simple_http_server\">")
        f.write(b"</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            shutil.copyfileobj(f, self.wfile)
            f.close()
        #每次提交post请求之后更新目录树文件
        self.p(translate_path(self.path))
        self.writeList(MyHTTPRequestHandler.treefile)

    def str_to_chinese(self,var):
        not_end = True
        while not_end:
            start1 = var.find("\\x")
            # print start1
            if start1 > -1:
                str1 = var[start1 + 2:start1 + 4]
                print(str1)
                start2 = var[start1 + 4:].find("\\x") + start1 + 4
                if start2 > -1:
                    str2 = var[start2 + 2:start2 + 4]

                    start3 = var[start2 + 4:].find("\\x") + start2 + 4
                    if start3 > -1:
                        str3 = var[start3 + 2:start3 + 4]
            else:
                not_end = False
            if start1 > -1 and start2 > -1 and start3 > -1:
                str_all = str1 + str2 + str3
                # print str_all
                str_all = codecs.decode(str_all, "hex").decode('utf-8')

                str_re = var[start1:start3 + 4]
                # print str_all, "   " ,str_re
                var = var.replace(str_re, str_all)
        # print var.decode('utf-8')
        return var

    def deal_post_data(self):
        boundary = self.headers["Content-Type"].split("=")[1].encode('ascii')
        print("boundary===", boundary)
        remain_bytes = int(self.headers['content-length'])
        print("remain_bytes===", remain_bytes)

        res = []
        line = self.rfile.readline()
        while boundary in line and str(line, encoding = "utf-8")[-4:] != "--\r\n":
            
            #line = self.rfile.readline()
            remain_bytes -= len(line)
            if boundary not in line:
                return False, "Content NOT begin with boundary"
            line = self.rfile.readline()
            remain_bytes -= len(line)
            print("line!!!",line)
            fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', str(line))
            if not fn:
                return False, "Can't find out file name..."
            path = translate_path(self.path)

            fname = fn[0]
            #fname = fname.replace("\\", "\\\\")
            fname = self.str_to_chinese(fname)
            print("------",fname)
            
            fn = os.path.join(path, fname)
            while os.path.exists(fn):
                fn += "_"
            print("!!!!",fn)
            dirname = os.path.dirname(fn)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            line = self.rfile.readline()
            remain_bytes -= len(line)
            line = self.rfile.readline()
            # b'\r\n'
            remain_bytes -= len(line)
            try:
                out = open(fn, 'wb')
            except IOError:
                return False, "Can't create file to write, do you have permission to write?"

            pre_line = self.rfile.readline()
            print("pre_line", pre_line)
            remain_bytes -= len(pre_line)
            print("remain_bytes", remain_bytes)
            Flag = True
            while remain_bytes > 0:
                line = self.rfile.readline()
                print("while line", line)
                
                if boundary in line:
                    remain_bytes -= len(line)
                    pre_line = pre_line[0:-1]
                    if pre_line.endswith(b'\r'):
                        pre_line = pre_line[0:-1]
                    out.write(pre_line)
                    out.close()
                    #return True, "File '%s' upload success!" % fn
                    res.append("File '%s' upload success!" % fn)
                    Flag = False
                    break
                else:
                    out.write(pre_line)
                    pre_line = line
            if pre_line is not None and Flag == True:
                out.write(pre_line)
                out.close()
                res.append("File '%s' upload success!" % fn)
            #return False, "Unexpect Ends of data."
        return True, res

    def send_head(self):
        """Common code for GET and HEAD commands.
        This sends the response code and MIME headers.
        Return value is either a file object (which has to be copied
        to the output file by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
        """
        path = translate_path(self.path)
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        content_type = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", content_type)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).
        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().
        """
        try:
            list_dir = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list_dir.sort(key=lambda a: a.lower())
        f = BytesIO()
        display_path = escape(unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title>Directory listing for %s</title>\n" % display_path.encode('ascii'))
        f.write(b"<body>\n<h2>Directory listing for %s</h2>\n" % display_path.encode('ascii'))
        f.write(b"<hr>\n")
        #上传目录
        f.write(b"<h3>Directory Updating</h3>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        #@change=\"handleChange\" @click=\"handelClick\"
        f.write(b"<input ref=\"input\" webkitdirectory multiple name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"uploadDir\"/></form>\n")
        f.write(b"<hr>\n")
        #上传文件
        f.write(b"<h3>Files Updating</h3>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input ref=\"input\" multiple name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"uploadFiles\"/></form>\n")

        f.write(b"<hr>\n")
        #表格
        f.write(b"<table with=\"100%\">")
        f.write(b"<tr><th>path</th>")
        f.write(b"<th>size(Byte)</th>")
        f.write(b"<th>modify time</th>")
        f.write(b"</tr>")

        for name in list_dir:
            fullname = os.path.join(path, name)
            display_name = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                for root, dirs, files in os.walk(fullname):
                # root 表示当前正在访问的文件夹路径
                # dirs 表示该文件夹下的子目录名list
                # files 表示该文件夹下的文件list
                    # 遍历文件
                    for fi in files:
                        #print("########",os.path.join(root, fi))
                        display_name = os.path.join(root, fi)
                        #删除前面的xx个字符，取出相对路径
                        relativePath = display_name[len(os.getcwd()):].replace('\\','/')
                        st = os.stat(display_name)
                        fsize = st.st_size
                        fmtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))
                        f.write(b"<tr>")
                        f.write(b'<td><a href="%s">%s</a></td>' % (quote(relativePath).encode('utf-8'), escape(relativePath).encode('utf-8')))
                        f.write(b"<td>%d</td>" % fsize)
                        f.write(b"<td>%s</td>" % escape(fmtime).encode('ascii'))
                        f.write(b"<td><a href=\"/delete/%s\">delete</a>" % escape(relativePath).encode('utf-8'))
                        f.write(b"</tr>")
                
                    # # 遍历所有的文件夹
                    # for d in dirs:
                    #     print(d)
                continue        
                #linkname = name + "/"
            
            #如果是链接文件
            #if os.path.islink(fullname):
                #display_name = name + "@"
                # Note: a link to a directory displays with @ and links with /
            #f.write(b'<li><a href="%s">%s</a>\n' % (quote(linkname).encode('ascii'), escape(display_name).encode('ascii')))
            
            #其他直接在根目录下的文件直接显示出来
            st = os.stat(display_name)
            fsize = st.st_size
            fmtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))
            f.write(b"<tr>")
            f.write(b'<td><a href="%s">%s</a></td>' % (quote(linkname).encode('utf-8'), escape(display_name).encode('utf-8')))
            f.write(b"<td>%d</td>" % fsize)
            f.write(b"<td>%s</td>" % escape(fmtime).encode('ascii'))
            f.write(b"<td><a href=\"/delete/%s\">delete</a>" % escape(display_name).encode('utf-8'))
            f.write(b"</tr>")
        f.write(b"</table>")
        f.write(b"\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def guess_type(self, path):
        """Guess the type of a file.
        Argument is a PATH (a filename).
        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.
        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.
        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


def translate_path(path):
    """Translate a /-separated PATH to the local filename syntax.
    Components that mean special things to the local file system
    (e.g. drive or directory names) are ignored.  (XXX They should
    probably be diagnosed.)
    """
    # abandon query parameters
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    path = posixpath.normpath(unquote(path))
    words = path.split('/')
    words = filter(None, words)
    path = os.getcwd()
    for word in words:
        drive, word = os.path.splitdrive(word)
        head, word = os.path.split(word)
        if word in (os.curdir, os.pardir):
            continue
        path = os.path.join(path, word)
    return path


def signal_handler(signal, frame):
    print("You choose to stop me.")
    exit()


def main():
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8001
    server_address = ('', port)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    server = httpd.socket.getsockname()
    print("server_version: " + MyHTTPRequestHandler.server_version + ", python_version: " + MyHTTPRequestHandler.sys_version)
    print("Serving HTTP on: " + str(server[0]) + ", port: " + str(server[1]) + " ...")
    httpd.serve_forever()


if __name__ == '__main__':
    main()