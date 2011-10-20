from MontyTagger import MontyTagger

class Wrapper():
    """
    This class is a wrapper for the MontyLingua POS-Tagger.

    It mainly converts a given text through the tagger to
    the NIF RDF format.
    """
    def pos_tag(self, text):
        # tag the text with MontyTagger
        tagger = MontyTagger()
        text = tagger.tag(text)
        
        # convert the tagged text to RDF
        pass

        return text
    
if __name__ == "__main__":
    text = raw_input("Text: ")
    print "---------------------"
    wrapper = Wrapper()
    print "---------------------\n" + wrapper.pos_tag(text)
