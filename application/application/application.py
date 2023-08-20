import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pyodbc
import webbrowser

class Database:
    def __init__(self):
        self.SQL_SERVER = 'YOUR SERVER'
        self.DRIVER = "{ODBC Driver 17 for SQL Server}"
        self.SQL_DATABASE = 'online_books'
        self.SQL_AUTHENTICATION = 'Trusted_Connection=yes'
        self.SQL_USERNAME = 'USER NAME'
        self.SQL_PASSWORD = 'password'  # No need if using local database engine DBSM

    def connect(self):
        connection_string = f"Driver={self.DRIVER};Server={self.SQL_SERVER};" \
                            f"Database={self.SQL_DATABASE};{self.SQL_AUTHENTICATION};" \
                            f"UID={self.SQL_USERNAME}"
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        return conn, cursor

class BookViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRM.app - books data")
        self.root.iconbitmap('C:\\Users\\HTH\\PycharmProjects\\scrape_tool\\application\\logo.ico')
        self.root.geometry('1200x660')
        self.root.config(background='#EEEEEE')

        self.db = Database()

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('Treeview', background='#C0C0C0', foreground='#000000',
                             rowheight='30', show="headings", fieldbackground='#99FFFF')
        self.style.map('Treeview', background=[('selected', '#3366FF')])
        self.style.configure("Treeview.Heading", font=("Consolas", 14))

        self.tree_frame = Frame(self.root)
        self.tree_frame.pack(pady=10)

        self.tree_scrollbar_y = Scrollbar(self.tree_frame, orient="vertical")
        self.tree_scrollbar_y.pack(side=RIGHT, fill=Y)

        self.tree_scrollbar_x = Scrollbar(self.tree_frame, orient="horizontal")
        self.tree_scrollbar_x.pack(side=BOTTOM, fill=X)

        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scrollbar_y.set,
                                   xscrollcommand=self.tree_scrollbar_x.set, selectmode='extended')
        self.my_tree.pack(padx=5)

        self.tree_scrollbar_y.config(command=self.my_tree.yview)
        self.tree_scrollbar_x.config(command=self.my_tree.xview)

        self.columns = ("title", "url", "offical_price", "discount", "author_id",
                        "publisher_id", "supplier_id", "book_cover_id")
        self.my_tree.config(columns=self.columns)

        self.my_tree.column('#0', width=0, stretch=NO)
        self.my_tree.column('title', width=500, anchor=W)
        self.my_tree.column('url', width=500, anchor=W)
        self.my_tree.column('offical_price', width=140, anchor=CENTER)
        self.my_tree.column('discount', width=140, anchor=CENTER)
        self.my_tree.column('author_id', width=140, anchor=CENTER)
        self.my_tree.column('publisher_id', width=140, anchor=CENTER)
        self.my_tree.column('supplier_id', width=140, anchor=CENTER)
        self.my_tree.column('book_cover_id', width=140, anchor=CENTER)

        self.my_tree.tag_configure('oddrow', background='#FFCC33')
        self.my_tree.tag_configure('evenrow', background='#99FFFF')

        for col in self.columns:
            self.my_tree.heading(col, text=col, anchor=CENTER)

        self.populate_tree()

        self.create_record()

        self.create_buttons()

        self.list_attribute = [self.author_entry, self.publisher_entry,
                          self.supplier_entry, self.book_cover_entry]

        self.list_id = ['author_id', 'publisher_id',
                   'supplier_id', 'book_cover_id']

        self.list_tag = ['author_info', 'publisher_info',
                    'supplier_info', 'book_cover_type']

        self.list_table = ['author_fahasa', 'publisher_fahasa',
                      'supplier_fahasa', 'book_cover_fahasa']

    def populate_tree(self):
        conn, cursor = self.db.connect()
        cursor.execute(
            '''
            SELECT title, url, current_price, discount, author_id,
            publisher_id, supplier_id, book_cover_id
            FROM books_fahasa        
            ''')
        # define index of record
        INDEX = 0
        for row in cursor.fetchall():
            if INDEX % 2 == 0:
                self.my_tree.insert(parent="", text="", index="end",
                               values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                               iid=INDEX, tags=('evenrow',))
            else:
                self.my_tree.insert(parent="", text="", index="end",
                               values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                               iid=INDEX, tags=('oddrow',))
            INDEX += 1
        cursor.commit()
        cursor.close()
        conn.close()

    def create_record(self):
        self.data_frame = LabelFrame(self.root, text="RECORD", border=5, font=('Bold Consolas', 15))
        self.data_frame.pack(fill='x', expand='yes', padx=10)

        self.title_label = Label(self.data_frame, text='Title', font=('Bold Consolas', 12))
        self.title_label.grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = Entry(self.data_frame, width=38, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.title_entry.grid(row=0, column=1, padx=5, pady=10)

        self.offical_price_label = Label(self.data_frame, text='Offical price', font=('Bold Consolas', 12))
        self.offical_price_label.grid(row=0, column=2, padx=15, pady=5)
        self.offical_price_entry = Entry(self.data_frame, width=10, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.offical_price_entry.grid(row=0, column=3, padx=5, pady=10)

        self.discount_label = Label(self.data_frame, text='Discount', font=('Bold Consolas', 12))
        self.discount_label.grid(row=0, column=4, padx=15, pady=5)
        self.discount_entry = Entry(self.data_frame, width=6, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.discount_entry.grid(row=0, column=5, padx=5, pady=10)

        self.author_label = Label(self.data_frame, text=' Author', font=('Bold Consolas', 12))
        self.author_label.grid(row=1, column=0, padx=10, pady=10)
        self.author_entry = Entry(self.data_frame, width=30, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.author_entry.grid(row=1, column=1, padx=5, pady=10)

        self.publisher_label = Label(self.data_frame, text='Publisher', font=('Bold Consolas', 12))
        self.publisher_label.grid(row=1, column=2, padx=10, pady=10)
        self.publisher_entry = Entry(self.data_frame, width=26, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.publisher_entry.grid(row=1, column=3, padx=5, pady=10)

        self.supplier_label = Label(self.data_frame, text='Supplier', font=('Bold Consolas', 12))
        self.supplier_label.grid(row=1, column=4, padx=10, pady=10)
        self.supplier_entry = Entry(self.data_frame, width=26, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.supplier_entry.grid(row=1, column=5, padx=5, pady=10)

        self.book_cover_label = Label(self.data_frame, text='Book Cover', font=('Bold Consolas', 12))
        self.book_cover_label.grid(row=2, column=0, padx=10, pady=10)
        self.book_cover_entry = Entry(self.data_frame, width=26, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.book_cover_entry.grid(row=2, column=1, padx=5, pady=10)

        self.url_label = Label(self.data_frame, text='URL', font=('Bold Consolas', 12))
        self.url_label.grid(row=2, column=2, padx=10, pady=10)
        self.url_entry = Entry(self.data_frame, width=75, font=('Consolas', 11), border=2, background='#DDDDDD')
        self.url_entry.grid(row=2, column=3, padx=5, pady=10, columnspan=3)

    def create_buttons(self):
        self.button_frame = LabelFrame(self.root, text="COMMANDS", border=5, font=('Bold Consolas', 15))
        self.button_frame.pack(fill='x', expand='yes', padx=10)

        self.view_button = Button(self.button_frame, text='View Details', border=4, font=('Bold Consolas', 12),
                                  state='disable', command=self.view_details)
        self.view_button.grid(row=0, column=0, ipadx=10, ipady=5, padx=15, pady=4)

        self.move_up_button = Button(self.button_frame, text='Move Up', border=4, font=('Bold Consolas', 12),
                                     state='disable', command=self.move_up)
        self.move_up_button.grid(row=0, column=1, ipadx=10, ipady=5, padx=15, pady=4)

        self.move_down_button = Button(self.button_frame, text='Move Down', border=4, font=('Bold Consolas', 12),
                                       state='disable', command=self.move_down)
        self.move_down_button.grid(row=0, column=2, ipadx=10, ipady=5, padx=15, pady=4)

        self.select_button = Button(self.button_frame, text='Select item', border=4, font=('Bold Consolas', 12),
                                    command=self.display_data)
        self.select_button.grid(row=0, column=3, ipadx=10, ipady=5, padx=20, pady=4)

        self.clear_button = Button(self.button_frame, text='Clear all', border=4, font=('Bold Consolas', 12),
                                   command=self.clear_entry)
        self.clear_button.grid(row=0, column=4, ipadx=10, ipady=5, padx=15, pady=4)

        self.update_button = Button(self.button_frame, text='Update', border=4, font=('Bold Consolas', 12),
                                    state='disable', command=self.update)
        self.update_button.grid(row=0, column=5, ipadx=10, ipady=5, padx=15, pady=4)

        self.check_id_button = Button(self.button_frame, text='Check ID', border=4, font=('Bold Consolas', 12),
                                      command=self.open_viewer_for_checking)
        self.check_id_button.grid(row=0, column=6, ipadx=10, ipady=5, padx=15, pady=4)

        self.support_button = Button(self.button_frame, text='Support', border=4, font=('Bold Consolas', 12),
                                     command=self.open_tools)
        self.support_button.grid(row=0, column=7, ipadx=10, ipady=5, padx=11, pady=4)

        self.img_logo = ImageTk.PhotoImage(
            file="C:\\Users\\HTH\\PycharmProjects\\scrape_tool\\application\\scout_regiment__.jpg")
        self.logo_label = Label(self.button_frame, text='', image=self.img_logo)
        self.logo_label.grid(row=0, column=8, padx=11, pady=4)

    def fill_entry(self, values):
        conn, cursor = self.db.connect()

        self.title_entry.insert(0, values[0])
        self.url_entry.insert(0, values[1])
        self.offical_price_entry.insert(0, values[2])
        self.discount_entry.insert(0, values[3])
        self.author_entry.insert(0, values[4])
        self.publisher_entry.insert(0, values[5])
        self.supplier_entry.insert(0, values[6])
        self.book_cover_entry.insert(0, values[7])

        index = 4
        for i in range(4):
            attribute = self.list_attribute[i]
            if values[index] is None or values[index] == 'None':
                index += 1
                continue
            cursor.execute(
                f'''
                    SELECT {self.list_tag[i]}
                    FROM {self.list_table[i]}   
                    WHERE {self.list_id[i]} = '{values[index]}'
                    ''')
            val = cursor.fetchall()
            for v in val:
                attribute.delete(0, END)
                attribute.insert(0, v[0])  # Assuming the result is in v[0], adjust accordingly
            index += 1

        cursor.commit()
        cursor.close()
        conn.close()

    def clear_entry(self):
        # set view mode to disable
        self.view_button.configure(state='disable')

        # set updata mode to disable
        self.update_button.configure(state='disable')

        # set checking mode to normal
        self.check_id_button.configure(state='normal')

        # set viewtools mode to normal
        self.support_button.configure(state='normal')

        # clear data
        self.title_entry.delete(0, END)
        self.url_entry.delete(0, END)
        self.offical_price_entry.delete(0, END)
        self.discount_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.publisher_entry.delete(0, END)
        self.supplier_entry.delete(0, END)
        self.book_cover_entry.delete(0, END)

    def display_data(self):
        # set moving moce to normal
        self.move_down_button.configure(state='normal')
        self.move_up_button.configure(state='normal')

        # clear entry
        self.clear_entry()

        # set updata mode to normal
        self.update_button.configure(state='normal')

        # set view mode to normal
        self.view_button.configure(state='normal')

        # get record Index Number
        selected = self.my_tree.focus()

        # get record Value
        values = self.my_tree.item(selected, 'values')

        # display data
        self.fill_entry(values)

    def view_details(self):
        url = self.url_entry.get()
        self.open_url(url)

    def move_up(self):
        self.move_down_button.configure(state='normal')
        row = self.my_tree.selection()[0]  # Get the ID of the selected row
        parent = self.my_tree.parent(row)  # Get the parent of the selected row
        index = self.my_tree.index(row)  # Get the index of the selected row
        if index > 0:
            self.my_tree.move(row, parent, index - 1)  # Move the row up one position
        else:
            self.move_up_button.configure(state='disable')
            return None

    def move_down(self):
        self.move_up_button.configure(state='normal')
        row = self.my_tree.selection()[0]  # Get the ID of the selected row
        parent = self.my_tree.parent(row)  # Get the parent of the selected row
        index = self.my_tree.index(row)  # Get the index of the selected row
        children = self.my_tree.get_children(parent)  # Get the list of children IDs
        if index < len(children) - 1:
            self.my_tree.move(row, parent, index + 1)  # Move the row down one position
        else:
            self.move_down_button.configure(state='disable')
            return None

    def update(self):
        # get record
        selected = self.my_tree.focus()

        # new data ready for update
        data = (self.title_entry.get(), self.url_entry.get(), self.offical_price_entry.get(),
                self.discount_entry.get(), self.author_entry.get(), self.publisher_entry.get(),
                self.supplier_entry.get(), self.book_cover_entry.get())

        # update data
        self.my_tree.item(selected, text='', values=data)

    def bind_treeview(self):
        self.my_tree.bind('<ButtonRelease-1>', self.select_record_in_treeview)

    def open_url(self, url):
        webbrowser.open(url)

    def select_record_in_treeview(self, event):
        self.move_down_button.configure(state='normal')
        self.move_up_button.configure(state='normal')

        self.clear_entry()
        self.view_button.configure(state='normal')

        selected = self.my_tree.focus()
        values = self.my_tree.item(selected, 'values')
        self.fill_entry(values)

    def open_viewer_for_checking(self):
        self.check_id_button.configure(state='disable')

        self.viewer_for_checking = Toplevel()
        self.viewer_for_checking.title('CheckID.Viewer')
        self.viewer_for_checking.iconbitmap('C:\\Users\\HTH\\PycharmProjects\\scrape_tool\\application\\logo.ico')
        self.viewer_for_checking.geometry('870x750')

        def insert_tree(tree, table_name):
            conn, cursor = self.db.connect()
            cursor.execute(
                f'''
                SELECT * FROM
                {table_name}
                ''')
            I = 0
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
        self.tree_frame1 = ttk.Frame(self.viewer_for_checking)
        self.tree_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tree_frame2 = ttk.Frame(self.viewer_for_checking)
        self.tree_frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tree_frame3 = ttk.Frame(self.viewer_for_checking)
        self.tree_frame3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree_frame4 = ttk.Frame(self.viewer_for_checking)
        self.tree_frame4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Create Treeviews for each Frame
        self.tree1 = create_treeview(self.tree_frame1, tree_name='author')
        self.tree2 = create_treeview(self.tree_frame2, tree_name='publisher')
        self.tree3 = create_treeview(self.tree_frame3, tree_name='supplier')
        self.tree4 = create_treeview(self.tree_frame4, tree_name='book_cover')
        insert_tree(self.tree1, table_name=self.list_table[0])
        insert_tree(self.tree2, table_name=self.list_table[1])
        insert_tree(self.tree3, table_name=self.list_table[2])
        insert_tree(self.tree4, table_name=self.list_table[3])

    def open_tools(self):
        self.support_button.configure(state='disable')
        webbrowser.open('https://github.com/KhaiHuy123/scrape_tool')

    def configure_buttons(self):
        self.select_button.configure(command=self.display_data)
        self.view_button.configure(command=self.view_details)
        self.clear_button.configure(command=self.clear_entry)
        self.move_up_button.configure(command=self.move_up)
        self.move_down_button.configure(command=self.move_down)
        self.update_button.configure(command=self.update)
        self.check_id_button.configure(command=self.open_viewer_for_checking)
        self.support_button.configure(command=self.open_tools)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookViewerApp(root)
    app.bind_treeview()  # Bind the treeview click event
    app.configure_buttons()
    root.mainloop()
