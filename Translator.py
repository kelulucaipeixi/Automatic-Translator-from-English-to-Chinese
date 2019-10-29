import urllib.request
from bs4 import BeautifulSoup
import PyHook3
import pythoncom
import tkinter
import win32clipboard
import sys,time
import pyautogui

def getMousePos():
	x,y=pyautogui.position()
	return x,y

def getWordMean(word):
	try:
		request=urllib.request.Request('http://iciba.com/'+word)
		reponse=urllib.request.urlopen('http://iciba.com/'+word)
		source_code=reponse.read()
		soup=BeautifulSoup(source_code,'html.parser')
		li=soup.find('li',class_='clearfix')
		means=li.findAll('span')
		result=""
		for item in means:
			result+=item.contents[0]
		create_frame(result)
	except:
		create_frame("查询失败")

def getClipBoardValues():
    # 获取粘贴板内容
    win32clipboard.OpenClipboard()
    value = win32clipboard.GetClipboardData()
    # win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    return value 
 
current_window=None
QUIT_WORD="EXIT"
QUIT_CONT=QUIT_WORD

def onKeyDown(event):
	global current_window,QUIT_WORD,QUIT_CONT
	if len(QUIT_WORD)==0:
		sys.exit()
		return False
	if event.Window!=current_window:
		current_window=event.Window
	if event.Key=='C':
		time.sleep(1.5)
		value=getClipBoardValues()
		ans=getWordMean(value)
	if event.Key==QUIT_WORD[0]:
		QUIT_WORD=QUIT_WORD[1:]
		if len(QUIT_WORD)==0:
			sys.exit()
			return False
	else:
		QUIT_WORD=QUIT_CONT
	return True
 
import threading
def create_frame(value):
    base = tkinter.Tk()
    base.wm_attributes('-topmost',1)
    base.title('translator')
    # btn = tkinter.Button(base, text="开始监控", command=start)
    # btn.pack()
    # base.mainloop()
    text=value
    show=tkinter.Text(base)
    show.insert('0.0',text)
    show.pack()
    # def autoClose():
    # 	time.sleep(6)
    # 	base.destroy()

    # t=threading.Thread(target=autoClose)
    # t.start()
    base.geometry("170x200+"+str(getMousePos()[0])+"+"+str(getMousePos()[1]))
    base.mainloop()

def start():
    # 注册管理器
    pyhm = PyHook3.HookManager()
    # 回调函数
    pyhm.KeyDown = onKeyDown
    # 勾住事件
    pyhm.HookKeyboard()
    # 输送出去
    pythoncom.PumpMessages()
 
if __name__ == '__main__':
    start()