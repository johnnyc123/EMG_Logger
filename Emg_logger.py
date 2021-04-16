import tkinter
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter import ttk
from db import Database
import datetime

db = Database("errors.db")
app = Tk()
app.title("EMG Error Logger")
myFont = Font(family="Helvetica", size=9)
app.geometry("900x600")
#Software Icon
app.iconbitmap('C:/Users/johnn/OneDrive/Documents/Intra_stuff/EMG_App/exe/dist/data.ico')
screenwidth = app.winfo_screenwidth()
screenheight = app.winfo_screenheight()

#Creating Treeview
my_tree = ttk.Treeview(app)
my_tree.grid(row=5, column=0, columnspan=7, rowspan=6, pady=20, padx=60, sticky='nw')

#Scrollbar
tree_scroll = Scrollbar(app, orient="vertical",command=my_tree.yview)
my_tree.configure(yscrollcommand=tree_scroll.set)#selectmode=extended
tree_scroll.grid(row=5, column=4, rowspan=6, sticky='ns')

#Add some Style
style = ttk.Style()
style.configure("Treeview.Heading", font=(myFont))
style.theme_use("winnative")
# style.configure("Treeview", 
#     background="grey",
#     foreground="black")

my_tree['columns'] = ("ID", "Conversion Failed", "Unsupported Attachments", "Batch Validation Failed", "Not Recieved","Attachment no Extension" ,"Invalid Filename", "Date")

#Format Columns
my_tree.column("#0",width=0, stretch=False, minwidth=0)
my_tree.column("ID",anchor=CENTER, width=30,stretch=False, minwidth=30)
my_tree.column("Conversion Failed",anchor=CENTER, width=110,stretch=False,minwidth=110)
my_tree.column("Unsupported Attachments",anchor=CENTER, width=120,stretch=False,minwidth=120)
my_tree.column("Batch Validation Failed" ,anchor=CENTER, width=100,stretch=False,minwidth=100)
my_tree.column("Not Recieved", anchor=CENTER, width=100, stretch=False, minwidth=100)
my_tree.column("Attachment no Extension",anchor=CENTER, width=140,stretch=False,minwidth=140)
my_tree.column("Invalid Filename",anchor=CENTER, width=100,stretch=False,minwidth=100)
my_tree.column("Date",anchor=CENTER, width=70,stretch=False,minwidth=70)

#Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="id",anchor=W)
my_tree.heading("Conversion Failed", text="Conversion Failed", anchor=W)
my_tree.heading("Unsupported Attachments", text="Unsupported Attach", anchor=W)
my_tree.heading("Batch Validation Failed", text="Batch Failure", anchor=W)
my_tree.heading("Not Recieved", text="Not Recieved", anchor=W)
my_tree.heading("Attachment no Extension", text="Attachment no Extension", anchor=W)
my_tree.heading("Invalid Filename", text="Invalid Filename", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)

# recent_entries = Listbox(app, height=15, width=100, border=0)
# Creat window object

def errors_check():
    errors = True
    while errors == True:
        if convf_text.get() == "" or part_text.get() == "" or batchval_text.get() == "" or nrec_text.get() == "" or attachext_text.get() == "" or invfile_text.get() == "" or date_text.get() == "":
            messagebox.showerror("Required Fields", "Please fill in all fields")
            return
        else:
            pass

        if convf_text.get().isdigit() and part_text.get().isdigit() and batchval_text.get().isdigit() and nrec_text.get().isdigit() and attachext_text.get().isdigit() and invfile_text.get().isdigit():
            pass
        else:
            messagebox.showerror("Invalid Value", "Please ensure only numbers are entered for errors")
            return
        try:
            datetime.datetime.strptime(date_text.get(), '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the date in the format dd/mm/yyyy")
            return

        for query_result in db.fetch() :
            if date_text.get() in query_result:
                messagebox.showerror("Date entry duplicate", "A record with this date has already been entered")
                return
            else:
                errors = False
        print("No errors were found!")

count = 1
def populate_list():
    my_tree.tag_configure("oddrow", background="lightblue")

    global count
    # recent_entries.delete(0, END)
    # my_tree.delete(0, END)
    my_tree.delete(*my_tree.get_children())

    for row in db.fetch():
        if count % 2 == 0:
            # recent_entries.insert(END, row)
            my_tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

        else:
            my_tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]), tags=("oddrow",))

        print(count)
        count = count + 1



