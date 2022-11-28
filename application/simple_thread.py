from PySide6.QtCore import QObject


class SimpleThread(QObject):

    def run(self):
        print('Thread run')