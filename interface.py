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
		self.error_demesize = interface.get_object("error_demesize")
		
		self.drawing_area = interface.get_object("drawingarea")
		
		self.drawing_area.set_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK )
		self.drawing_area.connect("expose-event", self.drawing_refresh)
        
	    
		
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
		
		""" command line refresh """
		line = '-ms ' + str(self.pop_size) 
		
		if self.nb_demes > 0:
			line += ' -I '
			
			for element in self.demes_list:
				line += str(element.size) + ' '
			
			line += str(self.nb_demes)
				
		
		self.command_line.set_text(line)
		
		""" Text refresh """
		chaine = 'Population size is ' + str(self.pop_size)
		
		
		if self.nb_demes == 0:
			chaine +=  ' and there is no deme'
			self.info.set_text(chaine)
			
		else:
			chaine += ' and there are ' + str(self.nb_demes) + ' demes.\n'
			i=0
			for element in self.demes_list:
				chaine += ' The deme ' + str(i+1) + ' has a size: ' + str(element.size) + '\n'
				i += 1
			
			self.info.set_text(chaine)
		
		
                                       
	def drawing_refresh(self,drawing_area,event):
		""" Drawing refresh """
		self.gc = self.drawing_area.window.new_gc()
		
	 	#couleur = gtk.gdk.color_parse('navajo white')
		#self.gc.background = gtk.gdk.color_parse()
		
		self.drawing_area.window.draw_rectangle(self.gc, True , 40, 20, 100, 40)
		self.drawing_area.window.draw_line(self.gc, 50, 100, 50, 300)
		self.drawing_area.window.draw_line(self.gc, 100, 100, 100, 300)
		self.drawing_area.window.draw_line(self.gc, 150, 100, 150, 300)
		self.drawing_area.window.draw_line(self.gc, 200, 100, 200, 300)
		

	def deme_plus_clicked(self, widget):
	
		self.nb_demes += 1
		new_deme = deme.Deme()
		self.demes_list.append(new_deme)
		self.deme_select.append_text(str(self.nb_demes))
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
	
	
	def entry_deme_size_activate(self, widget):
		entry=widget.get_text()
		
		try:
			entry = int(entry)
			assert entry >= 0 

		except ValueError:
			self.error_demesize.set_text("Not a number !!!")
			
		except AssertionError:
				self.error_demesize.set_text("Negative number !!")
			
		
		else:
			
			self.demes_list[int(self.deme_select.get_active_text())-1].size = entry 
			self.error_popsize.set_text(" ")
			self.pop_size_refresh()
			self.info_refresh()
		

if __name__ == "__main__":
	Interface()
	gtk.main()