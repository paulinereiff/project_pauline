import pygtk
pygtk.require("2.0")
import gtk
import deme
import math

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
		self.deme_select1 = interface.get_object("deme_select1")
		self.deme_select2 = interface.get_object("deme_select2")
		self.error_demesize = interface.get_object("error_demesize")
		self.error_migration = interface.get_object("error_migration")
		
		self.deme_select.set_active(0)
		self.deme_select1.set_active(0)
		self.deme_select2.set_active(0)
		
		""" Drawing area """
		self.drawing_area = interface.get_object("drawingarea")
		self.drawing_area.connect("expose-event", self.expose)
		
		
		
	
	    
		
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
		
		""" Drawing refresh """
		self.drawing_refresh()
	

		
	def expose(self, widget, event):
		
		cr = self.drawing_area.window.cairo_create()
		
		""""white background"""
		cr.set_source_rgb(1, 1, 1)
		cr.paint()
		
		self.draw_tree(self.nb_demes)
	
		
		
		
		
	def draw_tree_2(self):
		cr = self.drawing_area.window.cairo_create()
		
		cr.set_source_rgb(1, 1, 1)
		cr.paint()
		
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
		
		cr.set_line_width(5)
		cr.set_source_rgb(0.7, 0.2, 0.0)
		
		""" branche 1"""
		cr.translate((w/2)-(w/8), 0) 
		cr.move_to(0, 0) 
		cr.line_to(0, (h/2) )
		cr.move_to(0, (h/2) )
		cr.curve_to((-w/8)+50, (3*h/4)+50, (-w/8)+50, (3*h/4)+50, -w/4, h)
		cr.stroke_preserve()
	
		""" branche 2"""
		cr.translate(w/4, 0)
		cr.move_to(0, 0) 
		cr.line_to(0, (h/2) )
		cr.move_to(0, (h/2) )
		cr.curve_to((-w/8)+50, (3*h/4)+50, (-w/8)+50, (3*h/4)+50, w/4, h)
		cr.stroke_preserve()
		
		""" relier les extremites """
		cr.move_to(w/4,h)
		cr.line_to(-w/2,h)
		cr.move_to(0,0)
		cr.line_to(-w/4,0)
		cr.stroke_preserve()
		
		
	
	def draw_tree(self, param):
		
		
		cr = self.drawing_area.window.cairo_create()
		
		
		cr.set_source_rgb(1, 1, 1)
		cr.paint()
		
		
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
		
		if param > 0:
			i=0
			while i < param:
				cr.save()
				cr.set_line_width(5)
				""" choix de la couleur"""
				
				if self.demes_list[i].select:
					cr.set_source_rgb(0.7, 0.2, 0)
				else:
					cr.set_source_rgb(0, 0, 0)
				
				cr.translate((w*((2*i)+1))/(2*param)-(w/(param*8)), h/10) 
				cr.move_to(0, 0) 
				cr.line_to(0, (4*h/5) )
				cr.line_to(w/(4*param), (4*h/5))
				
				"""Texte"""
				cr.move_to(0,(4*h/5)+(h/20))
				cr.show_text('id= ') 
				cr.show_text(str(i+1)) #Text : id of the Deme
				
				cr.stroke()
		
		
				cr.translate(w/(4*param), 0)
				cr.move_to(0, 0) 
				cr.line_to(-w/(4*param),0)
				cr.move_to(0, 0) 
				cr.line_to(0, (4*h/5) )
				cr.stroke()
				
				
				
				cr.restore()
				i+=1
				
                                       
	def drawing_refresh(self):
		self.draw_tree(self.nb_demes)
		

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
			self.deme_select.remove_text(self.nb_demes)
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
			#print str(self.deme_select.get_active_text()-1)
			self.demes_list[int(self.deme_select.get_active_text())-1].size = entry 
			self.error_popsize.set_text(" ")
			self.pop_size_refresh()
			self.info_refresh()
		
	def on_deme_select_changed(self, widget):
		i=0
		while i < self.nb_demes:
			self.demes_list[i].select = False
			i +=1
			
		#print str(self.deme_select.get_active())
		if self.deme_select.get_active() is not 0:
			self.demes_list[int(self.deme_select.get_active_text())-1].select = True
		
		self.drawing_refresh()
		
	def on_deme_select1_changed(self, widget):
		
		self.error_migration.set_text(" ")
		i=0
		while i < self.nb_demes:
			self.demes_list[i].select = False
			i +=1
		
		#print str(self.deme_select.get_active())
		if self.deme_select1.get_active() is not 0:
			self.demes_list[int(self.deme_select1.get_active_text())-1].select = True
	
		if self.deme_select2.get_active() is not 0:
			self.demes_list[int(self.deme_select2.get_active_text())-1].select = True
	
		self.drawing_refresh()
		
	def button_migration_clicked(self, widget):
		try:
			assert self.deme_select1.get_active() is not 0
			assert self.deme_select2.get_active() is not 0
		
		except AssertionError:
			self.error_migration.set_text("Not enough deme selected")
			
		else:
			self.error_migration.set_text(" ")
			
			if self.deme_select1.get_active() is self.deme_select2.get_active():
				self.error_migration.set_text("The same deme is selected")
			else:
				self.error_migration.set_text(" ")

if __name__ == "__main__":
	Interface()
	gtk.main()