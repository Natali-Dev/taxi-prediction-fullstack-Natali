import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
import pandas as pd


def kpi(df):
    """-> labels, values"""
    labels = ["Rows of data", "Median distance km", "Median duration minutes"] #TODO gör typ denna för pris JUST NU/Ungefärligt pris för en resa mellan A-B km=x, min=x/. 
    values = [len(df), round(df["Trip_Distance_km"].median(),2), round(df["Trip_Duration_Minutes"].median(),2)]
    return labels, values

def chart(): 
    pass