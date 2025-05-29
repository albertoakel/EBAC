
import requests
import pandas as pd
from datetime import date

import matplotlib.pyplot as plt

link1 = 'https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/historico/'

payload = {'page':0, 'numberItems':50, 'symbol':'IFNC'}

r = requests.post("https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/historico/", json=payload)
print(r.status_code)


payload = {'page':0, 'numberItems':300, 'symbol':'IFNC'}
r = requests.post("https://www.infomoney.com.br/wp-json/infomoney/v1/quotes/history", json=payload)
print(r.status_code)

format = '%d/%m/%Y'
payload = {'page':0, 'numberItems':300, 'initialDate': date(2023, 1, 1).strftime(format), 'finalDate': date(2023, 1, 8).strftime(format), 'symbol':'IFNC'}


res = [[a['display'], b, c, d, e, f, g] for a, b, c, d, e, f, g in r.json()]
df = pd.DataFrame(res, columns=['DATA', 'ABERTURA', 'FECHAMENTO', 'VARIAÇÃO', 'MÍNIMO', 'MÁXIMO', 'VOLUME'])

# op=df.ABERTURA
o=df.VARIAÇÃO.to_numpy()
# plt.plot(df.VARIAÇÃO)
# plt.show()
#type(axes)
#lines = df.plot.line(x='DATA', y='ABERTURA')
#plt.show()
plt.plot(df.DATA,o)
plt.show()
