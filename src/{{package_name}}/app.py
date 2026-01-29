"""app main"""

from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    from lib.xlib_ui_load_screen import WindowLoadScreen

    load_screen = WindowLoadScreen()
    app.processEvents()
    from lib._cri_main_gui import Window

    window = Window()
    load_screen.close()
    app.setStyle("fusion")
    app.exec_()
