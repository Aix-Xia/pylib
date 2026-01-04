class Template:
	def __set_name__(self, owner, name):
		self.private_name = f'_{name}'
	def __get__(self, instance, owner):
		return getattr(instance, self.private_name)
	def __set__(self, instance, value):
		if not (isinstance(value, (int, float)) and value > 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a positive number')
		setattr(instance, self.private_name, value)

class Number(Template):
	def __set__(self, instance, value):
		if not isinstance(value, (int, float)):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a number')
		setattr(instance, self.private_name, value)
class PositiveNumber(Template):
	def __set__(self, instance, value):
		if not (isinstance(value, (int, float)) and value >= 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a positive number')
		setattr(instance, self.private_name, value)
class NegativeNumber(Template):
	def __set__(self, instance, value):
		if not (isinstance(value, (int, float)) and value <= 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a negative number')
		setattr(instance, self.private_name, value)

class Int(Template):
	def __set__(self, instance, value):
		if not isinstance(value, (int, )):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a int')
		setattr(instance, self.private_name, value)
class PositiveInt(Template):
	def __set__(self, instance, value):
		if not (isinstance(value, (int, )) and value >= 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a positive int')
		setattr(instance, self.private_name, value)
class NegativeInt(Template):
	def __set__(self, instance, value):
		if not (isinstance(value, (int, )) and value <= 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a negative int')
		setattr(instance, self.private_name, value)

class Float(Template):
	def __set__(self, instance, value):
		if not isinstance(value, (float, )):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a float')
		setattr(instance, self.private_name, value)
class PositiveFloat(Template):
	def __set__(self, instance, value):
		if not (isinstance(value, (float, )) and value >= 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a positive float')
		setattr(instance, self.private_name, value)
class NegativeFloat(Template):
	def __set__(self, instance, value):
		if not (isinstance(value, (float, )) and value <= 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a negative float')
		setattr(instance, self.private_name, value)

class String(Template):
	def __set__(self, instance, value):
		if not (isinstance(value, str) and len(value) > 0):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a string')
		setattr(instance, self.private_name, value)

class Bool(Template):
	def __set__(self, instance, value):
		if not isinstance(value, bool):
			raise ValueError(f'{self.private_name[1:].capitalize()} is required to be a bool')
		setattr(instance, self.private_name, value)

def main():
	class Circle:
		name = String()
		radius = PositiveNumber()

		def __init__(self, name, radius):
			self.name = name
			self.radius = radius

		def __repr__(self):
			return f' name : {self.name}\nradius: {self.radius}'

	r = Circle('r1', 10)
	print(r)

if __name__ == '__main__':
	main()
