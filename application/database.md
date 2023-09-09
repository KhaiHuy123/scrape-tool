### Interface:
The CRM desktop application features a user-friendly interface with the following components:

1. **Title and Icon**: The application window displays the title "CRM.app - books data" and an icon on the top bar.

2. **Main Window Size**: The main window is set to a size of 1200x660 pixels.

3. **Background**: The background of the application is a light gray color (#EEEEEE).

4. **Treeview**: The main data is presented in a Treeview widget, allowing users to view and interact with a list of books. The Treeview is configured with columns, headings, and scrollbars for navigation.

5. **Buttons**: Various buttons are provided below the Treeview for performing actions like viewing details, moving rows, selecting items, clearing input fields, updating records, checking IDs, and accessing support tools.

6. **Data Entry Fields**: User-friendly data entry fields are included in a labeled frame for inputting book information such as title, URL, official price, discount, author, publisher, supplier, and book cover.

7. **Support Button**: An additional button with the Scout Regiment logo is present, offering access to external support resources.

### Functionality:
The CRM desktop application offers the following functionality:

1. **Database Connection**: The app connects to a SQL Server database using the provided connection details, including server name, authentication, and database name.

2. **Data Display**: The application retrieves book data from the database and populates the Treeview widget with details such as title, URL, price, discount, and related IDs.

3. **Data Interaction**: Users can interact with the data by selecting rows, viewing details, moving rows up or down in the list, and updating book information.

4. **Data Editing**: Users can edit book information by filling in the data entry fields and clicking the "Update" button.

5. **URL Viewing**: The app allows users to view the URL associated with a selected book by clicking the "View Details" button.

6. **ID Checking**: Users can check the IDs of related attributes (authors, publishers, suppliers, and book covers) by clicking the "Check ID" button. This opens a new window displaying related data in separate Treeview widgets.

7. **Support Tools**: The application provides a "Support" button that opens a web browser to a specified URL for accessing additional support and resources.

8. **External Logo**: The Scout Regiment logo is displayed for branding and aesthetics.

This CRM desktop application is designed to efficiently manage and view book data, making it a valuable tool for businesses or individuals working with book-related information. Users can easily navigate, update, and check related attributes to ensure data accuracy and completeness.

Here is diagram of database used in this application. It represent for the basic relational database:

![image](https://github.com/KhaiHuy123/scrape_tool/assets/86825653/ca599e1e-2728-46ac-9ff1-e0e64fc2e95b)

