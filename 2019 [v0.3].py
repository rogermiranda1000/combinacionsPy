import os
from os.path import isfile, join
from math import factorial, log
import atexit
import time

#-----------------------
#- Variables generales -
#-----------------------
#Unico numero que debe usarse
unicoNumero = int(input("Numero a usar. Ex: 3. "))#3
#Veces que el numero (establecido anteriormente) debe usarse
introducido = input("Veces a usar el numero. Ex: 7. (-1 si no importa) ")
vecesUsado = int(introducido)#7
if introducido == "-1":
	vecesUsado = -1
#Numero deseado
esperado = float(input("Numero esperado. Ex: 2019. "))#2019
#Longitud de los archivos (mayor implica mas consumo de RAM pero mas rapidez y menos archivos)
MAXLENGHT = 3000
max = 1e+9
min = 1e-9
#2 > 12
#3 > 7

start = 0




#Variables
numIndex = 0
oldIndex = 0
notDone = True
#Evitar repeticion
esteLAST = -2
currentLAST = 0
solucionesDadas = []
ficherosAbiertos = []

#Solucion encontrada
def done(valor, cadena):
	#print('('+str(valor)+") "+cadena)
	if valor == esperado and not cadena in solucionesDadas:
		print("--- ! ---")
		print(cadena)
		print(str(int(round(time.time() * 1000))-start) + "ms")
		solucionesDadas.append(cadena)
		input("Pulsa enter para seguir.")

#Eliminar ficheros
def eliminar(concidencia):
	files = filter(os.path.isfile, os.listdir(os.curdir))
	for f in files:
		fichero = f[:3]
		if fichero==concidencia:
			os.remove(f)

def exit_handler():
	print("Saliendo...")
	for f in ficherosAbiertos:
		f.close()
	eliminar("old")
	eliminar("num")

def corresponde():
	global esteLAST
	global currentLAST
	
	if(esteLAST % 300) == 0:
		print(str(esteLAST)+'/'+str(currentLAST))
	esteLAST += 1
	if esteLAST-1 != currentLAST:
		return True
	currentLAST += 1
	return False
		
#Insertar valor a num
def lista(val, num):
	global numIndex
	global esteLAST
	global currentLAST
	global MAXLENGHT
	
	if isinstance(val.numero, complex):
		return
	elif val.numero == num:
		return
	
	lines = 0
	if os.path.exists("num"+str(numIndex)+".txt"):
		tmp = open("num"+str(numIndex)+".txt",'r')
		lines = len(tmp.readlines())
		tmp.close()
	w = open("num"+str(numIndex)+".txt",'a')
	if lines >= MAXLENGHT or not os.path.exists("num"+str(numIndex)+".txt"):
		if lines >= MAXLENGHT:
			numIndex += 1
		w = open("num"+str(numIndex)+".txt",'w')
	w.write(val.operacion+','+str(val.numero)+"\n")#+','+str(val.LAST)
	w.close()

class Numero:	
	#Operacion (+, -, *, /, ^, s, !)
	#Cantidad a operar
	#Establecer numero
	#Establecer operaciones principales
	#Establecer operaciones del operador
	#Cantidad de numeros usados
	#Invertido?
	def __init__(self, op, cant, last, operac, cantO, invert=False):
		global notDone
		self.numero = last
		self.operacion = str(last)
		
		if operac != "":
			self.operacion = operac
		self.cantOp = str(cant)
		if cantO != "":
			self.cantOp = cantO
		elif op != '!':
			return
			
		if (self.numerosUsados+self.cantOp.count(str(unicoNumero))) > vecesUsado and vecesUsado!=-1:
			return
		
		if corresponde():
			return
		
		if self.numero > max:
			return
		elif self.numero < min:
			return
		elif op=='!':
			tmp = self.numero
			for a in reversed(range(2, self.numero)):
				tmp *= a
				if tmp > max:
					return
		
		try:
			self.__oper(op, cant, invert)
		except Exception as e:
			#pass
			print("Error ("+op+'/'+str(cant)+'/'+str(invert)+") > "+str(e))
			
		if self.numerosUsados == vecesUsado:
			done(self.numero, self.operacion)
		elif self.numerosUsados < vecesUsado:
			notDone = True
			
		if vecesUsado==-1:
			done(self.numero, self.operacion)
			notDone = True
		
	def __oper(self, op, cant, invert):
		if op != 's' and op != 'l':
			if invert == True:
				string = '^'
				if op == '/':
					string = '/'
				if op == '+':
					string = '-'
				self.operacion = '('+self.cantOp + ")"+string+"("+self.operacion+')'
			else:
				self.operacion = '('+self.operacion+')'+op
				if op != '!':
					self.operacion += '('+self.cantOp+')'
		elif op == 's':
			if invert == True:
				self.operacion = "("+self.cantOp+")^(1/"+self.operacion+')'
			else:
				self.operacion = "("+self.operacion+")^(1/"+self.cantOp+')'
		elif op == 'l':
			if invert != True:
				self.operacion = "(log.("+self.cantOp+") ("+self.operacion+"))"
			else:
				self.operacion = "(log.("+self.operacion+") ("+self.cantOp+"))"
			
		if op == '+':
			self.numero += cant
		elif op == '-':
			self.numero -= cant
		elif op == '*':
			self.numero *= cant
		elif op == '/':
			if invert == True:
				self.numero = cant/self.numero
			else:
				self.numero /= cant
		elif op == '^':
			if invert == True:
				self.numero = pow(cant, self.numero)
			else:
				self.numero = pow(self.numero, cant)
		elif op == 's':
			if invert == True and cant>0:
				self.numero = pow(1/cant, self.numero)
			elif self.numero>0:
				self.numero = pow(self.numero, 1/cant)
		elif op == '!':
			self.numero = factorial(self.numero)
			#for a in reversed(range(2, self.numero)):
			#	self.numero *= a
		elif op == 'l':
			if invert == True:
				self.numero = log(cant, self.numero)
			else:
				self.numero = log(self.numero, cant)
	
	@property
	def numerosUsados(self):
		return self.operacion.count(str(unicoNumero))
	
