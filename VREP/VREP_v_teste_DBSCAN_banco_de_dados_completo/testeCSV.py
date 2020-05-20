import pandas as pd

rangeImageCompleteDf = pd.DataFrame()


rangeImageDf = pd.read_csv('complete.csv', index_col='object')
rangeImage2Df = pd.read_csv('teste.csv', index_col=0)
rangeImage2Df['label'] = ['teste'] * len(rangeImage2Df)
rangeImageCompleteDf = pd.concat([rangeImage2Df, rangeImageDf], ignore_index=True)
rangeImageCompleteDf.index.name = 'object'
rangeImageCompleteDf.to_csv('testeComplete.csv')
