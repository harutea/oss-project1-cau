#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################################
# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# made by Axel Schneider * https://github.com/Axel-Erfurt/
# August 2019
############################################
import sys
import os
import errno
import getpass
import socket
import typing
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QToolTip
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.Qt import QKeySequence, QCursor, QDesktopServices
import findFilesWindow
import QTextEdit
import Qt5Player
import QAudioPlayer
import QImageViewer
import QWebViewer
import QTerminalFolder
from zipfile import ZipFile
import shutil
import subprocess
import stat
from send2trash import send2trash
import git_handler
from enum import Enum
from git import repo
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt


#############################################################################################################################################################
#############################################################################################################################################################


# def gitTrue(file_list):
#    if len(file_list['staged']['new']) == 0 and len(file_list['staged']['modified']) == 0 and len(
#            file_list['staged']['deleted']) == 0:
#        if len(file_list['not_staged']['new']) == 0 and len(file_list['not_staged']['modified']) == 0 and len(
#                file_list['not_staged']['deleted']) == 0:
#            if len(file_list['untracked']) == 0:
#                return False
#    return True


def gitstatus(file_list, file_name):
    if file_list == 0:
        return False

    if QFileInfo(file_name).isDir():
        return "Directory"

    if file_name in file_list['staged']['renamed'] or file_name in file_list['staged']['new'] or file_name in file_list['staged']['modified'] or file_name in \
            file_list['staged']['deleted']:
        if file_name in file_list['not_staged']['renamed'] or file_name in file_list['not_staged']['new'] or file_name in file_list['not_staged']['modified'] or file_name in \
                file_list['not_staged']['deleted']:
            result = gitStatus.Staged_Modified
        elif file_name in file_list['untracked']:
            result = gitStatus.Staged_Untracked
        else:
            result = gitStatus.Staged
    elif file_name in file_list['not_staged']['renamed'] or file_name in file_list['not_staged']['new'] or file_name in file_list['not_staged']['modified'] or file_name in \
            file_list['not_staged']['deleted']:
        result = gitStatus.Modified
    elif file_name in file_list['untracked']:
        result = gitStatus.Untracked
    elif "./" in file_list['untracked']:
        result = gitStatus.Untracked
    else:
        result = gitStatus.Unmodified

    return result


class statusQFileSystemModel(QFileSystemModel):
    def __init__(self):
        super(statusQFileSystemModel, self).__init__()
        self.header = ["git status", "Name", "Size", "Type", "Date modified"]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]
        return super().headerData(section, orientation, role)

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return super().columnCount() + 1

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return super().data(index, role)

        if index.column() == 0 and role == Qt.DecorationRole:
            # 깃 파일 상태로 추후 변경

            file_name = super().data(index, Qt.DisplayRole)
            file_list = w.gitStatusList
            icon = QPixmap()

            # check if git status

            i = gitstatus(file_list, file_name)

            if i == "Directory" or i == False:
                return

            if i == gitStatus.Unmodified:
                icon.load(w.fileDirectories + "/icon/comitted.png")
                return icon
            elif i == gitStatus.Modified:
                icon.load(w.fileDirectories + "/icon/modified.png")
                return icon
            elif i == gitStatus.Staged:
                icon.load(w.fileDirectories + "/icon/staged.png")
                return icon
            elif i == gitStatus.Staged_Modified:
                icon.load(w.fileDirectories + "/icon/staged_modified.png")
                return icon
            elif i == gitStatus.Staged_Untracked:
                icon.load(w.fileDirectories + "/icon/staged_untracked.png")
                return icon
            elif i == gitStatus.Untracked:
                icon.load(w.fileDirectories + "/icon/untracked.png")
                return icon
            elif i == gitStatus.Nogit:
                return

        if index.column() == 0:
            return

        if 0 < index.column() <= 4:
            return super().data(index.siblingAtColumn(index.column() - 1), role)

        return super().data(index, role)


class MyMessageBox(QMessageBox):
    def resizeEvent(Event):
        super.resizeEvent(Event)
        self.setFixedWidth(666)
        self.setFixedHeight(666)

#############################################################################################################################################################
#############################################################################################################################################################


class gitStatus(Enum):
    Unmodified = 0
    Modified = 1
    Staged = 2
    Untracked = 3
    Nogit = 4
    Staged_Modified = 5
    Staged_Untracked = 6


#############################################################################################################################################################
#############################################################################################################################################################

