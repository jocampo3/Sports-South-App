import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QStackedWidget
import requests
import xml.etree.ElementTree as ET
import pandas as pd

class InvoiceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Invoices')
        layout = QVBoxLayout()
        # self.label = QLabel('This is the second window', self)
        # layout.addWidget(self.label)

        #customer_number, username, password, invoice_num, source

        # Widget 1 - Customer Number Input
        self.customer_input = QLineEdit(self)
        self.customer_input.setPlaceholderText('Enter your customer number')
        layout.addWidget(self.customer_input)

        self.customer_label = QLabel(self)
        layout.addWidget(self.customer_label)

        # Widget 2 - Username Input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Enter your username')
        layout.addWidget(self.username_input)

        self.username_label = QLabel(self)
        layout.addWidget(self.username_label)

        # Widget 3 - Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter your password')
        layout.addWidget(self.password_input)

        self.password_label = QLabel(self)
        layout.addWidget(self.password_label)

        # Widget 4 - Source Input
        self.invoice_input = QLineEdit(self)
        self.invoice_input.setPlaceholderText('Enter invoice number')
        layout.addWidget(self.invoice_input)

        self.invoice_label = QLabel(self)
        layout.addWidget(self.invoice_label)

        # Widget 5 - Start Date Input
        self.source_input = QLineEdit(self)
        self.source_input.setPlaceholderText('Enter your source')
        layout.addWidget(self.source_input)

        self.source_label = QLabel(self)
        layout.addWidget(self.source_label)

        self.button = QPushButton('Submit', self)
        self.button.clicked.connect(self.onSubmit)
        layout.addWidget(self.button)
        
        self.back_button = QPushButton('Back to Main Window', self)
        self.back_button.clicked.connect(self.goBack)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def onSubmit(self):
        # Get the text from the QLineEdit widgets and store them in instance variables
        self.customer_number = self.customer_input.text()
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        self.invoice_number = self.invoice_input.text()
        self.source = self.source_input.text()

        # Set the text to the QLabel widgets
        self.customer_label.setText(f'Customer Number: {self.customer_number}')
        self.username_label.setText(f'Username: {self.username}')
        self.password_label.setText(f'Password: {self.password}')
        self.source_label.setText(f'Source: {self.source}')
        self.invoice_label.setText(f'Start Date: {self.invoice_number}')

        # Make the API request and handle the response
        self.fetchOrderData()

    def fetchOrderData(self):
        url = "http://webservices.theshootingwarehouse.com/smart/invoices.asmx/GetDetail"
        params = {
            "CustomerNumber": self.customer_number,
            "UserName": self.username,
            "Password": self.password,
            "InvoiceNumber": self.invoice_number,
            "Source": self.source
        }
        try:
            # Make request
            response = requests.get(url, params=params)
            response.raise_for_status()

            # Parse XML response
            outer_root = ET.fromstring(response.content)
            inner_xml = outer_root.text

            root = ET.fromstring(inner_xml)

            self.invoice_data = []

            for table in root.findall(".//Table"):
                invoice = {child.tag: child.text for child in table}
                self.invoice_data.append(invoice)

            # Display first invoice in a separate window

            if self.invoice_data:
                # self.showInvoiceWindow(self.invoice_data[0])
                df = pd.DataFrame(self.invoice_data)
                df.to_csv("InvoiceData.csv")
            else:
                self.source_label.setText("No orders found")
        except requests.RequestException as e:
            self.source_label.setText(f"Request failed: {e}")
    
    def goBack(self):
        self.parent().setCurrentIndex(0)

