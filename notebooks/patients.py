#%%
import pandas as pd

#%%
year = 2026
month = 1

#%%
service_df = pd.read_csv(f"./data/{year}{month:02d}_atendimentos_sao_lucas.csv", encoding='utf-8-sig')
# %%
patients_df = service_df[["Cd Beneficiário", "Beneficiário", "Endereço Beneficiário"]].copy()
patients_df.columns = ['cd_patiente', 'nm_patiente', 'ds_endereco']

#%%
patients_df[["nm_patiente"]] = patients_df[["nm_patiente"]].apply(lambda x: x.str.replace(r'\s+', ' ', regex=True).str.strip())
patients_df[["ds_endereco"]] = patients_df[["ds_endereco"]].apply(lambda x: x.str.replace(r'\s+', ' ', regex=True).str.strip())
# %%
patients_df.drop_duplicates(subset=["cd_patiente"], keep="first", inplace=True)
# %%
