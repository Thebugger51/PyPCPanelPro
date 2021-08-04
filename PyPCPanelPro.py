'''
 module for interacting wit a pcpanel pro
 this module relies on the downloadable module pyusb, go to https://github.com/pyusb/pyusb to instruction on how to install it
'''

import usb.core
import usb.util
import threading

#define the function that will update the elements value
def thread_read_pcpro(self):
	while True:
		try:
			self.update_from_packet(self.device.read(0x81, 64, 100))
		except usb.core.USBTimeoutError:
			pass

class pcpro_element:

	def __init__(self, type):
		if type == 'knob':
			#for the knobs the available color modes are 'static' and 'gradient'
			self.color_mode = 'static'
			self.color = ['#000000', '#000000']
			self.value = 0
			self.type = 'knob'
		elif type =='label':
			#for labels the available color modes are 'static'
			self.color_mode = 'static'
			self.color = '#000000'
			self.type = 'label'
		elif type == 'slider':
			#for sliders the available color modes are 'static', 'gradient' and 'vol_gradient'
			self.color_mode = 'static'
			self.color = ['#000000', '#000000']
			self.value = 0
			self.type = 'slider'
		elif type == 'logo':
			#for the logo the available color modes are 'static', 'rainbow' and 'breath'
			#for the logo in rainbow mode the brightness and speed are used
			#for the logo in breath mode the hue, brightness and speed are used
			self.color_mode = 'static'
			self.color = '#000000'
			self.type = 'logo'
			self.hue = '00'
			self.brightness = 'ff'
			self.speed = '89'
		elif type == 'button':
			self.value = 0
			self.type = 'button'

