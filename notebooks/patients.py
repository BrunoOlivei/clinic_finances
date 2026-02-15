#%%
import pandas as pd

year = 2026
month = 1

#%%
service_df = pd.read_csv(f"../data/{year}{month:02d}_atendimentos_sao_lucas.csv", encoding='utf-8-sig')
# %%
patients_df = service_df[["Cd Beneficiário", "Beneficiário", "Endereço Beneficiário"]].copy()
patients_df.columns = ['cd_patient', 'nm_patient', 'ds_address']

#%%
patients_df[["nm_patient"]] = patients_df[["nm_patient"]].apply(lambda x: x.str.replace(r'\s+', ' ', regex=True).str.strip())
patients_df[["ds_address"]] = patients_df[["ds_address"]].apply(lambda x: x.str.replace(r'\s+', ' ', regex=True).str.strip())
# %%
patients_df.drop_duplicates(subset=["cd_patient"], keep="first", inplace=True)
# %%
