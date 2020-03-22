from io import BytesIO
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QLineEdit, QMainWindow
from PyQt5.QtGui import QPixmap, QImage, qRed, qGreen, qBlue, qRgba, QPainter
from PyQt5 import uic
import sys
from PIL import Image
from PyQt5.Qt import Qt
import requests


class MyLineEdit(QLineEdit):
    pass


class PIL(QWidget):
    def __init__(self):
        self.keys = [Qt.Key_PageUp, Qt.Key_PageDown, Qt.Key_Up, Qt.Key_Down,
                     Qt.Key_Left, Qt.Key_Right]
        self.sat = {'Карта': 'map', 'Спутник': 'sat', 'Гибрид': 'sat,skl'}
        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.search_api_server = "https://search-maps.yandex.ru/v1/"
        self.ll = (52.297113, 54.901383)
        self.type = 'map'
        self.z = '15'
        self.point = None
        self.postal = ''
        self.cur_address = ''
        self.is_post = True
        super().__init__()
        uic.loadUi('alpha.ui', self)
        self.update_pic()
        self.changed.clicked.connect(self.change_sat)
        self.btn_query.clicked.connect(self.find_object)
        self.reset.clicked.connect(self.reset_point)
        self.btn_index.clicked.connect(self.change_post)

    def update_pic(self):
        pic = self.get_picture_from_coordinates(self.ll)
        self.set_picture(pic)
        self.update_address()

    def set_picture(self, pic):
        self.picture.setPixmap(QPixmap.fromImage(QImage.fromData(pic)))

    def get_picture_from_coordinates(self, coords):
        map_params = {
            "l": self.type,
            'll': str(coords[0]) + ',' + str(coords[1]),
            'size': '600,450',
            'z': self.z
        }
        if self.point:
            map_params['pt'] = self.point
            print(0)
        response = requests.get(self.map_api_server, params=map_params)
        return bytes(response.content)

    def keyPressEvent(self, event):
        if event.key() in self.keys:
            if event.key() == Qt.Key_PageUp:
                self.z = str(max(int(self.z) - 1, 1))
            if event.key() == Qt.Key_PageDown:
                self.z = str(min(int(self.z) + 1, 17))
            if event.key() == Qt.Key_Left:
                self.ll = (self.ll[0] - 1.4 ** (-int(self.z))) % 180, self.ll[1]
            if event.key() == Qt.Key_Right:
                self.ll = (self.ll[0] + 1.4 ** (-int(self.z))) % 180, self.ll[1]
            if event.key() == Qt.Key_Up:
                self.ll = self.ll[0], min(self.ll[1] + 1.5 ** (-int(self.z)), 89)
                print(self.ll)
            if event.key() == Qt.Key_Down:
                self.ll = self.ll[0], max(self.ll[1] - 1.5 ** (-int(self.z)), -89)
            self.update_pic()

    def change_sat(self):
        cur = self.sat_type.currentText()
        self.type = self.sat[cur]
        self.update_address()
        QApplication.focusWidget().clearFocus()
        self.update_pic()

    def find_object(self):
        target = self.query.text()
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": target,
            "format": "json"
        }
        response_toponym = requests.get(self.geocoder_api_server, params=geocoder_params)
        try:
            json_response = response_toponym.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            address = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
            if 'postal_code' in toponym['metaDataProperty']['GeocoderMetaData']['Address']:
                self.postal = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
            else:
                self.postal = 'нет почтового индекса'
            self.ll = tuple(map(float, toponym_coodrinates.split(" ")))
            self.point = f'{self.ll[0]},{self.ll[1]},pm2dgl'
            self.cur_address = address
            QApplication.focusWidget().clearFocus()
            self.update_pic()
            self.update_address()
        except Exception:
            self.address.setText('Неправильный запрос')

    def reset_point(self):
        self.point = None
        self.cur_address = ''
        self.postal = ''
        QApplication.focusWidget().clearFocus()
        self.update_pic()

    def update_address(self):
        postal = str(', ' + self.postal) if self.is_post else ''
        self.address.setText(self.cur_address + postal)

    def change_post(self):
        if self.is_post:
            self.btn_index.setText('Индекс: выкл.')
        else:
            self.btn_index.setText('Индекс: вкл.')
        self.is_post = not self.is_post
        self.update_address()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PIL()
    ex.show()
    sys.exit(app.exec_())