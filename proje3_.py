import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QMainWindow, QAction, QLineEdit, QTableWidget, QTableWidgetItem, QListWidget, QDialog, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class AddBookWindow(QDialog):
    # Yeni sinyal tanımla
    kitapEklendi = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Kitap Ekle')
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.kitapAdiInput = QLineEdit(self)
        self.kitapAdiInput.setPlaceholderText('Kitap Adı')
        layout.addWidget(self.kitapAdiInput)

        self.yazarInput = QLineEdit(self)
        self.yazarInput.setPlaceholderText('Yazar Adı')
        layout.addWidget(self.yazarInput)

        ekleBtn = QPushButton('Ekle', self)
        ekleBtn.clicked.connect(self.kitapEkle)
        layout.addWidget(ekleBtn)

        self.setLayout(layout)

    def kitapEkle(self):
        kitap_adi = self.kitapAdiInput.text()
        # Yeni sinyali tetikle ve kitap adını gönder
        self.kitapEklendi.emit(kitap_adi)

    def getKitapAdi(self):
        return self.kitapAdiInput.text()

    def getYazarAdi(self):
        return self.yazarInput.text()

class LibraryGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kütüphane Yönetim Sistemi')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        layout = QVBoxLayout()

        self.uyeIdInput = QLineEdit(self)
        self.uyeIdInput.setPlaceholderText('Üye ID')
        layout.addWidget(self.uyeIdInput)

        self.uyeAdiInput = QLineEdit(self)
        self.uyeAdiInput.setPlaceholderText('Üye Adı')
        layout.addWidget(self.uyeAdiInput)

        self.uyeSoyadiInput = QLineEdit(self)
        self.uyeSoyadiInput.setPlaceholderText('Üye Soyadı')
        layout.addWidget(self.uyeSoyadiInput)

        self.kitapSecim = QComboBox(self)
        self.kitapSecim.addItem("Suç ve Ceza - Dostoyevski")
        self.kitapSecim.addItem("1984 - George Orwell")
        self.kitapSecim.addItem("Savaş ve Barış - Tolstoy")
        self.kitapSecim.addItem("Karamazov Kardeşler - Dostoyevski")
        self.kitapSecim.addItem("Usta ile Margarita - Bulgakov")
        self.kitapSecim.addItem("Don Kişot - Cervantes")
        layout.addWidget(self.kitapSecim)

        uyeEkleBtn = QPushButton('Üye Ekle', self)
        uyeEkleBtn.clicked.connect(self.uyeEkle)
        layout.addWidget(uyeEkleBtn)

        oduncAlBtn = QPushButton('Ödünç Al', self)
        oduncAlBtn.clicked.connect(self.oduncAl)
        layout.addWidget(oduncAlBtn)

        iadeEtBtn = QPushButton('Kitabı İade Et', self)
        iadeEtBtn.clicked.connect(self.iadeEt)
        layout.addWidget(iadeEtBtn)

        self.tableVisible = False
        self.toggleTableBtn = QPushButton('Tabloyu Göster', self)
        self.toggleTableBtn.clicked.connect(self.toggleTableVisibility)
        layout.addWidget(self.toggleTableBtn)

        self.veriTablosu = QTableWidget()
        self.veriTablosu.setColumnCount(4)
        self.veriTablosu.setHorizontalHeaderLabels(["Üye ID", "Üye Adı", "Ödünç Alınan Kitap", "İade Edilen Kitap"])
        layout.addWidget(self.veriTablosu)

        self.uyeListeBtn = QPushButton('Üye Listesini Göster', self)
        self.uyeListeBtn.clicked.connect(self.toggleUyeListesiVisibility)
        layout.addWidget(self.uyeListeBtn)

        self.uyeListesi = QListWidget()
        layout.addWidget(self.uyeListesi)
        self.uyeListesi.hide()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.createMenuBar()

    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Dosya')

        kitapEkleAction = QAction('&Kitap Ekle', self)
        kitapEkleAction.triggered.connect(self.showAddBookWindow)
        fileMenu.addAction(kitapEkleAction)

    def uyeEkle(self):
        uye_id = self.uyeIdInput.text()
        uye_adi = self.uyeAdiInput.text()
        uye_soyadi = self.uyeSoyadiInput.text()
        self.uyeListesi.addItem(f"{uye_id}: {uye_adi} {uye_soyadi}")

    def showAddBookWindow(self):
        dialog = AddBookWindow(self)
        # Yeni sinyali ana sayfada yakala ve işlem yap
        dialog.kitapEklendi.connect(self.kitapEkleAnaSayfa)
        dialog.exec_()

    # Ana sayfadaki seçenekli listeye kitap ekle
    def kitapEkleAnaSayfa(self, kitap_adi):
        self.kitapSecim.addItem(kitap_adi)

    def oduncAl(self):
        selected_item = self.uyeListesi.currentItem()
        if selected_item is not None:
            uye_info = selected_item.text().split(': ')
            uye_id = uye_info[0]
            uye_adi = uye_info[1].split()[0]
            kitap_adi = self.kitapSecim.currentText()
            self.veriTablosu.insertRow(self.veriTablosu.rowCount())
            self.veriTablosu.setItem(self.veriTablosu.rowCount() - 1, 0, QTableWidgetItem(uye_id))
            self.veriTablosu.setItem(self.veriTablosu.rowCount() - 1, 1, QTableWidgetItem(uye_adi))
            self.veriTablosu.setItem(self.veriTablosu.rowCount() - 1, 2, QTableWidgetItem(kitap_adi))
            QMessageBox.information(self, 'Bilgi', f"{kitap_adi} ödünç alındı.")
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir üye seçin.')

    def iadeEt(self):
        current_row = self.veriTablosu.currentRow()
        if current_row != -1:
            self.veriTablosu.removeRow(current_row)
            QMessageBox.information(self, 'Bilgi', 'Kitap İade Edildi')
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen iade edilecek kitabı seçin.')

    def toggleTableVisibility(self):
        if self.tableVisible:
            self.veriTablosu.hide()
            self.toggleTableBtn.setText('Tabloyu Göster')
        else:
            self.veriTablosu.show()
            self.toggleTableBtn.setText('Tabloyu Gizle')
        self.tableVisible = not self.tableVisible

    def toggleUyeListesiVisibility(self):
        if self.uyeListesi.isHidden():
            self.uyeListesi.show()
            self.uyeListeBtn.setText('Üye Listesini Gizle')
        else:
            self.uyeListesi.hide()
            self.uyeListeBtn.setText('Üye Listesini Göster')

def main():
    app = QApplication(sys.argv)
    ex = LibraryGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

