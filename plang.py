# RAM LIMITADA 512 números de 32 bits
# evitar cosas raras
# no existe entrada de usuario

import math

class Vars:
	def __init__(self):
		self.varnames = [""] * 512
		self.is_free = [1] * 512
	def new_var(self, name):
		if name in self.varnames:
			return -1
		for var_pos in range(len(self.is_free)):
			if self.is_free[var_pos] == 1:
				self.is_free[var_pos] = 0
				self.varnames[var_pos] = name
				return 1
		return -2
	def remove_var(self, name):
		pos = search_var(name)
		if pos < 0:
			return -3
		else:
			self.varnames[pos] = ""
			self.is_free[pos] = 1
	def search_var(self, name):
		if name in self.varnames:
			return self.varnames.index(name)
		else:
			return -3
class TagManager:
	def __init__(self):
		self.tags = []
		self.pos = []
	def new_tag(self, name, pos):
		self.tags.append(name)
		self.pos.append(pos)
	def view_pos(self, name):
		try:
			return self.pos[self.tags.index(name)]
		except Exception:
			return 0

global memanager
memanager = Vars()
global tager
tager = TagManager()

global nins
nins = 0

def compile(file, out):
	f = open(file, "r")
	lines = f.readlines()
	outlines = []
	for i in lines:
		try:
			translate(i)
		except Exception:
			pass
	nins = 0
	for i in range(len(lines)):
		outlines.append(translate(lines[i]))
	f.close()
	ff = open(out, "w")
	ff.write("MOV IX NUM 9\n")
	ff.write("ADD IX NUM 1\n")
	for line in outlines:
		ff.write(line)
