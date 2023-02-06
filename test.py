import pandas as pd
df_price=pd.read_excel('directg_price_list.xlsx',sheet_name="Sheet1")
df_discount=pd.read_excel('directg_discount_list.xlsx',sheet_name='Sheet1')
df_price=df_price.melt(var_name='게임',value_name='가격')
df_discount=df_discount.melt(var_name="게임",value_name="할인율") 
df_price=df_price.drop(0,axis=0)
df_price=df_discount.drop(0,axis=0)
print(df_price)
print(df_discount)