# Konect-Aggregate-Statistics
Aggregate statistics from the http://konect.cc/ project

Webscraped data on the networks over on the KONECT project. Features so far includes 1326 networks with:
* Name (some meaningless symbols (*) have been appended to use the name as a primary key)
* Attributes (list of strings)
* n (# of nodes, [source](http://konect.cc/statistics/size/))
* n1 (# of left nodes for bipartite networks, [source](http://konect.cc/statistics/size/) )
* n2 (# of right nodes for bipartite networks, [source](http://konect.cc/statistics/size/) )
* δ diameter (the maximal distance between any two nodes, where the distance between two nodes is defined as the number of edges in the shortest path from one node to another, [source](http://konect.cc/statistics/diam/))
* c Cluster Coefficient (the probability that a random chosen wedge (i.e., 2-star) is completed by a third edge to form a triangle. Multiple edges, edge directions and loops are not taken into account, [source](http://konect.cc/statistics/clusco/) )

## To Be Added
* Maximal (in-) degrees
* Size of gian component
* Median distance 
* 90\% quantile of typical distance