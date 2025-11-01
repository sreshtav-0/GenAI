#Streamlit Magic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.DataFrame({ "col1": np.random.randn(1000) for _ in range(20)})
df

x = 10
'x', x

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

fig