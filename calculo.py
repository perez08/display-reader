import time

def calcular(abonado, lectura, precio200,precio201):#se reciben datos generados en hora (##:00)
	hora= time.strftime("%H:%M") #calcula la hora actual
	fecha=time.strftime("%d") # calcula el dia del mes
	inicial=0
	instante=0
	if fecha=='17' and hora=='00:01': # logica para reiniciar el archivo todos los 17 de cada mes
	#if fecha==fecha and hora==hora: # linea realizada para pruebas
		inicial=lectura
		instante=lectura
		g=open("lectura"+str(abonado)+".txt", "w")
		g.write(str(inicial))
		f = open(str(abonado)+".txt", "w")  
		f.write(str(inicial)+','+str(instante)+',') # se escribe el valor inicial al archivo
	else:
		g=open("lectura"+str(abonado)+".txt", "r")
		inicial=float(g.read())
		instante=lectura
		f = open(str(abonado)+".txt", "a+") 
		f.write(str(inicial)+','+str(instante)+',')
	f.close()
	g.close()
	#############################################
	#Se realizan los calculos###
	kwhconsumidos=instante-inicial #kWh consumidos hasta el momento
	if kwhconsumidos<=40:
		pagarAlMomento=40*precio200 #define el precio base
	elif kwhconsumidos>40 and kwhconsumidos<=200: #precio kWh antes de consumir 200 kWh
		pagarAlMomento=kwhconsumidos*precio200
	elif kwhconsumidos>200: #precio kWh despues de consumir 200 kWh
		pagarAlMomento=(200*precio200)+((kwhconsumidos-200)*precio201)
	dato=open(str(abonado)+".txt","a+")
	pagarAlMomento=str(pagarAlMomento)
	dato.write(str(kwhconsumidos)+','+'¢'+pagarAlMomento[:pagarAlMomento.find(".")+3]+';')
	dato.close()

	#leer=open(str(abonado)+".txt","r")
	#print(leer.read())
	#leer.close()
	
def main():
	lista=[12345,16363] #envia la función de ema
	abonado=lista[0]
	lectura=lista[1]
	calcular(abonado,lectura,77.90,140.40)

if __name__ == '__main__':
	main()