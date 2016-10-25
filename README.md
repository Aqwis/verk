# verk

Generates a social network graph of names extracted from a set of articles. (In this context, the word "article" refers to any piece of text but is typically a news article or similar.) `verk` outputs a CSV representation of the social network graph on the format used by the graph visualization tool [gephi](https://gephi.org/).

`verk` works by looking at each article in the set individually, extracting a list of the names found in the article. The weight of the vertex (connection) between two names is increased by one each time the two names are found in the same article. In other words, people who often get mentioned in the same article will be strongly connected in the graph, while people who rarely or never get mentioned together will have a weak or no connection. Note that `verk` only generates a CSV file consisting of pairs of names and the weight of the connection between them. A tool such as `gephi` must be used to *visualise* the graph.

The original application of `verk` was to visualise connections between members of the student community in Trondheim, Norway based on articles from the online student newspaper [dusken.no](http://dusken.no/). An example visualisation of a graph generated on the basis of the most recent 1100 articles at dusken.no (as of April 2016) can be seen below.

<a href="url"><img src="examples/dusken.png?raw=true" height="500" width="500" ></a>

In this example, the vertices (people) and edges (connections) are coloured according to cluster membership.

## How to use

```
pip install -r requirements.txt
./verk.py --help
```

For example, if the articles for the dusken.no example are contained in the folder `dusken/`, the graph above may be generated using the command `./verk.py -v --parser dusken --clean dusken`.
