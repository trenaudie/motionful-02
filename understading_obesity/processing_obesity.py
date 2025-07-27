#%% 
import pandas as pd
df = pd.read_csv('NCD_RisC_Lancet_2024_BMI_age_standardised_country.csv')
# %%
df.columns
#%%##
obesity_column = 'Prevalence of BMI>=30 kg/m² (obesity)'
df[obesity_column] 
index_columns = ['Year','Country/Region/World', 'Sex']

# %%
df[index_columns + [obesity_column]].set_index(index_columns).head(10).to_json()
#%% 


# %%

df['Country/Region/World'].unique()