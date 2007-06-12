# -*- coding: iso-8859-1 -*-

#Copyright (C) Fiz Vazquez vud1@sindominio.net

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import os

from lib.xmlUtils import XMLParser
from lib.system import checkConf

from gui.windowextensions import WindowExtensions

class Extension:
	def __init__(self, data_path = None):
		self.data_path=data_path
		self.conf = checkConf()
	
	def getActiveExtensions(self):
		retorno = []
		for extension in self.getExtensionList():
			if self.getExtensionInfo(extension[0])[2] == "1":
				retorno.append(extension[0])
		return retorno	
	
	def manageExtensions(self):
		ExtensionList = self.getExtensionList()
		windowextension = WindowExtensions(self.data_path, self)
		windowextension.setList(ExtensionList)
		windowextension.run()

	def getExtensionList(self):
		extensiondir = self.data_path+"/extensions"
		extensionList = []
		for extension in os.listdir(extensiondir):
			extensionxmlfile = extensiondir+"/"+extension+"/conf.xml"
			if os.path.isfile(extensionxmlfile):
				extensioninfo = XMLParser(extensionxmlfile)
				name = extensioninfo.getValue("pytrainer-extension","name")
				description = extensioninfo.getValue("pytrainer-extension","description")
				extensionList.append((extensiondir+"/"+extension,name,description))
	
		return extensionList
	
	def getExtensionInfo(self,pathExtension):
		info = XMLParser(pathExtension+"/conf.xml")
		name = info.getValue("pytrainer-extension","name")
		description = info.getValue("pytrainer-extension","description")
		code = info.getValue("pytrainer-extension","extensioncode")
		extensiondir = self.conf.getValue("extensiondir")
		helpfile = pathExtension+"/"+info.getValue("pytrainer-extension","helpfile")
		type = info.getValue("pytrainer-extension","type")
		if not os.path.isfile(extensiondir+"/"+code+"/conf.xml"):
			status = 0
		else:
			info = XMLParser(extensiondir+"/"+code+"/conf.xml")
			status = info.getValue("pytrainer-extension","status")
		return name,description,status,helpfile,type

	def getExtensionConfParams(self,pathExtension):
		info = XMLParser(pathExtension+"/conf.xml")
		code = info.getValue("pytrainer-extension","extensioncode")
		extensiondir = self.conf.getValue("extensiondir")
		if not os.path.isfile(extensiondir+"/"+code+"/conf.xml"):
			params = info.getAllValues("conf-values")
			params.append(("status","0"))
		else:
			prefs = info.getAllValues("conf-values")
			prefs.append(("status","0"))
			info = XMLParser(extensiondir+"/"+code+"/conf.xml")
			params = []
			for pref in prefs:
				params.append((pref[0],info.getValue("pytrainer-extension",pref[0])))
		return params

	def setExtensionConfParams(self,pathExtension,savedOptions):
		info = XMLParser(pathExtension+"/conf.xml")
		code = info.getValue("pytrainer-extension","extensioncode")
		extensiondir = self.conf.getValue("extensiondir")+"/"+code
		if not os.path.isdir(extensiondir):
			os.mkdir(extensiondir)
		if not os.path.isfile(extensiondir+"/conf.xml"):
			savedOptions.append(("status","0"))
		info = XMLParser(extensiondir+"/conf.xml")
		info.createXMLFile("pytrainer-extension",savedOptions)

	def loadExtension(self,pathExtension):
		print "Loading extension: %s" %pathExtension
		confParams = self.getExtensionConfParams(pathExtension)
		extension = __init__(pathExtension+"/main.py")
		object = extension.main(confParams)
		object.run()

	def getCodeConfValue(self,code,value):
		extensiondir = self.conf.getValue("extensiondir")
		info = XMLParser(extensiondir+"/"+code+"/conf.xml")
		return info.getValue("pytrainer-extension",value)