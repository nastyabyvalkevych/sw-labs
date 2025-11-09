# 2. Напишіть один SPARQL запит, який буде повертати результати на основі таких
# інструкцій:
# - назви країн, які починаються з великої літери «А» на континентах «Європа» та
# «Північна Америка», упорядкувавши результати в алфавітному порядку;
# - для кожної країни перелічити усі назви їхніх пов’язаних мов (кожна назва мови має
# бути у верхньому регістрі, якщо мов декілька - мови повинні розділятися символом
# «|», наприклад HUNGARIAN|GERMAN);
# - країни повинні відображатися у таблиці, навіть якщо не мають пов’язаних мов.

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

QUERY = """
SELECT ?countryLabel
       (COALESCE(GROUP_CONCAT(DISTINCT ?langName; separator="|"), "") AS ?languages)
WHERE {
  ?country wdt:P31 wd:Q6256 .
  ?country wdt:P30 ?continent .
  FILTER(?continent IN (wd:Q46, wd:Q49)) .

  OPTIONAL { ?country rdfs:label ?countryLabelUk FILTER(LANG(?countryLabelUk)="uk") }
  OPTIONAL { ?country rdfs:label ?countryLabelEn FILTER(LANG(?countryLabelEn)="en") }
  BIND(COALESCE(?countryLabelUk, ?countryLabelEn) AS ?countryLabel)

  FILTER(BOUND(?countryLabelUk) && STRSTARTS(?countryLabelUk, "А"))

  OPTIONAL {
    ?country wdt:P37 ?lang .
    OPTIONAL { ?lang rdfs:label ?langLabelUk FILTER(LANG(?langLabelUk)="uk") }
    OPTIONAL { ?lang rdfs:label ?langLabelEn FILTER(LANG(?langLabelEn)="en") }
    BIND(UCASE(STR(COALESCE(?langLabelUk, ?langLabelEn))) AS ?langName)
  }
}
GROUP BY ?countryLabel
ORDER BY ?countryLabel
"""

# Налаштовуємо SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(QUERY)
sparql.setReturnFormat(JSON)

# Виконуємо запит
results = sparql.query().convert()

# Парсимо у DataFrame
rows = []
for b in results["results"]["bindings"]:
    rows.append({
        "country": b["countryLabel"]["value"],
        "languages": b["languages"]["value"]
    })

df = pd.DataFrame(rows)

print(df.to_string(index=False))
