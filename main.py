
developerRead = False

import copy
import sys
from bitarray import bitarray
from void import Void
import unit_

script = open('Main.luca', 'r').read()

LucaStored  = {}
LucaDefine  = {}
LucaClasses = {}
LucaCreated = {}

LucaStacked = []

LucaAllocate = {}

address = 1
for each in range(300):
	name = f"L24x{address}"
	LucaAllocate.update({name:None})
	address += 1

last_condition = None

building = True

binary = {'1', '0'}

error = ""

def seterror(message, syntax):
	error = colored2(255, 60, 0, f"SyntaxError : #>\n{syntax}\n{message}", False)


def colored(r, g, b, text, devonly=True, endl="\n"):
	global developerRead
	if developerRead and devonly:
		text = "\033[1m" + text
		text = text.replace('#>', f'\033[0m\033[38;2;{r};{g};{b}m')
		text = text.replace("\n", "\n >>> ", 1)
		print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=endl)

def colored2(r, g, b, text, devonly=True, endl="\n"):
	text = "\033[1m" + text
	text = text.replace('#>', f'\033[0m\033[38;2;{r};{g};{b}m')
	text = text.replace("\n", "\n >>> ", 1)
	print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=endl)


def log(object):
	global developerRead
	if developerRead: print(object)


def find_nth(haystack, needle, n):
	start = haystack.find(needle)
	while start >= 0 and n > 1:
		start = haystack.find(needle, start + len(needle))
		n -= 1
	return start


def findparr(segment):
	if '(' in segment and ')' in segment:
		return True
	else:
		return False


def get_factors(x):
	fact = []
	for i in range(1, x + 1):
		if x % i == 0:
			fact.append(i)

	return (fact)


