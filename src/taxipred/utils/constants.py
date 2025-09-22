from importlib.resources import files

# 'files' tar namnet för paketet (vi har satt name="taxipred" i setup.py)
# får tillbaka ett resource-träd med alla filer i paketet (Traversable)
# 'joinpath' skapar sedan en sökväg inne i paketet
# och vår Traversable(resultatet) ser ut såhär: <project-root>/src/taxipred/data/taxi_trip_pricing.csv

# files = taxipred innebär att vi väljer den mappen, och lägger till sökvägen data/...
TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")
# DATA_PATH = Path(__file__).parents[1] / "data"

print(f"\n{TAXI_CSV_PATH}\n")
