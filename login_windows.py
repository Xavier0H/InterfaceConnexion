import configparser

from PyQt5.QtGui import QPixmap, QBrush, QPalette
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGroupBox


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Load valid credentials from config file
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.valid_credentials = dict(self.config.items("credentials"))
        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_line_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")  # new button for registration
        self.message_label = QLabel("")

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_line_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_line_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)  # add new button to layout
        layout.addWidget(self.message_label)

        # create the registration form
        self.reg_form = QGroupBox("Registration Form")
        self.reg_form.setVisible(False)
        self.reg_form.setLayout(QVBoxLayout())
        self.reg_username_label = QLabel("Username:")
        self.reg_username_line_edit = QLineEdit()
        self.reg_password_label = QLabel("Password:")
        self.reg_password_line_edit = QLineEdit()
        self.reg_form.layout().addWidget(self.reg_username_label)
        self.reg_form.layout().addWidget(self.reg_username_line_edit)
        self.reg_form.layout().addWidget(self.reg_password_label)
        self.reg_form.layout().addWidget(self.reg_password_line_edit)
        self.reg_register_button = QPushButton("Register")
        self.reg_form.layout().addWidget(self.reg_register_button)
        layout.addWidget(self.reg_form)

        # Set layout
        self.setLayout(layout)

        # Connect signal to slot
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(lambda: self.reg_form.setVisible(not self.reg_form.isVisible()))
        self.reg_register_button.clicked.connect(self.register)  # connect registration button to register function

        # Set window properties
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 319, 339)

        # Set background image
        palette = QPalette()
        image = QPixmap("assets/sunset.jpg")
        brush = QBrush(image)
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

    def login(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        if username in self.valid_credentials and self.valid_credentials[username] == password:
            self.message_label.setText("Welcome!")
            self.message_label.setStyleSheet("color: green;")
        else:
            self.message_label.setText("Invalid username or password!")
            self.message_label.setStyleSheet("color: red;")

    def register(self):
        new_username = self.reg_username_line_edit.text()
        new_password = self.reg_password_line_edit.text()
        if new_username not in self.valid_credentials:
            self.valid_credentials[new_username] = new_password
            self.config.set("credentials", new_username, new_password)
            with open("config.ini", "w") as configfile:
                self.config.write(configfile)
            self.message_label.setText("Successful registration!")
            self.message_label.setStyleSheet("color: green;")
            self.reg_form.setVisible(False)
        else:
            self.message_label.setText("This username already exists!")
            self.message_label.setStyleSheet("color: red;")
        # Clear the fields
        self.username_line_edit.clear()
        self.password_line_edit.clear()
        self.reg_username_line_edit.clear()
        self.reg_password_line_edit.clear()
