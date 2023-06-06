# -- coding: utf-8 --
import tkinter
from tkinter import filedialog
import subprocess
import re
import logging
import os

def signfilePathopen():
    path = filedialog.askopenfilename()
    signfilePath.set(path)

def aabfilePathopen():
    path = filedialog.askopenfilename()
    aabfilePath.set(path)

def buttonHandler():
    if signfilePath.get() == '':
        errT.set("未选择签名文件.....")
        return
    if find_string(signfilePath.get(),'.jks'):
        if keyalias.get() == '':
            errT.set("请输入alias.....")
            return
        if keypassword.get() == '':
            errT.set("请输入password.....")
            return
        if find_string(aabfilePath.get(),'.aab'):
            print(os.getcwd())
            file_name = os.getcwd() + "\\app.apks"
            if os.path.exists(file_name):
                os.remove(file_name)
                print('成功删除文件:', file_name)
            print("java -jar "+ bundletool +"build-apks --bundle=" + aabfilePath.get() + " --output="+file_name+" --ks=" + signfilePath.get()+ " --ks-key-alias="+keyalias.get()+ " --ks-pass pass:"+keypassword.get())
            outapks = execCmd("java -jar "+ bundletool +"build-apks --bundle=" + aabfilePath.get() + " --output="+file_name+" --ks=" + signfilePath.get()+ " --ks-key-alias="+keyalias.get()+ " --ks-pass pass:"+keypassword.get())
            if os.path.exists(file_name):
                errT.set('开始安装.......')
                installapks = execCmd("java -jar "+ bundletool +"install-apks --apks=" + file_name)
                print(installapks)

        else:
            outsha1 = execCmd(keytool+ "-v -list -keystore " + signfilePath.get() + " -storepass "+  keypassword.get())
            if find_string(outsha1,'Exception'):
                errT.set('keystore password was incorrect')
                return
            a = outsha1.split('SHA1: ')
            b = a[1].split('SHA256')
            SHA1.set(b[0].strip())
            outHashkey = execCmd(keytool+ "-exportcert -alias " + keyalias.get() + " -storepass "+ keypassword.get() + " -keystore "+  signfilePath.get() + " | " + openssl+ "sha1 -binary | "+ openssl+ "base64")
            HasHkey.set(outHashkey.strip())
    elif find_string(signfilePath.get(),'.der'):
        outGoogleHashkey = execCmd(openssl+ "sha1 -binary " + signfilePath.get() + " | " + openssl+ "base64 ")
        HasHkey.set(outGoogleHashkey.strip())
        SHA1.set("***************************")
    else:
        errT.set("文件格式不对......")



def execCmd(command):
    subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="gbk")
    subp.wait()
    if subp.poll() == 0:
        logging.info(subp.communicate()[0])
        return subp.communicate()[0]
    else:
        errT.set("运行失败")


def addToClipboard(string ):
    r = tkinter.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(string)
    r.update()
    r.destroy()


# ***.jks android签名文件
# ***.der 谷歌二次签名文件
def find_string(s,t):
    return s.find(t) != -1

keytool = os.path.abspath('keytool')+".exe "
openssl = os.path.abspath('openssl')+".exe "
bundletool = os.path.abspath('bundletool')+".jar "

logging.basicConfig(filename=os.path.join(os.getcwd(),'keylog.txt'),level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
top = tkinter.Tk()
top.geometry('500x400')
Offsety = 40

# --------------------------------------------------------------

errT = tkinter.StringVar(value='')
o = tkinter.Label(top, width = 50, textvariable = errT, fg='#ff0000')
o.place(x = 100, y = Offsety*0, width=300, height=25)
# --------------------------------------------------------------

m = tkinter.Label(top, bd =5, width = 10, text = "aab文件：")
m.place(x = 0, y = Offsety*1, width=80, height=25)

aabfilePath = tkinter.StringVar(value='')
n = tkinter.Entry(top, bd =5, width = 40,textvariable=aabfilePath)
n.place(x = 75, y = Offsety*1, width=340, height=25)

o = tkinter.Button(top, text ="打开", command = aabfilePathopen)
o.place(x = 415, y = Offsety*1, width=60, height=25)

# --------------------------------------------------------------

a = tkinter.Label(top, bd =5, width = 10, text = "签名文件：")
a.place(x = 0, y = Offsety*2, width=80, height=25)

signfilePath = tkinter.StringVar(value='')
b = tkinter.Entry(top, bd =5, width = 40,textvariable=signfilePath)
b.place(x = 75, y = Offsety*2, width=340, height=25)

c = tkinter.Button(top, text ="打开", command = signfilePathopen)
c.place(x = 415, y = Offsety*2, width=60, height=25)

# --------------------------------------------------------------

d = tkinter.Label(top, bd =5, width = 10, text = "alias:")
d.place(x = 0, y = Offsety*3, width=80, height=25)

keyalias = tkinter.StringVar(value='')
e = tkinter.Entry(top, bd =5, width = 40,textvariable=keyalias)
e.place(x = 75, y = Offsety*3, width=400, height=25)

# --------------------------------------------------------------

f= tkinter.Label(top, bd =5, width = 10, text = "password:")
f.place(x = 0, y = Offsety*4, width=80, height=25)

keypassword = tkinter.StringVar(value='')
g = tkinter.Entry(top, bd =5, width = 40,textvariable=keypassword)
g.place(x = 75, y = Offsety*4, width=400, height=25)

# --------------------------------------------------------------

# --------------------------------------------------------------

h = tkinter.Label(top, bd =5, width = 10, text = "SHA1: ")
h.place(x = 0, y = Offsety*5, width=80, height=25)

SHA1 = tkinter.StringVar(value='')
i = tkinter.Entry(top, width = 50, textvariable = SHA1, background='#DDDDDD', fg='#000000')
i.place(x = 75, y = Offsety*5, width=320, height=25)

copySHA1 = tkinter.Button(top, text ="copy", command = lambda:addToClipboard(SHA1.get()))
copySHA1.place(x = 415, y = Offsety*5, width=60, height=25)

# --------------------------------------------------------------

j = tkinter.Label(top, bd =5, width = 10, text = "HasH key: ")
j.place(x = 0, y = Offsety*6, width=80, height=25)

HasHkey = tkinter.StringVar(value='')
k = tkinter.Entry(top, width = 50, textvariable = HasHkey, background='#DDDDDD', fg='#000000')
k.place(x = 75, y = Offsety*6, width=320, height=25)

copyHasHkey = tkinter.Button(top, text ="copy", command = lambda:addToClipboard(HasHkey.get()))
copyHasHkey.place(x = 415, y = Offsety*6, width=60, height=25)

# --------------------------------------------------------------

l = tkinter.Button(top, text ="开始生成", command = buttonHandler)
l.place(x = 215, y = Offsety*7, width=85, height=40)

# 进入消息循环
top.mainloop()
