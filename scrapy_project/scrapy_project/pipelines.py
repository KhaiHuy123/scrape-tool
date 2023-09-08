# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface

import re
import pandas as pd
import pyodbc
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured
from .items import FahasaBook, FahasaBookList

class ScrapyProjectPipeline:
    def process_item(self, item, spider):
        return item

class FileWriterPipeline:
    def open_spider(self, spider):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.data)
        df.to_excel('reference.xlsx', sheet_name='reference')

class Saveto_sqlServerTruyenqqiPipeline:
    def __init__(self, server, database, username, authentication):
        self.server = server
        self.database = database
        self.username = username
        self.authentication = authentication

    @classmethod
    def from_crawler(cls, crawler):
        server = crawler.settings.get("SQL_SERVER")
        database = crawler.settings.get("SQL_DATABASE")
        username = crawler.settings.get("SQL_USERNAME")
        authentication = crawler.settings.get("SQL_AUTHENTICATION")
        if not server or not database:
            raise NotConfigured("SQL Server connection details are missing.")
        return cls(server, database, username, authentication)

    def open_spider(self, spider):
        # Connection information
        driver = "{ODBC Driver 17 for SQL Server}"
        server_name = self.server
        database_name = self.database
        authentication = self.authentication
        username = self.username
        # Connection string
        connection_string = f"DRIVER={driver};SERVER={server_name};DATABASE={database_name};{authentication};UID=?"
        # Connect to database
        self.conn = pyodbc.connect(connection_string, params=(self.username,))
        self.cursor = self.conn.cursor()
        self.create_table_if_not_exists()

    def process_item(self, item, spider):
        self.insert_tag_data(item)
        self.insert_container_data(item)
        self.insert_main_data(item)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def create_table_if_not_exists(self):
        # Create TagTable
        self.cursor.execute(
            '''
            CREATE TABLE  tag_truyenqqi (
                tag_id INT IDENTITY(1,1),
                tag_info NVARCHAR(150) PRIMARY KEY
            )
            '''
        )
        # Create ContainerTable
        self.cursor.execute(
            '''
            CREATE TABLE  container_truyenqqi (
                container_id INT IDENTITY(1,1) ,
                container_info NVARCHAR(255) PRIMARY KEY
            )
            '''
        )
        # Create MainTable
        self.cursor.execute(
            '''
            CREATE TABLE  truyenqqi (
                product_id INT IDENTITY(1,1) ,
                container NVARCHAR(255),
                title NVARCHAR(255) PRIMARY KEY,
                discription NVARCHAR(4000),
                view_count DECIMAL,
                condition NVARCHAR(50),
                follow DECIMAL,
                lastest_chap DECIMAL,
                link NVARCHAR(255),
                teaser NVARCHAR(255),
                tag NVARCHAR(355)
            )
            '''
        )
        self.conn.commit()

    def insert_tag_data(self, item):
        # Convert the 'item['tag']' string to a list of values
        types = item['tag'].split(',')
        types = [type.strip() for type in types]

        # Create a list of tuples containing the values to be upserted
        values = [(tag,) for tag_group in types for tag in tag_group.split(',')]

        # Create a temporary table to hold the distinct values
        self.cursor.execute('''
            CREATE TABLE #temp_tag (tag_info NVARCHAR(255))
                ''')

        # Insert the distinct values into the temporary table
        self.cursor.executemany('''
            INSERT INTO #temp_tag (tag_info) VALUES (?)
                ''', values)

        # SQL code to upsert data from the temporary table to the 'tag' table
        sql_code = '''
            MERGE INTO tag_truyenqqi AS target
            USING #temp_tag AS source
            ON target.tag_info = source.tag_info
            WHEN NOT MATCHED THEN
                INSERT (tag_info) VALUES (source.tag_info);
                '''

        # Perform the upsert operation
        self.cursor.execute(sql_code)
        self.conn.commit()

        # Drop the temporary table
        self.cursor.execute('''
                    DROP TABLE #temp_tag
                ''')
        self.conn.commit()

    def insert_container_data(self, item):
        # Upsert data into container tables
        self.cursor.execute('''
            MERGE INTO container_truyenqqi AS target
            USING (VALUES (?)) AS source (container_info)
            ON target.container_info = source.container_info
            WHEN NOT MATCHED THEN
            INSERT (container_info) VALUES (source.container_info);
                ''', (item['container']))
        self.conn.commit()

    def insert_main_data(self, item):
        self.cursor.execute(
            ''' 
            INSERT INTO truyenqqi (
                container,
                title,
                discription,
                view_count,
                condition,
                follow,
                lastest_chap,
                link,
                teaser,
                tag
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['container'],
                item['title'],
                item['discription'],
                item['view'],
                item['condition'],
                item['follow'],
                item['lastest_chap'],
                item['link'],
                item['teaser'],
                item['tag']
            )
        )
        self.conn.commit()

class Saveto_sqlServerNettruyenPipeline:
    def __init__(self, server, database, username, authentication):
        self.server = server
        self.database = database
        self.username = username
        self.authentication = authentication

    @classmethod
    def from_crawler(cls, crawler):
        server = crawler.settings.get("SQL_SERVER")
        database = crawler.settings.get("SQL_DATABASE")
        username = crawler.settings.get("SQL_USERNAME")
        authentication = crawler.settings.get("SQL_AUTHENTICATION")
        if not server or not database:
            raise NotConfigured("SQL Server connection details are missing.")
        return cls(server, database, username, authentication)

    def open_spider(self, spider):
        # Connection information
        driver = "{ODBC Driver 17 for SQL Server}"
        server_name = self.server
        database_name = self.database
        authentication = self.authentication
        username = self.username
        # Connection string
        connection_string = f"DRIVER={driver};SERVER={server_name};DATABASE={database_name};{authentication};UID=?"
        # Connect to database
        self.conn = pyodbc.connect(connection_string, params=(self.username,))
        self.cursor = self.conn.cursor()
        self.create_tables_if_not_exist()

    def process_item(self, item, spider):
        self.insert_tag_data(item)
        self.insert_container_data(item)
        self.insert_main_data(item)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def create_tables_if_not_exist(self):
        # Create Tag table
        self.cursor.execute('''
            CREATE TABLE  tag_nettruyen (
                tag_id INT IDENTITY(1,1) ,
                tag_info NVARCHAR(255) PRIMARY KEY
            )
        ''')
        # Create Container table
        self.cursor.execute('''
            CREATE TABLE  container_nettruyen (
                container_id INT  IDENTITY(1,1) ,
                container_info NVARCHAR(255) PRIMARY KEY
            )
        ''')
        # Create MainTable
        self.cursor.execute(
            '''
            CREATE TABLE  nettruyen (
                product_id INT IDENTITY(1,1) , 
                container NVARCHAR(255) ,
                title NVARCHAR(255) PRIMARY KEY ,
                link NVARCHAR(255),
                discription NVARCHAR(4000),
                lastest_chap NVARCHAR(50),
                type_product NVARCHAR(355),
                view_count INT,
                follow INT,
                teaser NVARCHAR(255),
                condition NVARCHAR(50)
            )
            '''
        )
        self.conn.commit()

    def insert_container_data(self, item):
        # Upsert data into container tables
        self.cursor.execute('''
            MERGE INTO container_nettruyen AS target
            USING (VALUES (?)) AS source (container_info)
            ON target.container_info = source.container_info
            WHEN NOT MATCHED THEN
                INSERT (container_info) VALUES (source.container_info);
        ''', (item['container']))
        self.conn.commit()

    def insert_tag_data(self, item):
        # Convert the 'item['type']' string to a list of values
        types = item['type'].split(',')
        types = [type.strip() for type in types]

        # Create a list of tuples containing the values to be upserted
        values = [(tag,) for tag_group in types for tag in tag_group.split(',')]

        # Create a temporary table to hold the distinct values
        self.cursor.execute('''
            CREATE TABLE #temp_tag (tag_info NVARCHAR(255))
        ''')

        # Insert the distinct values into the temporary table
        self.cursor.executemany('''
            INSERT INTO #temp_tag (tag_info) VALUES (?)
        ''', values)

        # SQL code to upsert data from the temporary table to the 'tag' table
        sql_code = '''
            MERGE INTO tag_nettruyen AS target
            USING #temp_tag AS source
            ON target.tag_info = source.tag_info
            WHEN NOT MATCHED THEN
                INSERT (tag_info) VALUES (source.tag_info);
        '''

        # Perform the upsert operation
        self.cursor.execute(sql_code)
        self.conn.commit()

        # Drop the temporary table
        self.cursor.execute('''
            DROP TABLE #temp_tag
        ''')
        self.conn.commit()

    def insert_main_data(self, item):
        self.cursor.execute(
            ''' 
                INSERT INTO nettruyen (
                    container,
                    title,
                    link,
                    discription,
                    lastest_chap,
                    type_product,
                    view_count,
                    follow,
                    teaser,
                    condition
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ''', (
                item['container'],
                item['title'],
                item['link'],
                item['discription'],
                item['lastest_chap'],
                item['type'],
                item['view'],
                item['follow'],
                item['teaser'],
                item['condition']
            )
        )
        self.conn.commit()

class Saveto_sqlServerAmazonPipeline:
    def __init__(self, server, database, username, authentication):
        self.server = server
        self.database = database
        self.username = username
        self.authentication = authentication

    @classmethod
    def from_crawler(cls, crawler):
        server = crawler.settings.get("SQL_SERVER")
        database = crawler.settings.get("SQL_DATABASE")
        username = crawler.settings.get("SQL_USERNAME")
        authentication = crawler.settings.get("SQL_AUTHENTICATION")
        if not server or not database:
            raise NotConfigured("SQL Server connection details are missing.")
        return cls(server, database, username, authentication)

    def open_spider(self, spider):
        # Connection information
        driver = "{ODBC Driver 17 for SQL Server}"
        server_name = self.server
        database_name = self.database
        authentication = self.authentication
        username = self.username
        # Connection string
        connection_string = f"DRIVER={driver};SERVER={server_name};DATABASE={database_name};{authentication};UID={username}"
        # Connect to database
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.create_table_if_not_exists()

    def process_item(self, item, spider):
        self.insert_main_data(item)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def create_table_if_not_exists(self):
        # Create MainTable
        self.cursor.execute(
            '''
            CREATE TABLE  amazon (
                url VARCHAR(150) ,
                title VARCHAR(70) PRIMARY KEY ,
                picture VARCHAR(150) ,
                sub_title VARCHAR(70) ,
                name_author VARCHAR(70) ,
                role VARCHAR(50) , 
                rattings DECIMAL (12,2),
                tag_product VARCHAR(50) , 
                type_product VARCHAR(50) ,
                price DECIMAL ,
                discription VARCHAR(4200)
            )
            '''
        )
        self.cursor.commit()

    def insert_main_data(self, item):
        self.cursor.execute(
            ''' 
            INSERT INTO amazon (
                url ,
                title  ,
                picture  ,
                sub_title  ,
                name_author ,
                role  , 
                rattings ,
                tag_product  , 
                type_product ,
                price  ,
                discription 
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            ''', (
                item['url'],
                item['title'],
                item['picture'],
                item['sub_title'],
                item['name_author'],
                item['role'],
                item['rattings'],
                item['tag_product'],
                item['type_product'],
                item['price'],
                item['discription']
            )
        )
        self.cursor.commit()

class Saveto_sqlServerFahasaPipeline:
    def __init__(self, server, database, username, authentication):
        self.server = server
        self.database = database
        self.username = username
        self.authentication = authentication

    @classmethod
    def from_crawler(cls, crawler):
        server = crawler.settings.get("SQL_SERVER")
        database = crawler.settings.get("SQL_DATABASE")
        username = crawler.settings.get("SQL_USERNAME")
        authentication = crawler.settings.get("SQL_AUTHENTICATION")
        if not server or not database:
            raise NotConfigured("SQL Server connection details are missing.")
        return cls(server, database, username, authentication)

    def open_spider(self, spider):
        # Connection information
        driver = "{ODBC Driver 17 for SQL Server}"
        server_name = self.server
        database_name = self.database
        authentication = self.authentication
        username = self.username
        # Connection string
        connection_string = f"DRIVER={driver};SERVER={server_name};DATABASE={database_name};{authentication};UID={username}"
        # Connect to database
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.create_table_if_not_exists()

    def process_item(self, item, spider):
        self.insert_author_table(item)
        self.insert_publisher_table(item)
        self.insert_supplier_table(item)
        self.insert_book_cover_type_table(item)
        self.insert_book_cover_size_table(item)
        self.insert_discount_table(item)
        self.insert_price_table(item)
        self.insert_main_data(item)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def create_table_if_not_exists(self):
        # Create MainTable
        self.cursor.execute(
            '''
            CREATE TABLE books_fahasa (
                product_code INT IDENTITY(1,1) ,
                url NVARCHAR(255) ,
                title NVARCHAR(500) ,
                publisher NVARCHAR(500) ,
                supplier NVARCHAR(500) ,
                author NVARCHAR(500) ,
                book_cover_type NVARCHAR(80) ,
                book_cover_size NVARCHAR(80) ,
                product_id NVARCHAR(50) ,
                product_discription NVARCHAR(MAX) ,
                weight NVARCHAR(20) ,
                page_number NVARCHAR(10) ,
                picture NVARCHAR(255) ,
                current_price NVARCHAR(30) ,
                old_price NVARCHAR(30 ) ,
                discount NVARCHAR(20) ,
                release_day NVARCHAR(200) ,
                PRIMARY KEY (title) 
            )
            '''
        )
        # Create author table
        self.cursor.execute(
            '''
            CREATE TABLE  author_fahasa (
                author_id INT IDENTITY(1,1) PRIMARY KEY, 
                author_info NVARCHAR(255) 
            )
            '''
        )
        # Create publisher table
        self.cursor.execute(
            '''
            CREATE TABLE  publisher_fahasa (
                 publisher_id INT IDENTITY(1,1) PRIMARY KEY, 
                 publisher_info NVARCHAR(255) 
            )
            '''
        )
        # Create supplier table
        self.cursor.execute(
            '''
            CREATE TABLE  supplier_fahasa (
                 supplier_id INT IDENTITY(1,1) PRIMARY KEY,
                 supplier_info NVARCHAR(255) 
            )
            '''
        )
        # Create book_cover table
        self.cursor.execute(
            '''
            CREATE TABLE  book_cover_fahasa (
                 book_cover_id INT IDENTITY(1,1) PRIMARY KEY, 
                 book_cover_type NVARCHAR(255) 
            )
            '''
        )
        # Create book_cover_size table
        self.cursor.execute(
            '''
            CREATE TABLE  book_cover_size_fahasa (
                 book_cover_size_id INT IDENTITY(1,1) PRIMARY KEY, 
                 book_cover_size NVARCHAR(255) 
            )
            '''
        )
        # Create discount table
        self.cursor.execute(
            '''
            CREATE TABLE  discount_fahasa (
                 discount_id INT IDENTITY(1,1) PRIMARY KEY, 
                 discount_info NVARCHAR(20) 
            )
            '''
        )
        # Create product_price table
        self.cursor.execute(
            '''
            CREATE TABLE  product_price_fahasa (
                url NVARCHAR(255) ,
                title NVARCHAR(500) ,
                publisher NVARCHAR(500) ,
                supplier NVARCHAR(500) ,
                author NVARCHAR(500) ,
                book_cover_type NVARCHAR(80) ,
                book_cover_size NVARCHAR(80) ,
                product_id NVARCHAR(50) ,
                product_discription NVARCHAR(MAX) ,
                weight NVARCHAR(20) ,
                page_number NVARCHAR(10) ,
                picture NVARCHAR(255) ,
                current_price NVARCHAR(30) ,
                old_price NVARCHAR(30 ) ,
                discount NVARCHAR(20) ,
                release_day NVARCHAR(200) ,
                PRIMARY KEY (product_id) 
            )
            '''
        )
        self.cursor.commit()

    def insert_author_table(self, item):
        # Convert 'item['author']' to a list if it's not already a list
        if not isinstance(item['author'], list):
            authors = [item['author']]
        else:
            authors = item['author']

        # Loop through each author_info value
        for author_info in authors:
            # Check if author_info already exists in the author_fahasa table
            if author_info and author_info.strip():
                self.cursor.execute('''
                    SELECT COUNT(*) FROM author_fahasa WHERE author_info = ?
                        ''', (author_info))
                count = self.cursor.fetchone()[0]

                # If author_info does not exist, insert it into the author_fahasa table
                if count == 0:
                    self.cursor.execute('''
                        INSERT INTO author_fahasa (author_info) VALUES (?);
                            ''', (author_info))
                    self.conn.commit()

    def insert_publisher_table(self, item):
        # Convert 'item['publisher']' to a list if it's not already a list
        if not isinstance(item['publisher'], list):
            publishers = [item['publisher']]
        else:
            publishers = item['publisher']

        # Loop through each publisher_info value
        for publisher_info in publishers:
            # Check if publisher_info already exists in the publisher_fahasa table
            if publisher_info and publisher_info.strip():
                self.cursor.execute('''
                    SELECT COUNT(*) FROM publisher_fahasa WHERE publisher_info = ?
                        ''', (publisher_info))
                count = self.cursor.fetchone()[0]

                # If publisher_info does not exist, insert it into the publisher_fahasa table
                if count == 0:
                    self.cursor.execute('''
                        INSERT INTO publisher_fahasa (publisher_info) VALUES (?);
                            ''', (publisher_info))
                    self.conn.commit()

    def insert_supplier_table(self, item):
        # Convert 'item['supplier']' to a list if it's not already a list
        if not isinstance(item['supplier'], list):
            suppliers = [item['supplier']]
        else:
            suppliers = item['supplier']

        # Loop through each supplier_info value
        for supplier_info in suppliers:
            # Check if supplier_info already exists in the supplier_fahasa table
            if supplier_info and supplier_info.strip():
                self.cursor.execute('''
                    SELECT COUNT(*) FROM supplier_fahasa WHERE supplier_info = ?
                        ''', (supplier_info))
                count = self.cursor.fetchone()[0]

                # If supplier_info does not exist, insert it into the supplier_fahasa table
                if count == 0:
                    self.cursor.execute('''
                        INSERT INTO supplier_fahasa (supplier_info) VALUES (?);
                            ''', (supplier_info))
                    self.conn.commit()

    def insert_book_cover_type_table(self, item):
        # Convert 'item['book_cover_type']' to a list if it's not already a list
        if not isinstance(item['book_cover_type'], list):
            book_cover_types = [item['book_cover_type']]
        else:
            book_cover_types = item['book_cover_type']

        # Loop through each book_cover_info value
        for book_cover_info in book_cover_types:
            # Check if book_cover_info already exists in the book_cover_fahasa table
            if book_cover_info and book_cover_info.strip():
                self.cursor.execute('''
                    SELECT COUNT(*) FROM book_cover_fahasa WHERE book_cover_type = ?
                        ''', (book_cover_info))
                count = self.cursor.fetchone()[0]

                # If book_cover_info does not exist, insert it into the book_cover_fahasa table
                if count == 0:
                    self.cursor.execute('''
                        INSERT INTO book_cover_fahasa (book_cover_type) VALUES (?);
                            ''', (book_cover_info))
                    self.conn.commit()

    def insert_book_cover_size_table(self, item):
        # Convert 'item['book_cover_size']' to a list if it's not already a list
        if not isinstance(item['book_cover_size'], list):
            book_cover_sizes = [item['book_cover_size']]
        else:
            book_cover_sizes = item['book_cover_size']

        # Loop through each book_cover_size value
        for book_cover_size in book_cover_sizes:
            # Check if book_cover_size already exists in the book_cover_fahasa table
            if book_cover_size and book_cover_size.strip():
                self.cursor.execute('''
                    SELECT COUNT(*) FROM book_cover_size_fahasa WHERE book_cover_size = ?
                        ''', (book_cover_size))
                count = self.cursor.fetchone()[0]

                # If book_cover_size does not exist, insert it into the book_cover_size_fahasa table
                if count == 0:
                    self.cursor.execute('''
                        INSERT INTO book_cover_size_fahasa (book_cover_size) VALUES (?);
                            ''', (book_cover_size))
                    self.conn.commit()

    def insert_discount_table(self, item):
        # Convert 'item['discount']' to a list if it's not already a list
        if not isinstance(item['discount'], list):
            discounts = [item['discount']]
        else:
            discounts = item['discount']

        # Loop through each discount value
        for discount_info in discounts:
            # Check if discount already exists in the discount_fahasa table
            if discount_info and discount_info.strip():
                self.cursor.execute('''
                    SELECT COUNT(*) FROM discount_fahasa WHERE discount_info = ?
                        ''', (discount_info))
                count = self.cursor.fetchone()[0]

                # If discount does not exist, insert it into the discount_fahasa table
                if count == 0:
                    self.cursor.execute('''
                        INSERT INTO discount_fahasa (discount_info) VALUES (?);
                            ''', (discount_info))
                    self.conn.commit()

    def insert_price_table(self, item):
        self.cursor.execute(
            ''' 
            INSERT INTO product_price_fahasa (
                url  , 
                title  , 
                publisher ,
                supplier , 
                author  , 
                book_cover_type  , 
                book_cover_size  , 
                product_id  ,
                product_discription,
                weight  ,
                page_number ,
                picture ,
                current_price ,
                old_price  , 
                discount ,
                release_day  
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            ''', (
                item['url'],
                item['title'],
                item['publisher'],
                item['supplier'],
                item['author'],
                item['book_cover_type'],
                item['book_cover_size'],
                item['product_id'],
                item['product_discription'],
                item['weight'],
                item['page_number'],
                item['picture'],
                item['current_price'],
                item['old_price'],
                item['discount'],
                item['release_day']
            )
        )
        self.cursor.commit()

    def insert_main_data(self, item):
        self.cursor.execute(
            ''' 
            INSERT INTO books_fahasa (
                url  , 
                title  , 
                publisher ,
                supplier , 
                author  , 
                book_cover_type  , 
                book_cover_size  , 
                product_id  ,
                product_discription,
                weight  ,
                page_number ,
                picture ,
                current_price ,
                old_price  , 
                discount ,
                release_day  
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            ''', (
                item['url'],
                item['title'],
                item['publisher'],
                item['supplier'],
                item['author'],
                item['book_cover_type'],
                item['book_cover_size'],
                item['product_id'],
                item['product_discription'],
                item['weight'],
                item['page_number'],
                item['picture'],
                item['current_price'],
                item['old_price'],
                item['discount'],
                item['release_day']
            )
        )
        self.cursor.commit()

class Saveto_sqlServerFahasaPipeline_finalstate:
    def __init__(self, server, database, username, authentication):
        self.server = server
        self.database = database
        self.username = username
        self.authentication = authentication

    @classmethod
    def from_crawler(cls, crawler):
        server = crawler.settings.get("SQL_SERVER")
        database = crawler.settings.get("SQL_DATABASE")
        username = crawler.settings.get("SQL_USERNAME")
        authentication = crawler.settings.get("SQL_AUTHENTICATION")
        if not server or not database:
            raise NotConfigured("SQL Server connection details are missing.")
        return cls(server, database, username, authentication)

    def open_spider(self, spider):
        # Connection information
        driver = "{ODBC Driver 17 for SQL Server}"
        server_name = self.server
        database_name = self.database
        authentication = self.authentication
        username = self.username
        # Connection string
        connection_string = f"DRIVER={driver};SERVER={server_name};DATABASE={database_name};{authentication};UID={username}"
        # Connect to database
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.add_foreign_key_columns()
        self.add_foreign_key_constraints()

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        self.update_foreign_key_data()
        self.drop_unused_columns()
        self.data_type()
        self.cursor.close()
        self.conn.close()

    def add_foreign_key_columns(self):
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD publisher_id INT 
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD supplier_id INT 
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD author_id INT 
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD book_cover_id INT 
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD book_cover_size_id INT 
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            ADD discount_id INT
        ''')
        self.cursor.commit()

    def add_foreign_key_constraints(self):
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD FOREIGN KEY (author_id)
            REFERENCES author_fahasa(author_id)
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD FOREIGN KEY (supplier_id) 
            REFERENCES supplier_fahasa(supplier_id)
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD FOREIGN KEY (publisher_id) 
            REFERENCES publisher_fahasa(publisher_id)
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD FOREIGN KEY (book_cover_id) 
            REFERENCES book_cover_fahasa(book_cover_id)
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD FOREIGN KEY (book_cover_size_id) 
            REFERENCES book_cover_size_fahasa(book_cover_size_id)
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            ADD FOREIGN KEY (discount_id)
            REFERENCES discount_fahasa(discount_id)
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ADD FOREIGN KEY (product_id)
            REFERENCES product_price_fahasa(product_id)
        ''')
        self.cursor.commit()

    def update_foreign_key_data(self):
        self.cursor.execute('''
            UPDATE books_fahasa
            SET author_id = author_fahasa.author_id
            FROM books_fahasa INNER JOIN author_fahasa 
            ON books_fahasa.author = author_fahasa.author_info
        ''')
        self.cursor.execute('''
            UPDATE books_fahasa
            SET supplier_id = supplier_fahasa.supplier_id
            FROM books_fahasa INNER JOIN supplier_fahasa 
            ON books_fahasa.supplier = supplier_fahasa.supplier_info
        ''')
        self.cursor.execute('''
            UPDATE books_fahasa
            SET publisher_id = publisher_fahasa.publisher_id
            FROM books_fahasa INNER JOIN publisher_fahasa
            ON books_fahasa.publisher = publisher_fahasa.publisher_info
        ''')
        self.cursor.execute('''
            UPDATE books_fahasa
            SET book_cover_id = book_cover_fahasa.book_cover_id
            FROM books_fahasa INNER JOIN book_cover_fahasa
            ON books_fahasa.book_cover_type = book_cover_fahasa.book_cover_type
        ''')
        self.cursor.execute('''
            UPDATE books_fahasa
            SET book_cover_size_id = book_cover_size_fahasa.book_cover_size_id
            FROM books_fahasa INNER JOIN book_cover_size_fahasa
            ON books_fahasa.book_cover_size = book_cover_size_fahasa.book_cover_size
        ''')
        self.cursor.execute('''
            UPDATE product_price_fahasa
            SET discount_id = discount_fahasa.discount_id
            FROM product_price_fahasa INNER JOIN discount_fahasa
            ON product_price_fahasa.discount = discount_fahasa.discount_info
        ''')
        self.cursor.commit()

    def data_type(self):
        self.cursor.execute('''
            UPDATE books_fahasa
            SET  weight = 0
            WHERE weight IS NULL OR weight ='None'  ; -- Replace 0 with the desired value
        ''')
        self.cursor.execute('''
            UPDATE books_fahasa
            SET page_number = 0
            WHERE page_number IS NULL OR page_number ='None'  ; -- Replace 0 with the desired value
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ALTER COLUMN weight INT
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            ALTER COLUMN page_number INT
        ''')
        self.cursor.execute('''
            UPDATE product_price_fahasa
            SET  old_price = 0
            WHERE old_price IS NULL OR old_price ='None'  ; -- Replace 0 with the desired value
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            ALTER COLUMN old_price INT
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            ALTER COLUMN current_price INT
        ''')
        self.cursor.execute('''
            UPDATE discount_fahasa
            SET discount_info = CAST(REPLACE(discount_info, '%', '') AS DECIMAL(18, 2)) / 100
            WHERE discount LIKE '%%' ; -- Filter only rows with percentage values        
        ''')
        self.cursor.commit()
    
    def drop_unused_columns(self):
        # drop columns in books_fahasa table
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN author
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN supplier
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN publisher
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN book_cover_type
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN book_cover_size
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN discount
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN current_price
        ''')
        self.cursor.execute('''
            ALTER TABLE books_fahasa
            DROP COLUMN old_price
        ''')
        self.cursor.commit()

        # drop columns in product_price_fahasa table
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN discount
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN release_day 
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN picture
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN page_number
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN weight
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN product_discription
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN book_cover_size
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN book_cover_type
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN author
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN supplier
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN publisher
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN title
        ''')
        self.cursor.execute('''
            ALTER TABLE product_price_fahasa
            DROP COLUMN url
        ''')
        self.cursor.commit()

class AmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        # remove unexpected symbols
        for field_name in field_names:
            if field_name in ['discription', 'role', 'tag_product', 'type_product']:
                value = adapter.get(field_name)
                if value is not None and value != '':
                    value = str(value)
                    value = value.replace('\xa0', ' ')
                    value = value.replace('[','')
                    value = value.replace(']','')
                    value = value.replace("'",'')
                    value = value.replace('(','')
                    value = value.replace(')','')
                    value = value.replace('â€™', "'" )
                    adapter[field_name] = value.strip()
        # reduce plank
        strip_features = ['sub_title', 'title']
        for feature in strip_features :
            value = adapter.get(feature)
            if value is not None and value != '':
                value = str(value)
                adapter[feature] = value.strip()
        # change to lower keys string
        rattings_feature = 'rattings'
        value = adapter.get(rattings_feature)
        if value is not None and value != '':
            value = str(value)
            value = value.replace('ratings', '')
            value = value.replace('rating','')
            value = value.replace(',','')
            value = value.lower()
            adapter[rattings_feature] = float(value)
        # change to numerical datatype
        price_feature = 'price'
        value = adapter.get(price_feature)
        if value is not None and value != '':
            value = str(value)
            value = value.replace('$','')
            adapter[price_feature] = float(value)
        return item

class NettruyenPipeLine:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        # process discription feature
        discription_feature = 'discription'
        value = adapter.get(discription_feature)
        if value is not None and value != '':
            value = str(value)
            value = value.replace('<div class="box_text">','')
            value = value.replace('</div>', '')
            value = value.replace('\\','')
            value = value.replace('\xa0','')
            value = value.replace('\\n','')
            value = value.replace('\n','')
            adapter[discription_feature] = value.strip()
        # process view, follow, lastest_chap
        for field_name in field_names:
            if field_name in ['view', 'follow']:
                value = adapter.get(field_name)
                if value is not None and value != '':
                    value = str(value)
                    value = value.replace("K", '000')
                    value = value.replace("M", '000000')
                    value = value.replace(",", '')
                    value = value.strip()
                    adapter[field_name] = float(value)
        return item

class TruyenqqiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        # process tag feature
        tag_feature = 'tag'
        value = adapter.get(tag_feature)
        if value is not None and value != '':
            value = str(value)
            value = value.replace('[', '')
            value = value.replace(']', '')
            value = value.replace('\\xa0', '')
            value = value.replace('\n', '')
            value = value.replace('\\n', '')
            value = value.replace('\xa0', '')
            value = value.replace("'", '')
            adapter[tag_feature] = value.strip()
        # process view, follow, lastest_chap
        for field_name in field_names:
            if field_name in ['view', 'lastest_chap', 'follow']:
                value = adapter.get(field_name)
                if value is not None and value != '':
                    value = str(value)
                    value = value.replace('Chapter', '')
                    value = value.replace('Lượt xem:','')
                    value = value.replace('Lượt theo dõi:','')
                    value = value.replace("'", '')
                    value = value.replace(",", '')
                    value = value.strip()
                    adapter[field_name] = float(value)
        return item

class FahasaPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if value is not None and value != '':
                value = str(value)
                list_symbol = ['\n', '\t', '[', ']', '\xa0', '\\xa0', ' \\r', "'", '"', '\\n', '\\t', '\\r', '=',
                               '?????????̀???????? ????????̂???? ????????̛????̛́???? ??????? ',
                               '?????????̀???????? ????????̂???? ????????̛????̛́????',"cm",
                               '----------------------------------------------', '--------------------------',
                               '-, --------------------------, ', '\u200b','\\u200b','\n\t\t\t\t', '\t\t\t\t']
                for symbol in list_symbol:
                    value = value.replace(symbol, '').strip()

            adapter[field_name] = value

        page_number = 'page_number'
        adapter.get(page_number)
        value = str(value)
        value = value.strip()
        adapter[page_number] = value

        prices_pn = ['old_price', 'current_price', 'weight', 'book_cover_size']
        list_symbol = [",", "đ", "'", " ", "." ,"cm"]
        for price in prices_pn:
            value = str(adapter.get(price))
            for symbol in list_symbol:
                value = value.replace(symbol, "")
            value = value.strip()
            adapter[price] = value
        return item

class FahasaListPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            value = str(value)
            value = value.replace('[', '')
            value = value.replace(']', '')
        return item

class TheSunPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            value = str(value)
            value = value.replace('\xa0', '')
            value = value.replace('\\xa0', '')
            value = value.replace('\\', '')
            value = value.replace('[', '')
            value = value.replace(']', '')
            value = value.replace('\\u200','')
        return item

class DailyMailPipeline:
    def process_data(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            value = str(value)
            value = value.replace('\xa0', '')
            value = value.replace('\\xa0', '')
            value = value.replace('\\', '')
            value = value.replace('[', '')
            value = value.replace(']', '')
        return item
