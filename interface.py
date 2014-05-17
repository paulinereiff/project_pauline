import pygtk
pygtk.require("2.0")
import gtk
import deme
import migration
import junction
import math
import cairo

class Interface:
	def __init__(self):
		interface = gtk.Builder()
		interface.add_from_file('interface.glade')
		
		self.pop_size=0
		self.migration_list=list()
		self.junction_list = list()
		self.nb_join=0
		self.demes_list=list()
		self.deme_select_list=list()
		
		
		self.error_popsize = interface.get_object("error_popsize")
		self.info = interface.get_object("info")
		self.error_demes = interface.get_object("error_demes")
		self.command_line = interface.get_object("command_line")
		self.change_deme_size = interface.get_object("change_deme_size")
		
		self.error_demesize = interface.get_object("error_demesize")
		self.error_migration = interface.get_object("error_migration")
		self.error_join = interface.get_object("error_join")
		
		
		self.entry_amount = interface.get_object("entry_amount")
		self.entry_amount2 = interface.get_object("entry_amount2")
		
		
		self.select_selectable = interface.get_object("select_selectable")
		self.info_select = interface.get_object("info_select")
		self.label_deme = interface.get_object("label_deme")
		self.label_deme1 = interface.get_object("label_deme1")
		self.label_deme2 = interface.get_object("label_deme2")

		
		self.select_selectable.set_active(0)
		
		""" Drawing area """
		self.drawing_area = interface.get_object("drawingarea")
		self.drawing_area.connect("expose-event", self.expose)
		
		self.drawing_area.connect("button_press_event", self.button_press_event)
		self.drawing_area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		
	
		
		
		
	
	    
		
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
			
		if len(self.migration_list) > 0:
			
			
			for i in range(0, len(self.migration_list)):
				line += ' -m '
				line += str(self.migration_list[i].fro.id) + ' ' + str(self.migration_list[i].to.id)
				line += ' 1 '
		
		if len(self.junction_list) > 0:
			
			
			for i in range(0, len(self.junction_list)):
				line += ' -ej '
				line += ' t '
				line += str(self.junction_list[i].fro.id) + ' ' + str(self.junction_list[i].to.id)
				
				
		
		self.command_line.set_text(line)
		
		""" Text refresh """
		chaine = 'Population size is ' + str(self.pop_size)
		
		
		if len(self.demes_list) == 0:
			chaine +=  ' and there is no deme \n \n'
			
			
		else:
			chaine += ' and there are ' + str(len(self.demes_list)) + ' demes.\n \n'
			i=0
			for element in self.demes_list:
				chaine += ' The deme ' + str(self.demes_list[i].id) + ' has a size: ' + str(element.size) + '\n \n'
				i += 1
			
		if len(self.migration_list) == 0:
			chaine += 'There is no migration. \n'
			
		else:
			chaine += 'There are ' + str(len(self.migration_list)) + ' migrations.\n \n'
			for i in range(0, len(self.migration_list)):
 				chaine += 'There is a migration from the deme '+ str(self.migration_list[i].fro.id) + ' to the deme '+ str(self.migration_list[i].to.id) + ' \n with an amount of '+str(self.migration_list[i].amount) + '. \n\n'
		
		if len(self.junction_list) == 0:
			chaine += 'There is no junctions. \n'
			
		else:
			chaine += 'There are ' + str(len(self.junction_list)) + ' junctions.\n \n'
			for i in range(0, len(self.junction_list)):
 				chaine += 'The deme '+ str(self.junction_list[i].fro.id) + ' is joined to the deme '+ str(self.junction_list[i].to.id) + ' \n with an amount of '+str(self.junction_list[i].amount) + '. \n\n'
				
		self.info.set_text(chaine)
		
		""" Selection refresh """
		chaine2=''
		
		
		
			
		for i in range(0, len(self.demes_list)):
			if self.demes_list[i].select:
				chaine2 += 'You have selected the Deme '
				chaine2 += str(self.demes_list[i].id) + '\n'
				
		for i in range(0, len(self.migration_list)):
			if self.migration_list[i].select:
				chaine2 += 'You have selected the Migration from '
				chaine2 += str(self.migration_list[i].fro.id) + ' to ' + str(self.migration_list[i].to.id) + '. \n'
					

		
		self.info_select.set_text(chaine2)
		
		if len(self.deme_select_list)>=2:
			self.label_deme1.set_text('Deme ' + str(self.deme_select_list[0].id))
			self.label_deme2.set_text('Deme ' + str(self.deme_select_list[1].id))

		if len(self.deme_select_list)>=1:
			self.label_deme.set_text('Deme ' + str(self.deme_select_list[0].id))
		else:
			self.label_deme1.set_text('')
			self.label_deme2.set_text('')

		

		
	def expose(self, widget, event):
		
		cr = self.drawing_area.window.cairo_create()
		
		""""white background"""
		cr.set_source_rgb(1, 1, 1)
		cr.paint()
		
		
		
	def draw_triangle(self,cr,right):
		
		
		
		if right:
			cr.move_to(0,0)
			cr.line_to(-20, -15)
			cr.line_to(-20, 15)
			cr.line_to(0,0)
			cr.stroke()
		
		else:
			cr.move_to(0,0)
			cr.line_to(20, -15)
			cr.line_to(20, 15)
			cr.line_to(0,0)
			cr.stroke()
		
		
	def draw_migration(self):
		
		cr = self.drawing_area.window.cairo_create()

	
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
	
		cr.set_source_rgb(0, 0, 1)
	
		n_arrow=0
	
	
		for i in range(0, len(self.migration_list)):
			self.select_color_migration(cr, i)
			start=self.demes_list.index(self.deme_of_id(self.migration_list[i].fro.id))
			#end=self.migration_list[i].to.id
			end=self.demes_list.index(self.deme_of_id(self.migration_list[i].to.id))
			cr.save()
			cr.translate(0, (n_arrow+1)*h/(len(self.migration_list) + 1))
			cr.move_to((w*((2*start)+1))/(2*len(self.demes_list)), 0)
			cr.line_to((w*((2*(end))+1))/(2*len(self.demes_list)), 0 )
			cr.translate((w*((2*(end))+1))/(2*len(self.demes_list)), 0)
			
			if (w*((2*start)+1))/(2*len(self.demes_list)) < (w*((2*(end))+1))/(2*len(self.demes_list)):
				right = True
			else:
				right = False
		
			self.draw_triangle(cr, right)

			cr.stroke()
				
			n_arrow +=1
				
			cr.restore()
		
				
		
	def select_color(self, cr, index_deme):
		if self.demes_list[index_deme].select:
			cr.set_source_rgb(0.7, 0.2, 0)
		else:
			cr.set_source_rgb(0, 0, 0)
			
	def select_color_migration(self, cr, index_mig):
		if self.migration_list[index_mig].select:
			cr.set_source_rgb(1, 0, 1)
		else:
			cr.set_source_rgb(0, 0, 1)
			
	def select_color_junction(self, cr, index):
		if self.junction_list[index].select:
			cr.set_source_rgb(0.8, 0.5, 0)
		
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
				
				
			""" dessin join """
					
					
			
					
			for i in range(0, len(self.junction_list)):
				self.select_color_junction(cr, i)
				start=self.demes_list.index(self.deme_of_id(self.junction_list[i].fro.id)) #index dans la deme_list du deme de depart	
				end=self.demes_list.index(self.deme_of_id(self.junction_list[i].to.id))
				cr.save()
				cr.translate(0, (nb_arrow+1)*h/(len(self.junction_list) + 1))
				cr.move_to((w*((2*start)+1))/(2*len(self.demes_list)), 0)
				cr.line_to((w*((2*(end))+1))/(2*len(self.demes_list)), 0 )
				cr.translate((w*((2*(end))+1))/(2*len(self.demes_list)), 0)
	
				if (w*((2*start)+1))/(2*len(self.demes_list)) < (w*((2*(end))+1))/(2*len(self.demes_list)):
					right = True
				else:
					right = False
		

				self.draw_triangle(cr, right)

				cr.stroke()
			
				
			
				cr.restore()
			
			
				nb_arrow += 1
					
				
				cr.restore()
	
	def draw_text(self):
		cr = self.drawing_area.window.cairo_create()

		
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
		
		cr.set_source_rgb(0, 0, 0)
		
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
		self.info_refresh()
		self.draw_tree()
		self.draw_migration()
		self.draw_text()
		
		

	def deme_plus_clicked(self, widget):
	
		
		new_deme = deme.Deme(len(self.demes_list)+1)
		self.demes_list.append(new_deme)
		self.error_demes.set_text(" ")
		self.pop_size_refresh()
		self.drawing_refresh()
			
		
	def deme_minus_clicked(self, widget):
	
		
		try :
			del self.demes_list[len(self.demes_list)-1]
			
		except IndexError:
			self.error_demes.set_text("Negative number !!")
			
		else:
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
			
			self.pop_size_refresh()	
			self.drawing_refresh()
		
	def button_delete_junctions_clicked(self, widget):
		
		i=0	
		while i < len(self.demes_list):
			self.demes_list[i].join_to = []
			self.demes_list[i].is_joined_by = []
			i+=1
		
		self.nb_join=0
		self.junction_list = []
		self.drawing_refresh()
		
	
	def button_delete_migrations_clicked(self, widget):
		
		i=0	
		while i < len(self.demes_list):
			self.demes_list[i].migrato_to = []
			i+=1
		
		self.migration_list=[]
		self.drawing_refresh()
			
		
	
	def pop_size_refresh(self):
		self.pop_size = 0 
		for element in self.demes_list:
			self.pop_size += element.size
	
	
	def entry_deme_size_activate(self, widget):
		entry=widget.get_text()
		self.error_demesize.set_text(" ")
		try:
		
			assert len(self.deme_select_list) >= 1
		
		except AssertionError:
				self.error_demesize.set_text("You must select a Deme !")
				
		else:		
					
			try:
				entry = int(entry)
				assert entry >= 0 

			except ValueError:
				self.error_demesize.set_text("Not a number !!!")
			
			except AssertionError:
				self.error_demesize.set_text("Negative number !!")
			
		
			else:
		
				self.deme_of_id(self.deme_select_list[0].id).size = entry
				self.error_popsize.set_text(" ")
				self.pop_size_refresh()
				self.info_refresh()
		
	
		
	
		
	def button_migration_clicked(self, widget):
		try:
			assert len(self.deme_select_list) >= 2
			
		
		except AssertionError:
			self.error_migration.set_text("Not enough deme selected")
			
		else:
			self.error_migration.set_text(" ")
			
			i=0
			try:
				for j in range(0, len(self.demes_list)):
					if self.demes_list[j].id == int(self.deme_select_list[0].id):
						for i in range(0, len(self.demes_list[j].migrate_to)):	
							assert self.demes_list[j].migrate_to[i] is not self.deme_select_list[1].id	 
					
			except AssertionError:
				self.error_migration.set_text("This migration already exists")
			
			else:
				entry = self.entry_amount.get_text()
				try:
					entry = int(entry)
					assert entry >= 0

				except ValueError:
					self.error_migration.set_text("You must entry an amount !!!")
			
				except AssertionError:
					self.error_migration.set_text("Negative number !!")
			
				else:

					try : 
						assert entry <= self.deme_select_list[0].size
						
					except AssertionError:
						self.error_migration.set_text('The size of the deme ' + str(self.deme_select_list[0].id) + ' is not big enough.' )
						
					else :
						self.error_migration.set_text(" ")
						for j in range(0, len(self.demes_list)):
							if self.demes_list[j].id == int(self.deme_select_list[0].id):
								fro = self.demes_list[j]
								self.demes_list[j].migrate_to.append(self.deme_select_list[1].id)
							if self.demes_list[j].id == int(self.deme_select_list[1].id):
								to = self.demes_list[j]
					
			
						new_migration = migration.Migration(fro, to, self.entry_amount.get_text() )
						self.migration_list.append(new_migration)
						self.drawing_refresh()
		

	def button_join_clicked(self, widget):
		try:
			assert len(self.deme_select_list) >= 2
		
		except AssertionError:
			self.error_join.set_text("Not enough deme selected")
			
		else:
			self.error_join.set_text(" ")
			
			
			try:
				for j in range(0, len(self.demes_list)):
					if self.demes_list[j].id == int(self.deme_select_list[0].id):
						for i in range(0, len(self.demes_list[j].join_to)):	
							assert self.demes_list[j].join_to[i] is not self.deme_select_list[1].id	
							
					
			except AssertionError:
				self.error_join.set_text("This demes are already joined")
				
		
			
			else:
			
				entry = self.entry_amount2.get_text()
				try:
					entry = int(entry)
					assert entry >= 0

				except ValueError:
					self.error_join.set_text("You must entry an amount !!!")
			
				except AssertionError:
					self.error_join.set_text("Negative number !!")
			
				else:
				
					try: 
						assert entry <= self.deme_select_list[0].size
						
					except AssertionError:
						self.error_join.set_text('The size of the deme ' + str(self.deme_select_list[0].id) + ' is not big enough.' )
					
					else :
						self.error_join.set_text(" ")
						for j in range(0, len(self.demes_list)):
							if self.demes_list[j].id ==self.deme_select_list[0].id	:
								fro = self.demes_list[j]
								self.demes_list[j].join_to.append(self.deme_select_list[1].id	)
							if self.demes_list[j].id == int(self.deme_select_list[1].id	):
								self.demes_list[j].is_joined_by.append(self.deme_select_list[0].id	)
								to = self.demes_list[j]
								
						self.nb_join += 1
							
						new_junction = junction.Junction(fro, to, self.entry_amount2.get_text() )
						self.junction_list.append(new_junction)
						self.drawing_refresh()
				
	def button_invert_clicked(self, widget):
		a=self.deme_select_list[0]
		b=self.deme_select_list[1]
		self.deme_select_list[0]=b
		self.deme_select_list[1]=a
		
		self.drawing_refresh()
		
	def button_delete_one_migration_clicked(self, widget):
		
		print str(len(self.migration_list))			
		#for i in range(0, len(self.migration_list)):
		i=0
		while i <  len(self.migration_list):
			if self.migration_list[i].select:
				index_start = self.demes_list.index(self.deme_of_id(self.migration_list[i].fro.id))
				self.demes_list[index_start].migrate_to.remove(self.migration_list[i].to.id)
				self.migration_list.remove(self.migration_list[i])
			i+=1	
		
		self.drawing_refresh()
	
	def button_delete_one_junction_clicked(self, widget):
		
		print str(len(self.junction_list))			
	
		i=0
		while i <  len(self.junction_list):
			if self.junction_list[i].select:
				index_start = self.demes_list.index(self.deme_of_id(self.junction_list[i].fro.id))
				self.demes_list[index_start].join_to.remove(self.junction_list[i].to.id)
				self.junction_list.remove(self.junction_list[i])
			i+=1	
		
		self.drawing_refresh()
		nb_join -=1
			
	def button_press_event(self, widget, event):
		w = self.drawing_area.allocation.width
		h = self.drawing_area.allocation.height
		
		
		
		if self.select_selectable.get_active() is 0:
		
			for i in range(0, len(self.demes_list)):
				if event.x < (i+1)*w/len(self.demes_list) and event.x > i*w/len(self.demes_list) :
					self.demes_list[i].select = not self.demes_list[i].select
					
			
					
			
		elif self.select_selectable.get_active() is 1:
			for i in range(0, len(self.migration_list)):
				if event.y < (i+1)*h/len(self.migration_list) and event.y > i*h/len(self.migration_list):
					self.migration_list[i].select = not self.migration_list[i].select
					
			
		elif self.select_selectable.get_active() is 2:
			for i in range(0, len(self.junction_list)):
				if event.y < (i+1)*h/len(self.junction_list) and event.y > i*h/len(self.junction_list):
					self.junction_list[i].select = not self.junction_list[i].select

					
		
		
		""" Refresh deme_select_list """
		self.deme_select_list = []
		
		for i in range(0, len(self.demes_list)):
			if self.demes_list[i].select:
				self.deme_select_list.append(self.demes_list[i])
		
		
		self.drawing_refresh()
	

if __name__ == "__main__":
	Interface()
	gtk.main()