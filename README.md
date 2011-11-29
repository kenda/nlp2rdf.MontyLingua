# About
This is an adapter for [NLP2RDF](http://nlp2rdf.org) and the MontyLingua Toolkit.

# Requirements
- [MontyLingua](http://web.media.mit.edu/~hugo/montylingua/)
- [rdflib](http://www.rdflib.net/)

Before using the tool you have to define an environment variable called MONTYLINGUA which links to the directory containing the datafiles (.MDF).

For example:
`export MONTYLINGUA=/home/foo/montylingua-2.1/python`
  
# Usage
## Webservice
`python server.py`

The webservice runs on port 8001 at /service by default. For parameters etc see the [NIF spec](http://nlp2rdf.org/nif-1-0#toc-parameters).

Therefore you can `curl` your query like this

`curl "http://localhost:8001/service?nif=true&input-type=text&input=This%20is%20a%20city%20called%20Berlin."`

or simply use your browser to query the target.

## Console
`python nif.py`

But this method is mainly for debugging purposes and supports only hardcoded options.

# Example
Take a look at this [gist](https://gist.github.com/1309886) for an example output.

# Troubleshooting
* **There are abnormal POS tags used instead of the normal PENN tagset.**

	This means that the lexicon files of MontyLingua weren't created correctly.
	Try removing the `FASTLEXICON_*.MDF` files in the `python` directory of MontyLingua 
	and run your query again. MontyLingua will create new lexicon files.
 
 
