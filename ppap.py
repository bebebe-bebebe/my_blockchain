import warnings
warnings.filterwarnings("ignore")
import pandas as pd
pd.set_option('display.max_columns', None)
df=pd.read_csv(r'Global YouTube Statistics.csv', encoding="latin-1")
#print(df.info())
cat_date=[d for d in df.columns if df[d].dtype=='object']
num_date=[d for d ind df.columns df not in cat_date]
df_num=df[num_date]
df_num=df[cat_date]
