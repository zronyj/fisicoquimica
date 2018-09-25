import math
import matplotlib.pyplot as plt
import pandas as pd

def modelo(Xi=0.15, k1=1, k2=1, dR=0.001, graf=False):
	K = k2/k1
	pasos = 2 * int(Xi / dR)
	especies = {'X2':[0]*pasos, 'XP':[0]*pasos, 'P2':[0]*pasos, 'Rcon':[0]*pasos}
	especies['X2'][0] = Xi
	for i in xrange(1, pasos):
		dX2 = dR * (-1) * especies['X2'][i-1] / (especies['X2'][i-1] + K * especies['XP'][i-1])
		dP2 = dR * especies['XP'][i-1] / (especies['X2'][i-1] / K + especies['XP'][i-1])
		especies['X2'][i] = especies['X2'][i-1] + dX2
		especies['XP'][i] = especies['XP'][i-1] - dX2 - dP2
		especies['P2'][i] = especies['P2'][i-1] + dP2
		especies['Rcon'][i] = round(especies['Rcon'][i-1] + dR, 3)
	if graf:
		plt.plot(especies['Rcon'], especies['X2'], 'b-')
		plt.plot(especies['Rcon'], especies['XP'], 'g-')
		plt.plot(especies['Rcon'], especies['P2'], 'r-')
		plt.show()
	else:
		return especies

def error(df, especies):
	err = 0
	for e in xrange(1, len(df)):
		num = round(df['Rcon'][e],3)
		temp = especies['Rcon'].index(num)
		err += (df['X2'][e] - especies['X2'][temp])**2
		err += (df['XP'][e] - especies['XP'][temp])**2
		err += (df['P2'][e] - especies['P2'][temp])**2
	return math.sqrt(err)

def optimizador(data='data_k1.csv', Xi=0.15, k2i=1, k2f=2, dk=0.01, dR=0.001):
	df = pd.read_csv(data)
	pasos = int((k2f - k2i)/dk)
	errores = [0] * pasos
	for m in xrange(pasos):
		espec = modelo(Xi = Xi, k1 = 1, k2 = k2i + m * dk, dR = dR)
		temp = error(df, espec)
		errores[m] = temp
	mejor = min(errores)
	print '\nError:', mejor
	indice = errores.index(mejor)
	k2 = k2i + indice * dk
	print 'k2 =', k2
	modelo(Xi = Xi, k1 = 1, k2 = k2, dR = dR, graf=True)

optimizador()