def add_item():
    errors_check()
    db.insert(convf_text.get(), part_text.get(), batchval_text.get(), nrec_text.get(), attachext_text.get(), invfile_text.get(), date_text.get())
    # recent_entries.delete(0, END)
    # recent_entries.insert(END, (convf_text.get(), part_text.get(), batchval_text.get(), nrec_text.get(), attachext_text.get(), 
    # invfile_text.get(), date_text.get()))
    my_tree.delete(*my_tree.get_children())
    my_tree.insert('', 'end', (convf_text.get(), part_text.get(), batchval_text.get(), nrec_text.get(), attachext_text.get(), invfile_text.get(), date_text.get()))  
    # print(convf_text.get(), part_text.get(), batchval_text.get(), nrec_text.get(), attachext_text.get(), invfile_text.get(), date_text.get())
    clear_text()
    populate_list()

def select_item(event):
    global selected_item
    try:
        index = my_tree.focus()
        selected_item = my_tree.item(index, 'values')
        date_entry.delete(0, END)
        date_entry.insert(0, selected_item[7])
        convf_entry.delete(0, END)
        convf_entry.insert(0, selected_item[1])
        part_entry.delete(0, END)
        part_entry.insert(0, selected_item[2])
        batchval_entry.delete(0, END)
        batchval_entry.insert(0, selected_item[3])
        nrec_entry.delete(0, END)
        nrec_entry.insert(0, selected_item[4])
        attachext_entry.delete(0, END)
        attachext_entry.insert(0, selected_item[5])
        invfile_entry.delete(0, END)
        invfile_entry.insert(0, selected_item[6])
    except IndexError:
        pass


    # try:
    #     # index = recent_entries.curselection()[0]
    #     # selected_item = recent_entries.get(index)
    #     # index = my_tree.curselection()[0]
    #     index = my_tree.selection()[0]
    #     selected_item = my_tree.get(index)
    #     date_entry.delete(0, END)
    #     date_entry.insert(END, selected_item[7])
    #     convf_entry.delete(0, END)
    #     convf_entry.insert(END, selected_item[1])
    #     part_entry.delete(0, END)
    #     part_entry.insert(END, selected_item[2])
    #     batchval_entry.delete(0, END)
    #     batchval_entry.insert(END, selected_item[3])
    #     nrec_entry.delete(0, END)
    #     nrec_entry.insert(END, selected_item[4])
    #     attachext_entry.delete(0, END)
    #     attachext_entry.insert(END, selected_item[5])
    #     invfile_entry.delete(0, END)
    #     invfile_entry.insert(END, selected_item[6])
    # except IndexError:
    #     pass


def remove_item():
    try:
        x = selected_item[0]
    except NameError:
        messagebox.showerror("Error", "Please select a record to be removed")
        return 
    response = messagebox.askyesno("Delete", "Are You Sure?", icon='warning')
    if response:
        db.remove(selected_item[0])
        populate_list()
        messagebox.showinfo("Success", "Record successfully deleted")
        clear_text()
    else:
        pass

#the ID is passed in as a reference which is selected_item[0]
def update_item():
    try:
        x = selected_item[0]
    except NameError:
        messagebox.showerror("Error", "Please select a record to update")
        return
    try:
        db.update(selected_item[0], convf_text.get(), part_text.get(), batchval_text.get(), nrec_text.get(), attachext_text.get(), invfile_text.get(), date_text.get())
        populate_list()
        messagebox.showinfo("Success", "Record updated successfully")
        clear_text()
    except IndexError:
        pass

def clear_text():
    #Refreshes search boxes
    date_entry.delete(0, END)
    part_entry.delete(0, END)
    invfile_entry.delete(0, END)
    attachext_entry.delete(0, END)
    nrec_entry.delete(0, END)
    batchval_entry.delete(0, END)
    convf_entry.delete(0, END)


