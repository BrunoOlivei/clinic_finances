#%%
import sys
sys.path.insert(0, "..")

import pandas as pd
import matplotlib.pyplot as plt

from core import db

engine = db.engine
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (10, 5)

#%%
patients_df = pd.read_sql("SELECT * FROM patients", engine)
claims_df = pd.read_sql("SELECT * FROM insurance_claims", engine)