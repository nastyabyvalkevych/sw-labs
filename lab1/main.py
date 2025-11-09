from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, FOAF, XSD
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime

# Створення графу
g = Graph()

# Визначення namespace'ів
EX = Namespace("http://example.org/")
g.bind("ex", EX)
g.bind("foaf", FOAF)

# URI для персон
cade = EX.Cade
emma = EX.Emma

# Інформація про Кейда
g.add((cade, RDF.type, FOAF.Person))
g.add((cade, FOAF.name, Literal("Cade", lang="en")))
g.add((cade, FOAF.givenName, Literal("Cade", lang="en")))

# Адреса Кейда
cade_address = EX.CadeAddress
g.add((cade, EX.address, cade_address))
g.add((cade_address, EX.street, Literal("1516 Henry Street")))
g.add((cade_address, EX.city, Literal("Berkeley")))
g.add((cade_address, EX.state, Literal("California")))
g.add((cade_address, EX.postalCode, Literal("94709")))
g.add((cade_address, EX.country, Literal("USA")))

# Освіта Кейда
g.add((cade, EX.degree, Literal("Bachelor of Biology")))
g.add((cade, EX.university, Literal("University of California")))
g.add((cade, EX.graduationYear, Literal(2011, datatype=XSD.gYear)))

# Інтереси Кейда
g.add((cade, FOAF.interest, EX.Birds))
g.add((cade, FOAF.interest, EX.Ecology))
g.add((cade, FOAF.interest, EX.Environment))
g.add((cade, FOAF.interest, EX.Photography))
g.add((cade, FOAF.interest, EX.Travel))

# Країни, які відвідав Кейд
g.add((cade, EX.visited, EX.Canada))
g.add((cade, EX.visited, EX.France))

# Інформація про Емму
g.add((emma, RDF.type, FOAF.Person))
g.add((emma, FOAF.name, Literal("Emma", lang="en")))
g.add((emma, FOAF.givenName, Literal("Emma", lang="en")))

# Вік Емми (буде змінено пізніше на 36)
current_year = datetime.now().year
birth_year = current_year - 35  # спочатку 35, потім зміним на 36
g.add((emma, FOAF.age, Literal(35, datatype=XSD.integer)))

# Адреса Емми
emma_address = EX.EmmaAddress
g.add((emma, EX.address, emma_address))
g.add((emma_address, EX.street, Literal("Carrer de la Guardia Civil 20")))
g.add((emma_address, EX.city, Literal("Valencia")))
g.add((emma_address, EX.postalCode, Literal("46020")))
g.add((emma_address, EX.country, Literal("Spain")))

# Освіта Емми
g.add((emma, EX.degree, Literal("Master of Chemistry")))
g.add((emma, EX.university, Literal("University of Valencia")))
g.add((emma, EX.graduationYear, Literal(2015, datatype=XSD.gYear)))

# Експертиза Емми
g.add((emma, EX.expertise, Literal("Waste Management")))
g.add((emma, EX.expertise, Literal("Toxic Waste")))
g.add((emma, EX.expertise, Literal("Air Pollution")))

# Інтереси Емми
g.add((emma, FOAF.interest, EX.Cycling))
g.add((emma, FOAF.interest, EX.Music))
g.add((emma, FOAF.interest, EX.Travel))

# Країни, які відвідала Емма
g.add((emma, EX.visited, EX.Portugal))
g.add((emma, EX.visited, EX.Italy))
g.add((emma, EX.visited, EX.France))
g.add((emma, EX.visited, EX.Germany))
g.add((emma, EX.visited, EX.Denmark))
g.add((emma, EX.visited, EX.Sweden))

# Зв'язок між Кейдом та Еммою
g.add((cade, FOAF.knows, emma))

# Інформація про зустріч
meeting = EX.Meeting_Paris_2014
g.add((meeting, RDF.type, EX.Meeting))
g.add((meeting, EX.participant, cade))
g.add((meeting, EX.participant, emma))
g.add((meeting, EX.location, Literal("Paris")))
g.add((meeting, EX.date, Literal("2014-08", datatype=XSD.gYearMonth)))

print("=" * 70)
print("RDF ГРАФ СТВОРЕНО")
print("=" * 70)
print(f"Кількість трійок у графі: {len(g)}\n")

# ===== ВІЗУАЛІЗАЦІЯ ГРАФУ =====
print("=" * 70)
print("ВІЗУАЛІЗАЦІЯ ГРАФУ")
print("=" * 70)


