import hashlib
from rdflib import Graph, URIRef, Literal
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
        
        # iterate over the chunks
        for chunk in chunks:

            # create uri
            uri = self.create_uri(chunk)
            print uri

            # create triples
            graph.add((URIRef(uri), URIRef("http://nlp2rdf.lod2.eu/schema/sso/posTag"), Literal(chunk.split("/")[1])))

        # optionally serialize the graph in a given format
        # TODO RDF/json not supported by rdflib
        if self.options.get('format'):
            return graph.serialize(format=self.options.get("format")[0])
        else:
            return graph.serialize()

    def create_uri(self, chunk):
        # first we create the the base uri
        if self.options.get("prefix"):
            uri = self.options.get("prefix")
        else:
            uri = gethostname()

        word = chunk.split("/")[0]
        # now create the unique identifier
        if self.options.get("urirecipe") == "offset":
            uri += "#offset_"
            uri += str(self.text.find(word)) + "_"
            uri += str(self.text.find(word) + len(word)) + "_"
        elif self.options.get("urirecipe") == "context-hash":
            uri += "#hash_"
            uri += "4_"
            uri += str(len(word)) + "_"
            index = self.text.find(word)
            context = self.text[max(0,index-4):index]
            context += "(" + word + ")"
            context += self.text[index+len(word):min(len(self.text),index+len(word)+4)]
            uri += hashlib.md5(context).hexdigest() + "_"
        uri += word[:20]

        return uri
    
    def pos_tag(self):
        # tag the text with MontyTagger
        tagger = MontyTagger()
        text = tagger.tag(self.text)

        # return the text splitted into the chunks
        return text.split(" ")
    
if __name__ == "__main__":
    options = {
        'urirecipe': "context-hash",
        'prefix': "http://example.com"
        }
    text = raw_input("Text: ")
    print "---------------------"
    wrapper = Wrapper(text, options)
    print "---------------------\n"
    print wrapper.nlp2rdf()

