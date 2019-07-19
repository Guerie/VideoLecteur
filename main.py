import sys
from PySide2.QtWidgets import (QApplication, QWidget, QMainWindow, QFileDialog, QListWidgetItem)
from PySide2 import QtCore, QtUiTools
from ui_VideoLecteur import Ui_MainWindow
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtCore import QUrl, QTime, QFileInfo

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pbPlay.clicked.connect(self.lectureClicked)
        self.ui.pbPause.clicked.connect(self.pauseClicked)
        self.ui.pbStop.clicked.connect(self.stopClicked)
        self.ui.pbNext.clicked.connect(self.nextClicked)
        self.ui.pbPrevious.clicked.connect(self.previousClicked)
        self.ui.pbAdd.clicked.connect(self.addClicked)
        self.ui.pbDelete.clicked.connect(self.deleteClicked)
        self.ui.dVolume.valueChanged.connect(self.volume)
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.wLecteur)
        self.mediaPlayer.durationChanged.connect(self.mediaDurationCnahged)
        self.mediaPlayer.positionChanged.connect(self.mediaPositionCnahged)
        self.ui.wList.itemDoubleClicked.connect(self.mediaSelected)

        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)

    def lectureClicked(self):
        print("Play")
        self.mediaPlayer.play()

    def pauseClicked(self):
        print("Pause")
        if self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.mediaPlayer.play()
        else:
            self.mediaPlayer.pause()

    def stopClicked(self):
        print("Stop")
        self.mediaPlayer.stop()

    def nextClicked(self):
        print("Next")
        self.mediaPlayer.next()

    def previousClicked(self):
        print("Previous")
        self.mediaPlayer.previous()

    def volume(self):
        valeurVolume = self.ui.dVolume.value()
        self.mediaPlayer.setVolume(valeurVolume)
        self.ui.lPourcent.setText(str(valeurVolume)+"%")

    def mediaDurationCnahged(self):
        print("mediaLoaded")
        self.ui.lTemps.setText("00:00:00") #12
        mediaDuration = self.mediaPlayer.duration() #donne le temps en milisecondes
        self.ui.sTimeLine.setRange(0, mediaDuration) #12
        totalTimeMedia = QTime(0,0,0)
        totalTimeMedia = totalTimeMedia.addMSecs(mediaDuration) #convertir de milisecondes en H:m:s
        self.ui.lTempsTotal.setText(totalTimeMedia.toString("HH:mm:ss"))

    def mediaPositionCnahged(self):
        mediaPosition = self.mediaPlayer.position()
        self.ui.sTimeLine.setValue(mediaPosition) #12
        currentTimeMedia = QTime(0,0,0)
        currentTimeMedia = currentTimeMedia.addMSecs(mediaPosition)
        self.ui.lTemps.setText(currentTimeMedia.toString("HH:mm:ss"))

    def mediaSelected(self):
        currentItem = self.ui.wList.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile((currentItem.text())))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

    def addClicked(self):
        print("+")
        nomMedia = QFileDialog.getOpenFileName(self, "Choix Film", "C:/Users/AELION/Desktop/Aelion/PyCharm/VideoProject", "Movie files (*.avi *.mp4)")
        # item = QListWidgetItem(nomMedia[0])
        # self.ui.wList.addItem(item)
        fInfo = QFileInfo(nomMedia[0])
        fShortName = fInfo.baseName()
        item = QListWidgetItem(fShortName)
        item.setToolTip(nomMedia[0])
        self.ui.wList.addItem(item)

    def deleteClicked(self):
        print("-")
        rowItem = self.ui.wList.currentRow()
        if rowItem != -1:
            self.ui.wList.takeItem(rowItem)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