def todasOperaciones(last, new):
	#print(str(last.numero)+"&"+str(new.numero))
	if isinstance(new.numero, complex) or isinstance(last.numero, complex):
		return
	
	
	lista(Numero('+', new.numero, last.numero, last.operacion, new.operacion), last.numero)
	lista(Numero('-', new.numero, last.numero, last.operacion, new.operacion), last.numero)
	if new.numero != last.numero:
		lista(Numero('+', -new.numero, last.numero, last.operacion, new.operacion, True), last.numero)
	lista(Numero('*', new.numero, last.numero, last.operacion, new.operacion), last.numero)
	if last.numero > 2 and last.numero == new.numero and int(last.numero) == last.numero:
		lista(Numero('!', 0, int(last.numero), last.operacion, ""), last.numero)
	if new.numero != 0:
		lista(Numero('/', new.numero, last.numero, last.operacion, new.operacion), last.numero)
		if new.numero != last.numero:
			lista(Numero('/', new.numero, last.numero, last.operacion, new.operacion, True), last.numero)
		lista(Numero('s', new.numero, last.numero, last.operacion, new.operacion), last.numero)
	if new.numero >= 0 or last.numero != 0:
		lista(Numero('^', new.numero, last.numero, last.operacion, new.operacion), last.numero)
	if (last.numero >= 0 or new.numero != 0) and new.numero != last.numero:
		lista(Numero('^', new.numero, last.numero, last.operacion, new.operacion, True), last.numero)
	if last.numero != 0 and new.numero != last.numero:
		lista(Numero('s', new.numero, last.numero, last.operacion, new.operacion, True), last.numero)
	if last.numero >= 2 and new.numero >= 1:
		lista(Numero('l', new.numero, last.numero, last.operacion, new.operacion), last.numero)
	if new.numero >= 2 and last.numero >= 1 and new.numero != last.numero:
		lista(Numero('l', new.numero, last.numero, last.operacion, new.operacion, True), last.numero)

#Borrar ficheros
print("--Directorio-- "+str(os.listdir(os.curdir)))
eliminar("old")
eliminar("num")

#Al salir, borrar archivos
atexit.register(exit_handler)

#Primera generacion
start = int(round(time.time() * 1000))
lista(Numero('+', 0, unicoNumero, "", ""), -1)
lista(Numero('+', 0, -unicoNumero, "", ""), -1)

while notDone:
	print("Ciclo!")
	notDone = False
	esteLAST = 0
	
	#Old += num
	files = filter(os.path.isfile, os.listdir(os.curdir))
	for f in files:
		fichero = f[:3]
		if(fichero=="num"):
			#numeroFichero = f.replace("num", "")
			#numeroFichero = numeroFichero.replace(".txt", "")
			
			lines = 0
			if os.path.exists("old"+str(oldIndex)+".txt"):
				tmp = open("old"+str(oldIndex)+".txt",'r')
				lines = len(tmp.readlines())
				tmp.close()
			w = open("old"+str(oldIndex)+".txt",'a')
			if lines >= MAXLENGHT or not os.path.exists("old"+str(oldIndex)+".txt"):
				if lines >= MAXLENGHT:
					oldIndex += 1
				w = open("old"+str(oldIndex)+".txt",'w')
				
			r = open(f, "r")
			for x in r:
				w.write(x)
			w.close()
			r.close()
			
	#Reiniciar num
	eliminar("num")
	numIndex = 0
	
	#---Operar---
	#Obtener operador principal
	for b in range(oldIndex+1):
		r = open("old"+str(b)+".txt", "r")
		ficherosAbiertos.append(r)
		for x in r:
			#OPERADOR PRINCIPAL
			actual = Numero('+', 0, float(x.split(',')[1]), x.split(',')[0], "")
			todasOperaciones(actual, actual)
			#Operaciones con los demas valores
			for y in range(oldIndex+1):
				if b > y:
					continue
				a = open("old"+str(y)+".txt", "r")
				ficherosAbiertos.append(a)
				for z in a:
					if x >= z:
						continue
					nActual = Numero('+', 0, float(z.split(',')[1]), z.split(',')[0], "")
					todasOperaciones(actual, nActual)
				a.close()
				ficherosAbiertos.remove(a)
		r.close()
		ficherosAbiertos.remove(r)
	
	

#END
print("---END---")
while True:
	input()