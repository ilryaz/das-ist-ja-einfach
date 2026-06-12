import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow

def ensure_json_files_exist():
    pass


def main():
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()