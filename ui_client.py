import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLabel, QFileDialog)
from PyQt6.QtCore import Qt

# Import your existing client logic file directly!
import client 

class CloudClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Custom Cloud Sync - Testing UI")
        self.setGeometry(100, 100, 450, 250)
        
        # Turn on operating system drag and drop registration for this window frame
        self.setAcceptDrops(True)
        
        # Layout components
        self.status_label = QLabel("Status: Idle (Drag files here or choose below)", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; border: 2px dashed #aaa; padding: 20px;")

        self.upload_btn = QPushButton("Upload File", self)
        self.download_btn = QPushButton("Download File", self)
        
        self.upload_btn.clicked.connect(self.open_file_explorer)
        self.download_btn.clicked.connect(self.trigger_download)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.download_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    # --- UI INTERACTIVE METHODS ---
    def open_file_explorer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Upload Target", "", "All Files (*)")
        if file_path:
            self.execute_backend_upload(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.status_label.setStyleSheet("font-weight: bold; border: 2px dashed #00aa00; padding: 20px;")

    def dragLeaveEvent(self, event):
        self.status_label.setStyleSheet("font-weight: bold; border: 2px dashed #aaa; padding: 20px;")

    def dropEvent(self, event):
        self.status_label.setStyleSheet("font-weight: bold; border: 2px dashed #aaa; padding: 20px;")
        for url in event.mimeData().urls():
            file_path = str(url.toLocalFile())
            if os.path.isfile(file_path):
                self.execute_backend_upload(file_path)
                break # Process the first dropped file item 

    def execute_backend_upload(self, local_file_path):
        filename = os.path.basename(local_file_path)
        self.status_label.setText(f"Status: Syncing {filename}...")
        QApplication.processEvents() # Refresh visual interface threads immediately
        
        try:
            # Trigger the modular transaction execution directly out of client.py
            client.run_client_transaction(b'\x01', local_file_path)
            self.status_label.setText(f"Success: Sent {filename} completely!")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def trigger_download(self):
        self.status_label.setText("Status: Download requested (Placeholder).")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_window = CloudClientApp()
    client_window.show()
    sys.exit(app.exec())