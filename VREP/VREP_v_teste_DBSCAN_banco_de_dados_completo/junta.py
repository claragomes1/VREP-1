import pandas as pd

rangeImageCompleteDf = pd.DataFrame()

for each in ['corredor', 'saida_esquerda', 'saida_direita', 'saida_direita_esquerda', 'encruzilhada_direita', 'encruzilhada_esquerda', 'encruzilhada']:
	rangeImageDf = pd.read_csv(each + '_1.csv', index_col=0)
	rangeImage2Df = pd.read_csv(each + '_2.csv', index_col=0)
	rangeImageCompleteDf = pd.concat([rangeImageDf, rangeImage2Df], ignore_index=True)
	rangeImageCompleteDf.index.name = 'object'
	rangeImageCompleteDf.to_csv(each + '.csv')
