#/usr/bin/env python3
# -*- coding:utf-8 -*-

# GitPy.py - программка предназначенная 
# обеспечения наглядности при использовании
# системы контроля версий git.
# Для работы необходим python3 и PyQt4

from PyQt4 import QtCore, QtGui,uic
import sys
import subprocess

codec = QtCore.QTextCodec.codecForName("utf-8")
QtCore.QTextCodec.setCodecForLocale(codec)
QtCore.QTextCodec.setCodecForCStrings(codec)
QtCore.QTextCodec.setCodecForTr(codec)

#Класс отправки комманд git
class GitDo:
	def __init__(self,parent=None):
		self.wnd = parent
			
	def doGitCommand(self,source):
		print "%s" % source
		PIPE = subprocess.PIPE
		p = subprocess.Popen("%s" % source,shell = True,stdin=PIPE,
						stdout = PIPE,
						stderr =  subprocess.STDOUT,close_fds = True)
		s = p.stdout.read()
		if self.wnd:
			self.wnd.logEdit.setText(s)
		else:
			print(s)
	def create_git(self):
		self.doGitCommand('git init')		
	
	def add_files(self):
		myfile = QtGui.QFileDialog.getOpenFileNames(self.wnd,"Выбор файлов",".")
		for st in myfile:					
			strgit = 'git add '+st.split("/")[-1]			
			self.doGitCommand(strgit)
	
	def commit_git(self):
			self.doGitCommand('git commit -m "add"')
	
	def new_branch(self):
		text,ok = QtGui.QInputDialog.getText(self.wnd,"Ввод имени","Имя ветки:")
		if ok:
			strgit="git branch "+text
			self.doGitCommand(strgit)

#Класс главного окна			
class MyWindow(QtGui.QWidget):	
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		uic.loadUi("window.ui",self)
		self.prog = GitDo(self)
		self.connect(self.quitButton,QtCore.SIGNAL("clicked()"),
					QtGui.qApp.quit)
		self.connect(self.createButton,QtCore.SIGNAL("clicked()"),
					self.prog.create_git)
		self.connect(self.addfilesButton,QtCore.SIGNAL("clicked()"),
					self.prog.add_files)
		self.connect(self.commitButton,QtCore.SIGNAL("clicked()"),
					self.prog.commit_git)
		self.connect(self.newbranchButton,QtCore.SIGNAL("clicked()"),
					self.prog.new_branch)
if __name__=="__main__":
	import sys
	app =  QtGui.QApplication(sys.argv)
	window = MyWindow()
	window.show()
	sys.exit(app.exec_())
