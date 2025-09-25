import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
import pandas as pd

data = read_api_endpoint("taxi")
df = pd.DataFrame(data.json())

def kpi():
    """-> labels, values"""
    labels = ["Rows of data", "Mean price USD", "Median price USD"] #TODO gör typ denna för pris JUST NU/Ungefärligt pris för en resa mellan A-B km=x, min=x/. 
    values = [len(df), round(df["Trip_Price"].mean(),2), round(df["Trip_Price"].median(),2)]
    return labels, values

def chart(): 
    pass