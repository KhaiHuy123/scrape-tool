import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pyodbc
import webbrowser

SQL_SERVER = 'YOUR SERVER'
DRIVER = "{ODBC Driver 17 for SQL Server}"
# SQL_DATABASE = 'manga'
# SQL_DATABASE = 'manga_nettruyen'
# SQL_DATABASE = 'manga_truyenqqi'
SQL_DATABASE = 'online_books'
# SQL_DATABASE = 'product_web_scraping'
SQL_PASSWORD = 'password' # No need if using local database engine DBSM
SQL_AUTHENTICATION = 'Trusted_Connection=yes'
SQL_USERNAME = 'USER NAME'

def executer_database_commands():
    # connection_string = f"Driver={DRIVER};Server={SQL_SERVER};Database={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD};"
    connection_string = f"Driver={DRIVER};Server={SQL_SERVER};Database={SQL_DATABASE};{SQL_AUTHENTICATION};UID={SQL_USERNAME}"
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    return conn, cursor

def populate_tree(my_tree):
    conn, cursor = executer_database_commands()
    cursor.execute(
        '''
        SELECT title, url, current_price, discount, author_id,
        publisher_id, supplier_id, book_cover_id
        FROM books_fahasa        
        ''')
    # define index of record
    global INDEX
    INDEX = 0
    for row in cursor.fetchall():
        if INDEX %2 == 0:
            my_tree.insert(parent="",text="", index = "end",
                values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]),
                iid=INDEX,tags=('evenrow',))
        else:
            my_tree.insert(parent="",text="", index = "end",
                values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]),
                iid=INDEX,tags=('oddrow',))
        INDEX +=1
    cursor.close()
    conn.close()

# main feature
app = tk.Tk()
app.title("CRM.app - books data")
app.iconbitmap('C:\\Users\\HTH\\PycharmProjects\\scrape_tool\\application\\logo.ico')
app.geometry('1200x660')
app.config(background='#EEEEEE')

# define style
style = ttk.Style()
style.theme_use('default')
style.configure('Treeview', background ='#C0C0C0', foreground ='#000000',
    rowheight = '30', show="headings", fieldbackground='#99FFFF')
style.map('Treeview', background = [('selected', '#3366FF')])
style.configure("Treeview.Heading", font=("Consolas", 14))

# create tree_frame
tree_frame = Frame(app)
tree_frame.pack(pady=10)

# create scrollbar
tree_scrollbar_y = Scrollbar(tree_frame, orient="vertical")
tree_scrollbar_y.pack(side=RIGHT, fill = Y)

# Create horizontal scrollbar
tree_scrollbar_x = Scrollbar(tree_frame, orient="horizontal")
tree_scrollbar_x.pack(side=BOTTOM, fill=X)

# create treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar_y.set,
    xscrollcommand=tree_scrollbar_x.set, selectmode='extended')
my_tree.pack(padx=5)

# set command for scrollbar
tree_scrollbar_y.config(command=my_tree.yview)
tree_scrollbar_x.config(command=my_tree.xview)

# define columns
columns = ("title", "url", "offical_price", "discount", "author_id",
           "publisher_id", "supplier_id", "book_cover_id")
my_tree.config(columns=columns)

# format columns
my_tree.column('#0', width=0, stretch=NO)
my_tree.column('title', width=500, anchor=W)
my_tree.column('url', width=500, anchor=W)
my_tree.column('offical_price', width=140, anchor=CENTER)
my_tree.column('discount', width=140, anchor=CENTER)
my_tree.column('author_id', width=140, anchor=CENTER)
my_tree.column('publisher_id', width=140, anchor=CENTER)
my_tree.column('supplier_id', width=140, anchor=CENTER)
my_tree.column('book_cover_id', width=140, anchor=CENTER)

# create striped row tags
my_tree.tag_configure('oddrow', background='#FFCC33')
my_tree.tag_configure('evenrow', background='#99FFFF')

# define headings
for col in columns:
    my_tree.heading(col, text=col, anchor= CENTER)

# populate treeview with data from database
populate_tree(my_tree)

# add record information
data_frame = LabelFrame(app, text ="RECORD", border=5, font=('Bold Consolas',15))
data_frame.pack(fill='x', expand = 'yes', padx=10)

