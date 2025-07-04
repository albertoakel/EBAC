import pandas as pd
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px

from scipy import stats
from scipy.stats import (norm, expon, lognorm, gamma, beta, weibull_min,
                         gumbel_r, triang, uniform, anderson, kstest)

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix,roc_curve, roc_auc_score
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

from test_functions import identify_distribution as id_dist



#===== Leitura dos dados
def load_data(file) -> pd.DataFrame:
    return pd.read_csv(file,delimiter=';')


default_path = Path("/home/akel/PycharmProjects/EBAC/dados/CARDIO_BASE.csv")

try:
    df = load_data(default_path)
except FileNotFoundError:
    print("arquivo não encontrado")
    df = None     # Evita crash

# RECODIFICAÇÃO DA VARIAVEL gender
df['gender'] = df['gender'].replace({1: 1, 2: 0})
# CONVERSÃO DA VARIAVEL weight
df['weight']=df['weight'].str.replace(',', '.').astype(float)


#==== FILTRAGEM
def outliers_iqr(df,col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
    return df

# PASSO 1: Z-SCORE
df=df[(stats.zscore(df['weight'])<2)]
df=df[(stats.zscore(df['height'])<3)]

# Passo 2 : IQR
df=outliers_iqr(df,'age')
df=outliers_iqr(df,'weight')
df=outliers_iqr(df,'height')


N=len(df)
temp1=df['age']
dx1=5
bins1=np.arange(30,65+1,dx1)
c1, x1= np.histogram(temp1, bins1)
p1=c1/N*100

temp2=df['height']
dx2=5
bins2=np.arange(min(temp2),max(temp2),dx2)
c2, x2= np.histogram(temp2, bins2)
p2=c2/N*100

temp3=df['weight']
dx3=5
bins3=np.arange(40,106,dx3)
c3, x3= np.histogram(temp3, bins3)
p3=c3/N*100



bf,df=id_dist(temp2,plot=False)
pd.set_option('display.width',None)
print(df.sort_values(by='KS_Stat'))

