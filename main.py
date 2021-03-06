import sys
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from Equalizer import *

#volume에서 handle 크기 조정
class SliderProxyStyle(QProxyStyle):
    def pixelMetric(self, metric, option, widget):
        if metric == QStyle.PM_SliderThickness:
            return 60
        elif metric == QStyle.PM_SliderLength:
            return 40
        return super().pixelMetric(metric, option, widget)

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.List = ['stay-PostMalon', '잠이 오질 않네요-장범준', 'STAY-BLACKPINK', 'Piano-melody_1','Piano-melody_3']
        self.showplaylist = QDialog()
        self.currentidx = 0
        self.playlist = QMediaPlaylist()
        Qurlmusic = []

        for name in self.List:
            k = "music/" + name + ".wav"
            Qurlmusic.append(QUrl.fromLocalFile(k))
            #print(Qurlmusic[-1])
            self.playlist.addMedia(QMediaContent(Qurlmusic[-1]))
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.bartimer = 0
        self.Play()
        self.check = True

    def Play(self):
        #button,screen ...
        self.screen = QGroupBox()
        eq = QLabel("Equalizer",self)
        eq.move(25,10)
        eq.resize(100,50)
        self.label = QLabel(self.screen)

        self.screen.setStyleSheet("background:rgb(255,255,255)")
        self.label = QLabel(self.screen)
        self.label.move(200, 80)
        self.movie = QtGui.QMovie("icon/loading2.gif")
        self.label.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.movie.start()

        self.title = QLineEdit('') #title
        self.title.setReadOnly(True)
        self.title.setMaxLength(1000)
        self.title.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))

        # repeat button
        self.replaybutton = QPushButton()
        self.replaybutton.setIcon(QtGui.QIcon('icon/repeatone.png'))
        self.replaybutton.setIconSize(QtCore.QSize(35,35))
        self.replaybutton.clicked.connect(self.currretloop)

        # random button
        self.randombutton = QPushButton()
        self.randombutton.setIcon(QtGui.QIcon('icon/repeat.png'))
        self.randombutton.setIconSize(QtCore.QSize(35,35))
        self.randombutton.clicked.connect(self.loop)

        # playbar
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)

        #playbutton
        self.playbutton = QPushButton()
        self.playbutton.setIcon(QtGui.QIcon('icon/play.png'))
        self.playbutton.setIconSize(QtCore.QSize(60,60))
        self.playbutton.clicked.connect(self.playClicked)

        #next button
        self.nextbutton = QPushButton()
        self.nextbutton.setIcon(QtGui.QIcon('icon/next.png'))
        self.nextbutton.setIconSize(QtCore.QSize(80,60))
        self.nextbutton.clicked.connect(self.nextClicked)
        self.nextbutton.clicked.connect(self.openequalizer)

        #back button
        self.backbutton = QPushButton()
        self.backbutton.setIcon(QtGui.QIcon('icon/back.png'))
        self.backbutton.setIconSize(QtCore.QSize(80,60))
        self.backbutton.clicked.connect(self.prevClicked)
        self.backbutton.clicked.connect(self.openequalizer)

        #out button
        outbutton = QPushButton()
        outbutton.setIcon(QtGui.QIcon('icon/out.png'))
        outbutton.setIconSize(QtCore.QSize(50,50))
        outbutton.clicked.connect(self.Out)     

        # volume
        self.volume = QSlider(QtCore.Qt.Vertical)
        style = SliderProxyStyle(self.volume.style())
        self.volume.setStyle(style)
        self.volume.setStyleSheet("QSlider::handle:vertical{" 
                                  "background:rgb(0,0,0)}")
        self.volume.setRange(0, 100)
        self.volume.setValue(50)
        self.volume.valueChanged[int].connect(self.volumeChanged)

        # lyricsbutton
        self.lyricsbutton = QPushButton()
        self.lyricsbutton.setIcon(QtGui.QIcon('icon/lyrics.png'))
        self.lyricsbutton.setIconSize(QtCore.QSize(50,50))
        self.lyricsbutton.clicked.connect(self.ShowPLayList)

        #layout
        vv1box = QVBoxLayout()
        vv2box = QVBoxLayout()

        vv1_v1box = QVBoxLayout()
        vv1_h1box = QHBoxLayout()
        vv1_h2box = QHBoxLayout()
        vv1_h3box = QHBoxLayout()

        #screen 띄우는 위치
        vv1box.addLayout(vv1_v1box)
        vv1_v1box.addWidget(self.screen)

        #곡제목 위치
        vv1box.addLayout(vv1_h1box)
        vv1_h1box.addWidget(self.replaybutton)
        vv1_h1box.addWidget(self.title)
        vv1_h1box.addWidget(self.randombutton)

        #replay, playbar, random 버튼 위치
        vv1box.addLayout(vv1_h2box)
        vv1_h2box.addWidget(self.positionSlider)
        #back,play,next 버튼
        vv1box.addLayout(vv1_h3box)
        vv1_h3box.addStretch(1)
        vv1_h3box.addWidget(self.backbutton)
        vv1_h3box.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.openequalizer)
        vv1_h3box.addWidget(self.nextbutton)

        vv1_h3box.addStretch(1)

        #out, volume, lyrics 버튼
        vv2box.addWidget(outbutton)
        vv2box.addWidget(self.volume)
        vv2box.addWidget(self.lyricsbutton)

        Mainlayout = QHBoxLayout()
        Mainlayout.addLayout(vv1box)
        Mainlayout.addLayout(vv2box)

        self.setLayout(Mainlayout)

        self.setWindowTitle('main')
        self.setGeometry(500, 200, 1000, 700)
        self.show()

    def Out(self):
        self.close()

    def TTitle(self,idx):
        self.title.setText('{}'.format(self.List[idx]))

    def playClicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.playbutton.setIcon(QtGui.QIcon('icon/play.png'))
            self.playbutton.setIconSize(QtCore.QSize(60, 60))
            self.check = True
        else:
            self.player.play()
            self.playbutton.setIcon(QtGui.QIcon('icon/stop.png'))
            self.playbutton.setIconSize(QtCore.QSize(60, 60))
            self.TTitle(self.currentidx)
            self.check = False

    def nextClicked(self):
        self.step = 0
        self.currentidx +=1
        self.TTitle(self.currentidx)
        self.playlist.next()

    def prevClicked(self):
        self.step = 0
        self.currentidx -= 1
        self.TTitle(self.currentidx)
        self.playlist.previous()

    def volumeChanged(self):
        self.player.setVolume(self.volume.value())


    def ShowPLayList(self):
        for (i,j) in zip (self.List,range(10,110,20)):
            a = QLabel(i, self.showplaylist)
            a.move(10, j)

        label = QLabel(self.showplaylist)
        label.move(0, 110)
        label.resize(100, 100)

        self.showplaylist.setWindowTitle('PlayLIst')
        self.showplaylist.setWindowModality(Qt.ApplicationModal)
        self.showplaylist.setGeometry(1500, 400, 300, 200)
        self.showplaylist.show()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.player.setPosition(position)



    def closed(self,state):
        self.label.setVisible(state != Qt.Unchecked)

    def currretloop(self):
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

    def loop(self):
        self.playList.setPlaybackMode(QMediaPlaylist.Loop)

    def openequalizer(self):
        if(self.check == False):
            self.w = Window()
            self.w.show()
        else:
            self.w.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    main = Main()
    sys.exit(app.exec_())