def visualize_rdf_graph(rdf_graph):
    """Візуалізація RDF графу за допомогою NetworkX"""
    nx_graph = nx.DiGraph()

    # Додавання вузлів та ребер
    for subj, pred, obj in rdf_graph:
        subj_label = str(subj).split('/')[-1].split('#')[-1]
        pred_label = str(pred).split('/')[-1].split('#')[-1]

        if isinstance(obj, Literal):
            obj_label = str(obj)[:30]  # Обрізаємо довгі літерали
        else:
            obj_label = str(obj).split('/')[-1].split('#')[-1]

        nx_graph.add_edge(subj_label, obj_label, label=pred_label)

    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(nx_graph, k=2, iterations=50)

    nx.draw(nx_graph, pos, with_labels=True, node_color='lightblue',
            node_size=3000, font_size=8, font_weight='bold',
            arrows=True, edge_color='gray', arrowsize=20)

    plt.title("RDF Graph: Cade and Emma", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('rdf_graph.png', dpi=300, bbox_inches='tight')
    print("Граф збережено у файл: rdf_graph.png\n")


try:
    visualize_rdf_graph(g)
except Exception as e:
    print(f"Помилка візуалізації: {e}\n")

# ===== СЕРИАЛІЗАЦІЯ У РІЗНІ ФОРМАТИ =====
print("=" * 70)
print("СЕРИАЛІЗАЦІЯ ГРАФУ У РІЗНІ ФОРМАТИ")
print("=" * 70)

formats = {
    'turtle': 'graph.ttl',
    'xml': 'graph.rdf',
    'n3': 'graph.n3',
    'nt': 'graph.nt',
    'json-ld': 'graph.jsonld'
}

for format_name, filename in formats.items():
    try:
        g.serialize(destination=filename, format=format_name)
        print(f"✓ Граф збережено у форматі {format_name.upper()}: {filename}")
    except Exception as e:
        print(f"✗ Помилка при серіалізації в {format_name}: {e}")

print()

# ===== ЗАПИС У TURTLE =====
print("=" * 70)
print("ГРАФ У ФОРМАТІ TURTLE")
print("=" * 70)
turtle_content = g.serialize(format='turtle')
print(turtle_content)

# Зберігаємо у файл
with open('graph.ttl', 'w', encoding='utf-8') as f:
    f.write(turtle_content)

# ===== ЧИТАННЯ ВІДРЕДАГОВАНОГО ФАЙЛУ =====
print("=" * 70)
print("ЗАВАНТАЖЕННЯ ВІДРЕДАГОВАНОГО ГРАФУ")
print("=" * 70)

# Створюємо новий граф з оновленими даними
g_updated = Graph()
g_updated.bind("ex", EX)
g_updated.bind("foaf", FOAF)

# Копіюємо всі трійки
for triple in g:
    g_updated.add(triple)

# ДОДАЄМО НІМЕЧЧИНУ ДЛЯ КЕЙДА
g_updated.add((cade, EX.visited, EX.Germany))

# ЗМІНЮЄМО ВІК ЕММИ НА 36
g_updated.remove((emma, FOAF.age, Literal(35, datatype=XSD.integer)))
g_updated.add((emma, FOAF.age, Literal(36, datatype=XSD.integer)))

print("✓ Граф оновлено:")
print("  - Кейд тепер також відвідував Німеччину")
print("  - Вік Емми змінено на 36 років")
print(f"\nКількість трійок у оновленому графі: {len(g_updated)}\n")

# Зберігаємо оновлений граф
updated_turtle = g_updated.serialize(format='turtle')
with open('graph_updated.ttl', 'w', encoding='utf-8') as f:
    f.write(updated_turtle)
print("Оновлений граф збережено у: graph_updated.ttl\n")

# ===== ВИВЕДЕННЯ ВСІХ ТРІЙОК =====
print("=" * 70)
print("ВСІ ТРІЙКИ ГРАФУ")
print("=" * 70)
for i, (subj, pred, obj) in enumerate(g_updated, 1):
    print(f"{i}. {subj} -> {pred} -> {obj}")

print(f"\nВсього трійок: {len(g_updated)}\n")

# ===== ТРІЙКИ ПРО ЕММУ =====
print("=" * 70)
print("ТРІЙКИ ПРО ЕММУ")
print("=" * 70)
emma_triples = list(g_updated.triples((emma, None, None)))
for i, (subj, pred, obj) in enumerate(emma_triples, 1):
    print(f"{i}. {subj} -> {pred} -> {obj}")

print(f"\nТрійок про Емму: {len(emma_triples)}\n")

# ===== ТРІЙКИ З ІМЕНАМИ ЛЮДЕЙ =====
print("=" * 70)
print("ТРІЙКИ З ІМЕНАМИ ЛЮДЕЙ")
print("=" * 70)
name_triples = []

# Шукаємо трійки з foaf:name або foaf:givenName
for subj, pred, obj in g_updated:
    if pred == FOAF.name or pred == FOAF.givenName:
        name_triples.append((subj, pred, obj))

for i, (subj, pred, obj) in enumerate(name_triples, 1):
    print(f"{i}. {subj} -> {pred} -> {obj}")

print(f"\nТрійок з іменами: {len(name_triples)}\n")
