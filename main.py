# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from io import BytesIO
import mutagen.mp3
from PIL import Image
from PyQt5.QtGui import *
import pygame
from threading import Thread
from time import sleep

from modules.radiojavan import get_audio
import urllib

global clicked
clicked = False

class PicButton(QtWidgets.QAbstractButton):
    def __init__(self, pixmap, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap
        if clicked:
            pix = self.pixmap_pressed
        self.update()
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QtCore.QSize(80, 80)

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self,main_window,height,width):
        super().__init__()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.main_window = main_window
        self.src = os.path.join(self.path,"src")
        self.musics_path = os.path.join(self.path,"musics")
        os.makedirs(self.musics_path, exist_ok=True)
        self.names = []
        self.labels = []
        self.buttons = []
        self.music = 0
        self.links = []
        self.songs_name = []
        self.key = False
        self.height = height
        self.width = width
        pygame.mixer.init()



    def reset(self):
        self.names = []
        self.buttons = []
        self.music = 0
        self.links = []
        self.songs_name = []
    

    def apic_extract(self,mp3):
        try:
            tags = mutagen.mp3.Open(mp3)
        except:
            return False
        data = ""
        for i in tags:
            if i.startswith("APIC"):
                data = tags[i].data
                break
        if not data:
            return None
        return data


    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.src,'radio.png')), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.main_window.setWindowIcon(icon)
        self.main_window.setObjectName("main_window")
        self.main_window.resize(int(self.width*0.75),int(self.height*0.75))
        self.centralwidget = QtWidgets.QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.img_logo = QtWidgets.QLabel(self.centralwidget)
        self.img_logo.setMaximumSize(QtCore.QSize(300, 300))
        self.img_logo.setText("")
        self.img_logo.setPixmap(QtGui.QPixmap(os.path.join(self.src,"radio.png")))
        self.img_logo.setScaledContents(True)
        self.img_logo.setObjectName("img_logo")
        self.horizontalLayout.addWidget(self.img_logo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.img_album = QtWidgets.QLabel(self.centralwidget)
        self.img_album.setMaximumSize(QtCore.QSize(250, 200))
        self.img_album.setText("")
        self.img_album.setScaledContents(True)
        self.img_album.setObjectName("img_album")
        self.horizontalLayout.addWidget(self.img_album)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.edt_name = QtWidgets.QLineEdit(self.centralwidget)
        self.edt_name.setFont(font)
        self.edt_name.setObjectName("edt_name")
        self.horizontalLayout_2.addWidget(self.edt_name)
        font1 = QtGui.QFont()
        font1.setPointSize(12)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setFont(font1)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setMinimumWidth(250)
        self.comboBox.setMinimumHeight(44)
        self.horizontalLayout_2.addWidget(self.comboBox)
        search_pix = QtGui.QPixmap(self.src + "/search.png")
        self.btn_search = PicButton(search_pix,search_pix, self)
        self.horizontalLayout_2.addWidget(self.btn_search)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setFont(font)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 569, 232))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        previous_pix = QtGui.QPixmap(self.src + "/previous.png")
        self.btn_previous = PicButton(previous_pix,previous_pix, self)
        self.horizontalLayout_3.addWidget(self.btn_previous)
        pause_pix = QtGui.QPixmap(self.src  + "/pause.png")
        play_pix = QtGui.QPixmap(self.src + "/play.png")
        self.btn_play = PicButton(play_pix,pause_pix, self)
        self.horizontalLayout_3.addWidget(self.btn_play)
        next_pix = QtGui.QPixmap(self.src + "/next.png")
        self.btn_next =  PicButton(next_pix,next_pix, self)
        self.horizontalLayout_3.addWidget(self.btn_next)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)
    

        self.retranslateUi(self.main_window)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

        self.btn_play.clicked.connect(self.play_btn)
        self.btn_search.clicked.connect(self.search_btn)
        self.btn_next.clicked.connect(self.next_music)
        self.btn_previous.clicked.connect(self.previous_music)


    def download_iamge(self,href):
        urllib.request.urlretrieve(href,os.path.join(self.src,'album.jpg'))
    def download_music(self,href,name):
        urllib.request.urlretrieve(href,os.path.join(self.musics_path, name + '.mp3'))


    def search_btn(self):
        global clicked
        clicked = False
        try:
            pygame.mixer.music.stop()
        except :
            pass
        self.btn_play.update()
        self.reset()
        self.key = True
        artist = self.edt_name.text()
        if artist != '':
            self.names = get_audio.get_artist_name(artist)
            self.comboBox.clear()
            for name in self.names:
                self.comboBox.addItem(name['name'])

    def update_background(self,idx):
        for label in self.labels:
            if self.labels.index(label) == idx:
                label.setStyleSheet("background-color: #7f7f7f")
                label.update()
            else:
                label.setStyleSheet("")
                label.update()
    

    def btn_musics(self,btn):
        global clicked
        clicked = True
        self.key = False
        self.btn_play.update()
        idx = self.buttons.index(btn)
        
        thread = Thread(target=self.play,args=[(idx)])
        thread.start()

    
    def deleteItemsOfLayout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def play_btn(self):
        global clicked
        clicked = not clicked
        if self.key == True:
            for label in self.labels:
                label.clear()
            self.deleteItemsOfLayout(self.gridLayout)
            self.labels = []
            clicked = not clicked
            artist = self.comboBox.currentText()
            _translate = QtCore.QCoreApplication.translate
            for name in self.names:
                if name['name'] == artist:
                    self.download_iamge(name['photo'])
                    self.img_album.setPixmap(QtGui.QPixmap(os.path.join(self.src,"album.jpg")))
                    songs = get_audio.get_artist_mp3s(name['name'])
                    for i in range(len(songs)):
                        font = QtGui.QFont()
                        font.setPointSize(18)
                        label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                        label.setObjectName("label_{}".format(i))
                        label.setFont(font)
                        self.labels.append(label)
                        self.gridLayout.addWidget(label, i, 0, 1, 1)
                        play_pix = QtGui.QPixmap(self.src + "/play.png")
                        btn =  PicButton(play_pix,play_pix, self)
                        btn.setMaximumSize(QtCore.QSize(40, 40))
                        self.buttons.append(btn)
                        self.gridLayout.addWidget(btn, i, 1, 1, 1)
                    for idx,lable in enumerate(self.labels):
                        lable.setText(_translate("main_window",songs[idx]['song_name']))
                        self.links.append(songs[idx]['song_link'])
                        self.songs_name.append(songs[idx]['song_name'])
                    for btn in self.buttons:
                        btn.clicked.connect(lambda _, b=btn: self.btn_musics(btn=b))
                    
        else:
            if clicked == False:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

    def previous_music(self):
        try:
            previous_song = self.music - 1
            if previous_song < 0:
                previous_song = len(self.songs_name) - 1
            
            thread = Thread(target=self.play,args=[(previous_song)])
            thread.start()
        except:
            pass

    
    def play(self,idx):
            self.download_music(self.links[idx],self.songs_name[idx])
            img = self.apic_extract(os.path.join(self.musics_path,self.songs_name[idx] + '.mp3'))
            image = Image.open(BytesIO(img)).resize([200,190])
            image.save(os.path.join(self.src,"album.png"))
            self.img_album.setPixmap(QtGui.QPixmap(os.path.join(self.src,"album.png")))
            self.update_background(idx)
            pygame.mixer.music.load(os.path.join(self.musics_path,self.songs_name[idx] + '.mp3'))
            pygame.mixer.music.play(-1)
            self.music = idx


    def next_music(self):
        try:
            if self.music != 0:
                next_song = self.music + 1
            else:
                next_song = self.music
            if next_song >= len(self.songs_name):
                next_song = 0

            thread = Thread(target=self.play,args=[(next_song)])
            thread.start()
            
        except :
            pass
        



    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("main_window", "radiojavan"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    ui = Ui_MainWindow(main_window,height,width)
    ui.setupUi()
    main_window.show()
    sys.exit(app.exec_())
