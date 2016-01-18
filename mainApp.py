#!/usr/bin/python3

import os
import sys
import xml.etree.ElementTree as ET
from urllib import parse

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QWidget, QApplication,
                             QGroupBox, QHBoxLayout,
                             QVBoxLayout, QListWidget, QTreeView)

from CustomWidgets import DropArea
from xmltodict import XmlDictConfig


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.currentDict = {}
        self.initUI()

    def updateTree(self, data):
        print(data)
        # self.contents.show()

    def initUI(self):
        hLayout = QHBoxLayout()

        self.verticalGroupBox = QGroupBox()
        vLayout = QVBoxLayout()

        self.dropArea = DropArea("<drop here>", self)
        vLayout.addWidget(self.dropArea)

        self.dataList = QListWidget()
        vLayout.addWidget(self.dataList)

        self.verticalGroupBox.setLayout(vLayout)
        hLayout.addWidget(self.verticalGroupBox)

        self.contents = QTreeView()
        hLayout.addWidget(self.contents)

        self.setLayout(hLayout)
        self.setWindowTitle('Simplify3d to CSV')
        self.setGeometry(300, 300, 300, 150)

        self.dropArea.dropped.connect(self.onFileDropped)

    def onFileDropped(self, filename):
        filename = parse.unquote(filename)
        if filename.startswith('file:/'):
            filename = filename[6:]
        print(filename)
        if os.path.isfile(filename) is not True:
            return

        tree = ET.parse(filename)
        root = tree.getroot()
        self.currentDict = XmlDictConfig(root)
        '''
        QList<QStandardItem *> preparedRow =prepareRow("first", "second", "third");
        QStandardItem *item = standardModel->invisibleRootItem();
        // adding a row to the invisible root item produces a root element
        item->appendRow(preparedRow);

        QList<QStandardItem *> secondRow =prepareRow("111", "222", "333");
        // adding a row to an item starts a subtree
        preparedRow.first()->appendRow(secondRow);

        treeView->setModel(standardModel);
        treeView->expandAll();
        '''
        standardModel = QStandardItemModel()
        preparedRow = (QStandardItem("Title"), QStandardItem("Description"))
        item = standardModel.invisibleRootItem()
        item.appendRow(preparedRow)
        self.addDictTree(self.currentDict, item)
        self.contents.setModel(standardModel)
        self.contents.expandAll()

        print("dict reading finished")

    def addDictTree(self, data, item):
        for k,v in data.items():
            if isinstance(v, dict):
                childItem = QStandardItem(k)
                item.appendRow(childItem)
                self.addDictTree(v, childItem)
            else:
                try:
                    print(k+":"+v)
                    item.appendRow((QStandardItem(k), QStandardItem(v)))
                except:
                    print('Item adding failed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()
