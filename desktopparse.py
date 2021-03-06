#
# Static class to parse .desktop file for getting icon, title and exec strings
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
# 

from PyQt5.QtCore import QTextStream
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMessageBox

class DesktopParse:
    @staticmethod
    def extinFn(fn,exts):
        for ext in exts:
            if fn.endswith(ext):
                return True
        return False
    
    '''
    @staticmethod
    def getIconFromName(iconname):
        """Статическая функция для нахождения полного имени файла иконки по его имени.
            функция ищет в каталогах жёстко заданных в функции.
            Если файл не найден, фунция вернён входящее имя"""
        home = QDir.homePath()
        icondirs = [home+"/.local/share/icons/hicolor/48x48/apps/",
                          home+"/.local/share/icons/hicolor/64x64/apps/",
                          "/usr/share/icons/hicolor/48x48/apps/",
                          "/usr/share/icons/gnome/48x48/apps/",
                          "/usr/share/app-install/icons/",
                          "/usr/share/icons/hicolor/scalable/apps/",
                          "/usr/share/icons/HighContrast/48x48/apps/"]
        exts = [".png",".jpg",".jpeg",".bmp",".ico",".svg"]  
        
        if DesktopParse.extinFn(iconname,exts):
            for dir in icondirs:
                if QFile.exists(dir+iconname):
                    return dir+iconname
        else:
            for dir in icondirs:
                for ext in exts:
                    if QFile.exists(dir+iconname+ext):
                        return dir+iconname+ext
        return iconname    
    '''
    
    @staticmethod
    def parse(parent,path,lang = "[ru]"):
        """Статическая функция для парсинга файла с расширением .desktop
           для получения названия, исполняемой строки, и имя иконки.
           в качестве первого входящего параметра используется ссылка на родителя, 
           т.е. на MainWindow для вызова QMessageBox, в качество второго параметра
           имя файла, и третий не обязательный это код языка в кв. скобках.
           После того как будет получено имя иконки проверяем, существует ли этот файл,
           если нет, то пытаемся найти имя файла функцией getIconFromName.
           Опять проверяем на существование полученного результата, если не существуют
           то возвращаем путь к иконке "зашитой" в ресурсы :/images/icon.png.
        """
        file = QFile(path)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.information(parent,"Не могу открыть файл",path)
            return "","",""
        title = ""
        icon = ""
        exec = ""
        firstline = True
        if path.endswith(".desktop"):
            stream = QTextStream(file)
            while not stream.atEnd():
                line = stream.readLine()
                if len(line)>1:
                    if firstline:
                        if line == "[Desktop Entry]":
                            firstline = False
                    else:
                        if line.startswith("["): break
                        if line.startswith("Icon="):
                            icon = line[-len(line)+5:]
                        if line.startswith("Name"+lang+"="):
                            title = line[-len(line)+9:]
                        if line.startswith("Name=") and title == "":
                            title = line[-len(line)+5:]
                        if line.startswith("Exec="):
                            exec = line[-len(line)+5:]
        file.close()
        #if icon != "":
        #    if not QFile.exists(icon):
        #        icon = DesktopParse.getIconFromName(icon)
        #        if not QFile.exists(icon):
        #            icon = ":/images/icon.png"
        #else:
        #    if title != "" and exec != "": icon = ":/images/icon.png"
        return title,icon, exec
                            
