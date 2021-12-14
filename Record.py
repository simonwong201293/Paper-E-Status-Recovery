import random, json
from TimeRecord import TimeRecord

class Record:
	
	index = -1
	name = None
	records = []
    
	def __init__(self, index, name, timeslots, time_strs):
		self.index = index
		self.name = name
		i = 0
		for timeslot in timeslots:
			record = TimeRecord(time=timeslot, time_str=time_strs[i])
			if record not in self.records:
				self.records.append(TimeRecord(time=timeslot, time_str=time_strs[i]))
				i += 1

	def __str__(self):
		return json.dumps(self.__dict__)

# 	def refill_by_naive_method(self):
# 		for record in self.records:
# 			if record.get_size() == 0:
# 				self.records[self.records.index(record)] = naive_refilling(record, self.records)

	def get_training_data(self):
		X = []
		Y = []
		# print('len = {}'.format(len(self.records) - 3 - 2))
		for i in range(2, len(self.records) - 3):
			tmp = [self.index, self.records[i].time, self.records[i - 1].time,
				   self.records[i - 1].average_capacitor_voltage, self.records[i + 1].time,
				   self.records[i + 1].average_capacitor_voltage]
			X.append(tmp)
			Y.append(self.records[i].average_capacitor_voltage)
		return X, Y

	def get_size(self):
		return len(self.records)

	def get_working_size(self):
		i = 0
		for record in self.records:
			if record.get_size() > 0:
				i += 1
		return i

	def drop_record_until(self, number):
		tmp = self.records.copy()
		random.sample(self.records, number)
		for record in tmp:
			if record in self.records:
				continue
			else:
				record.battery_records = []
				record.capacitor_records = []
				record.average_battery_voltage = -1
				record.average_capacitor_voltage = -1
		self.records = tmp

	def add_time_record(self, timeslot, battery_voltage, capacitor_voltage, ts):
		for record in self.records:
			if record.time == timeslot:
				record.add_record(battery_voltage=battery_voltage, capacitor_voltage=capacitor_voltage)

	def freeze(self, ts):
		if len(self.records) > 0:
			for record in self.records:
				record.evaluate()
			self.records.sort(key=lambda x: x.time, reverse=False)

	def get_graph_time(self):
		result = []
		for record in self.records:
			if -1 < record.average_battery_voltage < 100 and -1 < record.average_capacitor_voltage < 100:
				result.append(record.time)
		return result

	def get_graph_real_time(self):
		result = []
		for record in self.records:
			if -1 < record.average_battery_voltage < 100 and -1 < record.average_capacitor_voltage < 100:
				result.append(record.time_str)
		return result

	def get_graph_battery_voltage(self):
		result = []
		for record in self.records:
			if -1 < record.average_battery_voltage < 100 and -1 < record.average_capacitor_voltage < 100:
				result.append(3.6 * record.average_battery_voltage / 100)
		return result

	def get_graph_capacitor_voltage(self):
		result = []
		for record in self.records:
			if -1 < record.average_battery_voltage < 100 and -1 < record.average_capacitor_voltage < 100:
				result.append(3.6 * record.average_capacitor_voltage / 100)
		return result