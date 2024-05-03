import io
import json

import matplotlib.pyplot as plt
import pydotplus
from IPython.display import display
from SPARQLWrapper import SPARQLWrapper, JSON, RDF
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, RDFS
from rdflib.tools.rdf2dot import rdf2dot


def visualize(g):
    for s, p, o in g:
        print((s, p, o))

    stream = io.StringIO()
    rdf2dot(g, stream, opts={display})
    dg = pydotplus.graph_from_dot_data(stream.getvalue())
    png = dg.create_png()
    image = plt.imread(io.BytesIO(png))

    plt.imshow(image)
    plt.show()


def build_graph1():
    print("Stwórz graf używając składni N3")
    g = Graph()
    n3data = """\
    @prefix : <http://example.org/ns/graph1#> .
    :Ola  :hasParent :Jan ;
          :gender    :female .
    :Ewa  :hasParent :Jan ;
          :gender    :female .
    :Jan  :gender    :male .
    :Mike :hasParent :Ewa ;
          :gender    :male ."""
    g.parse(data=n3data, format="n3")
    return g


def lookup_ewa_in_graph1(g):
    print("Wyszukaj Ewę po globalnym identyfikatorze")
    ewa = URIRef('http://example.org/ns/graph1#Ewa')
    print([o for o in g.predicate_objects(subject=ewa)])


def build_graph2():
    print("Stwórz graf konstruując węzły")
    g = Graph()

    zygmunt = URIRef("http://example.org/ludzie/Zygmunt")
    aniela = BNode()

    name = Literal('Zygmunt')
    age = Literal(24)

    g.add((zygmunt, RDF.type, FOAF.Person))
    g.add((zygmunt, FOAF.name, name))
    g.add((zygmunt, FOAF.age, age))
    g.add((zygmunt, FOAF.knows, aniela))

    g.add((aniela, RDF.type, FOAF.Person))
    g.add((aniela, FOAF.name, Literal('Aniela')))
    return g


def simple_sparql_query(g):
    print("Proste zapytanie SPARQL")
    result = g.query("SELECT * WHERE {?s ?p ?o}")
    for row in result:
        print(row)


def who_knows_each_other(g):
    result = g.query(
        """SELECT DISTINCT ?aname ?bname
           WHERE {
              ?a foaf:knows ?b .
              ?a foaf:name ?aname .
              ?b foaf:name ?bname .
           }""", initNs={'foaf': FOAF})

    for row in result:
        print("%s knows %s" % row)


def build_graph3():
    g = Graph()
    n3data = """
    @prefix ex: <http://example.org/schemas/vehicles#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .    
    ex:Zwierze            rdf:type          rdfs:Class .
    ex:Ssak               rdf:type          rdfs:Class .
    ex:Roslina            rdf:type          rdfs:Class .
    ex:Pies               rdf:type          rdfs:Class .
    ex:Karp               rdf:type          rdfs:Class .
    ex:Drzewo             rdf:type          rdfs:Class .

    ex:Ssak               rdfs:subClassOf   ex:Zwierze .
    ex:Pies               rdfs:subClassOf   ex:Ssak .
    ex:Karp               rdfs:subClassOf   ex:Zwierze .
    ex:Drzewo             rdfs:subClassOf   ex:Roslina .
    """

    g.parse(data=n3data, format="n3")
    return g


def which_is_zwierze(g):
    print("Zwraca zwierzeta")
    result = g.query(
        """SELECT DISTINCT ?s WHERE {
        ?s ?p ?o .
        ?s rdfs:subClassOf+ ex:Zwierze . }""",
        initNs={'rdfs': RDFS, 'rdf': RDF, 'ex': 'http://example.org/organizmy#'})

    for row in result:
        print(row)


def explore_dbpedia():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery("""
    SELECT ?city ?populationTotal
    WHERE {
      ?city rdf:type dbo:City .
      ?city dbo:populationTotal ?populationTotal .
      FILTER(?populationTotal > 20000000)
    }
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    json_string = json.dumps(results)
    print(json_string)


if __name__ == '__main__':
    g1 = build_graph1()
    visualize(g1)
    lookup_ewa_in_graph1(g1)

    # g2 = build_graph2()
    # visualize(g2)
    # simple_sparql_query(g2)
    # who_knows_each_other(g2)

    # g3 = build_graph3()
    # visualize(g3)
    # which_is_zwierze(g3)

    # explore_dbpedia()