global title_label, title_entry
title_label = Label(data_frame, text = 'Title', font=('Bold Consolas',12))
title_label.grid(row=0, column=0, padx=10, pady=10)
title_entry = Entry(data_frame, width=38, font=('Consolas',11), border=2, background='#DDDDDD')
title_entry.grid(row=0, column=1, padx=5, pady=10)

global offical_price_label, offical_price_entry
offical_price_label = Label(data_frame, text = 'Offical price', font=('Bold Consolas',12))
offical_price_label.grid(row=0, column=2, padx=15, pady=5)
offical_price_entry = Entry(data_frame, width=10, font=('Consolas',11), border=2, background='#DDDDDD')
offical_price_entry.grid(row=0, column=3, padx=5, pady=10)

global discount_label, discount_entry
discount_label = Label(data_frame, text = 'Discount', font=('Bold Consolas',12))
discount_label.grid(row=0, column=4, padx=15, pady=5)
discount_entry = Entry(data_frame, width=6, font=('Consolas',11), border=2, background='#DDDDDD')
discount_entry.grid(row=0, column=5, padx=5, pady=10)

global author_label, author_entry
author_label = Label(data_frame, text = ' Author', font=('Bold Consolas',12))
author_label.grid(row=1, column=0, padx=10, pady=10)
author_entry = Entry(data_frame, width=30, font=('Consolas',11), border=2, background='#DDDDDD')
author_entry.grid(row=1, column=1, padx=5, pady=10)

global publisher_label, publisher_entry
publisher_label = Label(data_frame, text = 'Publisher', font=('Bold Consolas',12))
publisher_label.grid(row=1, column=2, padx=10, pady=10)
publisher_entry = Entry(data_frame, width=26, font=('Consolas',11), border=2, background='#DDDDDD')
publisher_entry.grid(row=1, column=3, padx=5, pady=10)

global supplier_label, supplier_entry
supplier_label = Label(data_frame, text = 'Supplier', font=('Bold Consolas',12))
supplier_label.grid(row=1, column=4, padx=10, pady=10)
supplier_entry = Entry(data_frame,width=26, font=('Consolas',11), border=2, background='#DDDDDD')
supplier_entry.grid(row=1, column=5, padx=5, pady=10)

global book_cover_label, book_cover_entry
book_cover_label = Label(data_frame, text = 'Book Cover', font=('Bold Consolas',12))
book_cover_label.grid(row=2, column=0, padx=10, pady=10)
book_cover_entry = Entry(data_frame,width=26, font=('Consolas',11), border=2, background='#DDDDDD')
book_cover_entry.grid(row=2, column=1, padx=5, pady=10)

global url_label, url_entry
url_label = Label(data_frame, text = 'URL', font=('Bold Consolas',12))
url_label.grid(row=2, column=2, padx=10, pady=10)
url_entry = Entry(data_frame, width=75, font=('Consolas',11), border=2, background='#DDDDDD')
url_entry.grid(row=2, column=3, padx=5, pady=10, columnspan=3)

global list_attribute
list_attribute = [author_entry, publisher_entry,
                  supplier_entry, book_cover_entry]
global list_id
list_id = ['author_id', 'publisher_id',
            'supplier_id', 'book_cover_id']
global list_tag
list_tag = ['author_info', 'publisher_info',
            'supplier_info', 'book_cover_type']
global list_table
list_table = ['author_fahasa', 'publisher_fahasa',
              'supplier_fahasa', 'book_cover_fahasa']
# add button
button_frame = LabelFrame(app, text ="COMMANDS", border=5, font=('Bold Consolas',15))
button_frame.pack(fill='x', expand = 'yes', padx=10)

global view_button
view_button = Button(button_frame, text='View Details', border=4, font=('Bold Consolas',12), state='disable')
view_button.grid(row=0, column=0, ipadx=10, ipady=5, padx=15, pady=4)

global move_up_button
move_up_button = Button(button_frame, text='Move Up', border=4, font=('Bold Consolas',12), state='disable')
move_up_button.grid(row=0, column=1, ipadx=10, ipady=5, padx=15, pady=4)

global move_down_button
move_down_button = Button(button_frame, text='Move Down', border=4, font=('Bold Consolas', 12), state='disable')
move_down_button.grid(row=0, column=2, ipadx=10, ipady=5, padx=15, pady=4)

