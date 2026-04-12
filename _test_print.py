import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QWidget, QVBoxLayout
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("Test Print")
    
    def on_print():
        try:
            printer = QPrinter(QPrinter.Mode.HighResolution)
            dialog = QPrintDialog(printer, w)
            if dialog.exec() == QPrintDialog.Accepted:
                QMessageBox.information(w, "OK", "Printed!")
            else:
                QMessageBox.information(w, "OK", "Cancelled!")
        except Exception as e:
            QMessageBox.critical(w, "Erro", str(e))
            
    b = QPushButton("Print")
    b.clicked.connect(on_print)
    l = QVBoxLayout(w)
    l.addWidget(b)
    w.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
