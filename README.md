## A graph modification approach for k-anonymity in social networks using the genetic algorithm in Social Network Analysis and Mining
Social networks, which have become so popular today, allow their users to share information. The main challenge the users are facing is the security preservation of their information and privacy. Therefore, structural anonymity techniques were introduced that would hide the identity of users. One of the drawbacks of these techniques, which are based on graph modification, is the lack of attention about the structural semantics of graphs. This paper focuses on the popular notion of a privacy protection method called k-degree anonymization and tries to reduce utility loss on the graph. The new k-degree anonymization method, genetic k-degree edge modification, has two steps. The first step includes partitioning of vertices and community detection in the graph. The result of these two determines the needed increase in edges for every vertex in each society to achieve k-degree anonymization. The second step is graph modification using the genetic algorithm by adding some edges between vertices in each community. Average Path Length (APL), Average Clustering Coefficient, and Transitivity (T) are employed to evaluate the method. The proposed algorithm has been tested on four datasets, and the results have shown the average relative performance demonstrates more stability than the other four well-known algorithms. Also, APL criterion in our algorithm is better preserved than all other algorithms; furthermore, Transitivity parameters are the best result in most cases
### installation
```commandline
pd@asgar:~/Dev/Gits/genetic_alg$ python3 -m venv venv
pd@asgar:~/Dev/Gits/genetic_alg$ source venv/bin/activate
(venv) pd@asgar:~/Dev/Gits/genetic_alg$ pip install -r requirment.txt 
(venv) pd@asgar:~/Dev/Gits/genetic_alg$ sudo apt-get install python3-tk
```
### run 
```commandline
(venv) pd@asgar:~/Dev/Gits/genetic_alg$ python main.py 
reading file finished!
drawing graph.
draw finished.
run partitining
main.py:15: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3, and in 3.9 it will stop working
  if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
run community detection
community detection finished!
drawing nodes of communites...
drawing community detection finished!
drawing network edges...
0.0% is running. making ready genetic for: [{1: 1, 2: 0, 3: 0, 4: 1, 5: 0}, 1, 2, 1, 3, 2, 4, 2, 3, 2, 5, 3, 5, 3, 6, 4, 5, 5, 8, 8, 9, 8, 7, 9, 7, 7, 6]
running GA for  {1: 1, 2: 0, 3: 0, 4: 1, 5: 0}
0.5% is running. making ready genetic for: [{8: 0, 9: 1, 7: 0, 6: 1}, 1, 2, 1, 3, 2, 4, 2, 3, 2, 5, 3, 5, 3, 6, 4, 5, 5, 8, 8, 9, 8, 7, 9, 7, 7, 6]
running GA for  {8: 0, 9: 1, 7: 0, 6: 1}
drawing graph.
draw finished.
writing to file...

```

### Links:

- paper: https://rdcu.be/b4BMp

- citation:
```
@article{10.1007/s13278-020-00655-6, 
  author = {Rajabzadeh, Sara and Shahsafi, Pedram and Khoramnejadi, Mostafa}, 
  title = {{A graph modification approach for k-anonymity in social networks using the genetic algorithm}}, 
  issn = {1869-5450}, 
  doi = {10.1007/s13278-020-00655-6}, 
  abstract = {{Social networks, which have become so popular today, allow their users to share information. The main challenge the users are facing is the security preservation of their information and privacy. Therefore, structural anonymity techniques were introduced that would hide the identity of users. One of the drawbacks of these techniques, which are based on graph modification, is the lack of attention about the structural semantics of graphs. This paper focuses on the popular notion of a privacy protection method called k-degree anonymization and tries to reduce utility loss on the graph. The new k-degree anonymization method, genetic k-degree edge modification, has two steps. The first step includes partitioning of vertices and community detection in the graph. The result of these two determines the needed increase in edges for every vertex in each society to achieve k-degree anonymization. The second step is graph modification using the genetic algorithm by adding some edges between vertices in each community. Average Path Length (APL), Average Clustering Coefficient, and Transitivity (T) are employed to evaluate the method. The proposed algorithm has been tested on four datasets, and the results have shown the average relative performance demonstrates more stability than the other four well-known algorithms. Also, APL criterion in our algorithm is better preserved than all other algorithms; furthermore, Transitivity parameters are the best result in most cases.}}, 
  pages = {38}, 
  number = {1}, 
  volume = {10}, 
  journal = {Social Network Analysis and Mining}, 
  year = {2020}
}
```

- contact me: `pedram.shahsafi@email.kntu.ac.ir`

- any problem: make a new `issue`.