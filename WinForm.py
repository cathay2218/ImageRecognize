#https://ithelp.ithome.com.tw/articles/10247294

import tkinter
import time

def showtime():
    print (time.ctime())


#------------------------------------------------------
form = tkinter.Tk()     #declare new winform
form.title = "Python Form Test"     #set form title
form.geometry = ('800x400')     #set form size(width x height)
form.resizable = (False, False)     #set form can be resize? bool(width, height)
form.iconbitmap()      #set program icon (*.ico)

#declare a btn
btnstr = tkinter.StringVar() # 初始化tk的字串變數
btnstr.set('time')
btn = tkinter.Button(form, bg = 'pink', fg = 'black', textvariable=btnstr, font=('微軟正黑體', 20), command=showtime)
btn.pack()  #put btn to form

#declare a label
ShowTime_LB = tkinter.Label(form, bg = 'white', fg = 'black', textvariable=btnstr, font=('微軟正黑體', 20))
ShowTime_LB.pack()

form.mainloop()     #start winform