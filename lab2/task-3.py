# 3. Напишіть SPARQL запити, щоб дізнатися:
# - усіх лауреатів Нобелівської премії з фізики в порядку від найстаршого до
# наймолодшого;
# - 10 найкращих університетів із найбільшою кількістю лауреатів Нобелівської премії
# з фізики;
# - кількість лауреатів Нобелівської премії з фізики, які є іммігрантами (народилися в
# країні, відмінній від країни університету).

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

ENDPOINT = "https://dbpedia.org/sparql"


def run_query(q: str, timeout_s: int = 60):
    """Виконує SPARQL-запит до DBpedia з GET, таймаутом та User-Agent."""
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    sparql.setMethod("GET")
    sparql.setTimeout(timeout_s)
    sparql.addCustomHttpHeader("User-Agent", "UniversityLab/1.0 (student@example.com)")
    sparql.addCustomHttpHeader("Accept", "application/sparql-results+json")
    result = sparql.query().convert()
    return result["results"]["bindings"]


# ------------------------------------------------------------
# 1) ЛАУРЕАТИ НОБЕЛІВСЬКОЇ ПРЕМІЇ З ФІЗИКИ (від найстаршого до молодшого)
# ------------------------------------------------------------
Q1 = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?laureate ?name ?birthDate WHERE {
  ?laureate dbo:award dbr:Nobel_Prize_in_Physics ;
            dbo:birthDate ?birthDate ;
            rdfs:label ?name .
  FILTER (lang(?name) IN ("uk","en"))
}
ORDER BY ?birthDate
"""

rows1 = []
for b in run_query(Q1):
    rows1.append({
        "Laureate": b["name"]["value"],
        "BirthDate": b["birthDate"]["value"],
        "URI": b["laureate"]["value"]
    })

df1 = pd.DataFrame(rows1)
print("\n\n====================== 1) ЛАУРЕАТИ НОБЕЛІВСЬКОЇ ПРЕМІЇ (ФІЗИКА) ======================")
print(df1.to_string(index=False))


# ------------------------------------------------------------
# 2) ТОП-10 УНІВЕРСИТЕТІВ ЗА КІЛЬКІСТЮ ЛАУРЕАТІВ
# ------------------------------------------------------------
Q2 = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?univ ?univLabel (COUNT(DISTINCT ?laureate) AS ?laureateCount) WHERE {
  ?laureate dbo:award dbr:Nobel_Prize_in_Physics ;
            dbo:almaMater ?univ .
  ?univ a dbo:University ;
        rdfs:label ?univLabel .
  FILTER (lang(?univLabel) IN ("uk","en"))
}
GROUP BY ?univ ?univLabel
ORDER BY DESC(?laureateCount)
LIMIT 10
"""

rows2 = []
for b in run_query(Q2):
    rows2.append({
        "University": b["univLabel"]["value"],
        "LaureatesCount": int(b["laureateCount"]["value"]),
        "URI": b["univ"]["value"]
    })

df2 = pd.DataFrame(rows2)
print("\n\n====================== 2) ТОП-10 УНІВЕРСИТЕТІВ ======================")
print(df2.to_string(index=False))


# ------------------------------------------------------------
# 3) КІЛЬКІСТЬ ЛАУРЕАТІВ-ІММІГРАНТІВ
# ------------------------------------------------------------
Q3 = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT (COUNT(DISTINCT ?laureate) AS ?immigrantCount) WHERE {
  ?laureate dbo:award dbr:Nobel_Prize_in_Physics ;
            dbo:birthPlace ?birthPlace ;
            dbo:almaMater ?univ .
  ?birthPlace dbo:country ?birthCountry .
  ?univ dbo:country ?univCountry .
  FILTER (?birthCountry != ?univCountry)
}
"""

res3 = run_query(Q3)
imm_count = int(res3[0]["immigrantCount"]["value"])

df3 = pd.DataFrame([{"ImmigrantLaureates": imm_count}])
print("\n\n====================== 3) ЛАУРЕАТИ-ІММІГРАНТИ ======================")
print(df3.to_string(index=False))
