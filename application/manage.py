from PySide6 import QtWidgets as qw
import sys
from application.main import TheWindow


if __name__ == '__main__':
    app = qw.QApplication([])
    application = TheWindow()
    application.show()
    sys.exit(app.exec())