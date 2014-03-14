import pygtk
pygtk.require("2.0")
import gtk
import deme


class Interface:
	def __init__(self):
		interface = gtk.Builder()
		interface.add_from_file('interface.glade')
		
		self.pop_size=0
		self.nb_demes=0
		self.demes_list=list()
		
		
		self.error_popsize = interface.get_object("error_popsize")
		self.info = interface.get_object("info")
		self.error_demes = interface.get_object("error_demes")
		self.command_line = interface.get_object("command_line")
		
		interface.connect_signals(self)
		self.info_refresh()

	def on_mainWindow_destroy(self, widget):
		gtk.main_quit()

	def entry_popsize_activate(self, widget):
		
		entry=widget.get_text()
		
		
		try:
			entry = int(entry)
			assert entry >= 0

		except ValueError:
			self.error_popsize.set_text("Not a number !!!")
			
		except AssertionError:
			self.error_popsize.set_text("Negative number !!")
		
		else:
			self.pop_size = entry
			print self.pop_size
			self.info_refresh()
			
	def info_refresh(self):
	
		self.command_line.set_text('-ms ' + str(self.pop_size) + ' -I ' + str(self.nb_demes))
		
		chaine = 'Population size is ' + str(self.pop_size)
		
		if self.nb_demes == 1:
			chaine +=  'and there is ' + str(self.nb_demes) + ' deme. This deme has a size: ' + str(self.demes_list[0].size)
			self.info.set_text(chaine)
		
		elif self.nb_demes == 0:
			chaine +=  ' and there is no deme'
			self.info.set_text(chaine)
			
		else:
			chaine += ' and there are ' + str(self.nb_demes) + ' demes.\n'
			i=0
			for element in self.demes_list:
				chaine += ' The deme ' + str(i) + ' has a size: ' + str(element.size) + '\n'
				i += 1
			
			self.info.set_text(chaine)
		
	def deme_plus_clicked(self, widget):
	
		self.nb_demes += 1
		new_deme = deme.Deme(self.pop_size)
		self.demes_list.append(new_deme)
		self.info_refresh()
		
	def deme_minus_clicked(self, widget):
	
		self.nb_demes -= 1
		
		try :
			assert self.nb_demes >= 0
			
		except AssertionError:
			self.error_demes.set_text("Negative number !!")
			self.nb_demes += 1
			
		else:
			del self.demes_list[self.nb_demes-1]
			self.info_refresh()
			
		

if __name__ == "__main__":
	Interface()
	gtk.main()