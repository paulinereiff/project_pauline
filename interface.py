import pygtk
pygtk.require("2.0")
import gtk
import deme
import math
import cairo

class Interface:
	def __init__(self):
		interface = gtk.Builder()
		interface.add_from_file('interface.glade')
		
		self.pop_size=0
		self.nb_migration=0
		self.nb_join=0
		self.demes_list=list()
		
		
		self.error_popsize = interface.get_object("error_popsize")
		self.info = interface.get_object("info")
		self.error_demes = interface.get_object("error_demes")
		self.command_line = interface.get_object("command_line")
		self.change_deme_size = interface.get_object("change_deme_size")
		self.deme_select = interface.get_object("deme_select")
		self.deme_select_migration1 = interface.get_object("deme_select_migration1")
		self.deme_select_migration2 = interface.get_object("deme_select_migration2")
		self.error_demesize = interface.get_object("error_demesize")
		self.error_migration = interface.get_object("error_migration")
		self.error_join = interface.get_object("error_join")
		self.deme_select_join1 = interface.get_object("deme_select_join1")
		self.deme_select_join2 = interface.get_object("deme_select_join2")
		
		self.deme_select.set_active(0)
		self.deme_select_migration1.set_active(0)
		self.deme_select_migration2.set_active(0)
		self.deme_select_join1.set_active(0)
		self.deme_select_join2.set_active(0)
		
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
			assert entry >= 0 and len(self.demes_list) == 0

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
		
		if len(self.demes_list) > 0:
			line += ' -I '
			
			for element in self.demes_list:
				line += str(element.size) + ' '
			
			line += str(len(self.demes_list))
				
		
		self.command_line.set_text(line)
		
		""" Text refresh """
		chaine = 'Population size is ' + str(self.pop_size)
		
		
		if len(self.demes_list) == 0:
			chaine +=  ' and there is no deme'
			self.info.set_text(chaine)
			
		else:
			chaine += ' and there are ' + str(len(self.demes_list)) + ' demes.\n'
			i=0
			for element in self.demes_list:
				chaine += ' The deme ' + str(self.demes_list[i].id) + ' has a size: ' + str(element.size) + '\n'
				i += 1
			
			self.info.set_text(chaine)
		
		
	

		
	def expose(self, widget, event):
		
		cr = self.drawing_area.window.cairo_create()
		
		""""white background"""
		cr.set_source_rgb(1, 1, 1)
		cr.paint()
		
		self.draw_tree()
		

		
		
		
		
		
		
	def draw_migration(self):
		
		cr = self.drawing_area.window.cairo_create()

		
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
		
		cr.set_source_rgb(0, 0, 1)
		
		n_arrow=0
		
		i=0
		while i < len(self.demes_list):
			if len(self.demes_list[i].migrate_to) is not 0:
				
				j=0
				
				while j < len(self.demes_list[i].migrate_to):
					cr.save()
					cr.translate(0, (n_arrow+1)*h/(self.nb_migration + 1))
					cr.move_to((w*((2*i)+1))/(2*len(self.demes_list)), 0)
					cr.line_to((w*((2*(self.demes_list[i].migrate_to[j]-1))+1))/(2*len(self.demes_list)), 0 )
					cr.translate((w*((2*(self.demes_list[i].migrate_to[j]-1))+1))/(2*len(self.demes_list)),0)
					cr.arc(0, 0, h/50, 0, 2*math.pi)
					cr.stroke()
					
					n_arrow +=1
					j+= 1
					cr.restore()
		
			i += 1	
		
	def select_color(self, cr, index_deme):
		if self.demes_list[index_deme].select:
			cr.set_source_rgb(0.7, 0.2, 0)
		else:
			cr.set_source_rgb(0, 0, 0)
				
	def draw_tree(self):
		
		param = len(self.demes_list)
		cr = self.drawing_area.window.cairo_create()
		
		
		cr.set_source_rgb(1, 1, 1)
		cr.paint()
		
		
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
		
		if param > 0:
			nb_arrow=0
			for i in range(0, param):
				cr.save()
				cr.set_line_width(5)
				
				""" choix de la couleur"""
				self.select_color(cr, i)
				
			
				""""Dessin rectangle"""
				if len(self.demes_list[i].join_to) is 0: 
					cr.rectangle((w*((2*i)+1))/(2*param)-(w/(param*8)), h/10, w/(param*4), 4*h/5)
					cr.stroke()
				else:
					
					cr.rectangle((w*((2*i)+1))/(2*param)-(w/(param*8)), h*(nb_arrow+1)/(self.nb_join+1), w/(param*4), (9*h/10)-(h*(nb_arrow+1)/(self.nb_join+1)))
					cr.stroke()
					cr.move_to((w*((2*i)+1))/(2*param)-(w/(param*8)),h*(nb_arrow+1)/(self.nb_join+1))
					cr.set_source_rgb(0, 0, 0)
					""" dessin join """
					for k in range(0, len(self.demes_list[i].join_to)):
						cr.save()
						cr.move_to((w*((2*i)+1))/(2*param)-(w/(param*8)),h*(nb_arrow+1)/(self.nb_join+1) + 0.01*h*k)
						for j in range(0, len(self.demes_list)):
							if self.demes_list[j].id == self.demes_list[i].join_to[k]:
								cr.line_to((w*((2*j)+1))/(2*param)-(w/(param*8)),h*(nb_arrow+1)/(self.nb_join+1) + 0.01*h*k)
								cr.arc((w*((2*j)+1))/(2*param)-(w/(param*8)), h*(nb_arrow+1)/(self.nb_join+1) + 0.01*h*k, h/50, 0, 2*math.pi)
								cr.stroke()
						cr.restore()
				
					
					
					nb_arrow += 1
					
				
				cr.restore()
	
	def draw_text(self):
		cr = self.drawing_area.window.cairo_create()

		
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
		
		cr.set_source_rgb(0, 0, 1)
		
		for i in range(0, len(self.demes_list)):
			cr.save()
			cr.translate(w*((2*i)+1)/(2*len(self.demes_list))-(w/(len(self.demes_list)*8)), 19*h/20)
			cr.move_to(0,0)
			cr.show_text('id= ') 
			cr.show_text(str(self.demes_list[i].id)) #Text : id of the Deme
			cr.restore()
	
	def deme_of_id(self, index):
		for k in range(0, len(self.demes_list)):
			if self.demes_list[k].id == index:
				return self.demes_list[k] 			
	
	def order_demes_list(self):
		self.demes_list.sort(self.comp)
	
	def comp(self, a, b):
		if len(a.join_to) < len(b.join_to):
			return -1
		
		elif len(a.join_to) > len(b.join_to):
			return 1
		
		else:
			return 0
                                       
	def drawing_refresh(self):
		self.order_demes_list()
		self.draw_tree()
		self.draw_migration()
		self.draw_text()
		
		

	def deme_plus_clicked(self, widget):
	
		
		new_deme = deme.Deme(len(self.demes_list)+1)
		self.demes_list.append(new_deme)
		self.deme_select.append_text(str(len(self.demes_list)))
		self.error_demes.set_text(" ")
		self.pop_size_refresh()
		self.info_refresh()
		self.drawing_refresh()
			
		
	def deme_minus_clicked(self, widget):
	
		
		try :
			del self.demes_list[len(self.demes_list)-1]
			
		except IndexError:
			self.error_demes.set_text("Negative number !!")
			
		else:
			self.deme_select.remove_text(len(self.demes_list)+1)
			self.pop_size_refresh()
			self.error_demes.set_text(" ")
			
			i=0	
			while i < len(self.demes_list):
				j=0
				while j < len(self.demes_list[i].migrate_to):
					if self.demes_list[i].migrate_to[j] >= len(self.demes_list):
						self.demes_list[i].migrate_to.remove(self.demes_list[i].migrate_to[j])	
					j+=1
				i+=1
				
			self.info_refresh()
			self.drawing_refresh()
		
	def button_delete_migrations_clicked(self, widget):
		
		i=0	
		while i < len(self.demes_list):
			j=0
			len_migrate_to = len(self.demes_list[i].migrate_to)
			while j < len_migrate_to:
				self.demes_list[i].migrate_to.remove(self.demes_list[i].migrate_to[j-1])	
				j+=1
			i+=1
		self.info_refresh()
		self.drawing_refresh()
		self.nb_migration=0
		
	
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
		
	def on_deme_select_changed(self, widget):
		i=0
		while i < len(self.demes_list):
			self.demes_list[i].select = False
			i +=1
			
	
		if self.deme_select.get_active() is not 0:
				for i in range(0, len(self.demes_list)):
					if self.demes_list[i].id == self.deme_select.get_active():
						self.demes_list[i].select = True 
			
			
		
		
		self.drawing_refresh()
		
	def on_deme_select_migration_changed(self, widget):
		
		self.error_migration.set_text(" ")
		i=0
		while i < len(self.demes_list):
			self.demes_list[i].select = False
			i +=1
		

		if self.deme_select_migration1.get_active() is not 0:
			for i in range(0, len(self.demes_list)):
					if self.demes_list[i].id == self.deme_select_migration1.get_active():
						self.demes_list[i].select = True 
	
		if self.deme_select_migration2.get_active() is not 0:
			for i in range(0, len(self.demes_list)):
					if self.demes_list[i].id == self.deme_select_migration2.get_active():
						self.demes_list[i].select = True 
	
		self.drawing_refresh()
		
	def button_migration_clicked(self, widget):
		try:
			assert self.deme_select_migration1.get_active() is not 0
			assert self.deme_select_migration2.get_active() is not 0
		
		except AssertionError:
			self.error_migration.set_text("Not enough deme selected")
			
		else:
			self.error_migration.set_text(" ")
			
			i=0
			try:
				for j in range(0, len(self.demes_list)):
					if self.demes_list[j].id == int(self.deme_select_migration1.get_active()):
						for i in range(0, len(self.demes_list[j].migrate_to)):	
							assert self.demes_list[j].migrate_to[i] is not self.deme_select_migration2.get_active()	 
					
			except AssertionError:
				self.error_migration.set_text("This migration already exists")
			
			else:
			
				if self.deme_select_migration1.get_active() is self.deme_select_migration2.get_active():
					self.error_migration.set_text("The same deme is selected")
				
				else:
					self.error_migration.set_text(" ")
					for j in range(0, len(self.demes_list)):
						if self.demes_list[j].id == int(self.deme_select_migration1.get_active()):
							self.demes_list[j].migrate_to.append(self.deme_select_migration2.get_active())
					self.nb_migration += 1
					self.drawing_refresh()
		
	def on_deme_select_join_changed(self, widget):
	
		self.error_join.set_text(" ")
		i=0
		while i < len(self.demes_list):
			self.demes_list[i].select = False
			i +=1
	

		if self.deme_select_join1.get_active() is not 0:
			for i in range(0, len(self.demes_list)):
					if self.demes_list[i].id == self.deme_select_join1.get_active():
						self.demes_list[i].select = True 
			

		if self.deme_select_join2.get_active() is not 0:
			for i in range(0, len(self.demes_list)):
					if self.demes_list[i].id == self.deme_select_join2.get_active():
						self.demes_list[i].select = True 

		self.drawing_refresh()
		
	def button_join_clicked(self, widget):
		try:
			assert self.deme_select_join1.get_active() is not 0
			assert self.deme_select_join2.get_active() is not 0
		
		except AssertionError:
			self.error_join.set_text("Not enough deme selected")
			
		else:
			self.error_join.set_text(" ")
			
			
			try:
				for j in range(0, len(self.demes_list)):
					if self.demes_list[j].id == int(self.deme_select_join1.get_active()):
						for i in range(0, len(self.demes_list[j].join_to)):	
							assert self.demes_list[j].join_to[i] is not self.deme_select_join2.get_active()	 
							
					
			except AssertionError:
				self.error_join.set_text("This demes are already joined")
				
			else:
			
				if self.deme_select_join1.get_active() is self.deme_select_join2.get_active():
					self.error_join.set_text("The same deme is selected")
				
				else:
					self.error_join.set_text(" ")
					for j in range(0, len(self.demes_list)):
						if self.demes_list[j].id == int(self.deme_select_join1.get_active()):
							self.demes_list[j].join_to.append(self.deme_select_join2.get_active())
						if self.demes_list[j].id == int(self.deme_select_join2.get_active()):
							self.demes_list[j].is_joined_by.append(self.deme_select_join1.get_active())
					
					self.nb_join += 1
					self.drawing_refresh()
			
			

if __name__ == "__main__":
	Interface()
	gtk.main()