#Stops user adjusting columns
def disableEvent(event):
    if my_tree.identify_region(event.x, event.y) == "seperator":
        if my_tree.identify_column(event.x) == "#0": #or "Conversion Failed" or "Unsupported Attachments" or "Batch Validation Failed" or "Not Recieved" or "Attachment no Extension" or "Invalid Filename" or "Date":
            return "break"

date_text = StringVar()
date_int = IntVar()
date_label = Label(app, text="Enter the date of errors in the format dd/mm/yyyy", font=("bold", 10), pady=35, padx=15)
date_label.grid(row=0, column=0, sticky=W)
date_entry = Entry(app, textvariable=date_text)
date_entry.grid(row=0, column=1)

#Conversion Failed
convf_text = StringVar()
convf_int = IntVar()
convf_label = Label(app, text="Conversion Failed", font=("bold", 10), pady=10, padx=15)
convf_label.grid(row=1, column=0, sticky=W)
convf_entry = Entry(app, textvariable=convf_text)
convf_entry.grid(row=1, column=1)

#Unsupported Attachments
part_text = StringVar()
part_int = IntVar()
part_label = Label(app, text="Unsupported Attachments", font=("bold", 10), pady=10, padx=15)
part_label.grid(row=1, column=2, sticky=W)
part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=1, column=3)

#Batch Validation Failed
batchval_text = StringVar()
batchval_int = IntVar()
batchval_label = Label(app, text="Batch Validation Failed", font=("bold", 10), pady=10, padx=15)
batchval_label.grid(row=2, column=0, sticky=W)
batchval_entry = Entry(app, textvariable=batchval_text)
batchval_entry.grid(row=2, column=1)

#Not Recieved
nrec_text = StringVar()
nrec_int = IntVar()
nrec_label = Label(app, text="Not Recieved", font=("bold", 10), padx=15)
nrec_label.grid(row=2, column=2, sticky=W)
nrec_entry = Entry(app, textvariable=nrec_text)
nrec_entry.grid(row=2, column=3)

#Attachment with no extension
attachext_text = StringVar()
attachext_int = IntVar()
attachext_label = Label(app, text="Attachment with no extension", font=("bold", 10), pady=10, padx=15)
attachext_label.grid(row=3, column=0, sticky=W)
attachext_entry = Entry(app, textvariable=attachext_text)
attachext_entry.grid(row=3, column=1)

#Invalid filename
invfile_text = StringVar()
invfile_int = IntVar()
invfile_label = Label(app, text="Invalid Filename", font=("bold", 10), padx=15)
invfile_label.grid(row=3, column=2, sticky=W)
invfile_entry = Entry(app, textvariable=invfile_text)
invfile_entry.grid(row=3, column=3)

#Recent Entries
# recent_entries = Listbox(app, height=15, width=100, border=0)
# recent_entries.grid(row=5, column=0, columnspan=4, rowspan=6, pady=20, padx=60)

# Scrollbar
# scrollbar = Scrollbar(app)
# scrollbar.grid(row=5, column=3)
# recent_entries.configure(yscrollcommand=scrollbar.set)
# scrollbar.configure(command=recent_entries.yview)

#Select row - Selects row once user release mouse
# recent_entries.bind("<<ListboxSelect>>", select_item)
my_tree.bind('<ButtonRelease-1>', select_item)

# #Stops user resizing columns
my_tree.bind("<Button-1>", disableEvent)
my_tree.bind('<Motion>', disableEvent)


# Buttons
add_btn = Button(app, text="Enter data", width=12, command=add_item)
add_btn.grid(row=4, column=0, pady=20)

remove_item_btn = Button(app, text="Remove data", width=12, command=remove_item)
remove_item_btn.grid(row=4, column=1)

update_btn = Button(app, text="Update data", width=12, command=update_item)
update_btn.grid(row=4, column=2)

clear_btn = Button(app, text="Clear input", width=12, command=clear_text)
clear_btn.grid(row=4, column=3)

print(db.get_average())
# Populate data into the treeview
populate_list()


app.mainloop()