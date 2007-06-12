#!/usr/bin/python
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

import locale
import gettext
import sys
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

data_path = "./"

DIR = "./locale"

gettext.bindtextdomain("pytrainer", DIR)
gtk.glade.bindtextdomain("pytrainer", DIR)
gtk.glade.textdomain("pytrainer")
gettext.textdomain("pytrainer")
gettext.install("pytrainer",DIR,unicode=1)

from pytrainer.main import pyTrainer

def main():
	try:
		filename = sys.argv[1]
		pytrainer = pyTrainer(filename, data_path)
	except:
		pytrainer = pyTrainer(None, data_path)
		
	#pytrainer.run()

if __name__ == "__main__":
        main()