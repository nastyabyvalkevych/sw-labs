# pip install SPARQLWrapper pandas
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

QUERY = """
SELECT ?country ?countryLabel ?population WHERE {
  wd:Q27468 wdt:P527 ?country .
  ?country wdt:P31 wd:Q6256 .
  ?country wdt:P1082 ?population .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "uk,en". }
}
ORDER BY DESC(?population)
"""

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(QUERY)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

rows = []
for b in results["results"]["bindings"]:
    rows.append({
        "country": b["countryLabel"]["value"],
        "country_qid": b["country"]["value"].split("/")[-1],
        "population": int(float(b["population"]["value"]))
    })

df = pd.DataFrame(rows)
df = df.sort_values("population", ascending=False, ignore_index=True)

print(df.to_string(index=False))