class Lang:

	def validate(segment, scope=""):

		colored(258, 179, 234, f"[*] VALIDATION : now validating...#>\n{segment}\n")
		
		colored(258, 179, 234, f"[*] VALIDATION : scope presented : #>\n{scope}\n")

		statements = Lang.Statements(segment, scope)
		if statements[0]:
			colored(258, 179, 234, f"[*] VALIDATION : statement validating...#>\n{segment}\n")
			return [True, statements[1]]
		else:
			colored(258, 179, 234, f"[*] VALIDATION : function validating...#>\n{segment}\n")
			function = Lang.Function(segment, scope)
		
		if function[0]:
			try:
				if function[2] == "return point":
					return [True, function[1], function[2]]
			except:
				return [True, function[1]]
		else:
			colored(258, 179, 234, f"[*] VALIDATION : datatype validating...#>\n{segment}\n")
			datatype = Lang.Datatype(segment, scope)
		
		if datatype[0]:
			try:
				return [True, datatype[1]]
			except:
				return [True]
		else:
			colored(252, 90, 3, f"[*] VALIDATION : validation failure. #>\n{segment}\n")
			return [False]


	class Datatype:

		class NewObject:

			def __new__(self, segment, scope=""):
				if segment.startswith("new "):
					global LucaClasses, LucaCreated, LucaStored
					objectpointer = segment[len("new "):]
					objectpointer = objectpointer.replace('(', '.')
					objectpointer = objectpointer.replace(').', '.')
					objectpointer = objectpointer.replace(')', '.')
					objectpointer = objectpointer.split('.')
					pointed = objectpointer

					megapointed = []
					for name in pointed:
						if name == "":
							pass
						else:
							megapointed.append(name)
					pointed = megapointed
					
					first = True
					dir   = LucaCreated 
					ranconstr = ''
					for name in pointed:
						if first:
							try:
								LucaCreated.update({name:copy.deepcopy(LucaClasses[name])})
							except:
								try:
									LucaCreated.update({name:copy.deepcopy(LucaStored[name])})
								except:
									try:
										LucaCreated.update({name:copy.deepcopy(LucaStored["const:"+name])})
									except:
										try:
											LucaCreated.update({name:copy.deepcopy(LucaStored["final:"+name])})
										except:
											return [False]
							dir = dir[name]
							first = False
						else:
							if ':' in name:
								
								if '<__init__>'   in dir:
									initial   = dir['<__init__>']
								else:
									initial     = [{0:None}, '']

								if '<__constr__>' in dir:
									construct = dir['<__constr__>']
								else:
									construct   = [{0:None}, '']

								if '<method>' in dir:
									method    = dir['<method>']
								else:
									method      = [{0:None}, '']
									
								param = name.split(':')

								pos = 0
								for item in param:
									val = Lang.validate(param[pos])
									if val[0]:
										param[pos] = val[1]
									else:
										seterror('is not a valid argument', param[pos])
										return [False]
									pos += 1
	
								init_keys   = list(initial[0].keys())
								constr_keys = list(construct[0].keys())
								method_keys = list(method[0].keys())
								
								pos = 0
								for attrib in method_keys:
									method[0][attrib] = param[pos]
									LucaStored[attrib]   = param[pos]
									pos += 1
								
								pos = 0
								for attrib in constr_keys:
									construct[0][attrib] = param[pos]
									LucaStored[attrib]   = param[pos]
									pos += 1

								pos = 0
								for attrib in init_keys:
									initial[0][attrib] = param[pos]
									LucaStored[attrib] = param[pos]
									pos += 1

								megascoop = []
								scoop = pointed[:pointed.index(name)]
								for name in scoop:
									if ':' in name:
										pass
									else:
										megascoop.append(name)
								scoop = megascoop

								ranmethod = Lang(method[1],    ".".join(scoop[:-1]))
								ranconstr = Lang(construct[1], ".".join(scoop))
								raninit   = Lang(initial[1],   ".".join(scoop[:-1]))
								
								if str(type(raninit)) != "<class 'NoneType'>":
									return [False]

								for attrib in init_keys:
									LucaStored.pop(attrib, None)

								for attrib in constr_keys:
									LucaStored.pop(attrib, None)
								
								for attrib in method_keys:
									LucaStored.pop(attrib, None)
								
							else:
								if name != "":
									dir = dir[name]
									

					if ranconstr != None and ranconstr != "":
						dir = ranconstr

					return [True, dir]
				
				else:
					return [False]

		class SelfVariable:
			def __new__(self, segment, scope=""):
				if segment.startswith('self '):
					if ' = ' in segment:
						thename = segment[len('self '):segment.index(' = ')]
						value = segment[segment.index(' = ')+3:]

						thename = thename.strip()
						
						while value.startswith(' '):
							value = value[1:]
						while value.endswith(' '):
							value = value[:-1]

						val = Lang.validate(value)
						if val[0]:
							value = val[1]
						else:
							seterror('is not a valid syntax', segment)
							return [False]

						global LucaCreated
						dir = LucaCreated
						if scope == "":
							return [False]
							
						scoop = scope.split('.')
						for name in scoop:
							dir = dir[name]
						
						dir[thename] = value

						return [True, value]
					else:
						return [False]
				else:
					return [False]
									
		class Comment:

			def __new__(self, segment):
				if segment.startswith('//'):
					return [True, None]
				else:
					return [False]

		class String:

			def __new__(self, segment):
				if '"' in segment and segment.count('"') == 2 and segment.index(
				  '"') == 0 and segment.rindex('"') == len(segment) - 1:
					return [True, str(segment[1:-1])]
				else:
					return [False]

		class Integer:

			def __new__(self, segment):
				if segment.startswith('-'):
					if segment[1:].isdigit():
						return [True, int(segment)]
					else:
						return [False]
				elif segment.isdigit():
					return [True, int(segment)]
				else:
					return [False]

		class Float:

			def __new__(self, segment):
				if '.' in segment:
					whole, decimal, = segment[:segment.
					                          index('.')], segment[segment.index('.') + 1:]
					if whole.startswith('-'):
						if whole[1:].isdigit():
							pass
						else:
							return [False]
					elif whole.isdigit():
						pass
					else:
						return [False]
					if decimal.isdigit():
						return [True, float(segment)]
					else:
						return [False]
				else:
					return [False]

		class Boolean:

			def __new__(self, segment):
				if segment == 'true':
					return [True, True]
				elif segment == 'false':
					return [True, False]
				else:
					return [False]

		class Binomial:

			def __new__(self, segment):
				if segment == 'yes':
					return [True, True]
				elif segment == 'no':
					return [True, False]
				else:
					return [False]

		class List:

			def __new__(self, segment):
				if "list[" in segment and "]" in segment and segment.index(
				  'list[') == 0 and segment.rindex(']') == len(segment) - 1:
					colored(252, 152, 3, f"[?] DATATYPE : list validating... #>\n{segment}\n")
					contents = segment[segment.index("list[") + 5:segment.rindex("]")]
					contents = contents.split(',')

					contents2 = []
					for item in contents:
						while item.startswith(' '):
							item = item[1:]
						while item.endswith(' '):
							item = item[:-1]
						contents2.append(item)

					thearray = []
					for item in contents2:
						validate = Lang.validate(item)
						if validate[0]:
							thearray.append(validate[1])
						else:
							return [False]

					return [True, list(thearray)]
				else:
					return [False]

		class Tuple:

			def __new__(self, segment):
				if "tuple[" in segment and "]" in segment and segment.index(
				  'tuple[') == 0 and segment.rindex(']') == len(segment) - 1:
					colored(252, 152, 3,
					        f"[?] DATATYPE : tuple validating... #>\n{segment}\n")
					contents = segment[segment.index("tuple[") + 6:segment.index("]")]
					contents = contents.split(',')

					contents2 = []
					for item in contents:
						while item.startswith(' '):
							item = item[1:]
						while item.endswith(' '):
							item = item[:-1]
						contents2.append(item)

					thearray = []
					for item in contents2:
						validate = Lang.validate(item)
						if validate[0]:
							thearray.append(validate[1])
						else:
							return [False]

					return [True, tuple(thearray)]
				else:
					return [False]

		class Set:

			def __new__(self, segment):
				if "set[" in segment and "]" in segment and segment.index(
				  'set[') == 0 and segment.rindex(']') == len(segment) - 1:
					colored(252, 152, 3, f"[?] DATATYPE : set validating... #>\n{segment}\n")
					contents = segment[segment.index("set[") + 4:segment.index("]")]
					contents = contents.split(',')

					contents2 = []
					for item in contents:
						while item.startswith(' '):
							item = item[1:]
						while item.endswith(' '):
							item = item[:-1]
						contents2.append(item)

					thearray = []
					for item in contents2:
						validate = Lang.validate(item)
						if validate[0]:
							thearray.append(validate[1])
						else:
							return [False]

					return [True, set(thearray)]
				else:
					return [False]

		class Range:

			def __new__(self, segment):
				if "range[" in segment and "]" in segment and segment.index(
				  'range[') == 0 and segment.rindex(']') == len(segment) - 1:
					colored(252, 152, 3,
					        f"[?] DATATYPE : range validating... #>\n{segment}\n")
					contents = segment[segment.index("range[") + 6:segment.index("]")]

					validate = Lang.validate(contents)
					if validate[0]:
						contents = validate[1]
					else:
						return [False]

					return [True, range(contents)]
				else:
					return [False]

		class Dictionary:

			def __new__(self, segment):
				if "dict[" in segment and "]" in segment and segment.index(
				  'dict[') == 0 and segment.rindex(']') == len(segment) - 1:
					colored(252, 152, 3,
					        f"[?] DATATYPE : dictionary validating... #>\n{segment}\n")
					contents = segment[segment.index("dict[") + 5:segment.index("]")]
					contents = contents.split(',')

					# CONTINUE AT SCHOOL.
					contents2 = []
					for item in contents:
						while item.startswith(' '):
							item = item[1:]
						while item.endswith(' '):
							item = item[:-1]
						contents2.append(item)

					# [["  data"," data"],["data","data"]]
					contents3 = []
					for item in contents2:
						if ":" in item:
							item = item.split(':')
							while item[0].startswith(' '):
								item[0] = item[0][1:]
							while item[0].endswith(' '):
								item[0] = item[0][:-1]
							while item[1].startswith(' '):
								item[1] = item[1][1:]
							while item[1].endswith(' '):
								item[1] = item[1][:-1]
							contents3.append(item)
						else:
							return [False]

					# [["data","data"],["data","data"]]
					for keyvaluepair in contents3:
						val1 = Lang.validate(keyvaluepair[0])
						val2 = Lang.validate(keyvaluepair[1])
						if val1[0]:
							keyvaluepair[0] = val1[1]
						else:
							return [False]
						if val2[0]:
							keyvaluepair[1] = val2[1]
						else:
							return [False]

					return [True, dict(contents3)]
				else:
					return [False]
	
		class Blank:

			def __new__(self, segment):
				if segment == '':
					return [True, None]
				else:
					return [False]
	
		class Expression:

			def __new__(self, segment, scope=""):
				if   ' - ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : expression validating... #>\n{segment}\n")
					object1 = segment[:segment.index('-')]
					object2 = segment[segment.index('-') + 1:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1, scope)
					validateObject2 = Lang.validate(object2, scope)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					colored(252, 152, 3,
					        f"[?] DATATYPE : expression operands #>\n{[object1, object2]}\n")

					return [True, object1 - object2]
				elif ' + ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : expression validating... #>\n{segment}\n")
					object1 = segment[:segment.index('+')]
					object2 = segment[segment.index('+') + 1:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1, scope)
					validateObject2 = Lang.validate(object2, scope)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					colored(252, 152, 3,
					        f"[?] DATATYPE : expression operands #>\n{[object1, object2]}\n")

					return [True, object1 + object2]
				elif ' / ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : expression validating... #>\n{segment}\n")
					object1 = segment[:segment.index('/')]
					object2 = segment[segment.index('/') + 1:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1, scope)
					validateObject2 = Lang.validate(object2, scope)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					colored(252, 152, 3,
					        f"[?] DATATYPE : expression operands #>\n{[object1, object2]}\n")

					return [True, object1 / object2]
				elif ' * ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : expression validating... #>\n{segment}\n")
					object1 = segment[:segment.index('*')]
					object2 = segment[segment.index('*') + 1:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1, scope)
					validateObject2 = Lang.validate(object2, scope)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					colored(252, 152, 3,
					        f"[?] DATATYPE : expression operands #>\n{[object1, object2]}\n")

					return [True, object1 * object2]
				else:
					return [False]
	
		class Comparison:

			def __new__(self, segment):
				if ' and ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('and')]
					object2 = segment[segment.index('and') + 3:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					if object1 and object2:
						return [True, True]
					else:
						return [True, False]
				elif ' or ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('or')]
					object2 = segment[segment.index('or') + 2:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					log([object1, object2])

					if object1 or object2:
						return [True, True]
					else:
						return [True, False]
				elif ' in ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('in')]
					object2 = segment[segment.index('in') + 2:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					log([object1, object2])

					if object1 in object2:
						return [True, True]
					else:
						return [True, False]
				elif ' == ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('==')]
					object2 = segment[segment.index('==') + 2:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					if object1 == object2:
						return [True, True]
					else:
						return [True, False]
				elif ' != ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('!=')]
					object2 = segment[segment.index('!=') + 2:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					log([object1, object2])

					if object1 != object2:
						return [True, True]
					else:
						return [True, False]
				elif ' >= ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('>=')]
					object2 = segment[segment.index('>=') + 2:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					log([object1, object2])

					if object1 >= object2:
						return [True, True]
					else:
						return [True, False]
				elif ' <= ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('<=')]
					object2 = segment[segment.index('<=') + 2:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					log([object1, object2])

					if object1 <= object2:
						return [True, True]
					else:
						return [True, False]
				elif ' > ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('>')]
					object2 = segment[segment.index('>') + 1:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					log([object1, object2])

					if object1 > object2:
						return [True, True]
					else:
						return [True, False]
				elif ' < ' in segment:
					colored(252, 152, 3,
					        f"[?] DATATYPE : comparison validating... #>\n{segment}\n")
					object1 = segment[:segment.index('<')]
					object2 = segment[segment.index('<') + 1:]

					if object1.endswith(' '):
						while object1.endswith(' '):
							object1 = object1[:-1]
					if object1.startswith(' '):
						while object1.startswith(' '):
							object1 = object1[1:]

					if object2.endswith(' '):
						while object2.endswith(' '):
							object2 = object2[:-1]
					if object2.startswith(' '):
						while object2.startswith(' '):
							object2 = object2[1:]

					validateObject1 = Lang.validate(object1)
					validateObject2 = Lang.validate(object2)

					if validateObject1[0]:
						object1 = validateObject1[1]
					else:
						return [False]

					if validateObject2[0]:
						object2 = validateObject2[1]
					else:
						return [False]

					log([object1, object2])

					if object1 < object2:
						return [True, True]
					else:
						return [True, False]
				else:
					return [False]

		class SelfPointer:

			def __new__(self, segment, scope=""):
				global LucaClasses
				if segment.startswith('self@'):
					scope = scope.split('.')
					name = segment[segment.index('@')+1:]

					if scope == "":
						return [False]

					reen = LucaCreated
					for space in scope:
						reen = reen[space]

					if name in reen:
						return [True, reen[name]]
					elif "const:" + name in reen:
						return [True, reen["const:" + name]]
					elif "final:" + name in reen:
						return [True, reen["final:" + name]]
					else:
						return [False]

				else:
					return [False]

		class Pointer:

			def __new__(self, segment, scope=""):
				global LucaClasses
				global LucaStored
				colored(219, 145, 15, f"[?] POINTER : scope present.#>\n{scope + '.' + segment}\n")
				if scope == "":
					if segment in LucaStored:
						return [True, LucaStored[segment]]
					elif "const:" + segment in LucaStored:
						return [True, LucaStored["const:" + segment]]
					elif "final:" + segment in LucaStored:
						return [True, LucaStored["final:" + segment]]
					else:
						return [False]
				elif scope != "":
					scope = scope.split('.')
					
					megascope = []
					for name in scope:
						if name == "":
							pass
						else:
							megascope.append(name)
					scope = megascope

					dex = LucaClasses
					for name in scope:
						dex = dex[name]

					if segment in dex:
						return [True, dex[segment]]
					elif "const:" + segment in dex:
						return [True, dex["const:" + segment]]
					elif "final:" + segment in dex:
						return [True, dex["final:" + segment]]
					else:
						return [False]
				else:
					colored(219, 145, 15, f"[?] POINTER : pointer is not valid.#>\n{scope + '.' + segment}\n")
					return [False]

		class Variable:

			def __new__(self, segment, scope="", const=False, final=False, inst=False, prop=False):
				if " = " in segment:
					colored(252, 152, 3, f"[?] DATATYPE : variable validating... #>\n{segment}\n")

					if const:
						if segment.startswith('const '):
							segment = segment[len('const '):]
						else: return [False]
					
					if final:
						if segment.startswith('final '):
							segment = segment[len('final '):]
						else: return [False]

					if inst:
						if segment.startswith('inst '):
							segment = segment[len('inst '):]
						else: return [False]

					if prop:
						if segment.startswith('prop '):
							segment = segment[len('prop '):]
						else: return [False]
					
					assigned = segment[:segment.index(' = ')].replace(' ', '')

					if "final:" + assigned in LucaStored.keys():
						return [False]
					elif "const:" + assigned in LucaStored.keys():
						return [False]

					if assigned.isidentifier():
						pass
					else:
						return [False]
					
					if   const:
						if assigned in LucaStored:
							return [False]
						if ("const:" + assigned) in LucaStored:
							return [False]
					elif final:
						if assigned not in LucaStored:
							return [False]
						if ("final:" + assigned) in LucaStored:
							return [False]
					else:
						pass

					colored(
					 252, 152, 3,
					 f"[?] DATATYPE : variable assigned is identifier #>\n{assigned}\n")

					object = segment[segment.index(' = ') + 3:]
					if object.startswith(' '):
						while object.startswith(' '):
							object = object[1:]
					else:
						pass

					validate = Lang.validate(object)
					if validate[0]:
						object = validate[1]
					else:
						colored(252, 152, 3,f"[X] DATATYPE : variable object is NOT valid #>\n{object}\n")
						return [False]

					colored(252, 152, 3,f"[?] DATATYPE : variable object is valid #>\n{object}\n")
					
					if inst:
						scopespace = LucaCreated
					elif prop:
						scopespace = LucaClasses
					else:
						scopespace = LucaCreated

					if scope != "":
						scope = list(scope.split('.'))
						for name in scope:
							scopespace = scopespace[name]

						if   const: 
							scopespace["const:" + assigned] = object
						elif final: 
							scopespace.pop(assigned)
							scopespace["final:" + assigned] = object
						else:		
							scopespace[assigned] = object
					else:
						if   const: 
							LucaStored["const:" + assigned] = object
						elif final: 
							LucaStored.pop(assigned)
							LucaStored["final:" + assigned] = object
						else:		LucaStored[assigned] = object

					return [True, object]
				else:
					return [False]

		class Constant:
			def __new__(self, segment, scope=""):

				constant = Lang.Datatype.Variable(segment, scope, const=True)
				if constant[0]:
					return [True, constant[1]]
				else:
					return [False]
			
		class Final:
			def __new__(self, segment, scope=""):

				final = Lang.Datatype.Variable(segment, scope, final=True)
				if final[0]:
					return [True, final[1]]
				else:
					return [False]
		
		class Instance:
			def __new__(self, segment, scope=""):

				inst = Lang.Datatype.Variable(segment, scope, inst=True)
				if inst[0]:
					return [True, inst[1]]
				else:
					return [False]
		
		class Property:
			def __new__(self, segment, scope=""):

				inst = Lang.Datatype.Variable(segment, scope, prop=True)
				if inst[0]:
					return [True, inst[1]]
				else:
					return [False]

		class Nonetype:

			def __new__(self, segment):
				if segment == "none":
					return [True, None]
				else:
					return [False]

		class Void:

			def __new__(self, segment):
				if segment == "void":
					return [True, Void()]
				else:
					return [False]

		class Unit:

			def __new__(self, segment):
				if segment == "unit":
					return [True, unit_.Unit()]
				else:
					return [False]

		class Bit:
			def __new__(self, segment, scope=""):
				if segment.startswith("bit "):
					content = segment[len("bit "):]
					if len(content) == 1:
						bitlist = bitarray()
						for bit in content:
							if bit in binary:
								bitlist.append(int(bit))
							else:
								return [False]
						return [True, [True, str(bitlist)[10:-2]]]
					else:
						return [False]
				else:
					return [False]
				
		class Crumb:
			def __new__(self, segment, scope=""):
				if segment.startswith("crumb "):
					content = segment[len("crumb "):]
					if len(content) == 2:
						bitlist = bitarray()
						for bit in content:
							if bit in binary:
								bitlist.append(int(bit))
							else:
								return [False]
						return [True, str(bitlist)[10:-2]]
					else:
						return [False]
				else:
					return [False]

		def __new__(self, segment, scope=""):

			comment = Lang.Datatype.Comment(segment)
			if comment[0]:
				colored(139, 179, 7, f"[*] DATATYPE : co validated.#>\n{segment}\n")
				return [True, comment[1]]
				
			selfvariable = Lang.Datatype.SelfVariable(segment, scope)
			if selfvariable[0]:
				colored(139, 179, 7, f"[*] DATATYPE : self variable validated.#>\n{segment}\n")
				return [True, selfvariable[1]]
				
			constant = Lang.Datatype.Constant(segment, scope)
			if constant[0]:
				colored(139, 179, 7, f"[*] DATATYPE : constant validated.#>\n{segment}\n")
				return [True, constant[1]]

			final = Lang.Datatype.Final(segment, scope)
			if final[0]:
				colored(139, 179, 7, f"[*] DATATYPE : final validated.#>\n{segment}\n")
				return [True, final[1]]

			instance = Lang.Datatype.Instance(segment, scope)
			if instance[0]:
				colored(139, 179, 7, f"[*] DATATYPE : instance validated.#>\n{segment}\n")
				return [True, instance[1]]

			property = Lang.Datatype.Property(segment, scope)
			if property[0]:
				colored(139, 179, 7, f"[*] DATATYPE : property validated.#>\n{segment}\n")
				return [True, instance[1]]

			variable = Lang.Datatype.Variable(segment, scope)
			if variable[0]:
				colored(139, 179, 7, f"[*] DATATYPE : variable validated.#>\n{segment}\n")
				return [True, variable[1]]

			list = Lang.Datatype.List(segment)
			if list[0]:
				colored(139, 179, 7, f"[*] DATATYPE : list validated.#>\n{segment}\n")
				return [True, list[1]]

			tuple = Lang.Datatype.Tuple(segment)
			if tuple[0]:
				colored(139, 179, 7, f"[*] DATATYPE : tuple validated.#>\n{segment}\n")
				return [True, tuple[1]]

			set = Lang.Datatype.Set(segment)
			if set[0]:
				colored(139, 179, 7, f"[*] DATATYPE : set validated.#>\n{segment}\n")
				return [True, set[1]]

			range = Lang.Datatype.Range(segment)
			if range[0]:
				colored(139, 179, 7, f"[*] DATATYPE : range validated.#>\n{segment}\n")
				return [True, range[1]]

			dictionary = Lang.Datatype.Dictionary(segment)
			if dictionary[0]:
				colored(139, 179, 7,
				        f"[*] DATATYPE : dictionary validated.#>\n{segment}\n")
				return [True, dictionary[1]]

			expression = Lang.Datatype.Expression(segment, scope)
			if expression[0]:
				colored(139, 179, 7,
				        f"[*] DATATYPE : expression validated.#>\n{segment}\n")
				return [True, expression[1]]

			comparison = Lang.Datatype.Comparison(segment)
			if comparison[0]:
				colored(139, 179, 7,
				        f"[*] DATATYPE : comparison validated.#>\n{segment}\n")
				return [True, comparison[1]]

			string = Lang.Datatype.String(segment)
			if string[0]:
				colored(139, 179, 7, f"[*] DATATYPE : string validated.#>\n{segment}\n")
				return [True, string[1]]

			integer = Lang.Datatype.Integer(segment)
			if integer[0]:
				colored(139, 179, 7, f"[*] DATATYPE : integer validated.#>\n{segment}\n")
				return [True, integer[1]]

			float = Lang.Datatype.Float(segment)
			if float[0]:
				colored(139, 179, 7, f"[*] DATATYPE : float validated.#>\n{segment}\n")
				return [True, float[1]]

			boolean = Lang.Datatype.Boolean(segment)
			if boolean[0]:
				colored(139, 179, 7, f"[*] DATATYPE : boolean validated.#>\n{segment}\n")
				return [True, boolean[1]]

			binomial = Lang.Datatype.Binomial(segment)
			if binomial[0]:
				colored(139, 179, 7, f"[*] DATATYPE : binomial validated.#>\n{segment}\n")
				return [True, binomial[1]]

			bit = Lang.Datatype.Bit(segment)
			if bit[0]:
				colored(139, 179, 7, f"[*] DATATYPE : bit validated.#>\n{segment}\n")
				return [True, bit[1]]

			crumb = Lang.Datatype.Crumb(segment)
			if crumb[0]:
				colored(139, 179, 7, f"[*] DATATYPE : crumb validated.#>\n{segment}\n")
				return [True, crumb[1]]

			nonetype = Lang.Datatype.Nonetype(segment)
			if nonetype[0]:
				colored(139, 179, 7, f"[*] DATATYPE : nonetype validated.#>\n{segment}\n")
				return [True, nonetype[1]]

			void = Lang.Datatype.Void(segment)
			if void[0]:
				colored(139, 179, 7, f"[*] DATATYPE : void validated.#>\n{segment}\n")
				return [True]

			unit = Lang.Datatype.Unit(segment)
			if unit[0]:
				colored(139, 179, 7, f"[*] DATATYPE : unit validated.#>\n{segment}\n")
				return [True, unit[1]]

			blank = Lang.Datatype.Blank(segment)
			if blank[0]:
				colored(139, 179, 7, f"[*] DATATYPE : blank validated.#>\n{segment}\n")
				return [True, blank[1]]

			newobject = Lang.Datatype.NewObject(segment, scope)
			if newobject[0]:
				colored(139, 179, 7,
				        f"[*] DATATYPE : new object validated.#>\n{segment}\n")
				return [True, newobject[1]]

			selfpointer = Lang.Datatype.SelfPointer(segment, scope)
			if selfpointer[0]:
				colored(139, 179, 7,
				        f"[*] DATATYPE : self pointer validated.#>\n{segment}\n")
				return [True, selfpointer[1]]

			pointer = Lang.Datatype.Pointer(segment, scope)
			if pointer[0]:
				colored(139, 179, 7,
				        f"[*] DATATYPE : pointer validated.#>\n{segment}\n")
				return [True, pointer[1]]
			else:
				return [False]
				
	class Function:

		##### KEYS #####
		def end(segment, scope=""):
			if "end" in segment and segment.index("end") == 0:
				quit()
			else:
				return [False]

		def alloc(segment, scope=""):
			if "alloc" in segment and segment.index("alloc") == 0:
				global LucaAllocate
				data = segment[len("alloc "):]
				data = data.split(':')

				val = Lang.validate(data[0])
				if val[0]:
					data[0] = val[1]
				else: return [False]

				LucaAllocate[data[1]] = data[0]

				return [True, None]

			else:
				return [False]


		def lucadev(segment, scope=""):
			if "lucadev" in segment and segment.index("lucadev") == 0:
				value = segment[len("lucadev "):]
				colored(26, 37, 237, f"[*] FUNCKEY : lucadev value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					if validate[1] == True:
						developerRead = True
					elif validate[1] == False:
						developerRead = False
					else:
						return [False]
					return [True]
				else:
					return [False]
			else:
				return [False]
		
		
		def outln(segment, scope=""):
			if "outln" in segment and segment.index("outln") == 0:
				value = segment[len("outln "):]
				colored(26, 37, 237, f"[*] FUNCKEY : outln value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					colored(26, 37, 237, f"[*] FUNCKEY : outln output#>")
					colored(26, 37, 237, f" >>> ", '')
					print(validate[1])
					colored(26, 37, 237, f"")
					return [True]
				else:
					return [False]
			else:
				return [False]

		def string(segment, scope=""):
			if "string" in segment and segment.index("string") == 0:
				value = segment[len("string "):]
				colored(26, 37, 237, f"[*] FUNCKEY : string value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, str(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def integer(segment, scope=""):
			if "integer" in segment and segment.index("integer") == 0:
				value = segment[len("integer "):]
				colored(26, 37, 237, f"[*] FUNCKEY : integer value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, int(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def float_(segment, scope=""):
			if "float" in segment and segment.index("float") == 0:
				value = segment[len("float "):]
				colored(26, 37, 237, f"[*] FUNCKEY : float value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, float(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def boolean(segment, scope=""):
			if "boolean" in segment and segment.index("boolean") == 0:
				value = segment[len("boolean "):]
				colored(26, 37, 237, f"[*] FUNCKEY : boolean value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, bool(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def list_(segment, scope=""):
			if "list" in segment and segment.index("list") == 0:
				value = segment[len("list "):]
				colored(26, 37, 237, f"[*] FUNCKEY : list value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, list(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def tuple_(segment, scope=""):
			if "tuple" in segment and segment.index("tuple") == 0:
				value = segment[len("tuple "):]
				colored(26, 37, 237, f"[*] FUNCKEY : tuple value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, tuple(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def set_(segment, scope=""):
			if "set" in segment and segment.index("set") == 0:
				value = segment[len("set "):]
				colored(26, 37, 237, f"[*] FUNCKEY : set value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, set(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def dict_(segment, scope=""):
			if "dict" in segment and segment.index("dict") == 0:
				value = segment[len("dict "):]
				colored(26, 37, 237, f"[*] FUNCKEY : dict value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, dict(validate[1])]
				else:
					return [False, None]
			else:
				return [False, None]

		def return_(segment, scope=""):
			if "return" in segment and segment.index("return") == 0:
				value = segment[len("return "):]
				colored(26, 37, 237, f"[*] FUNCKEY : return value given :#>\n{segment}\n")
				validate = Lang.validate(value, scope)
				if validate[0]:
					return [True, validate[1]]
				else:
					return [False, None]
			else:
				return [False, None]

		##### PARS #####
		def index(segment, scope=""):
			if ('.index(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : index validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.index(')]
				index_parameter = segment[segment.rindex('.index(') +
				                          7:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) == 1:
					return [True, object[index[0]]]
				elif len(index) == 2:
					return [True, object[index[0]:index[1]]]
				elif len(index) == 3:
					return [True, object[index[0]:index[1]:index[2]]]
				else:
					return [False]
			else:
				return [False]

		def append(segment, scope=""):
			if ('.append(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : append validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.append(')]
				index_parameter = segment[segment.rindex('.append(') +
				                          8:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.append(index[0])

				return [True, object]

			else:
				return [False]

		def clear(segment, scope=""):
			if ('.clear(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : clear validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.clear(')]
				index_parameter = segment[segment.rindex('.clear(') +
				                          7:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.clear()

				return [True, object]

			else:
				return [False]

		def copy(segment, scope=""):
			if ('.copy(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : copy validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.copy(')]
				index_parameter = segment[segment.rindex('.copy(') + 6:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.copy()

				return [True, object]

			else:
				return [False]

		def count(segment, scope=""):
			if ('.count(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : count validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.count(')]
				index_parameter = segment[segment.rindex('.count(') +
				                          7:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.count(index[0])

				return [True, object]

			else:
				return [False]

		def extend(segment, scope=""):
			if ('.extend(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : extend validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.extend(')]
				index_parameter = segment[segment.rindex('.extend(') +
				                          8:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.extend(index[0])

				return [True, object]

			else:
				return [False]

		def indexOf(segment, scope=""):
			if ('.indexOf(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : indexOf validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.indexOf(')]
				index_parameter = segment[segment.rindex('.indexOf(') +
				                          9:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.index(index[0])

				return [True, object]

			else:
				return [False]

		def insert(segment, scope=""):
			if ('.insert(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : insert validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.insert(')]
				index_parameter = segment[segment.rindex('.insert(') +
				                          8:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 2:
					return [False]

				object = object.insert(index[0], index[1])

				return [True, object]

			else:
				return [False]

		def pop(segment, scope=""):
			if ('.pop(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : pop validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.pop(')]
				index_parameter = segment[segment.rindex('.pop(') + 5:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.pop(index[0])

				return [True, object]

			else:
				return [False]

		def remove(segment, scope=""):
			if ('.remove(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : pop validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.remove(')]
				index_parameter = segment[segment.rindex('.remove(') +
				                          8:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.remove(index[0])

				return [True, object]

			else:
				return [False]

		def reverse(segment, scope=""):
			if ('.reverse(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : pop validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.reverse(')]
				index_parameter = segment[segment.rindex('.reverse(') +
				                          9:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.reverse()

				return [True, object]

			else:
				return [False]

		def capitalize(segment, scope=""):
			if ('.capitalize(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : capitalize validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.capitalize(')]
				index_parameter = segment[segment.rindex('.capitalize(') +
				                          11:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None])

				object = object.capitalize()

				return [True, object]

			else:
				return [False]

		def casefold(segment, scope=""):
			if ('.casefold(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : casefold validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.casefold(')]
				index_parameter = segment[segment.rindex('.casefold(') +
				                          10:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				object = object.casefold()

				return [True, object]

			else:
				return [False]

		def center(segment, scope=""):
			if ('.center(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : center validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.center(')]
				index_parameter = segment[segment.rindex('.center(') +
				                          8:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 2:
					return [False]

				index.extend([None, None, None, None])

				object = object.center(index[0], index[1])

				return [True, object]

			else:
				return [False]

		def encode(segment, scope=""):
			if ('.encode(' in segment and ')' in segment):
				colored(26, 37, 237, f"[*] FUNCPAR : encode validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.encode(')]
				index_parameter = segment[segment.rindex('.encode(') +
				                          8:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 2:
					return [False]

				index.extend([None, None, None, None])

				object = object.count(index[0], index[1])

				return [True, object]

			else:
				return [False]

		def endswith(segment, scope=""):
			if ('.endswith(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : endswith validating... #>\n{segment}\n")
				object = segment[:segment.rindex('.endswith(')]
				index_parameter = segment[segment.rindex('.endswith(') +
				                          10:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 3:
					return [False]

				index.extend([None, None, None, None])

				object = object.endswith(index[0], index[1], index[2])

				return [True, object]

			else:
				return [False]

		def expandtabs(segment, scope=""):
			if ('.expandtabs(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : expandtabs validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.expandtabs(')]
				index_parameter = segment[segment.rindex('.expandtabs(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.expandtabs(index[0])

				return [True, object]

			else:
				return [False]

		def find(segment, scope=""):
			if ('.find(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : find validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.find(')]
				index_parameter = segment[segment.rindex('.find(') + 2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.find(index[0], index[1], index[2])

				return [True, object]

			else:
				return [False]

		def isalnum(segment, scope=""):
			if ('.isalnum(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isalnum validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isalnum(')]
				index_parameter = segment[segment.rindex('.isalnum(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isalnum(index[0])

				return [True, object]

			else:
				return [False]

		def isalpha(segment, scope=""):
			if ('.isalpha(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isalpha validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isalpha(')]
				index_parameter = segment[segment.rindex('.isalpha(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isalpha(index[0])

				return [True, object]

			else:
				return [False]

		def isdecimal(segment, scope=""):
			if ('.isdecimal(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isdecimal validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isdecimal(')]
				index_parameter = segment[segment.rindex('.isdecimal(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isdecimal(index[0])

				return [True, object]

			else:
				return [False]

		def isdigit(segment, scope=""):
			if ('.isdigit(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isdigit validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isdigit(')]
				index_parameter = segment[segment.rindex('.isdigit(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isdigit(index[0])

				return [True, object]

			else:
				return [False]

		def isidentifier(segment, scope=""):
			if ('.isidentifier(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isidentifier validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isidentifier(')]
				index_parameter = segment[segment.rindex('.isidentifier(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isidentifier(index[0])

				return [True, object]

			else:
				return [False]

		def islower(segment, scope=""):
			if ('.islower(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : islower validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.islower(')]
				index_parameter = segment[segment.rindex('.islower(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.islower(index[0])

				return [True, object]

			else:
				return [False]

		def isnumeric(segment, scope=""):
			if ('.isnumeric(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isnumeric validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isnumeric(')]
				index_parameter = segment[segment.rindex('.isnumeric(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isnumeric(index[0])

				return [True, object]

			else:
				return [False]

		def isprintable(segment, scope=""):
			if ('.isprintable(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isprintable validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isprintable(')]
				index_parameter = segment[segment.rindex('.isprintable(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isprintable(index[0])

				return [True, object]

			else:
				return [False]

		def isspace(segment, scope=""):
			if ('.isspace(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isspace validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isspace(')]
				index_parameter = segment[segment.rindex('.isspace(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isspace(index[0])

				return [True, object]

			else:
				return [False]

		def istitle(segment, scope=""):
			if ('.istitle(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : istitle validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.istitle(')]
				index_parameter = segment[segment.rindex('.istitle(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.istitle(index[0])

				return [True, object]

			else:
				return [False]

		def isupper(segment, scope=""):
			if ('.isupper(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isupper validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.isupper(')]
				index_parameter = segment[segment.rindex('.isupper(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.isupper(index[0])

				return [True, object]

			else:
				return [False]

		def join(segment, scope=""):
			if ('.join(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : join validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.join(')]
				index_parameter = segment[segment.rindex('.join(') + 2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.join(index[0])

				return [True, object]

			else:
				return [False]

		def ljust(segment, scope=""):
			if ('.ljust(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : ljust validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.ljust(')]
				index_parameter = segment[segment.rindex('.ljust(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.ljust(index[0], index[1])

				return [True, object]

			else:
				return [False]

		def lower(segment, scope=""):
			if ('.lower(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : lower validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.lower(')]
				index_parameter = segment[segment.rindex('.lower(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.lower(index[0])

				return [True, object]

			else:
				return [False]

		def lstrip(segment, scope=""):
			if ('.lstrip(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : lstrip validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.lstrip(')]
				index_parameter = segment[segment.rindex('.lstrip(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.lstrip(index[0])

				return [True, object]

			else:
				return [False]

		def maketrans(segment, scope=""):
			if ('.maketrans(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : maketrans validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.maketrans(')]
				index_parameter = segment[segment.rindex('.maketrans(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.maketrans(index[0], index[1], index[2])

				return [True, object]

			else:
				return [False]

		def partition(segment, scope=""):
			if ('.partition(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : partition validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.partition(')]
				index_parameter = segment[segment.rindex('.partition(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.partition(index[0])

				return [True, object]

			else:
				return [False]

		def rfind(segment, scope=""):
			if ('.rfind(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rfind validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.rfind(')]
				index_parameter = segment[segment.rindex('.rfind(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.rfind(index[0], index[1], index[2])

				return [True, object]

			else:
				return [False]

		def rindex(segment, scope=""):
			if ('.rindex(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rindex validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.rindex(')]
				index_parameter = segment[segment.rindex('.rindex(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.rindex(index[0], index[1], index[2])

				return [True, object]

			else:
				return [False]

		def rjust(segment, scope=""):
			if ('.rjust(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rjust validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.rjust(')]
				index_parameter = segment[segment.rindex('.rjust(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.rjust(index[0], index[1])

				return [True, object]

			else:
				return [False]

		def rpartition(segment, scope=""):
			if ('.rpartition(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rpartition validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.rpartition(')]
				index_parameter = segment[segment.rindex('.rpartition(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.rpartition(index[0])

				return [True, object]

			else:
				return [False]

		def rsplit(segment, scope=""):
			if ('.rsplit(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rsplit validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.rsplit(')]
				index_parameter = segment[segment.rindex('.rsplit(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.rsplit(index[0], index[1])

				return [True, object]

			else:
				return [False]

		def rstrip(segment, scope=""):
			if ('.rstrip(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rstrip validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.rstrip(')]
				index_parameter = segment[segment.rindex('.rstrip(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.rstrip(index[0])

				return [True, object]

			else:
				return [False]

		def split(segment, scope=""):
			if ('.split(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : split validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.split(')]
				index_parameter = segment[segment.rindex('.split(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.split(index[0], index[1])

				return [True, object]

			else:
				return [False]

		def splitlines(segment, scope=""):
			if ('.splitlines(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : splitlines validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.splitlines(')]
				index_parameter = segment[segment.rindex('.splitlines(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.splitlines(index[0])

				return [True, object]

			else:
				return [False]

		def startswith(segment, scope=""):
			if ('.startswith(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : startswith validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.startswith(')]
				index_parameter = segment[segment.rindex('.startswith(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.startswith(index[0], index[1], index[2])

				return [True, object]

			else:
				return [False]

		def strip(segment, scope=""):
			if ('.strip(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : strip validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.strip(')]
				index_parameter = segment[segment.rindex('.strip(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.strip(index[0])

				return [True, object]

			else:
				return [False]

		def swapcase(segment, scope=""):
			if ('.swapcase(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : swapcase validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.swapcase(')]
				index_parameter = segment[segment.rindex('.swapcase(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.swapcase(index[0])

				return [True, object]

			else:
				return [False]

		def title(segment, scope=""):
			if ('.title(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : title validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.title(')]
				index_parameter = segment[segment.rindex('.title(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.title(index[0])

				return [True, object]

			else:
				return [False]

		def translate(segment, scope=""):
			if ('.translate(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : translate validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.translate(')]
				index_parameter = segment[segment.rindex('.translate(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.translate(index[0])

				return [True, object]

			else:
				return [False]

		def upper(segment, scope=""):
			if ('.upper(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : upper validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.upper(')]
				index_parameter = segment[segment.rindex('.upper(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.upper(index[0])

				return [True, object]

			else:
				return [False]

		def zfill(segment, scope=""):
			if ('.zfill(' in segment and ')' in segment):
				colored(26, 37, 237,
				        f"[*] FUNCPAR : zfill validating... #>\n" + segment + "\n")
				object = segment[:segment.rindex('.zfill(')]
				index_parameter = segment[segment.rindex('.zfill(') +
				                          2:segment.rindex(')')]
				index_parameter = index_parameter.split(':')

				index = []
				for integer in index_parameter:
					val = Lang.validate(integer)
					if val[0]:
						index.append(val[1])
					else:
						return [False]

				val = Lang.validate(object)
				if val[0]:
					object = val[1]
				else:
					return [False]

				if len(index) > 1:
					return [False]

				index.extend([None, None, None, None, None])

				object = object.zfill(index[0])

				return [True, object]

			else:
				return [False]

		def FUNCTIONDEFINED(segment, scope=""):
			global LucaDefine
			if "(" in segment and ")" in segment:
				name = segment[:segment.index('(')]
				parameters = segment[segment.index('(') + 1:segment.index(")")].split(":")

				if name in LucaDefine:
					defined = LucaDefine[name]
				else:
					return [False]

				pos = 0
				for each in defined[0]:
					val = Lang.validate(parameters[pos])
					if val[0]:
						parameters[pos] = val[1]
					else:
						return [False]

					LucaStored[defined[0][pos]] = parameters[pos]
					pos += 1

				returned = Lang(defined[1])

				for each in defined[0]:
					LucaStored.pop(each)

				return [True, returned]
			else:
				return [False]
		
		def __new__(self, segment, scope=""):

			# KEYS
			endkeyfunc = Lang.Function.end(segment, scope)
			if endkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : end validated.#>\n{segment}\n")
				return [True, None]

			allockeyfunc = Lang.Function.alloc(segment, scope)
			if allockeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : alloc validated.#>\n{segment}\n")
				return [True, None]

			lucadevkeyfunc = Lang.Function.lucadev(segment, scope)
			if lucadevkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : lucadev validated.#>\n{segment}\n")
				return [True, None]

			returnkeyfunc = Lang.Function.return_(segment, scope)
			if returnkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : return validated.#>\n{segment}\n")
				return [True, returnkeyfunc[1], "return point"]

			outlnkeyfunc = Lang.Function.outln(segment, scope)
			if outlnkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : outln validated.#>\n{segment}\n")
				return [True, None]

			stringkeyfunc = Lang.Function.string(segment, scope)
			if stringkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : string validated.#>\n{segment}\n")
				return [True, stringkeyfunc[1]]

			integerkeyfunc = Lang.Function.integer(segment, scope)
			if integerkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : integer validated.#>\n{segment}\n")
				return [True, integerkeyfunc[1]]

			floatkeyfunc = Lang.Function.float_(segment, scope)
			if floatkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : float validated.#>\n{segment}\n")
				return [True, floatkeyfunc[1]]

			booleankeyfunc = Lang.Function.boolean(segment, scope)
			if booleankeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : boolean validated.#>\n{segment}\n")
				return [True, booleankeyfunc[1]]

			listkeyfunc = Lang.Function.list_(segment, scope)
			if listkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : list validated.#>\n{segment}\n")
				return [True, listkeyfunc[1]]

			tuplekeyfunc = Lang.Function.tuple_(segment, scope)
			if tuplekeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : tuple validated.#>\n{segment}\n")
				return [True, tuplekeyfunc[1]]

			setkeyfunc = Lang.Function.set_(segment, scope)
			if setkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : set validated.#>\n{segment}\n")
				return [True, setkeyfunc[1]]

			dictkeyfunc = Lang.Function.dict_(segment, scope)
			if dictkeyfunc[0]:
				colored(26, 37, 237, f"[*] FUNCKEY : dict validated.#>\n{segment}\n")
				return [True, dictkeyfunc[1]]

			# PAREN
			indexparfunc = Lang.Function.index(segment, scope)
			if indexparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : index validated.#>\n{segment}\n")
				return [True, indexparfunc[1]]

			reverseparfunc = Lang.Function.reverse(segment, scope)
			if reverseparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : reverse validated.#>\n{segment}\n")
				return [True, reverseparfunc[1]]

			capitalizeparfunc = Lang.Function.capitalize(segment, scope)
			if capitalizeparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : capitalize validated.#>\n{segment}\n")
				return [True, capitalizeparfunc[1]]

			casefoldparfunc = Lang.Function.casefold(segment, scope)
			if casefoldparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : casefold validated.#>\n{segment}\n")
				return [True, casefoldparfunc[1]]

			centerparfunc = Lang.Function.center(segment, scope)
			if centerparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : center validated.#>\n{segment}\n")
				return [True, centerparfunc[1]]

			encodeparfunc = Lang.Function.encode(segment, scope)
			if encodeparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : encode validated.#>\n{segment}\n")
				return [True, encodeparfunc[1]]

			endswithparfunc = Lang.Function.endswith(segment, scope)
			if endswithparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : endswith validated.#>\n{segment}\n")
				return [True, endswithparfunc[1]]

			removeparfunc = Lang.Function.remove(segment, scope)
			if removeparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : remove validated.#>\n{segment}\n")
				return [True, removeparfunc[1]]

			popparfunc = Lang.Function.pop(segment, scope)
			if popparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : pop validated.#>\n{segment}\n")
				return [True, popparfunc[1]]

			appendparfunc = Lang.Function.append(segment, scope)
			if appendparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : append validated.#>\n{segment}\n")
				return [True, appendparfunc[1]]

			clearparfunc = Lang.Function.clear(segment, scope)
			if clearparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : clear validated.#>\n{segment}\n")
				return [True, clearparfunc[1]]

			copyparfunc = Lang.Function.copy(segment, scope)
			if copyparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : copy validated.#>\n{segment}\n")
				return [True, copyparfunc[1]]

			countparfunc = Lang.Function.count(segment, scope)
			if countparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : count validated.#>\n{segment}\n")
				return [True, countparfunc[1]]

			extendparfunc = Lang.Function.extend(segment, scope)
			if extendparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : extend validated.#>\n{segment}\n")
				return [True, extendparfunc[1]]

			indexofparfunc = Lang.Function.indexOf(segment, scope)
			if indexofparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : indexOf validated.#>\n{segment}\n")
				return [True, indexofparfunc[1]]

			insertofparfunc = Lang.Function.insert(segment, scope)
			if insertofparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : insert validated.#>\n{segment}\n")
				return [True, insertofparfunc[1]]

			expandtabsparfunc = Lang.Function.expandtabs(segment, scope)
			if expandtabsparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : expandtabs validated.#>\n" + segment + "\n")
				return [True, expandtabsparfunc[1]]

			findparfunc = Lang.Function.find(segment, scope)
			if findparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : find validated.#>\n" + segment + "\n")
				return [True, findparfunc[1]]

			isalnumparfunc = Lang.Function.isalnum(segment, scope)
			if isalnumparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isalnum validated.#>\n" + segment + "\n")
				return [True, isalnumparfunc[1]]

			isalphaparfunc = Lang.Function.isalpha(segment, scope)
			if isalphaparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isalpha validated.#>\n" + segment + "\n")
				return [True, isalphaparfunc[1]]

			isdecimalparfunc = Lang.Function.isdecimal(segment, scope)
			if isdecimalparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isdecimal validated.#>\n" + segment + "\n")
				return [True, isdecimalparfunc[1]]

			isdigitparfunc = Lang.Function.isdigit(segment, scope)
			if isdigitparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isdigit validated.#>\n" + segment + "\n")
				return [True, isdigitparfunc[1]]

			isidentifierparfunc = Lang.Function.isidentifier(segment, scope)
			if isidentifierparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isidentifier validated.#>\n" + segment + "\n")
				return [True, isidentifierparfunc[1]]

			islowerparfunc = Lang.Function.islower(segment, scope)
			if islowerparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : islower validated.#>\n" + segment + "\n")
				return [True, islowerparfunc[1]]

			isnumericparfunc = Lang.Function.isnumeric(segment, scope)
			if isnumericparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isnumeric validated.#>\n" + segment + "\n")
				return [True, isnumericparfunc[1]]

			isprintableparfunc = Lang.Function.isprintable(segment, scope)
			if isprintableparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isprintable validated.#>\n" + segment + "\n")
				return [True, isprintableparfunc[1]]

			isspaceparfunc = Lang.Function.isspace(segment, scope)
			if isspaceparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isspace validated.#>\n" + segment + "\n")
				return [True, isspaceparfunc[1]]

			istitleparfunc = Lang.Function.istitle(segment, scope)
			if istitleparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : istitle validated.#>\n" + segment + "\n")
				return [True, istitleparfunc[1]]

			isupperparfunc = Lang.Function.isupper(segment, scope)
			if isupperparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : isupper validated.#>\n" + segment + "\n")
				return [True, isupperparfunc[1]]

			joinparfunc = Lang.Function.join(segment, scope)
			if joinparfunc[0]:
				colored(26, 37, 237, f"[*] FUNCPAR : join validated.#>\n" + segment + "\n")
				return [True, joinparfunc[1]]

			ljustparfunc = Lang.Function.ljust(segment, scope)
			if ljustparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : ljust validated.#>\n" + segment + "\n")
				return [True, ljustparfunc[1]]

			lowerparfunc = Lang.Function.lower(segment, scope)
			if lowerparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : lower validated.#>\n" + segment + "\n")
				return [True, lowerparfunc[1]]

			lstripparfunc = Lang.Function.lstrip(segment, scope)
			if lstripparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : lstrip validated.#>\n" + segment + "\n")
				return [True, lstripparfunc[1]]

			maketransparfunc = Lang.Function.maketrans(segment, scope)
			if maketransparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : maketrans validated.#>\n" + segment + "\n")
				return [True, maketransparfunc[1]]

			partitionparfunc = Lang.Function.partition(segment, scope)
			if partitionparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : partition validated.#>\n" + segment + "\n")
				return [True, partitionparfunc[1]]

			rfindparfunc = Lang.Function.rfind(segment, scope)
			if rfindparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rfind validated.#>\n" + segment + "\n")
				return [True, rfindparfunc[1]]

			rindexparfunc = Lang.Function.rindex(segment, scope)
			if rindexparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rindex validated.#>\n" + segment + "\n")
				return [True, rindexparfunc[1]]

			rjustparfunc = Lang.Function.rjust(segment, scope)
			if rjustparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rjust validated.#>\n" + segment + "\n")
				return [True, rjustparfunc[1]]

			rpartitionparfunc = Lang.Function.rpartition(segment, scope)
			if rpartitionparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rpartition validated.#>\n" + segment + "\n")
				return [True, rpartitionparfunc[1]]

			rsplitparfunc = Lang.Function.rsplit(segment, scope)
			if rsplitparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rsplit validated.#>\n" + segment + "\n")
				return [True, rsplitparfunc[1]]

			rstripparfunc = Lang.Function.rstrip(segment, scope)
			if rstripparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : rstrip validated.#>\n" + segment + "\n")
				return [True, rstripparfunc[1]]

			splitparfunc = Lang.Function.split(segment, scope)
			if splitparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : split validated.#>\n" + segment + "\n")
				return [True, splitparfunc[1]]

			splitlinesparfunc = Lang.Function.splitlines(segment, scope)
			if splitlinesparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : splitlines validated.#>\n" + segment + "\n")
				return [True, splitlinesparfunc[1]]

			startswithparfunc = Lang.Function.startswith(segment, scope)
			if startswithparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : startswith validated.#>\n" + segment + "\n")
				return [True, startswithparfunc[1]]

			stripparfunc = Lang.Function.strip(segment, scope)
			if stripparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : strip validated.#>\n" + segment + "\n")
				return [True, stripparfunc[1]]

			swapcaseparfunc = Lang.Function.swapcase(segment, scope)
			if swapcaseparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : swapcase validated.#>\n" + segment + "\n")
				return [True, swapcaseparfunc[1]]

			titleparfunc = Lang.Function.title(segment, scope)
			if titleparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : title validated.#>\n" + segment + "\n")
				return [True, titleparfunc[1]]

			translateparfunc = Lang.Function.translate(segment, scope)
			if translateparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : translate validated.#>\n" + segment + "\n")
				return [True, translateparfunc[1]]

			upperparfunc = Lang.Function.upper(segment, scope)
			if upperparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : upper validated.#>\n" + segment + "\n")
				return [True, upperparfunc[1]]

			zfillparfunc = Lang.Function.zfill(segment, scope)
			if zfillparfunc[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : zfill validated.#>\n" + segment + "\n")
				return [True, zfillparfunc[1]]

			FUNCTIONDEFINEDPAR = Lang.Function.FUNCTIONDEFINED(segment, scope)
			if FUNCTIONDEFINEDPAR[0]:
				colored(26, 37, 237,
				        f"[*] FUNCPAR : defined function validated.#>\n" + segment + "\n")
				return [True, FUNCTIONDEFINEDPAR[1]]
			else:
				return [False]
				
	class Statements:

		def Empty(segment):
			if segment.startswith('{') and segment.endswith('}'):
				Lang(segment[1:-1])
				return [True, None]
			else:
				return [False]

		def If(segment):
			if segment.startswith("if ") and segment.endswith('}'):
				if ('(' in segment and segment.index('(') == len('if ')) and (
				  ')' in segment and segment.index(')') < segment.index('{')):
					global last_condition
					colored(219, 116, 20,
					        f"[?] STATEMENT : if statement validation... #>\n{segment}\n")
					condition = segment[segment.index('(') + 1:segment.index(')')]
					try:
						execution = segment[segment.index('{') + 1:segment.rindex('}')]
					except:
						return [False]

					validate = Lang.validate(condition)
					if validate[0]:
						condition = validate[1]
					else:
						return [False]

					if condition == True:
						Lang(execution)
						last_condition = True
						return [True]
					else:
						last_condition = False
						return [True]
				else:
					return [False]
			else:
				return [False]

		def ElseIf(segment):
			if segment.startswith("elseif ") and segment.endswith('}'):
				if ('(' in segment and segment.index('(') == len('elseif ')) and (
				  ')' in segment and segment.index(')') < segment.index('{')):
					global last_condition
					colored(
					 219, 116, 20,
					 f"[?] STATEMENT : elseif statement validation... #>\n{segment}\n")
					condition = segment[segment.index('(') + 1:segment.index(')')]
					try:
						execution = segment[segment.index('{') + 1:segment.rindex('}')]
					except:
						return [False]

					validate = Lang.validate(condition)
					if validate[0]:
						condition = validate[1]
					else:
						return [False]

					if last_condition == False:
						if condition == True:
							Lang(execution)
							last_condition = True
							return [True]
						else:
							last_condition = False
							return [True]
					else:
						return [True]
				else:
					return [False]
			else:
				return [False]

		def Else(segment):
			if segment.startswith("else ") and segment.endswith('}'):
				global last_condition
				colored(219, 116, 20,
				        f"[?] STATEMENT : else statement validation... #>\n{segment}\n")
				try:
					execution = segment[segment.index('{') + 1:segment.rindex('}')]
				except:
					return [False]

				if last_condition == False:
					Lang(execution)
					last_condition = None
					return [True]
				elif last_condition == True:
					last_condition = None
					return [True]
				else:
					return [False]
			else:
				return [False]
				
		def While(segment):
			if segment.startswith("while ") and segment.endswith('}'):
				if ('(' in segment and segment.index('(') == len('while ')) and (
				  ')' in segment and segment.index(')') < segment.index('{')):
					global last_condition
					colored(219, 116, 20,
					        f"[?] STATEMENT : while statement validation... #>\n{segment}\n")
					condition = segment[segment.index('(') + 1:segment.index(')')]
					try:
						execution = segment[segment.index('{') + 1:segment.rindex('}')]
					except:
						return [False]

					validate = Lang.validate(condition)
					if validate[0]:
						condition = validate[1]
					else:
						return [False]

					while condition == True:
						Lang(execution)
						last_condition = True

						condition = segment[segment.index('(') + 1:segment.index(')')]
						validate = Lang.validate(condition)
						if validate[0]:
							condition = validate[1]
						else:
							return [False]
					else:
						last_condition = False
						return [True]
				else:
					return [False]
			else:
				return [False]
				
		def For(segment):
			if segment.startswith("for ") and segment.endswith('}'):
				if ('(' in segment and segment.index('(') == len('for ')) and (
				  ')' in segment and segment.index(')') < segment.index('{')):
					global last_condition
					colored(219, 116, 20,
					        f"[?] STATEMENT : for statement validation... #>\n{segment}\n")
					condition = segment[segment.index('(') + 1:segment.index(')')]
					try:
						execution = segment[segment.index('{') + 1:segment.rindex('}')]
					except:
						return [False]

					condition = condition.split('in')

					condition[0] = condition[0].strip()
					condition[1] = condition[1].strip()

					validate = Lang.validate(condition[0])
					if validate[0]:
						condition[0] = validate[1]
					else:
						if condition[0].isidentifier():
							pass
						else:
							return [False]

					validate = Lang.validate(condition[1])
					if validate[0]:
						condition[1] = validate[1]
					else:
						return [False]

					for item in condition[1]:
						LucaStored[condition[0]] = condition[1][condition[1].index(item)]
						Lang(execution)
						last_condition = True
					return [True]
				else:
					return [False]
			else:
				return [False]

		def RepeatUntil(segment):
			if segment.startswith("repeat until ") and segment.endswith('}'):
				if ('(' in segment and segment.index('(') == len('repeat until ')) and (
				  ')' in segment and segment.index(')') < segment.index('{')):
					global last_condition
					colored(
					 219, 116, 20,
					 f"[?] STATEMENT : repeat until statement validation... #>\n{segment}\n")
					condition = segment[segment.index('(') + 1:segment.index(')')]
					try:
						execution = segment[segment.index('{') + 1:segment.rindex('}')]
					except:
						return [False]

					validate = Lang.validate(condition)
					if validate[0]:
						condition = validate[1]
					else:
						return [False]

					while condition == False:
						Lang(execution)
						last_condition = True

						condition = segment[segment.index('(') + 1:segment.index(')')]
						validate = Lang.validate(condition)
						if validate[0]:
							condition = validate[1]
						else:
							return [False]
					else:
						last_condition = False
						return [True]
				else:
					return [False]
			else:
				return [False]

		def Function(segment):
			if segment.startswith("function ") and segment.endswith('}'):
				if ('(' in segment and ')' in segment
				    and segment.index(')') < segment.index('{')):
					global last_condition
					colored(
					 219, 116, 20,
					 f"[?] STATEMENT : function statement validation... #>\n{segment}\n")

					functionname = segment[segment.index(" ") + 1:segment.index('(')]
					parameters = segment[segment.index('(') + 1:segment.index(')')]
					try:
						execution = segment[segment.index('{') + 1:segment.rindex('}')]
					except:
						return [False]

					LucaDefine[functionname] = [parameters.split(':'), execution]

					return [True, None]
				else:
					return [False]
			else:
				return [False]

		def Namespace(segment, scope=""):
			if segment.startswith('namespace '):
				colored(
					 219, 116, 20,
					 f"[?] STATEMENT : namespace statement validation... #>\n{segment}\n")
				global LucaClasses
				classname = segment[len('namespace '):segment.index('{')]
				try:
					body      = segment[segment.index('{')+1:segment.rindex('}')]
				except:
					return [False]

				while classname.startswith(' '):
					classname = classname[1:]
				while classname.endswith(' '):
					classname = classname[:-1]

				if classname.isidentifier() == False:
					return [False]
					
				if scope == "":
					LucaClasses[classname] = {
						"<classname>":classname,
					}
					Lang(body, classname)
				else:
					dir = LucaClasses
					scope = scope.split('.')
					for name in scope:
						dir = dir[name]
					dir[classname] = {
						"<classname>":classname,
					} 
					scoop = ".".join(scope)
					Lang(body, f"{scoop}.{classname}")

				return [True, None]
			else:
				return [False]

		def Class(segment, scope=""):
			if segment.startswith('class '):
				colored(
					 219, 116, 20,
					 f"[?] STATEMENT : class statement validation... #>\n{segment}\n")
				global LucaClasses
				classname = segment[len('class '):segment.index('{')]
				try:
					body      = segment[segment.index('{')+1:segment.rindex('}')]
				except:
					return [False]

				while classname.startswith(' '):
					classname = classname[1:]
				while classname.endswith(' '):
					classname = classname[:-1]

				if classname.isidentifier() == False:
					return [False]
					
				if scope == "":
					LucaClasses[classname] = {
						"<classname>":classname,
					}
					colored(
					 219, 116, 20,
					 f"[?] STATEMENT : class statement returned scope: #>\n{classname}\n")
					Lang(body, classname)
				else:
					dir = LucaClasses
					scope = scope.split('.')
					for name in scope:
						dir = dir[name]
					dir[classname] = {
						"<classname>":classname,
					} 
					scoop = ".".join(scope)
					Lang(body, f"{scoop}.{classname}")

				return [True, LucaClasses[classname]]
			else:
				return [False]

		def Initial(segment, scope=""):
			if segment.startswith("initial ") and '(' in segment and ')' in segment and segment.endswith('}'):
				parameter = segment[segment.index('(')+1:segment.index(')')]
				parameter = parameter.split(':')

				body = segment[segment.index('{')+1:segment.rindex('}')]

				if scope == "":
					return [False]
				else:
					dir = LucaClasses
					scope = scope.split(".")
					for name in scope:
						dir = dir[name]

					pos = 0
					for item in parameter:
						parameter[pos] = [parameter[pos], None]
						pos += 1
					
					dir = dir.update({"<__init__>":[dict(parameter), body]})

				return [True, None]
			else:
				return [False]

		def Construct(segment, scope=""):
			if segment.startswith("construct ") and '(' in segment and ')' in segment and segment.endswith('}'):
				parameter = segment[segment.index('(')+1:segment.index(')')]
				parameter = parameter.split(':')

				body = segment[segment.index('{')+1:segment.rindex('}')]

				if scope == "":
					return [False]
				else:
					dir = LucaClasses
					scope = scope.split(".")
					for name in scope:
						dir = dir[name]

					pos = 0
					for item in parameter:
						parameter[pos] = [parameter[pos], None]
						pos += 1
					
					dir = dir.update({"<__constr__>":[dict(parameter), body]})

				return [True, None]
			else:
				return [False]

		def Method(segment, scope=""):
			if segment.startswith('method ') and segment.endswith('}'):
				methodname = segment[len('method '):segment.index('{')]
				methodname = methodname.strip()

				mname = methodname[:methodname.index('(')]
				parameters = methodname[methodname.index('(')+1:methodname.index(')')].split(':')
				body = segment[segment.index('{')+1:segment.rindex('}')] 

				colored(
				 166, 20, 219,
				 f"[*] STATEMENT : method statement recieved scope : #>\n{scope}\n")

				if scope == "":
					return [False]
				
				scope = scope.split('.')

				global LucaClasses

				dir = LucaClasses
				for name in scope:
					dir = dir[name]

				parms = {}
				for each in parameters:
					parms.update({each:None})

				parameters = parms

				dir.update({mname:{'<method>':[parameters, body]}})

				return [True, None]
			else:
				return [False]


		def __new__(self, segment, scope=""):
			empty_ 			= Lang.Statements.Empty(segment)
			if_ 			= Lang.Statements.If(segment)
			elseif_ 		= Lang.Statements.ElseIf(segment)
			else_ 			= Lang.Statements.Else(segment)
			while_ 			= Lang.Statements.While(segment)
			for_ 			= Lang.Statements.For(segment)
			repeatuntil_ 	= Lang.Statements.RepeatUntil(segment)
			function_ 		= Lang.Statements.Function(segment)
			namespace_ 		= Lang.Statements.Namespace(segment, scope)
			class_ 			= Lang.Statements.Class(segment, scope)
			initial_ 		= Lang.Statements.Initial(segment, scope)
			construct_	    = Lang.Statements.Construct(segment, scope)
			method_ 		= Lang.Statements.Method(segment, scope)

			if   empty_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : if statement validated.#>\n{segment}\n")
				return [True, None]
			elif   if_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : if statement validated.#>\n{segment}\n")
				return [True, None]
			elif elseif_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : elseif statement validated.#>\n{segment}\n")
				return [True, None]
			elif else_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : else statement validated.#>\n{segment}\n")
				return [True, None]
			elif while_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : while statement validated.#>\n{segment}\n")
				return [True, None]
			elif for_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : for statement validated.#>\n{segment}\n")
				return [True, None]
			elif repeatuntil_[0]:
				colored(
				 166, 20, 219,
				 f"[*] STATEMENT : repeat until statement validated.#>\n{segment}\n")
				return [True, None]
			elif function_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : function statement validated.#>\n{segment}\n")
				return [True, None]
			elif namespace_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : namespace statement validated.#>\n{segment}\n")
				return [True, None]
			elif class_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : class statement validated.#>\n{segment}\n")
				return [True, class_[1]]
			elif initial_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : initial statement validated.#>\n{segment}\n")
				return [True, None]
			elif construct_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : construct statement validated.#>\n{segment}\n")
				return [True, None]
			elif method_[0]:
				colored(166, 20, 219,
				        f"[*] STATEMENT : method statement validated.#>\n{segment}\n")
				return [True, None]
			else:
				return [False]
				
	
	class Bracket:

		def __new__(self, segment, scope=""):

			# STEP 1: Check '{' before ';'
			for char in segment:
				if char == "{":
					colored(40, 212, 120,
					        "[?] BRACKET : caught \'{\', continue...#>\n" + segment + "\n")
					break
				elif char == ';':
					colored(40, 212, 120, f"[X] BRACKET : caught \';\'#>\n{segment}\n")
					return [False]

			# STEP 2: Check if '{' are closed
			bracket, lastclosed = '0', 0
			colored(40, 212, 120,
			        f"[?] BRACKET : now open-closed checking...#>\n{segment}\n")
			for char in segment:
				if char == '{':
					colored(40, 212, 120,
					        "[*] BRACKET : '{' is opened...#>\n" + segment + "\n")
					bracket = int(bracket) + 1
				elif char == '}' and type(bracket) != str:
					colored(40, 212, 120,
					        "[*] BRACKET : '}' is closed.  #>\n" + segment + "\n")
					bracket -= 1
					lastclosed += 1
				else:  # log("pass... : " + char)
					pass
				if type(bracket) == int and bracket == 0:
					colored(40, 212, 120,
					        f"[*] BRACKET : brackets are lassoed closed...#>\n{segment}\n")
					break
			if bracket != 0 or type(bracket) == str:
				colored(40, 212, 120,
				        f"[X] BRACKET : brackets are loose...#>\n{segment}\n")
				return [False]

			# STEP 3: Save last '}' from last step.
			buffer = find_nth(segment, '}', lastclosed)

			# STEP 4: Executes before buffer, and returns after buffer
			execute = segment[:buffer + 1]
			returned = segment[buffer + 1:]

			execute = Lang.validate(execute, scope)
			if execute[0]:
				colored(40, 212, 120, f"[*] BRACKET : bracket validated. #>\n{segment}\n")
				execute = execute[1]
			else:
				return [False]

			colored(40, 212, 120, f"[*] BRACKET : following returned code : #>\n{returned}\n")

			# Execute 'execute' after programming if, elseif, else statement
			return [True, returned]

	class Column:

		def __new__(self, segment, scope=""):

			if ";" in segment:
				returned = segment[segment.index(';') + 1:]
				segment = segment[:segment.index(';')]
			else:
				returned = ""

			validate = Lang.validate(segment, scope)
			if validate[0]:
				try:
					return [True, returned, validate[1], validate[2]]
				except:
					return [True, returned]
			else:
				return [False]

	def __new__(self, segment, scope=""):
		global last_condition
		segment = segment.replace('\n', '')
		segment = segment.replace('\t', '')
		while True:
			if segment.startswith(' '):
				while segment.startswith(' '):
					segment = segment[1:]

			bracket = Lang.Bracket(segment, scope)

			if segment == '':
				break

			if bracket[0]:
				segment = bracket[1]
				colored(
					 219, 116, 20,
					 f"[*] LANG : new code returned #>\n{segment}\n")
				
			elif bracket[0] == False:

				column = Lang.Column(segment, scope)
				if column[0]:
					try:
						if column[3] == "return point":
							return column[2]
						else:
							pass
					except:
						pass
					segment = column[1]
					colored(
						219, 116, 20,
						f"[*] LANG : new code returned #>\n{segment}\n")
				else:
					seterror('is not a valid syntax', segment)
					print(error)
					break
					
			else:
				seterror('main method is not found.', segment)
				print(error)
				break

		return None

import traceback
from pprint import pprint

try:
	Lang(script)
except Exception:
    pass

print('\nClasses : ')
pprint(LucaClasses, indent=0.5)
print()

print('\nCreated : ')
pprint(LucaCreated, indent=0.5)
print()

print('\nDefined : ')
print(LucaDefine)
print()

print('\nStored : ')
print(LucaStored)
print()
""""""
