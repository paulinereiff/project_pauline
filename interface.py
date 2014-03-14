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
		self.change_deme_size = interface.get_object("change_deme_size")
		self.deme_select = interface.get_object("deme_select")
		
		
		interface.connect_signals(self)
		self.info_refresh()

	def on_mainWindow_destroy(self, widget):
		gtk.main_quit()

	def entry_popsize_activate(self, widget):
		
		entry=widget.get_text()
		
		
		try:
			entry = int(entry)
			assert entry >= 0 and self.nb_demes == 0

		except ValueError:
			self.error_popsize.set_text("Not a number !!!")
			
		except AssertionError:
			if entry < 0:
				self.error_popsize.set_text("Negative number !!")
			else:
				self.error_popsize.set_text("incombatible with the size of the demes")
		
		else:
			self.pop_size = entry
			self.error_popsize.set_text(" ")
			self.info_refresh()
			
	def info_refresh(self):
	
		line = '-ms ' + str(self.pop_size) 
		
		if self.nb_demes > 0:
			line += ' -I '
			
			for element in self.demes_list:
				line += str(element.size) + ' '
			
			line += str(self.nb_demes)
				
		
		self.command_line.set_text(line)
		
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
		new_deme = deme.Deme()
		self.demes_list.append(new_deme)
		self.deme_select.append_text('Deme ' + str(self.nb_demes))
		self.error_demes.set_text(" ")
		self.pop_size_refresh()
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
			self.pop_size_refresh()
			self.error_demes.set_text(" ")
			self.info_refresh()
	
	def pop_size_refresh(self):
		self.pop_size = 0 
		for element in self.demes_list:
			self.pop_size += element.size
			
	def deme_select_changed(self, widget):
		chaine = 'Change the size of the deme ' + str(deme_select.get_active_text()) + ' : '
		

if __name__ == "__main__":
	Interface()
	gtk.main()