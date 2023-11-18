import sys
import cv2
import mss
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QScrollArea, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main vertical layout
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Horizontal layout for webcam and chat
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # Webcam label
        self.webcam_label = QLabel(self)
        self.top_layout.addWidget(self.webcam_label, 2)  # 2/3 of the space

        # Label for screen recording
        self.screen_recording_label = QLabel(self)
        self.top_layout.addWidget(self.screen_recording_label, 1)  # Allocate space next to the webcam

        # Timer for updating screen recording
        self.screen_timer = QTimer(self)
        self.screen_timer.timeout.connect(self.update_screen_recording)
        self.screen_timer.start(100)  # Adjust the interval as needed

        # Chat layout with title, text box, and translate button
        self.chat_layout = QVBoxLayout()  # Vertical layout for chat components

        # Create a horizontal layout for the title and button
        self.title_button_layout = QHBoxLayout()

        # Chat title label
        self.chat_title = QLabel("Text I want to Sign:", self)
        self.chat_title.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align text to the left
        self.title_button_layout.addWidget(self.chat_title)

        # Translate button
        self.translate_button = QPushButton("Translate", self)
        self.title_button_layout.addWidget(self.translate_button)

        # Add the horizontal layout to the chat layout
        self.chat_layout.addLayout(self.title_button_layout)

        # Chat textbox
        self.chat_textbox = QTextEdit(self)
        self.chat_layout.addWidget(self.chat_textbox)

        # Additional chat layout for signed text
        self.signed_chat_title = QLabel("Signed Text From Other Person", self)
        self.signed_chat_title.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the title
        self.chat_layout.addWidget(self.signed_chat_title)
        self.signed_chat_textbox = QTextEdit(self)
        self.chat_layout.addWidget(self.signed_chat_textbox)

        # Add chat layout to top layout
        self.top_layout.addLayout(self.chat_layout, 1)  # 1/3 of the space

        # Scroll area for images
        self.scroll_area = QScrollArea(self)
        self.image_container = QWidget()  # Container widget for images
        self.image_layout = QHBoxLayout(self.image_container)  # Horizontal layout for images
        self.scroll_area.setWidget(self.image_container)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Setup webcam
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Calculate aspect ratio of the frame
            height, width, _ = frame_rgb.shape
            aspect_ratio = width / height

            # Calculate new dimensions
            label_width = 800#self.webcam_label.width()
            label_height = 600#self.webcam_label.height()
            new_width, new_height = self.calculate_new_dimensions(label_width, label_height, aspect_ratio)

            # Resize the frame
            frame_resized = cv2.resize(frame_rgb, (new_width, new_height))

            # Convert the resized frame to QPixmap
            q_img = QImage(frame_resized.data, new_width, new_height, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)

            # Set the QPixmap to the label
            self.webcam_label.setPixmap(pixmap)

    def calculate_new_dimensions(self, label_width, label_height, aspect_ratio):
        """
        Calculate new dimensions for the frame to fit into the label without losing aspect ratio.
        """
        if label_width / aspect_ratio <= label_height:
            # Fit to width
            return label_width, int(label_width / aspect_ratio)
        else:
            # Fit to height
            return int(label_height * aspect_ratio), label_height
    
    def add_image(self, image_path):
        """Add an image to the scroll area."""
        pixmap = QPixmap(image_path)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setScaledContents(True)  # Scale the image to fit the label
        self.image_layout.addWidget(label)

    def update_screen_recording(self):
        with mss.mss() as sct:
            # Specify the monitor number or the monitor part to capture
            monitor = sct.monitors[1]  # You might need to adjust this for multiple monitors

            # Capture the screen
            screenshot = sct.grab(monitor)
            screenshot = np.array(screenshot)

            # Convert from BGR to RGB (mss captures in BGRA)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)

            # Resize and convert the screenshot to QPixmap
            q_img = QImage(screenshot.data, screenshot.shape[1], screenshot.shape[0], QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.screen_recording_label.setPixmap(pixmap.scaled(self.screen_recording_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()

    main_win.add_image("images/test_image.JPG")
    main_win.add_image("images/test_image.JPG")

    main_win.show()
    sys.exit(app.exec())