global select_button
select_button = Button(button_frame, text='Select item', border=4, font=('Bold Consolas', 12))
select_button.grid(row=0, column=3, ipadx=10, ipady=5, padx=20, pady=4)

global clear_button
clear_button = Button(button_frame, text='Clear all', border=4, font=('Bold Consolas', 12))
clear_button.grid(row=0, column=4, ipadx=10, ipady=5, padx=15, pady=4)

global update_button
update_button = Button(button_frame, text='Update', border=4, font=('Bold Consolas', 12), state='disable')
update_button.grid(row=0, column=5, ipadx=10, ipady=5, padx=15, pady=4)

global check_id_button
check_id_button = Button(button_frame, text='Check ID', border=4, font=('Bold Consolas', 12))
check_id_button.grid(row=0, column=6, ipadx=10, ipady=5, padx=15, pady=4)

global support_button
support_button = Button(button_frame, text='Support', border=4, font=('Bold Consolas', 12))
support_button.grid(row=0, column=7, ipadx=10, ipady=5, padx=11, pady=4)

img_logo = ImageTk.PhotoImage(file="C:\\Users\\HTH\\PycharmProjects\\"
                              "scrape_tool\\application\\scout_regiment__.jpg")
global logo_label
logo_label = Label(button_frame, text='', image=img_logo)
logo_label.grid(row=0, column=8, padx=11, pady=4)

def fill_entry(values):
    conn, cursor = executer_database_commands()

    title_entry.insert(0, values[0])
    url_entry.insert(0, values[1])
    offical_price_entry.insert(0, values[2])
    discount_entry.insert(0, values[3])
    author_entry.insert(0, values[4])
    publisher_entry.insert(0, values[5])
    supplier_entry.insert(0, values[6])
    book_cover_entry.insert(0, values[7])

    index = 4
    for i in range(4) :
        attribute = list_attribute[i]
        if values[index] is None or values[index] =='None':
            index +=1
            continue
        cursor.execute(
            f'''
            SELECT {list_tag[i]}
            FROM {list_table[i]}   
            WHERE {list_id[i]} = '{values[index]}'
            ''')
        val = cursor.fetchall()
        for v in val:
            attribute.delete(0, END)
            attribute.insert(0, v[0]) # Assuming the result is in v[0], adjust accordingly
        index +=1

    cursor.commit()
    cursor.close()
    conn.close()

def clear_entry():
    # set view mode to disable
    view_button.configure(state='disable')
    # set updata mode to disable
    update_button.configure(state='disable')
    # set checking mode to normal
    check_id_button.configure(state='normal')
    # set viewtools mode to normal
    support_button.configure(state='normal')
    # clear data
    title_entry.delete(0, END)
    url_entry.delete(0, END)
    offical_price_entry.delete(0, END)
    discount_entry.delete(0, END)
    author_entry.delete(0, END)
    publisher_entry.delete(0, END)
    supplier_entry.delete(0, END)
    book_cover_entry.delete(0, END)

def display_data():
    # set moving moce to normal
    move_down_button.configure(state='normal')
    move_up_button.configure(state='normal')

    # clear entry
    clear_entry()

    # set updata mode to normal
    update_button.configure(state='normal')

    # set view mode to normal
    view_button.configure(state='normal')

    # get record Index Number
    selected = my_tree.focus()

    # get record Value
    values = my_tree.item(selected, 'values')

    # display data
    fill_entry(values)

def select_record_In_treeview(event):
    # set moving moce to normal
    move_down_button.configure(state='normal')
    move_up_button.configure(state='normal')

    # clear entry
    clear_entry()

    # set view mode to normal
    view_button.configure(state='normal')

    # get record Index Number
    selected = my_tree.focus()

    # get record Value
    values = my_tree.item(selected, 'values')

    # display data
    fill_entry(values)

def open_url(url):
    webbrowser.open(url)

def view_details():
    url = url_entry.get()
    open_url(url)

def move_up():
    move_down_button.configure(state='normal')
    row = my_tree.selection()[0] # Get the ID of the selected row
    parent = my_tree.parent(row) # Get the parent of the selected row
    index = my_tree.index(row) # Get the index of the selected row
    if index > 0:
        my_tree.move(row, parent, index - 1) # Move the row up one position
    else:
        move_up_button.configure(state='disable')
        return None

