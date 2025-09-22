from setuptools import setup
from setuptools import find_packages

# find_packages will find all the packages with __init__.py
# print(find_packages())

setup(
    name="taxipred", #namn på paketet, det som syns när man listar 
    version="0.0.1", #verision på paketet
    description="this package contains taxipred app", #beskrivning
    author="Natali", #vem som har gjort paketet
    author_email="author@mail.se", #email
    install_requires=["streamlit", "pandas", "fastapi", "uvicorn"], # Vilka paket som behövs för att använda ditt program
    package_dir={"": "src"}, #Vars paketet finns
    package_data={"taxipred": ["data/*.csv"]}, # Vars datan till paketet finns
    packages=find_packages(), # Letar efter paket genom att kolla mappar som har dunder init
)