class helpWindow(QMainWindow):
    def __init__(self):
        super(helpWindow, self).__init__()
        self.setStyleSheet(mystylesheet(myWindow()))
        self.helpText = """<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><!--StartFragment--><span style=" font-family:'Helvetica'; font-size:11pt; font-weight:600; text-decoration: underline; color:#2e3436;">Shortcuts:</span></p><br>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">rename File (F2)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">copy File(s) (Ctrl-C)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">paste File(s) (Ctrl-V)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">cut File(s) (Ctrl-X)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">open with TextEditor (F6)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">move File(s) to Trash(Del)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">delete File(s) (Shift+Del)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">find File(s) (Ctrl-F)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">play with vlc (F3)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">open folder in Terminal (F7)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">execute File in Terminal (F8)</span>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">go back (Backspace)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">refresh View (F5)</span></p>
<!--EndFragment--></p>
                                        """
        self.helpViewer = QLabel(self.helpText, self)
        self.helpViewer.setAlignment(Qt.AlignCenter)
        self.btnAbout = QPushButton("about")
        self.btnAbout.setFixedWidth(80)
        self.btnAbout.setIcon(QIcon.fromTheme("help-about"))
        self.btnAbout.clicked.connect(self.aboutApp)

        self.btnClose = QPushButton("Close")
        self.btnClose.setFixedWidth(80)
        self.btnClose.setIcon(QIcon.fromTheme("window-close"))
        self.btnClose.clicked.connect(self.close)

        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        layout.addWidget(self.helpViewer)
        layout.addStretch()
        layout.addWidget(self.btnAbout, alignment=Qt.AlignCenter)
        layout.addWidget(self.btnClose, alignment=Qt.AlignCenter)
        self.setCentralWidget(widget)

        #        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon.fromTheme("help-about"))

    def aboutApp(self):
        sysinfo = QSysInfo()
        myMachine = "currentCPU Architecture: " + sysinfo.currentCpuArchitecture() + "<br>" + \
            sysinfo.prettyProductName() + "<br>" + sysinfo.kernelType() + \
            " " + sysinfo.kernelVersion()
        title = "about QFileManager"
        message = """
                    <span style='color: #3465a4; font-size: 20pt;font-weight: bold;text-align: center;'
                    ></span></p><center><h3>QFileManager<br>1.0 Beta</h3></center>created by  
                    <a title='Axel Schneider' href='http://goodoldsongs.jimdo.com' target='_blank'>Axel Schneider</a> with PyQt5<br><br>
                    <span style='color: #555753; font-size: 9pt;'>©2019 Axel Schneider<br><br></strong></span></p>
                        """ + myMachine
        self.infobox(title, message)

    def infobox(self, title, message):
        QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self,
                    Qt.Dialog | Qt.NoDropShadowWindowHint | Qt.FramelessWindowHint).show()


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()

        self.setStyleSheet(mystylesheet(self))
        self.setWindowTitle("Filemanager")
        self.setWindowIcon(QIcon.fromTheme("system- file-manager"))
        self.process = QProcess()

        self.settings = QSettings("QFileManager", "QFileManager")
        self.clip = QApplication.clipboard()
        self.isInEditMode = False

        self.treeview = QTreeView()
        self.listview = QTreeView()

        self.cut = False
        self.hiddenEnabled = False
        self.folder_copied = ""

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.listview)

        hlay = QHBoxLayout()
        hlay.addWidget(self.splitter)

        wid = QWidget()
        wid.setLayout(hlay)
        self.createStatusBar()
        self.setCentralWidget(wid)
        self.setGeometry(0, 26, 900, 500)

        path = QDir.rootPath()
        self.copyPath = ""
        self.copyList = []
        self.copyListNew = ""

        self.createActions()

        self.findfield = QLineEdit()
        self.findfield.addAction(QIcon.fromTheme(
            "edit-find"), QLineEdit.LeadingPosition)
        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(150)
        self.findfield.setPlaceholderText("find")
        self.findfield.setToolTip("press RETURN to find")
        self.findfield.setText("")
        self.findfield.returnPressed.connect(self.findFiles)

        self.findfield.installEventFilter(self)

        self.tBar = self.addToolBar("Tools")
        self.tBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.tBar.setMovable(False)
        self.tBar.setIconSize(QSize(32, 32))
        self.tBar.addAction(self.createFolderAction)
        # self.tBar.addAction(self.copyFolderAction)
        # self.tBar.addAction(self.pasteFolderAction)
        # self.tBar.addSeparator()
        # self.tBar.addAction(self.copyAction)
        # self.tBar.addAction(self.cutAction)
        # self.tBar.addAction(self.pasteAction)
        # self.tBar.addSeparator()
        # self.tBar.addAction(self.findFilesAction)
        # self.tBar.addSeparator()
        # self.tBar.addAction(self.delActionTrash)
        # self.tBar.addAction(self.delAction)
        # self.tBar.addSeparator()
        # self.tBar.addAction(self.terminalAction)
        # self.tBar.addSeparator()
        # self.tBar.addAction(self.helpAction)

        # empty = QWidget()
        # empty.setMinimumWidth(60)
        # self.tBar.addWidget(empty)
        self.tBar.addSeparator()

        #############################################################################################################################################################
        #############################################################################################################################################################
        self.combo = QComboBox()

        self.tBar.addAction(self.gitinit)
        self.tBar.addAction(self.gitcommit)
        self.tBar.addWidget(self.combo)
        self.tBar.addAction(self.gitbranch)
        self.combo.insertItems(
            1, ["Create Branch", "Delete Branch", "Rename Branch", "Checkout Branch"])
        self.tBar.addAction(self.gitmerge)
        self.tBar.addAction(self.gitclone)
        self.tBar.addAction(self.gittree)
        self.tBar.addSeparator()
        #############################################################################################################################################################
        #############################################################################################################################################################

        self.tBar.addAction(self.btnHome)
        self.tBar.addAction(self.btnDocuments)
        self.tBar.addAction(self.btnDownloads)
        self.tBar.addAction(self.btnMusic)
        self.tBar.addAction(self.btnVideo)
        self.tBar.addSeparator()
        self.tBar.addAction(self.btnBack)
        self.tBar.addAction(self.btnUp)

        # self.tBar.addWidget(self.findfield)

        self.dirModel = QFileSystemModel()
        self.dirModel.setReadOnly(False)
        self.dirModel.setFilter(QDir.NoDotAndDotDot |
                                QDir.AllDirs | QDir.Drives)
        self.dirModel.setRootPath(QDir.rootPath())
        #############################################################################################################################################################
        #############################################################################################################################################################
        # self.fileModel = QFileSystemModel()
        self.fileModel = statusQFileSystemModel()
        #############################################################################################################################################################
        #############################################################################################################################################################
        self.fileModel.setReadOnly(False)
        self.fileModel.setFilter(QDir.NoDotAndDotDot |
                                 QDir.AllDirs | QDir.Files)
        self.fileModel.setResolveSymlinks(True)

        self.treeview.setModel(self.dirModel)
        self.treeview.hideColumn(1)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)

        self.listview.setModel(self.fileModel)
        self.treeview.setRootIsDecorated(True)

        #############################################################################################################################################################
        #############################################################################################################################################################
        # self.listview.header().resizeSection(0, 320)
        # self.listview.header().resizeSection(1, 80)
        # self.listview.header().resizeSection(2, 80)

        self.listview.header().resizeSection(0, 20)
        self.listview.header().resizeSection(1, 320)
        self.listview.header().resizeSection(2, 80)
        self.listview.header().resizeSection(3, 80)
        #############################################################################################################################################################
        #############################################################################################################################################################
        self.listview.setSortingEnabled(True)
        self.treeview.setSortingEnabled(True)

        self.treeview.setRootIndex(self.dirModel.index(path))

        #        self.treeview.clicked.connect(self.on_clicked)
        self.treeview.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        self.listview.doubleClicked.connect(self.list_doubleClicked)

        docs = QStandardPaths.standardLocations(
            QStandardPaths.DocumentsLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        #        self.treeview.expand(self.treeview.currentIndex())

        self.treeview.setTreePosition(0)
        self.treeview.setUniformRowHeights(True)
        self.treeview.setExpandsOnDoubleClick(True)
        self.treeview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeview.setIndentation(12)
        self.treeview.setDragDropMode(QAbstractItemView.DragDrop)
        self.treeview.setDragEnabled(True)
        self.treeview.setAcceptDrops(True)
        self.treeview.setDropIndicatorShown(True)
        self.treeview.sortByColumn(0, Qt.AscendingOrder)

        self.splitter.setSizes([20, 160])

        self.listview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listview.setDragDropMode(QAbstractItemView.DragDrop)
        self.listview.setDragEnabled(True)
        self.listview.setAcceptDrops(True)
        self.listview.setDropIndicatorShown(True)
        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listview.setIndentation(10)
        self.listview.sortByColumn(0, Qt.AscendingOrder)

        self.listview.setItemsExpandable(False)
        self.listview.setRootIsDecorated(False)

        self.fileDirectories = os.getcwd()
        if git_handler.git_status(self.currentPath):
            self.gitStatusList = git_handler.get_status_list(self.currentPath)
        else:
            self.gitStatusList = False
        print("Welcome to QFileManager")
        self.readSettings()
        self.enableHidden()
        self.getRowCount()
        self.fileModel.directoryLoaded.connect(self.refreshStatus)

        self.currentBranch = ""

    @pyqtSlot()
    def refreshStatus(self):
        if git_handler.git_status(self.currentPath):
            self.currentBranch = "Current Branch : " + \
                git_handler.git_show_branch_list(self.currentPath)[1]
            self.setWindowTitle(self.currentBranch)
            self.gitStatusList = git_handler.get_status_list(self.currentPath)
        else:
            self.currentBranch = ""
            self.gitStatusList = False
        self.initButtonPulse()

    def getRowCount(self):
        count = 0
        index = self.treeview.selectionModel().currentIndex()
        path = QDir(self.dirModel.fileInfo(index).absoluteFilePath())
        count = len(path.entryList(QDir.Files))
        self.statusBar().showMessage("%s %s" % (count, "Files"), 0)
        return count

    def closeEvent(self, e):
        print("writing settings ...\nGoodbye ...")
        self.writeSettings()

    def readSettings(self):
        print("reading settings ...")
        if self.settings.contains("pos"):
            pos = self.settings.value("pos", QPoint(200, 200))
            self.move(pos)
        else:
            self.move(0, 26)
        if self.settings.contains("size"):
            size = self.settings.value("size", QSize(800, 600))
            self.resize(size)
        else:
            self.resize(800, 600)
        if self.settings.contains("hiddenEnabled"):
            if self.settings.value("hiddenEnabled") == "false":
                self.hiddenEnabled = True
            else:
                self.hiddenEnabled = False

    def writeSettings(self):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("size", self.size())
        self.settings.setValue("hiddenEnabled", self.hiddenEnabled, )

    def enableHidden(self):
        if self.hiddenEnabled == False:
            self.fileModel.setFilter(
                QDir.NoDotAndDotDot | QDir.Hidden | QDir.AllDirs | QDir.Files)
            self.dirModel.setFilter(
                QDir.NoDotAndDotDot | QDir.Hidden | QDir.AllDirs)
            self.hiddenEnabled = True
            self.hiddenAction.setChecked(True)
            print("set hidden files to true")
        else:
            self.fileModel.setFilter(
                QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
            self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
            self.hiddenEnabled = False
            self.hiddenAction.setChecked(False)
            print("set hidden files to false")

    def openNewWin(self):
        self.copyListNew = ""
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        theApp = sys.argv[0]
        if QDir(path).exists:
            print("open '", path, "' in new window")
            self.process.startDetached("python3", [theApp, path])

    # actions
    def createActions(self):
        self.btnBack = QAction(QIcon.fromTheme(
            "go-previous"), "go back", triggered=self.goBack)
        self.btnUp = QAction(QIcon.fromTheme("go-up"),
                             "go up", triggered=self.goUp)
        self.btnHome = QAction(QIcon.fromTheme(
            "go-home"), "home folder", triggered=self.goHome)
        self.btnMusic = QAction(QIcon.fromTheme(
            "folder-music"), "music folder", triggered=self.goMusic)
        self.btnDocuments = QAction(QIcon.fromTheme(
            "folder-documents"), "documents folder", triggered=self.goDocuments)
        self.btnDownloads = QAction(QIcon.fromTheme(
            "folder-downloads"), "downloads folder", triggered=self.goDownloads)
        self.btnVideo = QAction(QIcon.fromTheme(
            "folder-video"), "video folder", triggered=self.goVideo)
        self.openAction = QAction(QIcon.fromTheme(
            "system-run"), "open File", triggered=self.openFile)

        #############################################################################################################################################################
        #############################################################################################################################################################
        self.gitinit = QAction(QIcon("icons8-git-48.png"),
                               "git init", triggered=self.init)
        self.gitinitOff = QAction(
            QIcon("giticon.png"), "git initOff", triggered=self.initOff)
        # self.treeview.addAction(self.initAction)
        self.gitcommit = QAction(
            QIcon("icons8-commit-git-64.png"), "git commit", triggered=self.commit)
        self.gitmerge = QAction(
            QIcon("icon/merge.png"), "git merge", triggered=self.merge)
        self.gitbranch = QAction(
            QIcon("gitbranch.png"), "git branch", triggered=self.branch)
        self.gitclone = QAction(
            QIcon("icon/gitclone.png"), "git clone", triggered=self.clone)
        self.gittree = QAction(
            QIcon("icon/tree.png"), "git tree", triggered=self.tree
        )
        #############################################################################################################################################################
        #############################################################################################################################################################

        self.openAction.setShortcut(QKeySequence(Qt.Key_Return))
        self.openAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.openAction)

        self.newWinAction = QAction(QIcon.fromTheme(
            "folder-new"), "open in new window", triggered=self.openNewWin)
        self.newWinAction.setShortcut(QKeySequence("Ctrl+n"))
        self.newWinAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.newWinAction)

        self.openActionText = QAction(QIcon.fromTheme("system-run"), "open File with built-in Texteditor",
                                      triggered=self.openFileText)
        self.openActionText.setShortcut(QKeySequence(Qt.Key_F6))
        self.openActionText.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.openActionText)

        self.openActionTextRoot = QAction(QIcon.fromTheme("applications-system"), "edit as root",
                                          triggered=self.openFileTextRoot)
        self.listview.addAction(self.openActionTextRoot)

        self.renameAction = QAction(QIcon.fromTheme("accessories-text-editor"), "rename File",
                                    triggered=self.renameFile)
        self.renameAction.setShortcut(QKeySequence(Qt.Key_F2))
        self.renameAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.renameAction)
        self.treeview.addAction(self.renameAction)

        self.renameFolderAction = QAction(QIcon.fromTheme("accessories-text-editor"), "rename Folder",
                                          triggered=self.renameFolder)
        self.treeview.addAction(self.renameFolderAction)

        self.copyAction = QAction(QIcon.fromTheme(
            "edit-copy"), "copy File(s)", triggered=self.copyFile)
        self.copyAction.setShortcut(QKeySequence("Ctrl+c"))
        self.copyAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.copyAction)

        self.copyFolderAction = QAction(QIcon.fromTheme(
            "edit-copy"), "copy Folder", triggered=self.copyFolder)
        self.treeview.addAction(self.copyFolderAction)

        self.pasteFolderAction = QAction(QIcon.fromTheme(
            "edit-paste"), "paste Folder", triggered=self.pasteFolder)
        self.treeview.addAction(self.pasteFolderAction)
        #        self.listview.addAction(self.pasteFolderAction)

        self.cutAction = QAction(QIcon.fromTheme(
            "edit-cut"), "cut File(s)", triggered=self.cutFile)
        self.cutAction.setShortcut(QKeySequence("Ctrl+x"))
        self.cutAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.cutAction)

        self.pasteAction = QAction(QIcon.fromTheme(
            "edit-paste"), "paste File(s) / Folder", triggered=self.pasteFile)
        self.pasteAction.setShortcut(QKeySequence("Ctrl+v"))
        self.pasteAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.pasteAction)

        self.delAction = QAction(QIcon.fromTheme(
            "edit-delete"), "delete File(s)", triggered=self.deleteFile)
        self.delAction.setShortcut(QKeySequence("Shift+Del"))
        self.delAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.delAction)

        self.delFolderAction = QAction(QIcon.fromTheme(
            "edit-delete"), "delete Folder", triggered=self.deleteFolder)
        self.treeview.addAction(self.delFolderAction)

        self.delActionTrash = QAction(QIcon.fromTheme(
            "user-trash"), "move to trash", triggered=self.deleteFileTrash)
        self.delActionTrash.setShortcut(QKeySequence("Del"))
        self.delActionTrash.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.delActionTrash)

        self.imageAction = QAction(QIcon.fromTheme(
            "image-x-generic"), "show Image", triggered=self.showImage)
        self.listview.addAction(self.imageAction)

        self.urlAction = QAction(QIcon.fromTheme(
            "browser"), "preview Page", triggered=self.showURL)
        self.listview.addAction(self.urlAction)

        self.dbAction = QAction(QIcon.fromTheme(
            "image-x-generic"), "show Database", triggered=self.showDB)
        self.listview.addAction(self.dbAction)

        self.py2Action = QAction(QIcon.fromTheme(
            "python"), "run in python", triggered=self.runPy2)
        self.listview.addAction(self.py2Action)

        self.py3Action = QAction(QIcon.fromTheme(
            "python3"), "run in python3", triggered=self.runPy3)
        self.listview.addAction(self.py3Action)

        self.findFilesAction = QAction(QIcon.fromTheme(
            "edit-find"), "find in folder", triggered=self.findFiles)
        self.findFilesAction.setShortcut(QKeySequence("Ctrl+f"))
        self.findFilesAction.setShortcutVisibleInContextMenu(True)
        self.treeview.addAction(self.findFilesAction)

        self.zipAction = QAction(QIcon.fromTheme(
            "zip"), "create zip from folder", triggered=self.createZipFromFolder)
        self.treeview.addAction(self.zipAction)

        self.zipFilesAction = QAction(QIcon.fromTheme("zip"), "create zip from selected files",
                                      triggered=self.createZipFromFiles)
        self.listview.addAction(self.zipFilesAction)

        self.unzipHereAction = QAction(QIcon.fromTheme(
            "application-zip"), "extract here ...", triggered=self.unzipHere)
        self.listview.addAction(self.unzipHereAction)

        self.unzipToAction = QAction(QIcon.fromTheme(
            "application-zip"), "extract to ...", triggered=self.unzipTo)
        self.listview.addAction(self.unzipToAction)

        self.playAction = QAction(QIcon.fromTheme("multimedia-player"), "play with Qt5Player",
                                  triggered=self.playInternal)
        self.playAction.setShortcut(QKeySequence(Qt.Key_F3))
        self.playAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.playAction)

        self.playInternalAction = QAction(QIcon.fromTheme(
            "vlc"), "play with vlc", triggered=self.playMedia)
        self.listview.addAction(self.playInternalAction)

        self.mp3Action = QAction(QIcon.fromTheme(
            "audio-x-generic"), "convert to mp3", triggered=self.makeMP3)
        self.listview.addAction(self.mp3Action)

        self.playlistAction = QAction(QIcon.fromTheme("audio-x-generic"), "make playlist from all mp3 files",
                                      triggered=self.makePlaylist)
        self.listview.addAction(self.playlistAction)

        self.playlistPlayerAction = QAction(QIcon.fromTheme("audio-x-generic"), "play Playlist",
                                            triggered=self.playPlaylist)
        self.listview.addAction(self.playlistPlayerAction)

        self.refreshAction = QAction(QIcon.fromTheme("view-refresh"), "refresh View", triggered=self.refreshList,
                                     shortcut="F5")
        self.refreshAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.refreshAction)

        self.hiddenAction = QAction(
            "show hidden Files", triggered=self.enableHidden)
        self.hiddenAction.setShortcut(QKeySequence("Ctrl+h"))
        self.hiddenAction.setShortcutVisibleInContextMenu(True)
        self.hiddenAction.setCheckable(True)
        self.listview.addAction(self.hiddenAction)

        self.goBackAction = QAction(QIcon.fromTheme(
            "go-back"), "go back", triggered=self.goBack)
        self.goBackAction.setShortcut(QKeySequence(Qt.Key_Backspace))
        self.goBackAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.goBackAction)

        self.helpAction = QAction(QIcon.fromTheme(
            "help"), "Help", triggered=self.showHelp)
        self.helpAction.setShortcut(QKeySequence(Qt.Key_F1))
        self.helpAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.helpAction)

        self.terminalAction = QAction(QIcon.fromTheme("terminal"), "open folder in Terminal",
                                      triggered=self.showInTerminal)
        self.terminalAction.setShortcut(QKeySequence(Qt.Key_F7))
        self.terminalAction.setShortcutVisibleInContextMenu(True)
        self.treeview.addAction(self.terminalAction)
        self.listview.addAction(self.terminalAction)

        self.startInTerminalAction = QAction(QIcon.fromTheme("terminal"), "execute in Terminal",
                                             triggered=self.startInTerminal)
        self.startInTerminalAction.setShortcut(QKeySequence(Qt.Key_F8))
        self.startInTerminalAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.startInTerminalAction)

        self.executableAction = QAction(QIcon.fromTheme("applications-utilities"), "make executable",
                                        triggered=self.makeExecutable)
        self.listview.addAction(self.executableAction)

        self.createFolderAction = QAction(QIcon.fromTheme("folder-new"), "create new Folder",
                                          triggered=self.createNewFolder)
        self.createFolderAction.setShortcut(QKeySequence("Shift+Ctrl+n"))
        self.createFolderAction.setShortcutVisibleInContextMenu(True)
        self.treeview.addAction(self.createFolderAction)

        self.gitaddAction = QAction(
            QIcon("giticon.png"), "git add", triggered=self.gitadd)
        self.listview.addAction(self.gitaddAction)

        self.gitrestoreAction = QAction(
            QIcon("giticon.png"), "git restore", triggered=self.gitrestore)
        self.listview.addAction(self.gitrestoreAction)

        self.gitrestore_stagedAction = QAction(QIcon("giticon.png"), "git restore -- staged",
                                               triggered=self.gitrestore_staged)
        self.listview.addAction(self.gitrestore_stagedAction)

        self.gitrm_cachedAction = QAction(
            QIcon("giticon.png"), "git rm --cached", triggered=self.gitrm_cached)
        self.listview.addAction(self.gitrm_cachedAction)

        self.gitrmAction = QAction(
            QIcon("giticon.png"), "git rm", triggered=self.gitrm)
        self.listview.addAction(self.gitrmAction)

        self.gitmvAction = QAction(
            QIcon("giticon.png"), "git mv", triggered=self.gitmv)
        self.listview.addAction(self.gitmvAction)

        self.gitaddAction = QAction(
            QIcon("giticon.png"), "git add", triggered=self.gitadd)
        self.listview.addAction(self.gitaddAction)

        self.gitrestoreAction = QAction(
            QIcon("giticon.png"), "git restore", triggered=self.gitrestore)
        self.listview.addAction(self.gitrestoreAction)

        self.gitrestore_stagedAction = QAction(QIcon("giticon.png"), "git restore -- staged",
                                               triggered=self.gitrestore_staged)
        self.listview.addAction(self.gitrestore_stagedAction)

        self.gitrm_cachedAction = QAction(
            QIcon("giticon.png"), "git rm --cached", triggered=self.gitrm_cached)
        self.listview.addAction(self.gitrm_cachedAction)

        self.gitrmAction = QAction(
            QIcon("giticon.png"), "git rm", triggered=self.gitrm)
        self.listview.addAction(self.gitrmAction)

        self.gitmvAction = QAction(
            QIcon("giticon.png"), "git mv", triggered=self.gitmv)
        self.listview.addAction(self.gitmvAction)

    def playPlaylist(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            self.player = QAudioPlayer.Player('')
            self.player.setGeometry(100, 100, 500, 350)
            self.player.show()
            self.player.clearList()
            self.player.openOnStart(path)
            print("added Files to playlist")

    def showImage(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            print("show image: ", path)
            self.win = QImageViewer.ImageViewer()
            self.win.show()
            self.win.filename = path
            self.win.loadFile(path)

    def showDB(self):
        if self.listview.selectionModel().hasSelection():
            import DBViewer
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            print("show image: ", path)
            self.db_win = DBViewer.MyWindow()
            self.db_win.show()
            self.db_win.fileOpenStartup(path)

    def checkIsApplication(self, path):
        st = subprocess.check_output("file  --mime-type '" + path + "'", stderr=subprocess.STDOUT,
                                     universal_newlines=True, shell=True)
        print(st)
        if "application/x-executable" in st:
            print(path, "is an application")
            return True
        else:
            return False

    def makeExecutable(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            print("set", path, "executable")
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)

    def showInTerminal(self):
        if self.treeview.hasFocus():
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).absoluteFilePath()
        elif self.listview.hasFocus():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
        self.terminal = QTerminalFolder.MainWindow()
        self.terminal.show()
        if self.terminal.isVisible():
            os.chdir(path)
            self.terminal.shellWin.startDir = path
            self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                           + ":" + str(path) + "$ ")
            self.terminal.shellWin.appendPlainText(self.terminal.shellWin.name)

    def startInTerminal(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            filename = self.fileModel.fileInfo(index).fileName()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            folderpath = self.fileModel.fileInfo(index).path()
            if not self.fileModel.fileInfo(index).isDir():
                self.terminal = QTerminalFolder.MainWindow()
                self.terminal.show()
                if self.terminal.isVisible():
                    os.chdir(folderpath)
                    self.terminal.shellWin.startDir = folderpath
                    self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                                   + ":" + str(folderpath) + "$ ")
                    self.terminal.shellWin.appendPlainText(
                        self.terminal.shellWin.name)
                    self.terminal.shellWin.insertPlainText("./%s" % (filename))
            else:
                self.terminal = QTerminalFolder.MainWindow()
                self.terminal.show()
                if self.terminal.isVisible():
                    os.chdir(path)
                    self.terminal.shellWin.startDir = path
                    self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                                   + ":" + str(path) + "$ ")
                    self.terminal.shellWin.appendPlainText(
                        self.terminal.shellWin.name)

    def createZipFromFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).filePath()
        fname = self.dirModel.fileInfo(index).fileName()
        print("folder to zip:", path)
        self.copyFile()
        target, _ = QFileDialog.getSaveFileName(self, "Save as... (do not add .zip)", path + "/" + fname,
                                                "zip files (*.zip)")
        if (target != ""):
            shutil.make_archive(target, 'zip', path)

    def createZipFromFiles(self):
        if self.listview.selectionModel().hasSelection():
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).filePath()
            fname = self.dirModel.fileInfo(index).fileName()
            print("folder to zip:", path)
            self.copyFile()
            target, _ = QFileDialog.getSaveFileName(
                self, "Save as...", path + "/" + "archive.zip", "zip files (*.zip)")
            if (target != ""):
                zipText = ""
                with ZipFile(target, 'w') as myzip:
                    for file in self.copyList:
                        fname = os.path.basename(file)
                        myzip.write(file, fname)

    def unzipHere(self):
        if self.listview.selectionModel().hasSelection():
            file_index = self.listview.selectionModel().currentIndex()
            file_path = self.fileModel.fileInfo(file_index).filePath()
            folder_index = self.treeview.selectionModel().currentIndex()
            folder_path = self.dirModel.fileInfo(folder_index).filePath()
            with ZipFile(file_path, 'r') as zipObj:
                # Extract zip file in current directory
                zipObj.extractall(folder_path)

    def unzipTo(self):
        file_index = self.listview.selectionModel().currentIndex()
        file_path = self.fileModel.fileInfo(file_index).filePath()
        dirpath = QFileDialog.getExistingDirectory(
            self, "selectFolder", QDir.homePath(), QFileDialog.ShowDirsOnly)
        if dirpath:
            with ZipFile(file_path, 'r') as zipObj:
                zipObj.extractall(dirpath)

    def findFiles(self):
        print("find")
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        print("open findWindow")
        self.w = findFilesWindow.ListBox()
        self.w.show()
        self.w.folderEdit.setText(path)
        self.w.findEdit.setText(self.findfield.text())

    def refreshList(self):
        print("refreshing view")
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).path()
        self.treeview.setCurrentIndex(self.fileModel.index(path))
        self.treeview.setFocus()
        print(self.combo.currentText())
        if git_handler.git_status(self.currentPath):
            self.currentBranch = "Current Branch : " + \
                git_handler.git_show_branch_list(self.currentPath)[1]
            self.setWindowTitle(self.currentBranch)
            self.gitStatusList = git_handler.get_status_list(self.currentPath)
        else:
            self.currentBranch = ""
            self.gitStatusList = False
        self.initButtonPulse()
        # print(self.gitStatusList)
        # print(self.currentPath)

    def makeMP3(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).filePath()
            ext = self.fileModel.fileInfo(index).suffix()
            newpath = path.replace("." + ext, ".mp3")
            print(ext)
            self.statusBar().showMessage("%s '%s'" % ("converting:", path))
            self.process.startDetached("ffmpeg", ["-i", path, newpath])
            print("%s '%s'" % ("converting", path))

    def makePlaylist(self):
        if self.listview.selectionModel().hasSelection():
            index = self.treeview.selectionModel().currentIndex()
            foldername = self.dirModel.fileInfo(index).fileName()

            path = self.currentPath + "/" + foldername + ".m3u"
            pl = QFile(path)
            pl.open(QIODevice.ReadWrite | QIODevice.Truncate)
            mp3List = []

            for name in os.listdir(self.currentPath):
                if os.path.isfile(os.path.join(self.currentPath, name)):
                    if ".mp3" in name:
                        mp3List.append(self.currentPath + "/" + name)

            mp3List.sort(key=str.lower)

            with open(path, 'w') as playlist:
                playlist.write('\n'.join(mp3List))
                playlist.close()

    def showHelp(self):
        top = self.y() + 26
        left = self.width() / 2 - 100
        print(top)
        self.w = helpWindow()
        self.w.setWindowFlags(Qt.FramelessWindowHint)
        self.w.setWindowModality(Qt.ApplicationModal)
        self.w.setGeometry(left, top, 300, 360)
        self.w.show()

    def on_clicked(self, index):
        if self.treeview.selectionModel().hasSelection():
            index = self.treeview.selectionModel().currentIndex()
            if not (self.treeview.isExpanded(index)):
                self.treeview.setExpanded(index, True)
            else:
                self.treeview.setExpanded(index, False)

    def getFolderSize(self, path):
        size = sum(os.path.getsize(f)
                   for f in os.listdir(folder) if os.path.isfile(f))
        return size

    def on_selectionChanged(self):
        self.treeview.selectionModel().clearSelection()
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listview.setRootIndex(self.fileModel.setRootPath(path))
        self.currentPath = path
        # self.gitStatusList = git_handler.get_status_list(self.currentPath)
        self.setWindowTitle(path)
        self.getRowCount()

    def openFile(self):
        if self.listview.hasFocus():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            self.copyFile()
            for files in self.copyList:
                print("%s '%s'" % ("open file", files))
                if self.checkIsApplication(path) == True:
                    self.process.startDetached(files)
                else:
                    QDesktopServices.openUrl(
                        QUrl(files, QUrl.TolerantMode | QUrl.EncodeUnicode))

    def openFileText(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            self.texteditor = QTextEdit.MainWindow()
            self.texteditor.show()
            self.texteditor.loadFile(path)

    def openFileTextRoot(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            file = sys.argv[0]
            mygksu = os.path.join(os.path.dirname(file), "mygksu")
            self.process.startDetached(mygksu, ["xed", path])

    def playInternal(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).filePath()
            self.statusBar().showMessage("%s '%s'" % ("file:", path))
            self.player = Qt5Player.VideoPlayer('')
            self.player.show()
            self.player.loadFilm(path)
            print("%s '%s'" % ("playing", path))

    def playMedia(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).filePath()
            self.statusBar().showMessage("%s '%s'" % ("file:", path))
            self.process.startDetached("cvlc", [path])
            print("%s '%s'" % ("playing with vlc:", path))

    def showURL(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            self.webview = QWebViewer.MainWindow()
            self.webview.show()
            self.webview.load_url(path)

    def list_doubleClicked(self):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        #        folderpath = self.fileModel.fileInfo(index).path()
        if not self.fileModel.fileInfo(index).isDir():
            if self.checkIsApplication(path) == True:
                self.process.startDetached(path)
            else:
                QDesktopServices.openUrl(
                    QUrl(path, QUrl.TolerantMode | QUrl.EncodeUnicode))
        else:
            self.treeview.setCurrentIndex(self.dirModel.index(path))
            self.treeview.setFocus()
            #            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)
        # self.gitStatusList = git_handler.get_status_list(self.currentPath)

    def goBack(self):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).path()
        self.treeview.setCurrentIndex(self.dirModel.index(path))

    def goUp(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).path()
        print(path)
        self.treeview.setCurrentIndex(self.dirModel.index(path))

    def goHome(self):
        docs = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goMusic(self):
        docs = QStandardPaths.standardLocations(
            QStandardPaths.MusicLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goVideo(self):
        docs = QStandardPaths.standardLocations(
            QStandardPaths.MoviesLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goDocuments(self):
        docs = QStandardPaths.standardLocations(
            QStandardPaths.DocumentsLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goDownloads(self):
        docs = QStandardPaths.standardLocations(
            QStandardPaths.DownloadLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    #############################################################################################################################################################
    #############################################################################################################################################################

    def handle_merged__clicked(self):
        merged_branch = self.list_widget.currentItem().text()
        result = git_handler.git_merge(merged_branch)
        if "conflicts" in result:
            QMessageBox.critical(self, "fail", result)
        else:
            QMessageBox.about(self, "success", result)

    def init(self):
        index = self.listview.selectionModel().currentIndex()
        dir = self.currentPath
        path = self.fileModel.fileInfo(index).fileName()
        git_handler.git_init(dir)

    def initOff(self):
        pass

    def merge(self):
        # print('--------------------------------')
        # targetBranch = 'test'
        # git_handler.git_merge(self.currentPath, targetBranch)

        # listofbranch = git_handler.git_show_branch_list(self.currentPath)[0]
        # window = QWidget()
        # layout = QVBoxLayout(window)

        # now_branch = git_handler.git_show_branch_list(self.currentPath)[1]

        # list_widget = QListWidget()

        # for branch in listofbranch:
        #    if branch is not now_branch:
        #        list_widget.addItem(branch)

        # list_widget.itemClicked.connect(self.handle_merged_branch_clicked)

        # layout.addWidget(list_widget)

        # window.show()

        dlg = QInputDialog(self)
        items = git_handler.git_show_branch_list(self.currentPath)[0]
        items.remove(
            '* ' + git_handler.git_show_branch_list(self.currentPath)[1])
        item, ok = dlg.getItem(
            self, 'Merge Branch', "Select Branch", items, 0, False)
        if ok and item:
            result = git_handler.git_merge(self.currentPath, item)
            if not result == True:
                errorBox = QMessageBox()
                errorBox.setWindowTitle("Error")
                errorMessage = ''
                for i in result:
                    print("line : " + i)
                    if 'CONFLICT ' in i:
                        print("ERRORLINE : " + i)
                        errorMessage += i
                print("ERROR " + errorMessage)
                errorBox.setText(errorMessage)
                errorBox.setStandardButtons(QMessageBox.Ok)
                errorBox.setInformativeText("")
                errorBox.exec()

    def commit(self):
        # print(self.gitStatusList)
        if not git_handler.git_status(self.currentPath):
            return
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Git Commit")
        str = "Renamed\n"
        # print("Ahoy")
        for file_name in self.gitStatusList['staged']['renamed']:
            # print(file_name)
            str += file_name + "\n"
        str += "\nNew\n"
        for file_name in self.gitStatusList['staged']['new']:
            # print(file_name)
            str += file_name + "\n"
        str += "\nModified\n"
        for file_name in self.gitStatusList['staged']['modified']:
            print(file_name)
            str += file_name + "\n"
        str += "\nDeleted\n"
        for file_name in self.gitStatusList['staged']['deleted']:
            # print(file_name)
            str += file_name + "\n"
        str += "\nThese files have been staged.    "
        msgBox.setText(str)
        msgBox.setInformativeText("Do you want to commit your work?")
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        # msgBox.resize()
        ret = msgBox.exec()
        while ret == QMessageBox.Yes:
            dlg = QInputDialog(self)
            newname, ok = dlg.getText(
                self, 'Git', "Commit Message:", QLineEdit.Normal, "", Qt.Dialog)
            if ok:
                if not newname == "":
                    git_handler.git_commit(self.currentPath, newname)
                    self.gitStatusList = git_handler.get_status_list(
                        self.currentPath)
                    return
                else:
                    errorBox = QMessageBox()
                    errorBox.setWindowTitle("Error")
                    errorBox.setText("You must insert commit message.")
                    errorBox.setStandardButtons(QMessageBox.Ok)
                    errorBox.setInformativeText("")
                    errorBox.exec()
            else:
                ret = QMessageBox.No
        return

    def branch(self):
        # git_handler 함수 이름 기다리는중
        if not git_handler.git_status(self.currentPath):
            return
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).path()
        if self.combo.currentText() == "Create Branch":
            dlg = QInputDialog(self)
            newname, ok = dlg.getText(
                self, 'Create Branch', "Branch Name:", QLineEdit.Normal, "", Qt.Dialog)
            if ok:
                if '  ' + newname in git_handler.git_show_branch_list(self.currentPath)[0]:
                    errorBox = QMessageBox()
                    errorBox.setWindowTitle("Error")
                    errorBox.setText("A branch named " +
                                     newname + " already exists")
                    errorBox.setStandardButtons(QMessageBox.Ok)
                    errorBox.setInformativeText("")
                    errorBox.exec()
                if newname == git_handler.git_show_branch_list(self.currentPath)[1]:
                    errorBox = QMessageBox()
                    errorBox.setWindowTitle("Error")
                    errorBox.setText("You are currently on " + newname)
                    errorBox.setStandardButtons(QMessageBox.Ok)
                    errorBox.setInformativeText("")
                    errorBox.exec()
                git_handler.git_create_branch(self.currentPath, newname)
                # print(newname)
                # git_handler.git_branch(dir, path, newname)
                # self.gitStatusList = git_handler.get_status_list(self.currentPath)
        elif self.combo.currentText() == "Delete Branch":
            dlg = QInputDialog(self)
            items = git_handler.git_show_branch_list(self.currentPath)[0]
            item, ok = dlg.getItem(
                self, 'Delete Branch', "Select Branch", items, 0, False)
            if ok and item:
                git_handler.git_delete_branch(self.currentPath, item)
                print(item)
                # git_handler.git_dbranch(dir, path, item)
        elif self.combo.currentText() == "Rename Branch":
            dlg = QInputDialog(self)
            items = git_handler.git_show_branch_list(self.currentPath)[0]
            temp = git_handler.git_show_branch_list(self.currentPath)[1]
            item, ok = dlg.getItem(
                self, 'Rename Branch', "Select Branch", items, 0, False)
            if ok and item:
                print(item)
                dlg = QInputDialog(self)
                newname, ok = dlg.getText(
                    self, 'Rename Branch', "Branch Name:", QLineEdit.Normal, "", Qt.Dialog)
                if ok:
                    git_handler.git_checkout_branch(self.currentPath, item)
                    if '  ' + newname in git_handler.git_show_branch_list(self.currentPath)[0]:
                        errorBox = QMessageBox()
                        errorBox.setWindowTitle("Error")
                        errorBox.setText("A branch named " +
                                         newname + " already exists")
                        errorBox.setStandardButtons(QMessageBox.Ok)
                        errorBox.setInformativeText("")
                        errorBox.exec()
                    if newname == git_handler.git_show_branch_list(self.currentPath)[1]:
                        errorBox = QMessageBox()
                        errorBox.setWindowTitle("Error")
                        errorBox.setText(
                            "You cannot name " + newname + " because you are currently on it")
                        errorBox.setStandardButtons(QMessageBox.Ok)
                        errorBox.setInformativeText("")
                        errorBox.exec()
                    git_handler.git_rename_branch(self.currentPath,newname)
                    print(newname)
            git_handler.git_checkout_branch(self.currentPath, temp)
            self.currentBranch = "Current Branch : " + \
                git_handler.git_show_branch_list(self.currentPath)[1]
            self.setWindowTitle(self.currentBranch)
            # git_handler.git_rbranch(dir, path, item, newname)
        elif self.combo.currentText() == "Checkout Branch":
            dlg = QInputDialog(self)
            items = git_handler.git_show_branch_list(self.currentPath)[0]
            item, ok = dlg.getItem(
                self, 'Checkout Branch', "Select Branch", items, 0, False)
            if ok and item:
                if '* ' in item:
                    errorBox = QMessageBox()
                    errorBox.setWindowTitle("Error")
                    errorBox.setText(
                        "You are already on " + git_handler.git_show_branch_list(self.currentPath)[1])
                    errorBox.setStandardButtons(QMessageBox.Ok)
                    errorBox.setInformativeText("")
                    errorBox.exec()
                git_handler.git_checkout_branch(self.currentPath,item)
                self.currentBranch = "Current Branch : " + \
                    git_handler.git_show_branch_list(self.currentPath)[1]
                self.setWindowTitle(self.currentBranch)
                print(item)
                # git_handler.cbranch(dir, path, item)

    def clone(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Git Clone")
        str = 'Is the cloning repository public?'
        msgBox.setText(str)
        #msgBox.setInformativeText("Is the cloning repository is public")
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        # msgBox.resize()
        ret = msgBox.exec()
        if ret == QMessageBox.Yes:
            address, ok = QInputDialog.getText(
                self, 'repository address', 'Enter Github repository address:')
            if ok:
                if not git_handler.git_clone(self.currentPath, self.currentBranch, '', '', address):
                    errorBox = QMessageBox()
                    errorBox.setWindowTitle("Error")
                    errorBox.setText(
                        address + " is not a valid repository address")
                    errorBox.setStandardButtons(QMessageBox.Ok)
                    errorBox.setInformativeText("")
                    errorBox.exec()
        elif ret == QMessageBox.No:
            address, ok = QInputDialog.getText(
                self, 'repository address', 'Enter Github repository address:')
            if ok:
                id, ok = QInputDialog.getText(
                    self, 'username', 'Enter Github username:')
                if ok:
                    token, ok = QInputDialog.getText(
                        self, 'token', 'Enter Github token:')
                #print('Github address:', address)
                    if ok:
                        if not git_handler.git_clone(self.currentPath, self.currentBranch, id, token, address):
                            errorBox = QMessageBox()
                            errorBox.setWindowTitle("Error")
                            errorBox.setText(
                                address + " is not a valid repository address or " +
                                id + " is not a valid user name or " +
                                token + " is not a valid token")
                            errorBox.setStandardButtons(QMessageBox.Ok)
                            errorBox.setInformativeText("")
                            errorBox.exec()
                #print("======================================")
                #print(result)


            # if "Username" in result:
            #     id, _ = QInputDialog.getText(
            #         self, 'userid', "Enter Github Id: ")
            #     token, _ = QInputDialog.getText(
            #         self, 'accesstoken', "Enter Github Access Token: ")

            #     repos_name = address.split("/")[-1].split(".")[0]
            #     address = "https://" + id + ":" + token + "@github.com/" + id+"/" + repos_name

            # git_handler.git_clone(
            #     self.currentPath, self.currentBranch, id, token, address)

            # https: // github.com/KIMIS12/capstonIMAGEtest1.git
            # git clone https://사용자ID:개인액세스토큰@github.com/사용자ID/저장소이름.git

    def tree(self):

        class LineWidget(QWidget):
            def __init__(self, graph_data):
                super().__init__()
                self.initUI()
                self.graph_data = graph_data
                # self.paintEvent()
                # self.draw_line()

            def initUI(self):
                self.setWindowTitle("git tree")
                self.resize(500, 500)
                self.show()
                QToolTip.setFont(QFont('SansSerif', 10))

                btn = QPushButton('commit', self)
                btn.setToolTip('Hello')
                btn.move(curr_x, curr_y)
                btn.resize(btn.sizeHint())

            def paintEvent(self, e):
                qp = QPainter()
                qp.begin(self)
                self.draw_graph(qp)

            def draw_graph(self, qp):
                # draws graph from top(latest commit) to bottom
                start_x = 230
                start_y = 40
                delta_x = 10
                delta_y = 10
                commit_circle_size = 4
                curr_y = start_y
                qp.setPen(QPen(Qt.blue, 2))
                qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))

                for graph_line in self.graph_data:
                    curr_x = start_x
                    for graph_symbol in graph_line:
                        if graph_symbol == '*':
                            # qp.drawEllipse(curr_x, curr_y, commit_circle_size, commit_circle_size)
                            btn = QPushButton('commit', self)
                            btn.setToolTip('Hello')
                            btn.move(curr_x, curr_y)
                            btn.resize(btn.sizeHint())
                        elif graph_symbol == '|':
                            qp.drawLine(curr_x, curr_y, curr_x, curr_y + delta_y)
                        elif graph_symbol == '/':
                            qp.drawLine(curr_x, curr_y, curr_x - delta_x, curr_y + delta_y)
                        elif graph_symbol == '\\':
                            qp.drawLine(curr_x, curr_y, curr_x + delta_x, curr_y + delta_y)
                        curr_x += delta_x
                    curr_y += delta_y

        # tmp = ["git tree"]
        # app2 = QApplication()

        graph_data = git_handler.git_parse_log(self.currentPath)
        
        global widget
        widget = LineWidget(graph_data)
        # widget.show()
        # sys.exit(app2.exec_())

    def initButtonPulse(self):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).path()
        if self.gitStatusList == False:
            self.tBar.removeAction(self.gitinit)
            self.tBar.removeAction(self.gitinitOff)
            self.tBar.insertAction(self.gitcommit, self.gitinit)
        else:
            self.tBar.removeAction(self.gitinit)
            self.tBar.removeAction(self.gitinitOff)
            self.tBar.insertAction(self.gitcommit, self.gitinitOff)

            # self.tBar.addAction(self.gitcommit)
            # self.tBar.addSeparator()

    #############################################################################################################################################################
    #############################################################################################################################################################

    def infobox(self, message):
        title = "QFilemager"
        QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self,
                    Qt.Dialog | Qt.NoDropShadowWindowHint).show()

    def contextMenuEvent(self, event):

        selected = self.listview.selectionModel().selectedRows()

        count = len(selected)

        i = 0
        if count == 1:
            for index in selected:
                # print("After")
                # print(self.fileModel.fileInfo(index).fileName())
                file_list = self.gitStatusList
                filename = self.fileModel.fileInfo(index).fileName()
                i = gitstatus(file_list, filename)

            # for index in selected:
            # path = self.currentPath + "/" + self.fileModel.data(index,self.fileModel.FileNameRole)
            # print(path, "copied to clipboard")
            # self.copyList.append(path)
            # self.clip.setText('\n'.join(self.copyList))
        # print("%s\n%s" % ("filepath(s) copied:", '\n'.join(self.copyList)))

        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        self.menu = QMenu(self.listview)

        if self.listview.hasFocus():
            # if "Untracked files" in git_handler.git_status(self.currentPath):
            if i == gitStatus.Untracked:
                self.menu.addAction(self.gitaddAction)
            # elif "Changes not staged for commit" in git_handler.git_status(self.currentPath):
            elif i == gitStatus.Modified:
                self.menu.addAction(self.gitaddAction)
                self.menu.addAction(self.gitrestoreAction)
            # elif "changes to be commited" in git_handler.git_status(self.currentPath):
            elif i == gitStatus.Staged:
                self.menu.addAction(self.gitrestore_stagedAction)
            # elif "Untracked files" not in git_handler.git_status(self.currentPath):
            elif i == gitStatus.Unmodified:
                self.menu.addAction(self.gitrm_cachedAction)
                self.menu.addAction(self.gitrmAction)
                self.menu.addAction(self.gitmvAction)
            elif i == gitStatus.Staged_Modified:
                self.menu.addAction(self.gitaddAction)
                self.menu.addAction(self.gitrestoreAction)
            elif i == gitStatus.Staged_Untracked:
                self.menu.addAction(self.gitaddAction)

            self.menu.addSeparator()
            self.menu.addAction(self.createFolderAction)
            # self.menu.addAction(self.openAction)
            # self.menu.addAction(self.openActionText)
            # self.menu.addAction(self.openActionTextRoot)
            # self.menu.addSeparator()
            # if os.path.isdir(path):
            # self.menu.addAction(self.newWinAction)
            self.menu.addSeparator()
            self.menu.addAction(self.renameAction)
            self.menu.addSeparator()
            # self.menu.addAction(self.copyAction)
            # self.menu.addAction(self.cutAction)
            # self.menu.addAction(self.pasteAction)
            #            self.menu.addAction(self.pasteFolderAction)
            # self.menu.addAction(self.terminalAction)
            # self.menu.addAction(self.startInTerminalAction)
            # self.menu.addAction(self.executableAction)
            # database viewer
            # db_extension = [".sql", "db", "sqlite",
            #                "sqlite3", ".SQL", "DB", "SQLITE", "SQLITE3"]
            # for ext in db_extension:
            #    if ext in path:
            #        self.menu.addAction(self.dbAction)
            # html viewer
            # url_extension = [".htm", ".html"]
            # for ext in url_extension:
            #    if ext in path:
            #        self.menu.addAction(self.urlAction)
            # run in python
            # if path.endswith(".py"):
            #    self.menu.addAction(self.py2Action)
            #    self.menu.addAction(self.py3Action)
            # image viewer
            # image_extension = [".png", "jpg", ".jpeg", ".bmp", "tif", ".tiff", ".pnm", ".svg",
            #                   ".exif", ".gif"]
            # for ext in image_extension:
            #    if ext in path or ext.upper() in path:
            #        self.menu.addAction(self.imageAction)
            # self.menu.addSeparator()
            # self.menu.addAction(self.delActionTrash)
            # self.menu.addAction(self.delAction)
            # self.menu.addSeparator()
            # if ".m3u" in path:
            #    self.menu.addAction(self.playlistPlayerAction)
            # extensions = [".mp3", ".mp4", "mpg", ".m4a", ".mpeg", "avi", ".mkv", ".webm",
            #              ".wav", ".ogg", ".flv ", ".vob", ".ogv", ".ts", ".m2v", "m4v", "3gp", ".f4v"]
            # for ext in extensions:
            #    if ext in path or ext.upper() in path:
            #        self.menu.addSeparator()
            #        self.menu.addAction(self.playAction)
            #        self.menu.addAction(self.playInternalAction)
            #        self.menu.addSeparator()
            # extensions = [".mp4", "mpg", ".m4a", ".mpeg", "avi", ".mkv", ".webm",
            #              ".wav", ".ogg", ".flv ", ".vob", ".ogv", ".ts", ".m2v", "m4v", "3gp", ".f4v"]
            # for ext in extensions:
            #    if ext in path or ext.upper() in path:
            #        self.menu.addAction(self.mp3Action)
            #        self.menu.addSeparator()
            # if ".mp3" in path:
            #    self.menu.addAction(self.playlistAction)
            self.menu.addAction(self.refreshAction)
            self.menu.addAction(self.hiddenAction)
            # self.menu.addAction(self.zipFilesAction)
            # zip_extension = [".zip", ".tar.gz"]
            # for ext in zip_extension:
            #    if ext in path:
            #        self.menu.addAction(self.unzipHereAction)
            #        self.menu.addAction(self.unzipToAction)
            # self.menu.addSeparator()
            # self.menu.addAction(self.helpAction)
            self.menu.popup(QCursor.pos())
        else:
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).absoluteFilePath()
            print("current path is:", path)
            self.menu = QMenu(self.treeview)
            if os.path.isdir(path):
                # if "Untracked files" in git_handler.git_status(path):
                if i == gitStatus.Untracked:
                    self.menu.addAction(self.gitaddAction)
                # elif "Changes not staged for commit" in git_handler.git_status(path):
                elif i == gitStatus.Modified:
                    self.menu.addAction(self.gitaddAction)
                    self.menu.addAction(self.gitrestoreAction)
                # elif "changes to be commited" in git_handler.git_status(path):
                elif i == gitStatus.Staged:
                    self.menu.addAction(self.gitrestore_stagedAction)
                # elif "Untracked files" not in git_handler.git_status(path):
                elif i == gitStatus.Unmodified:
                    self.menu.addAction(self.gitrm_cachedAction)
                    self.menu.addAction(self.gitrmAction)
                    self.menu.addAction(self.gitmvAction)
                elif i == gitStatus.Staged_Modified:
                    self.menu.addAction(self.gitaddAction)
                    self.menu.addAction(self.gitrestoreAction)
                elif i == gitStatus.Staged_Untracked:
                    self.menu.addAction(self.gitaddAction)
                self.menu.addSeparator()
                self.menu.addAction(self.newWinAction)
                self.menu.addAction(self.createFolderAction)
                self.menu.addAction(self.renameFolderAction)
                self.menu.addAction(self.copyFolderAction)
                self.menu.addAction(self.pasteFolderAction)
                self.menu.addAction(self.delFolderAction)
                self.menu.addAction(self.terminalAction)
                self.menu.addAction(self.findFilesAction)
                self.menu.addAction(self.zipAction)
            self.menu.popup(QCursor.pos())

    def createNewFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        dlg = QInputDialog(self)
        foldername, ok = dlg.getText(
            self, 'Folder Name', "Folder Name:", QLineEdit.Normal, "", Qt.Dialog)
        if ok:
            success = QDir(path).mkdir(foldername)

    def gitadd(self):
        index = self.listview.selectionModel().currentIndex()
        dir = self.currentPath
        path = self.fileModel.fileInfo(index).fileName()
        git_handler.git_add(dir, path)
        self.gitStatusList = git_handler.get_status_list(self.currentPath)

    def gitrestore(self):
        index = self.listview.selectionModel().currentIndex()
        dir = self.currentPath
        path = self.fileModel.fileInfo(index).fileName()
        git_handler.git_restore(dir, path)
        self.gitStatusList = git_handler.get_status_list(self.currentPath)

    def gitrestore_staged(self):
        index = self.listview.selectionModel().currentIndex()
        dir = self.currentPath
        path = self.fileModel.fileInfo(index).fileName()
        git_handler.git_restore_staged(dir, path)
        self.gitStatusList = git_handler.get_status_list(self.currentPath)

    def gitrm_cached(self):
        index = self.listview.selectionModel().currentIndex()
        dir = self.currentPath
        path = self.fileModel.fileInfo(index).fileName()
        git_handler.git_untrack(dir, path)
        self.gitStatusList = git_handler.get_status_list(self.currentPath)

    def gitrm(self):
        index = self.listview.selectionModel().currentIndex()
        dir = self.currentPath
        path = self.fileModel.fileInfo(index).fileName()
        git_handler.git_rm(dir, path)
        self.gitStatusList = git_handler.get_status_list(self.currentPath)

    def gitmv(self):
        index = self.listview.selectionModel().currentIndex()
        dir = self.currentPath
        path = self.fileModel.fileInfo(index).fileName()
        dlg = QInputDialog(self)
        newname, ok = dlg.getText(
            self, 'Git MV', "Git mv:", QLineEdit.Normal, "", Qt.Dialog)
        if ok:
            git_handler.git_mv(dir, path, newname)
            self.gitStatusList = git_handler.get_status_list(self.currentPath)

    def runPy2(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            self.process.startDetached("python", [path])

    def runPy3(self):
        if self.listview.selectionModel().hasSelection():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            error = QProcess.error(self.process)
            self.process.startDetached("python3", [path])
            if self.process.errorOccurred():
                self.infobox(error)

    def renameFile(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                basepath = self.fileModel.fileInfo(index).path()
                print(basepath)
                oldName = self.fileModel.fileInfo(index).fileName()
                dlg = QInputDialog()
                newName, ok = dlg.getText(
                    self, 'new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
                if ok:
                    newpath = basepath + "/" + newName
                    QFile.rename(path, newpath)
        elif self.treeview.hasFocus():
            self.renameFolder()

    def renameFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        basepath = self.dirModel.fileInfo(index).path()
        print("pasepath:", basepath)
        oldName = self.dirModel.fileInfo(index).fileName()
        dlg = QInputDialog()
        newName, ok = dlg.getText(
            self, 'new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
        if ok:
            newpath = basepath + "/" + newName
            print(newpath)
            nd = QDir(path)
            check = nd.rename(path, newpath)

    def copyFile(self):
        self.copyList = []
        selected = self.listview.selectionModel().selectedRows()
        count = len(selected)
        for index in selected:
            path = self.currentPath + "/" + \
                self.fileModel.data(index, self.fileModel.FileNameRole)
            print(path, "copied to clipboard")
            self.copyList.append(path)
            self.clip.setText('\n'.join(self.copyList))
        print("%s\n%s" % ("filepath(s) copied:", '\n'.join(self.copyList)))

    def copyFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        folderpath = self.dirModel.fileInfo(index).absoluteFilePath()
        print("%s\n%s" % ("folderpath copied:", folderpath))
        self.folder_copied = folderpath
        self.copyList = []

    def pasteFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        target = self.folder_copied
        destination = self.dirModel.fileInfo(index).absoluteFilePath(
        ) + "/" + QFileInfo(self.folder_copied).fileName()
        print("%s %s %s" % (target, "will be pasted to", destination))
        try:
            shutil.copytree(target, destination)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(target, destination)
            else:
                self.infobox('Error', 'Directory not copied. Error: %s' % e)

    def pasteFile(self):
        if len(self.copyList) > 0:
            index = self.treeview.selectionModel().currentIndex()
            file_index = self.listview.selectionModel().currentIndex()
            for target in self.copyList:
                print(target)
                destination = self.dirModel.fileInfo(
                    index).absoluteFilePath() + "/" + QFileInfo(target).fileName()
                print("%s %s" % ("pasted File to", destination))
                QFile.copy(target, destination)
                if self.cut == True:
                    QFile.remove(target)
                self.cut == False
        else:
            index = self.treeview.selectionModel().currentIndex()
            target = self.folder_copied
            destination = self.dirModel.fileInfo(index).absoluteFilePath() + "/" + QFileInfo(
                self.folder_copied).fileName()
            try:
                shutil.copytree(target, destination)
            except OSError as e:
                # If the error was caused because the source wasn't a directory
                if e.errno == errno.ENOTDIR:
                    shutil.copy(target, destination)
                else:
                    print('Directory not copied. Error: %s' % e)

    def cutFile(self):
        self.cut = True
        self.copyFile()

    def deleteFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        delFolder = self.dirModel.fileInfo(index).absoluteFilePath()
        msg = QMessageBox.question(self, "Info", "Caution!\nReally delete this Folder?\n" + delFolder,
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            print('Deletion confirmed.')
            self.statusBar().showMessage("%s %s" % ("folder deleted", delFolder), 0)
            self.fileModel.remove(index)
            print("%s %s" % ("folder deleted", delFolder))
        else:
            print('No clicked.')

    def deleteFile(self):
        self.copyFile()
        msg = QMessageBox.question(self, "Info", "Caution!\nReally delete this Files?\n" + '\n'.join(self.copyList),
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            print('Deletion confirmed.')
            index = self.listview.selectionModel().currentIndex()
            self.copyPath = self.fileModel.fileInfo(index).absoluteFilePath()
            print("%s %s" % ("file deleted", self.copyPath))
            self.statusBar().showMessage("%s %s" % ("file deleted", self.copyPath), 0)
            for delFile in self.listview.selectionModel().selectedIndexes():
                self.fileModel.remove(delFile)
        else:
            print('No clicked.')

    def deleteFileTrash(self):
        index = self.listview.selectionModel().currentIndex()
        self.copyFile()
        msg = QMessageBox.question(self, "Info",
                                   "Caution!\nReally move this Files to Trash\n" +
                                   '\n'.join(self.copyList),
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            print('Deletion confirmed.')
            for delFile in self.copyList:
                try:
                    send2trash(delFile)
                except OSError as e:
                    self.infobox(str(e))
                print("%s %s" % ("file moved to trash:", delFile))
                self.statusBar().showMessage("%s %s" % ("file moved to trash:", delFile), 0)
        else:
            print('No clicked.')

    def createStatusBar(self):
        sysinfo = QSysInfo()
        myMachine = "current CPU Architecture: " + sysinfo.currentCpuArchitecture() + " *** " + \
            sysinfo.prettyProductName() + " *** " + sysinfo.kernelType() + \
            " " + sysinfo.kernelVersion()
        self.statusBar().showMessage(myMachine, 0)


def mystylesheet(self):
    return """
QTreeView
{
background: #e9e9e9;
selection-color: white;
border: 1px solid lightgrey;
selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
color: #202020;
outline: 0;
} 
QTreeView::item::hover{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);
}
QTreeView::item::focus
{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
border: 0px;
}
QMenu
{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QMenu::item::selected
{
color: white;
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 lightblue, stop: 1  blue);
border: 0px;
}
QHeaderView
{
background: #d3d7cf;
color: #555753;
font-weight: bold;
}
QStatusBar
{
font-size: 8pt;
color: #555753;
}
QMenuBar
{
background: transparent;
border: 0px;
}
QToolBar
{
background: transparent;
border: 0px;
}
QMainWindow
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QLabel
{
    font-size: 10pt;
    text-align: center;
     background: transparent;
    color:#204a87;
}
QMessageBox
{
    font-size: 10pt;
    text-align: center;
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    color:#204a87;
}
QPushButton{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 grey);
border-style: solid;
border-color: darkgrey;
height: 26px;
width: 66px;
font-size: 8pt;
border-width: 1px;
border-radius: 6px;
}
QPushButton:hover:!pressed{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 lightblue, stop: 1  blue);
border-style: solid;
border-color: darkgrey;
height: 26px;
width: 66px;
border-width: 1px;
border-radius: 6px;
}
QPushButton:hover{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 lightgreen, stop: 1  green);
border-style: solid;
border-color: darkgrey;
border-width: 1px;
border-radius: 4px;
}
QToolButton
{
padding-left: 2px; padding-right: 2px;
}
    """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWindow()
    w.show()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(path)
        w.listview.setRootIndex(w.fileModel.setRootPath(path))
        w.treeview.setRootIndex(w.dirModel.setRootPath(path))
        w.setWindowTitle(path)
    sys.exit(app.exec_())