class OrderWindow(QWidget):
    def __init__(self, order_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Order Details')
        layout = QVBoxLayout()

        self.order_data = QTextEdit(self)
        self.order_data.setReadOnly(True)
        layout.addWidget(self.order_data)

        self.back_button = QPushButton('Back to Main Window', self)
        self.back_button.clicked.connect(self.goBack)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.displayOrder(order_data)

    def displayOrder(self, order_data):
        self.order_data.setPlainText(str(order_data))

    def goBack(self):
        self.parent().setCurrentIndex(0)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Set the main layout
        layout = QVBoxLayout()

        # Widget 1 - Customer Number Input
        self.customer_input = QLineEdit(self)
        self.customer_input.setPlaceholderText('Enter your customer number')
        layout.addWidget(self.customer_input)

        self.customer_label = QLabel(self)
        layout.addWidget(self.customer_label)

        # Widget 2 - Username Input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Enter your username')
        layout.addWidget(self.username_input)

        self.username_label = QLabel(self)
        layout.addWidget(self.username_label)

        # Widget 3 - Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter your password')
        layout.addWidget(self.password_input)

        self.password_label = QLabel(self)
        layout.addWidget(self.password_label)

        # Widget 5 - Start Date Input
        self.start_date_input = QLineEdit(self)
        self.start_date_input.setPlaceholderText('Enter your start date')
        layout.addWidget(self.start_date_input)

        self.start_date_label = QLabel(self)
        layout.addWidget(self.start_date_label)

        # Widget 6 - End Date Input
        self.end_date_input = QLineEdit(self)
        self.end_date_input.setPlaceholderText('Enter your end date')
        layout.addWidget(self.end_date_input)

        self.end_date_label = QLabel(self)
        layout.addWidget(self.end_date_label)

        # Widget 4 - Source Input
        self.source_input = QLineEdit(self)
        self.source_input.setPlaceholderText('Enter your source')
        layout.addWidget(self.source_input)

        self.source_label = QLabel(self)
        layout.addWidget(self.source_label)

        # Create a QPushButton widget to submit the input
        self.button = QPushButton('Submit', self)
        self.button.clicked.connect(self.onSubmit)
        layout.addWidget(self.button)

        # Button to open the second window
        self.second_window_button = QPushButton('Open Second Window', self)
        self.second_window_button.clicked.connect(self.openSecondWindow)
        layout.addWidget(self.second_window_button)

        # Set the layout for the main window
        self.setLayout(layout)
        # Set the window title and size
        self.setWindowTitle('Main Window')

    def openSecondWindow(self):
        self.parent().setCurrentIndex(1)
    
    def onSubmit(self):
        # Get the text from the QLineEdit widgets and store them in instance variables
        self.customer_number = self.customer_input.text()
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        self.source = self.source_input.text()
        self.start_date = self.start_date_input.text()
        self.end_date = self.end_date_input.text()

        # Set the text to the QLabel widgets
        self.customer_label.setText(f'Customer Number: {self.customer_number}')
        self.username_label.setText(f'Username: {self.username}')
        self.password_label.setText(f'Password: {self.password}')
        self.source_label.setText(f'Source: {self.source}')
        self.start_date_label.setText(f'Start Date: {self.start_date}')
        self.end_date_label.setText(f'End Date: {self.end_date}')

        # Make the API request and handle the response
        self.fetchOrderData()

    def fetchOrderData(self):
        url = "http://webservices.theshootingwarehouse.com/smart/invoices.asmx/GetByDate"
        params = {
            "CustomerNumber": self.customer_number,
            "UserName": self.username,
            "Password": self.password,
            "StartDate": self.start_date,
            "EndDate": self.end_date,
            "Source": self.source
        }

        try:
            # Make the GET request
            response = requests.get(url, params=params)
            response.raise_for_status()

            # Parse the XML response
            outer_root = ET.fromstring(response.content)
            # Assuming the response content is in a string tag
            inner_xml = outer_root.text

            root = ET.fromstring(inner_xml)

            self.order_data = []
            for table in root.findall(".//Table"):
                order = {child.tag: child.text for child in table}
                self.order_data.append(order)

            # Display the first order in a separate window if available
            if self.order_data:
                self.showOrderWindow(self.order_data[0])
                df = pd.DataFrame(self.order_data)
                df.to_csv("OrderDataTest.csv")
            else:
                self.source_label.setText("No orders found.")
        except requests.RequestException as e:
            self.source_label.setText(f"Request failed: {e}")

    def showOrderWindow(self, order_data):
        self.parent().widget(2).displayOrder(order_data)
        self.parent().setCurrentIndex(2)

class MainApplication(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow(self)
        self.second_window = InvoiceWindow(self)
        self.order_window = OrderWindow(None, self)

        self.addWidget(self.main_window)
        self.addWidget(self.second_window)
        self.addWidget(self.order_window)

        self.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()