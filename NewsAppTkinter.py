from tkinter import*
from tkinter import ttk
from NewsAppFunctions import*

def newsWindow():
    news_app(e1.get(), e2.get())
    newsWindow = Toplevel(root)
    newsWindow.title("Morning News")
    
    configfile = Text(newsWindow, wrap=WORD, width=100, height=200)
    configfile.pack()
    
    filename = './output/news_summary.txt'
    with open(filename, 'r') as f:
        configfile.insert(INSERT, f.read())

root = Tk()
root.title("Morning News")
Label(root, text="Enter your news topic").grid(row=0)
Label(root, text="Your preferred language").grid(row=1)

e1 = Entry(root)
e1.grid(row=0, column=1)

langs = ('ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh')
   
# Create a combobox widget
e2 = StringVar()
cb= ttk.Combobox(root, textvariable= e2)
cb['values']= langs
cb['state']= 'readonly'
cb.grid(row=1, column=1)

Button(root, text='Quit', command=root.quit).grid(row=3, column=2, sticky=W, pady=4)
Button(root, text='Read News', command=newsWindow).grid(row=3, column=1, sticky=W, pady=4)

mainloop()