def translate(texto): #estoy pensando en prohibir calculos sin usar variables, para facilitarme la vida
	global nins
	global memanager
	global tager
	at = False
	txt = texto.split(" ")
	ltxt = len(txt)
	outxt = []
	if txt[0] == "var_num":
		outxt.append("MOV AX NUM 0\n")
		outxt.append("MOV BX NUM 0\n")
		nins += 2
		try:
			memanager.new_var(txt[1])
		except Exception:
			raise ValueError(texto + " → La variable no esta indicada")
		try:
			number = int(txt[2])
		except Exception:
			raise ValueError(texto + " → El valor de la variable no esta definido")
		try:
			h = int(txt[1])
		except Exception:
			pass
		else:
			raise Exception(texto + " → El nombre de la variable no puede ser un número")
		nd = []
		tnp = number
		while tnp > 0:
			nd.append(tnp % 10)
			tnp //= 10
		nd.reverse()
		for i in nd:
			tmp = str(i)
			outxt.append(f"ADD AX NUM {tmp}\n")
			outxt.append(f"MUL AX REG IX\n")
			nins += 2
		pos = memanager.search_var(txt[1])
		tnp = pos
		nd = []
		while tnp > 0:
			nd.append(tnp % 10)
			tnp //= 10
		nd.reverse()
		for i in nd:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append(f"MUL BX REG IX\n")
			nins += 2
		outxt.append(f"DIV AX REG IX\n")
		outxt.append(f"DIV BX REG IX\n")
		outxt.append(f"STR BX REG AX\n")
		nins += 3
		at = True
	elif txt[0] == "var_var":
		outxt.append(f"MOV BX NUM 0\n")
		nins += 1
		try:
			memanager.new_var(txt[1])
			pos_t = memanager.search_var(txt[1])
			pos = memanager.search_var(txt[2])
		except Exception:
			raise Exception(texto + " → La Variable o Variables no estan siendo definidas")
		nd = []
		try:
			h = int(txt[1])
			v = int(txt[2])
			print("FATAL ERROR VARNAMES CAN NOT BE NUMBERS")
		except Exception:
			pass
		else:
			raise Exception
		while pos > 0:
			nd.append(pos % 10)
			pos //= 10
		nd.reverse()
		for i in nd:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append(f"MUL BX REG IX\n")
			nins += 2
		outxt.append("DIV BX REG IX\n")
		outxt.append(f"LOA AX REG BX\n")
		nins += 2
		nd = []
		while pos_t > 0:
			nd.append(pos_t % 10)
			pos_t //= 10
		nd.reverse()
		outxt.append("MOV BX NUM 0\n")
		nins += 1
		for i in nd:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append(f"MUL BX REG IX\n")
			nins += 2
		outxt.append("DIV BX REG IX\n")
		outxt.append("STR BX REG AX\n")
		nins += 2
		at = True
	elif txt[0] == "remove":
		try:
			memanager.remove_var(txt[1])
		except Exception:
			raise ValueError(texto + " la variable no esta indicada")
		at = True
	elif txt[0] == "tag":
		at = True
		tager.new_tag(txt[1], nins)
	elif txt[0] == "jmp":
		outxt.append("MOV BX NUM 0")
		nins += 1
		pos = tager.view_pos(txt[1])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append("MUL BX REG IX\n")
			nins += 2
		outxt.append("DIV BX REG IX\n")
		nins += 1
		outxt.append("JMP AX REG BX\n")
		nins += 1
	elif txt[0] == "jlt":
		outxt.append("MOV BX NUM 0\n")
		outxt.append("MOV AX NUM 0\n")
		nins += 2
		pos = tager.view_pos(txt[2])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append("MUL BX REG IX\n")
			nins += 2
		outxt.append("DIV BX REG IX\n")
		nins += 1
		apos = memanager(txt[1])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD AX NUM {tmp}\n")
			outxt.append("MUL AX REG IX\n")
			nins += 2
		outxt.append("DIV AX REG IX\n")
		nins += 1
		outxt.append("JLT AX REG BX\n")
		nins += 1
	elif txt[0] == "jgt":
		outxt.append("MOV AX NUM 0\n")
		outxt.append("MOV BX NUM 0\n")
		nins += 2
		pos = tager.view_pos(txt[2])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append("MUL BX REG IX\n")
			nins += 2
		outxt.append("DIV BX REG IX\n")
		nins += 1
		apos = memanager(txt[1])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD AX NUM {tmp}\n")
			outxt.append("MUL AX REG IX\n")
			nins += 2
		outxt.append("DIV AX REG IX\n")
		nins += 1
		outxt.append("JGT AX REG BX\n")
		nins += 1
	elif txt[0] == "jeq":
		outxt.append("MOV BX NUM 0\n")
		outxt.append("MOV AX NUM 0\n")
		nins += 2
		pos = tager.view_pos(txt[2])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append("MUL BX REG IX\n")
			nins += 2
		outxt.append("DIV BX REG IX\n")
		nins += 1
		apos = memanager(txt[1])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD AX NUM {tmp}\n")
			outxt.append("MUL AX REG IX\n")
			nins += 2
		outxt.append("DIV AX REG IX\n")
		nins += 1
		outxt.append("JQT AX REG BX\n")
		nins += 1
	elif txt[0] == "jnq":
		outxt.append("MOV AX NUM 0\n")
		outxt.append("MOV BX NUM 0\n")
		nins += 2
		pos = tager.view_pos(txt[2])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD BX NUM {tmp}\n")
			outxt.append("MUL BX REG IX\n")
			nins += 2
		outxt.append("DIV BX REG IX\n")
		nins += 1
		apos = memanager(txt[1])
		pos_t = []
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		pos_t.reverse()
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD AX NUM {tmp}\n")
			outxt.append("MUL AX REG IX\n")
			nins += 2
		outxt.append("DIV AX REG IX\n")
		nins += 1
		outxt.append("JNQ AX REG BX\n")
		nins += 1
	elif txt[0] == "putchar":
		outxt.append("MOV CX NUM 0\n")
		outxt.append("MOV DX NUM 0\n")
		nins += 2
		try:
			char_var = memanager.search_var(txt[1])
			pos = memanager.search_var(txt[2])
		except Exception:
			raise Exception(texto + "     <------ faltan cosas crack")
		pos_t = []
		char_t = []
		while char_var > 0:
			char_t.append(char_var % 10)
			char_var //= 10
		while pos > 0:
			pos_t.append(pos % 10)
			pos //= 10
		char_t.reverse()
		pos_t.reverse()
		for i in char_t:
			tmp = str(i)
			outxt.append(f"ADD CX NUM {tmp}\n")
			outxt.append("MUL CX REG IX\n")
			nins += 2
		outxt.append("DIV CX REG IX\n")
		nins += 1
		for i in pos_t:
			tmp = str(i)
			outxt.append(f"ADD DX NUM {tmp}\n")
			outxt.append("MUL DX REG IX\n")
			nins += 2
		outxt.append("DIV DX REG IX\n")
		nins += 1
		outxt.append("LOA AX REG CX\n")
		outxt.append("LOA BX REG DX\n")
		outxt.append("INT AX PUT BX\n")
		nins += 3
	elif memanager.search_var(txt[0]) >= 0:
		pos = search_var(txt[0])
		outxt.append("MOV CX NUM 0\n")
		outxt.append("MOV DX NUM 0 \n")
		nins += 2
		poses = []
		while pos > 0:
			poses.append(pos % 10)
			pos //= 10
		poses.reverse()
		for i in poses:
			tmp = str(i)
			outxt.append(f"ADD CX NUM {tmp}\n")
			outxt.append(f"MUL CX REG IX\n")
			nins += 2
		outxt.append("DIV CX REG IX\n")
		nins += 1
		try:
			pos_t = memanager.search_var(txt[2])
		except Exception:
			raise Exception(texto + " → Falta la variable")
		poses = []
		while pos_t > 0:
			poses.append(pos_t % 10)
			pos_t //= 10
		poses.reverse()
		for i in poses:
			tmp = str(i)
			outxt.append(f"ADD DX NUM {tmp}\n")
			outxt.append(f"MUL DX REG IX\n")
			nins += 2
		outxt.append("DIV DX REG IX\n")
		nins += 1
		outxt.append("LOA AX REG CX\n")
		outxt.append("LOA BX REG DX\n")
		nins += 2
		if txt[1] == "*=":
			outxt.append("MUL AX REG BX\n")
		elif txt[1] == "/=":
			outxt.append("DIV AX REG BX\n")
		elif txt[1] == "+=":
			outxt.append("ADD AX REG BX\n")
		elif txt[1] == "-=":
			outxt.append("SUB AX REG BX\n")
		else:
			raise Exception("MAL PUESTA LA ORDEN: " + texto)
		nins += 1
		outxt.append("STR CX REG AX\n")
		nins += 1
	if not at and texto != '\n':
		raise Exception("LA ORDEN NO ES VALIDA")
	return "".join(outxt)