def move_down():
    move_up_button.configure(state='normal')
    row = my_tree.selection()[0] # Get the ID of the selected row
    parent = my_tree.parent(row) # Get the parent of the selected row
    index = my_tree.index(row) # Get the index of the selected row
    children = my_tree.get_children(parent) # Get the list of children IDs
    if index < len(children) - 1:
        my_tree.move(row, parent, index + 1) # Move the row down one position
    else:
        move_down_button.configure(state='disable')
        return None

def update():
    # get record
    selected = my_tree.focus()
    # new data ready for update
    data=(title_entry.get(),url_entry.get(),offical_price_entry.get(),
          discount_entry.get(),author_entry.get(), publisher_entry.get(),
          supplier_entry.get(),book_cover_entry.get())
    # update data
    my_tree.item(selected, text='', values=data)

def open_viewer_for_checking():
    check_id_button.configure(state='disable')
    global viewer_for_checking
    viewer_for_checking = Toplevel()
    viewer_for_checking.title('CheckID.Viewer')
    viewer_for_checking.iconbitmap('C:\\Users\\HTH\\PycharmProjects\\scrape_tool\\application\\logo.ico')
    viewer_for_checking.geometry('870x750')

    def insert_tree(tree, table_name):
        conn, cursor = executer_database_commands()
        cursor.execute(
            f'''
            SELECT * FROM
            {table_name}
            ''')
        I=0
        for row in cursor.fetchall():
            if I % 2 == 0:
                tree.insert(parent="", text="", index="end",
                               values=(row[0], row[1]),
                               iid=I, tags=('evenrow',))
            else:
                tree.insert(parent="", text="", index="end",
                               values=(row[0], row[1]),
                               iid=I, tags=('oddrow',))
            I += 1
        cursor.close()
        conn.close()

    def create_treeview(frame, tree_name, bg_color='lightgray'):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(pady=10)

        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=tree_scrollbar.set,
            columns=(f"{tree_name}_id", f"{tree_name}_info"),
            show="headings"
        )

        tree.pack(fill="both", expand=True)

        tree_scrollbar.config(command=tree.yview)

        tree.column(f"{tree_name}_id", width=150)
        tree.column(f"{tree_name}_info", width=250)

        tree.heading(f"{tree_name}_id", text=f"{tree_name}_id", anchor=CENTER)
        tree.heading(f"{tree_name}_info", text=f"{tree_name}_info", anchor=CENTER)

        # Apply alternating row colors
        tree.tag_configure("evenrow", background=bg_color)
        tree.tag_configure("oddrow", background="white")

        return tree

    # Create a Frame for each Treeview
    tree_frame1 = ttk.Frame(viewer_for_checking)
    tree_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tree_frame2 = ttk.Frame(viewer_for_checking)
    tree_frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    tree_frame3 = ttk.Frame(viewer_for_checking)
    tree_frame3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tree_frame4 = ttk.Frame(viewer_for_checking)
    tree_frame4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Create Treeviews for each Frame
    tree1 = create_treeview(tree_frame1,tree_name='author')
    tree2 = create_treeview(tree_frame2, tree_name='publisher')
    tree3 = create_treeview(tree_frame3, tree_name='supplier')
    tree4 = create_treeview(tree_frame4, tree_name='book_cover')
    insert_tree(tree1, table_name=list_table[0])
    insert_tree(tree2, table_name=list_table[1])
    insert_tree(tree3, table_name=list_table[2])
    insert_tree(tree4, table_name=list_table[3])

def open_tools():
    support_button.configure(state='disable')
    webbrowser.open('https://github.com/KhaiHuy123/scrape_tool')
    pass

select_button.configure(command=display_data)
view_button.configure(command=view_details)
clear_button.configure(command=clear_entry)
move_up_button.configure(command=move_up)
move_down_button.configure(command=move_down)
update_button.configure(command=update)
check_id_button.configure(command=open_viewer_for_checking)
support_button.configure(command=open_tools)

# bind treeview
my_tree.bind('<ButtonRelease-1>', select_record_In_treeview)

app.mainloop()
