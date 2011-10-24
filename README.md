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

## Console
`python nif.py`

But this method doesn't support any options yet.

# Example
Take a look at this [gist](https://gist.github.com/1309886) for an example output.
