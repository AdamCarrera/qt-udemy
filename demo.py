import sys
from PySide2.QtWidgets import *
import ui.demo as demo


class Demo(QWidget, demo.Ui_Form):
    def __init__(self):
        super(Demo, self).__init__()

        self.setupUi(self)
        self.configure_signals()

    def configure_signals(self):
        self.button1.clicked.connect(lambda: print('5'))


def main():
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()