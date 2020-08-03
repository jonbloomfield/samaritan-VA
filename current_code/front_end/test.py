import tkinter as tk
import tkinter.ttk as ttk
root=tk.Tk()
scrollbar = tk.Scrollbar()
scrollbar.grid(column=1,row=0,sticky="ns")
text = tk.Text(wrap="word", yscrollcommand=scrollbar.set)
text.grid(row=0,column=0)
text.insert(1.0,"test \n"*10)
scrollbar.config(command=text.yview)

root.mainloop()