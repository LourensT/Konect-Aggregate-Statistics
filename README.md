# Konect-Aggregate-Statistics
Aggregate statistics from the http://konect.cc/ project

Webscraped data on the networks over on the KONECT project. Features so far includes 1326 networks with:
* Name (some meaningless symbols (*) have been appended to use the name as a primary key)
* Attributes (list of strings)
* n (# of nodes, [source](http://konect.cc/statistics/size/))
* n1 (# of left nodes for bipartite networks, [source](http://konect.cc/statistics/size/) )
* n2 (# of right nodes for bipartite networks, [source](http://konect.cc/statistics/size/) )
* diameter (the maximal distance between any two nodes, where the distance between two nodes is defined as the number of edges in the shortest path from one node to another, [source](http://konect.cc/statistics/diam/))