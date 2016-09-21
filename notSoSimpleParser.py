# load necessary libraries, create a Graph object and feed it with the triples
try:
    from rdflib import Graph, URIRef
except ImportError:
    print("Det verkar som att rdflib inte är installerat. Är du säker på att du startat Python 3?")
g = Graph()
try:
    g.parse('beskrivningar.rdf', format="turtle")
except IOError:
    print("Filen kan inte hittas. Kontrollera filens namn och var den ligger i filsystemet")
except SyntaxError:
    print("RDF-filen är inte helt korrekt")
# create an empty list to append with all subjects of the RDF file
List = []
# create an empty list to append with all creator values of the RDF file
authors = []
a = Graph()
for (s,p,o) in g:
    List.append(s)
# make each item in the list unique
Terms = set(List)
# get and print creator, year and title for each subject (manifestation)
authorsInDBpedia = []
for i in Terms:
    Data = {}
    for (l,m,o) in g:
        if l == i and 'creator' in m and type(o) == URIRef:
            # resolve the URI for creators to get their authorized names
            # The string with the largest length is catched, though it is not always the best
            if o not in authors: # Check if creator graph from Libris is not already retrieved
                authors.append(o) # Here it is a URIRef
                a.parse(o) # Here the triples for o is added to the creator store a
            name = URIRef(u"http://xmlns.com/foaf/0.1/name") 
            abst = URIRef(u'http://www.w3.org/2002/07/owl#sameAs')
            h = [] # A container for a set of explicit name strings for creator o
            for (b,c,d) in a.triples((o,name,None)): # If there is a name string for creator
                h.append(d) # add the name to h
                for (x,y,z) in a.triples((o,abst,None)): # Traverse the a graph to determine if there is a link to dbpedia
                    if 'dbpedia' in z:
                        # print(z)
                        authorsInDBpedia.append(z) # append this Libris-link to the list of creators with dbpedia content
            Data['auth'] = max(h, key=len) # Add the longest explicit name as author
        elif l == i and 'creator' in m: # Only if Libris-link is missing, add explicit string: fall-back
            Data['auth'] = o
        elif l == i and 'date' in m:
            Data['year'] = o
        elif l == i and 'title' in m:
            Data['tit'] = o
    try:
        print(Data['auth']+'. ('+Data['year']+'). '+Data['tit'])
    except Exception:
        print('Dina data saknar troligen title, creator eller date för subjektet')
Authorities = set(authorsInDBpedia)

for i in Authorities:
    y = Graph()
    try: 
        y.parse(i)
        generator = y.objects(i, URIRef(u'http://dbpedia.org/ontology/abstract'))
        for i in generator:
            if i.language == 'en':
                print('\n'+i)
    except Exception:
        print("Problem med accessen till DBpedia. Försök senare")
    