class pcpro_panel:

	def __init__(self):
		#define auxiliary variables
		self.lights_on = True
		#define the elements of the panel
		self.k1 = pcpro_element('knob')
		self.k2 = pcpro_element('knob')
		self.k3 = pcpro_element('knob')
		self.k4 = pcpro_element('knob')
		self.k5 = pcpro_element('knob')
		self.s1 = pcpro_element('slider')
		self.s2 = pcpro_element('slider')
		self.s3 = pcpro_element('slider')
		self.s4 = pcpro_element('slider')
		self.l1 = pcpro_element('label')
		self.l2 = pcpro_element('label')
		self.l3 = pcpro_element('label')
		self.l4 = pcpro_element('label')
		self.logo = pcpro_element('logo')
		self.b1 = pcpro_element('button')
		self.b2 = pcpro_element('button')
		self.b3 = pcpro_element('button')
		self.b4 = pcpro_element('button')
		self.b5 = pcpro_element('button')
		#get the device 
		self.device = usb.core.find(idVendor= 0x483, idProduct=0xa3c5)
		if self.device is None:
			raise ValueError('Device not found')
		#claim the interface
		try:
			self.device.detach_kernel_driver(0)
		except usb.core.USBError:
			pass
		usb.util.claim_interface(self.device, 0)
		#start the thread that will maintan updated the values
		self.thread = threading.Thread(target=thread_read_pcpro, args=(self,))
		self.thread.start()

	def update_colors(self):
		#function to form the packets to send via usb
		packets = {'kp' : b'\x05\x02', 'lp' : b'\x05\x01', 'sp' : b'\x05\x00', 'lgp' : b'\x05\x03'}
		off_packets = {\
			'kp': b'\x05\x02\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00',\
			'lp': b'\x05\x01\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00',\
			'sp': b'\x05\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00',\
			'lgp': b'\x05\x03\x01\x00\x00\x00\x00\x00\x00'\
			}

		if self.lights_on == False:
			packets = off_packets
		else:
			#assemble the first packet
			knobs = [self.k1, self.k2, self.k3, self.k4, self.k5]
			for j in knobs:
				if j.color_mode == 'static':
					packets['kp'] = packets['kp'] + b'\x01' + bytes.fromhex(j.color[0][1:7] + j.color[1][1:7])
				else:
					packets['kp'] = packets['kp'] + b'\x02' + bytes.fromhex(j.color[0][1:7] + j.color[1][1:7])

			#assemble the second packet
			labels = [self.l1, self.l2, self.l3, self.l4]
			for j in labels:
				packets['lp'] = packets['lp'] + b'\x01' + bytes.fromhex(j.color[1:7]) + b'\x00\x00\x00'
			#fill the rest of the packet with zeros

			#assemble the third packet
			sliders = [self.s1, self.s2, self.s3, self.s4]
			for j in sliders:
				if j.color_mode == 'static':
					packets['sp'] = packets['sp'] + b'\x01' + bytes.fromhex(j.color[0][1:7] + j.color[1][1:7])
				else:
					packets['sp'] = packets['sp'] + b'\x03' + bytes.fromhex(j.color[0][1:7] + j.color[1][1:7])

			#assemble the fourth packet
			if self.logo.color_mode == 'static':
				packets['lgp'] = packets['lgp'] + b'\x01' + bytes.fromhex(self.logo.color[1:7])
			elif self.logo.color_mode == 'rainbow':
				packets['lgp'] = packets['lgp'] + b'\x02\xff' + bytes.fromhex(self.logo.brightness[0:2] + self.logo.speed[0:2])
			else:
				packets['lgp'] = packets['lgp'] + b'\x03' + bytes.fromhex(self.logo.hue + self.logo.brightness + self.logo.speed)
		
		self.device.write(0x1,packets['kp'],1000)
		self.device.write(0x1,packets['lp'],1000)
		self.device.write(0x1,packets['sp'],1000)
		self.device.write(0x1,packets['lgp'],1000)


	def update_from_packet(self, packet):
		#check if it is a button
		if packet[0] == 2:
			if packet[1] == 0:
				self.b1.value = packet[2]
			elif packet[1] == 1:
				self.b2.value = packet[2]
			elif packet[1] == 2:
				self.b3.value = packet[2]
			elif packet[1] == 3:
				self.b4.value = packet[2]
			elif packet[1] == 4:
				self.b5.value = packet[2]
		else:
			#if not a button
			if packet[1] == 0:
				self.k1.value = packet[2]
			elif packet[1] ==1:
				self.k2.value = packet[2]
			elif packet[1] ==2:
				self.k3.value = packet[2]
			elif packet[1] ==3:
				self.k4.value = packet[2]
			elif packet[1] ==4:
				self.k5.value = packet[2]
			elif packet[1] ==5:
				self.s1.value = packet[2]
			elif packet[1] ==6:
				self.s2.value = packet[2]
			elif packet[1] ==7:
				self.s3.value = packet[2]
			elif packet[1] ==8:
				self.s4.value = packet[2]


	def print(self, tag = 'colors'):
		pp_elements = {'k1':self.k1, 'k2':self.k2, 'k3':self.k3, 'k4':self.k4, 'k5':self.k5, 's1':self.s1, 's2':self.s2, 's3':self.s3, 's4':self.s4}
		pp_buttons = {'b1':self.b1, 'b2':self.b2, 'b3':self.b3, 'b4':self.b4, 'b5':self.b5}
		pp_no_val = {'logo':self.logo, 'l1':self.l1, 'l2':self.l2, 'l3':self.l3, 'l4':self.l4}
		
		#iterate the elements list
		if tag == 'colors':
			for name, var in pp_elements.items():		
				print('{} - mode : {} - color {}'.format(name, var.color_mode, var.color))
			for name, var in pp_no_val.items():		
				print('{} - mode : {} - color {}'.format(name, var.color_mode, var.color))
		
		#iterate both the lists
		if tag == 'values':
			for name, var in pp_elements.items():
				print('{} - value : {}'.format(name, var.value))
			for name, var in pp_buttons.items():
				print('{} - value : {}'.format(name, var.value))


	#turns of or on the panel lights
	def toggle_lights(self):
		if self.lights_on == True:
			self.lights_on = False
		else:
			self.lights_on = True
		self.update_colors()