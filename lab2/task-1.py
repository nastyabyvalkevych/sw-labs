# Напишіть SPARQL запит, який буде повертати чисельність населення кожної з країн
# Східної Європи. Результат запиту необхідно впорядкувати за спадінням чисельності
# населення країн.

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd


# wd:Q27468 — «Східна Європа».
# wdt:P527 — підмножина країн, що входять до регіону.
# wdt:P31 wd:Q6256 — гарантує, що частини є саме країнами.
# wdt:P1082 — «населення»

QUERY = """
SELECT ?country ?countryLabel ?population WHERE {
  wd:Q27468 wdt:P527 ?country .
  ?country wdt:P31 wd:Q6256 .
  ?country wdt:P1082 ?population .
  ?country rdfs:label ?countryLabel .
  FILTER (LANG(?countryLabel) = "uk")
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
