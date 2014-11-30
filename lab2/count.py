import pandas as pd
from avro.datafile import DataFileReader
from avro.io import DatumReader

data = []

reader = DataFileReader(open("countries.avro", "r"), DatumReader())
for entry in reader:
  data.append(entry)

reader.close()

countries = pd.DataFrame(data)
print len(countries[countries.population > 10000000])