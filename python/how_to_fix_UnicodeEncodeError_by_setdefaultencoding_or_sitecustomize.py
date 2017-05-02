#
# how to fix UnicodeEncodeError by setdefaultencoding or sitecustomize.py
#
1) Phenomenon: UnicodeEncodeError: 'ascii' codec can't encode characters in position 23-28: ordinal not in range(128)
    
    <= caused by tkFileDialog.askopenfilename(), when the file name contains Chinese character.
    <= source code:
        from Tkinter import *
        from tkFileDialog import askopenfilename
        from tkColorChooser import askcolor
        from tkSimpleDialog import askfloat
        from tkMessageBox import askquestion, showerror
        from quitter import Quitter
        
        # consts
        #   for mapping
        demos = {
            'Open': askopenfilename,
            'Color': askcolor,
            'Query': lambda: askquestion('Warning', 'You typed "rm *".\nConfirm?'),
            'Error': lambda: showerror('Error', "He's dead, Jim."),
            'Input': lambda: askfloat('Entry', 'Enter credit card numer')
        }
        
        class Demo(Frame):
            def __init__(self, parent=None, **options):
                Frame.__init__(self, parent, **options)
                self.pack()
                Label(self, text='Basic dmons').pack()
                for (k, v) in demos.items():
                    Button(self, text=k, command=(lambda k=k: self.printit(k))).pack(side=TOP, fill=BOTH)
                    # func = (lambda k=k: self.printit(k))
                    # Button(self, text=k, command=func).pack(side=TOP, fill=BOTH)
                Quitter(self).pack(side=TOP, fill=BOTH)
        
            def printit(self, name):
                reload(sys)
                sys.setdefaultencoding('utf-8')
                print('{0} returns => {1}'.format(name, demos[name]()))
                # print('{0} returns => {1}'.format(name, demos[name]() if name!='Open' else demos[name]().decode('utf-8')))
        
        if __name__ == '__main__':
            Demo().mainloop()
            
2) fix:
               import sys
               reload(sys)
               sys.setdefaultencoding('utf-8')
               
      Method1. in a .py script using encoding-related functions.
      Method2. in sitecustomize.py under same directory as 
                /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site.py.

3) use sys.getdefaultencoding() to check the default encoding set for file contents.


# ref:      http://blog.csdn.net/zuyi532/article/details/8851316


                
      
