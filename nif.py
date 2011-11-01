import hashlib
import urllib
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from socket import gethostname

from MontyTagger import MontyTagger

class Wrapper():
    """
    This class is a wrapper for the MontyLingua POS-Tagger.

    It mainly converts a given text through the tagger to
    the NIF RDF format.
    """
    def __init__(self, text, options=None):
        self.text = text
        self.options = options

    def nlp2rdf(self):
        chunks = self.pos_tag()
        print chunks

        graph = Graph()

        # define some namespaces
        STRING = Namespace("http://nlp2rdf.lod2.eu/schema/string/")
        SSO =  Namespace("http://nlp2rdf.lod2.eu/schema/sso/")

        # generate the triples referencing the document as a whole
        doc_uri = self.create_uri(self.text)
        graph.add((URIRef(doc_uri), RDF.type, STRING["Document"]))
        graph.add((URIRef(doc_uri), STRING["sourceString"], Literal(self.text)))

        
        uri_recipe = "OffsetBasedString" if self.options.get("urirecipe") == "offset" else "ContextHashBasedString"
        graph.add((URIRef(doc_uri), RDF.type, STRING[uri_recipe]))
        
        # iterate over the chunks
        for chunk in chunks:

            uri = self.create_uri(chunk)

            # normative requirements
            graph.add((URIRef(uri), RDF.type, STRING[uri_recipe]))
            graph.add((URIRef(doc_uri), SSO["word"], URIRef(uri)))
            
            # plain pos tag
            graph.add((URIRef(uri), SSO["posTag"], Literal(chunk.split("/")[1])))

        # some prefix beauty
        graph.bind('sso', URIRef("http://nlp2rdf.lod2.eu/schema/sso/"))
        graph.bind('string', URIRef("http://nlp2rdf.lod2.eu/schema/string/"))
            
        # optionally serialize the graph in a given format
        # TODO RDF/json not supported by rdflib
        if self.options.get('format'):
            return graph.serialize(format=self.options.get("format"))
        else:
            return graph.serialize()

    def create_uri(self, chunk):
        # first we create the the base uri
        if self.options.get("prefix"):
            prefix = self.options.get("prefix")
        else:
            prefix = gethostname()

        word = chunk.split("/")[0]
        # now create the unique identifier
        if self.options.get("urirecipe") == "offset":
            uri = "offset_"
            uri += str(self.text.find(word)) + "_"
            uri += str(self.text.find(word) + len(word)) + "_"
        elif self.options.get("urirecipe") == "context-hash":
            uri = "hash_"
            uri += "4_"
            uri += str(len(word)) + "_"
            index = self.text.find(word)
            context = self.text[max(0,index-4):index]
            context += "(" + word + ")"
            context += self.text[index+len(word):min(len(self.text),index+len(word)+4)]
            uri += hashlib.md5(context).hexdigest() + "_"
        uri += word[:20]

        return prefix + urllib.quote_plus(uri)
    
    def pos_tag(self):
        # tag the text with MontyTagger
        tagger = MontyTagger()
        text = tagger.tag(self.text)

        # return the text splitted into the chunks
        return text.split(" ")
    
if __name__ == "__main__":
    options = {
        'urirecipe': "context-hash",
        'prefix': "http://example.com#"
        }
    text = raw_input("Text: ")
    print "---------------------"
    wrapper = Wrapper(text, options)
    print "---------------------\n"
    print wrapper.nlp2rdf()

