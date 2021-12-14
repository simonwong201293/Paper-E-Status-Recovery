import json

class TimeRecord:
    
	time = -1
	time_str = None
	battery_records = []
	capacitor_records = []
	average_battery_voltage = -1
	average_capacitor_voltage = -1

	def __init__(self, time, time_str):
		self.time = time
		self.time_str = time_str
		self.battery_records = []
		self.capacitor_records = []
		self.average_battery_voltage = -1
		self.average_capacitor_voltage = -1

	def __eq__(self, obj):
		return isinstance(obj, TimeRecord) and self.time == obj.time

	def __str__(self):
		return json.dumps(self.__dict__)

	def is_estimated(self):
		return len(self.battery_records) <= 0

	def get_size(self):
		return len(self.battery_records)

	def add_record(self, battery_voltage, capacitor_voltage):
		self.battery_records.append(battery_voltage)
		self.capacitor_records.append(capacitor_voltage)

	def evaluate(self):
		if len(self.battery_records) == 0 or len(self.capacitor_records) == 0:
			return
		avg = 0
		for record in self.battery_records:
			avg += record
		self.average_battery_voltage = avg / len(self.battery_records)
		avg = 0
		for record in self.capacitor_records:
			avg += record
		self.average_capacitor_voltage = avg / len(self.capacitor_records)