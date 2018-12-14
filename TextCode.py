from tqdm import tqdm
from collections import defaultdict 
from collections import deque
import matplotlib.pyplot as plt 
import random
import sys
sys.setrecursionlimit(5000)
def utils(nodes, value=None):
    P = {}
    for node in nodes:
        if value is None:
            P[node] = []
        else:
            P[node] = value
    return P

class Graph(object):
    
    def __init__(self, txt_file, sample):

        with open(txt_file) as f:
            self.words = f.readlines()
        self.words = [word[:-1] for word in self.words if word[:-1] != '']
        if sample is not None: self.words = self.words[:sample]
        d = {}
        self.graph = defaultdict(list)
        # nodes = [Node(word) for word in self.words]
        self.word_to_indices = {word: i for i, word in enumerate(self.words)}
        # print(word_to_indices["whish"])
#         self.graph = [[]] * len(self.words)
        for word in self.words:
#             self.graph[self.word_to_indices[word]] = []
            for i in range(len(word)):
                bucket = word[:i] + '_' + word[i+1:]
                if bucket in d:
                    d[bucket].append(word)
                else:
                    d[bucket] = [word]

    # add vertices and edges for words in the same bucket
        for bucket in d.keys():        
          for word1 in d[bucket]:
              for word2 in d[bucket]:
                if word1 != word2:
                    self.graph[self.word_to_indices[word1]].append((self.word_to_indices[word2], 1))
                              # print(word2)
                    # for word in self.graph[self.word_to_indices[word1]]:
                    #     print(self.words[word], end=' ')
                    #     print('\n')
                    #     if word1 == 'wolds':
        for word in self.words: 
            if self.word_to_indices[word] not in self.graph:
                self.graph[self.word_to_indices[word]] = []

        self.neighbors = {}
        for node in self.graph:
            self.neighbors[node] = []
            for adjcent_node, w in self.graph[node]:
                self.neighbors[node].append(adjcent_node)

    def weights(self):
        sum_ = 0
        for node1 in self.graph:
            for node2, w in self.graph[node1]:
                sum_ += w 

        return sum_ / 2

    def getEdges(self, get_weight=False):
        edges = []
        for node1 in self.graph:
            for node2, w, in self.graph[node1]:
                if (node1, node2) in edges or (node2, node1) in edges:
                    continue
                if get_weight:
                    item = (node1, node2, w)
                else:
                    item = (node1, node2)
                edges.append(item)

        return edges

    def getNeighbors(self, vertex):
        neighbors = []
        for node, _ in self.graph[vertex]:
            neighbors.append(node)

        return neighbors

    def removeEdges(self, r):
        for node1 in self.graph:
            for node2, w in self.graph[node1]:
                if node1 in r and node2 in r:                   
                     self.graph[node1].remove((node2, w))
                    

    def updateEdges(self, all_Betweenness):
        for node1 in self.graph:
            for i in range(len(self.graph[node1])):
              temp = list(self.graph[node1][i])
              try:
                  temp[1] = all_Betweenness[(node1, self.graph[node1][i][0])]
              except:
                  temp[1] = all_Betweenness[(self.graph[node1][i][0], node1)]
              self.graph[node1][i] = tuple(temp)
                

    def dfsUtil(self, v, visited, _list):
        visited[v] = True
        _list.append(v)
        for i, _ in self.graph[v]:
            if visited[i] == False:
                self.dfsUtil(i, visited, _list)

    def connectedComponents(self):
        visited = [False]*len(self.graph)
        count = 0
        connected_Components = {}
        for i in self.graph:
            if visited[i] == False:
                connected_Components['{}th'.format(count)] = []
                self.dfsUtil(i, visited, connected_Components['{}th'.format(count)])
                count = count + 1

        return connected_Components

    def printConnectedComponents(self):
        connected_Components = self.connectedComponents()
        for subgraph in connected_Components:
            print('The ' + subgraph + ' connected components are : ', end=' ')
            for node in connected_Components[subgraph]:
                print(node, end=' ')
            print('\n')

    def BFS(self, source, destination):
        start = self.word_to_indices[source]
        target = self.word_to_indices[destination]
        visited = [False] * len(self.graph)
        pred = [-1] * len(self.graph)
        dist = [len(self.graph) + 1] * len(self.graph)
        queue = []
        visited[start] = True
        dist[start] = 0
        queue.append(start)

        while len(queue):
            temp = queue.pop(0)
#             print(self.words[temp], end=" ")
            for i, _ in self.graph[temp]:  
                if visited[i] == False: 
                    visited[i] = True
#                     print(self.words[i], end=" ")
                    pred[i] = temp
                    dist[i] = dist[temp] + 1
                    queue.append(i) 
                    if i == target:
                        self.pred = pred
                        self.dist = dist
                        return True
#             print("\n")
        return False

    def printShortestDistance(self, start, target):
        if self.BFS(start, target) is False:
            print("Given source and destination are not connected")
        else:
            print("Done!!")
            path = []
            crawl = self.word_to_indices[target]
            path.append(crawl)
            while self.pred[crawl] != -1:
                path.append(self.pred[crawl])
                crawl = self.pred[crawl]

            print("Shortest path length is : ", self.dist[self.word_to_indices[target]])
            print("Path is:", end=" ")
            for i in path[::-1]:
                print(self.words[i], end=" "),

class gravinNewman(object):

    def __init__(self, g):
        self.g = g

    @staticmethod
    def calBetweenness(g):
        _edges = g.getEdges()
        all_Betweenness = {}
        for edge in _edges:
            all_Betweenness[edge] = 0

        for node in g.graph:
            vertex = node
            visited = set()
            visited.add(vertex) 
            to_visit = deque(g.neighbors[vertex])
            nodes = {}
            level = 1
            nodes[vertex] = 0
            for item in to_visit:
                nodes[item] = level
            while(to_visit):
                start_node = to_visit.popleft()
                visited.add(start_node)
                all_neighbors = g.neighbors[start_node]
                neighbors = []
                for item in all_neighbors:
                    if item not in visited and item not in to_visit:
                        neighbors.append(item)
                        # try:
                        level = nodes[start_node] + 1
                        nodes[item] = level
                for item2 in neighbors:
                    to_visit.append(item2)
                
            lowest_level = 0
            for k, v in nodes.items():
                if lowest_level < v:
                    lowest_level = v
            edges = {}
            nodes_value = {}
            for i_node, value in nodes.items():
                nodes_value[i_node] = 1

            for i in range(lowest_level, 0, -1):
                nodes_lvl = []
                for k1, v1 in nodes.items():
                    if v1 == i:
                        nodes_lvl.append(k1)

                for node_lvl in nodes_lvl:
                    parents = []
                    node_neighbors = g.neighbors[node_lvl]
                    for node_neighbor in node_neighbors:
                        if nodes[node_neighbor] == nodes[node_lvl] - 1:
                            parents.append(node_neighbor)
                    weight = nodes_value[node_lvl] / len(parents)
                    for parent in parents:
                        nodes_value[parent] += weight
                        edges[(node_lvl, parent)] = edges.setdefault((node_lvl, parent), 0) + nodes_value[node_lvl]

            for k3, v3 in edges.items():
                for k4, v4 in all_Betweenness.items():
                    if k3 == k4 or (k3[1] == k4[0] and k3[0] == k4[1]):
                        all_Betweenness[k4] += v3 / 2.0
        max_result = 0
        for i in all_Betweenness:
            if max_result < all_Betweenness[i]:
                max_result = all_Betweenness[i]
        # print(max_result, end=' ')
        g.updateEdges(all_Betweenness)

        return g

    def myCalBetweenness(self, g):
        betweenness = {}
        for node in g.nodes:
            betweenness[node] = 0.0

        for node1, node2 in g.edges:
            betweenness[(node1, node2)] = 0.0

        nodes = g.nodes
        for s in nodes:
            S, P, sigma = self._single_source_shortest_path_basic(g, s)
            betweenness = self._accumulate_edges(betweenness, S, P, sigma, s)

        for node in g.graph:
            del betweenness[node]
        betweenness = self._rescale(betweenness, len(g.graph))
        g.updateEdges(betweenness)
        return betweenness

    @staticmethod
    def _single_source_shortest_path_basic(g, s):
        S = []
        P = utils(g.nodes)
        sigma = utils(g.nodes, value=0.0)
        D = {}
        sigma[s] = 1.0
        D[s] = 0
        Q = [s]
        while Q:
            v = Q.pop(0)
            S.append(v)
            Dv = D[v]
            sigmav = sigma[v]
            for w in G[v]:
                if w not in D:
                    Q.append(w)
                    D[w] = Dv + 1
                if D[w] == Dv + 1:   # this is a shortest path, count paths
                    sigma[w] += sigmav
                    P[w].append(v)  # predecessors
        return S, P, sigma

    @staticmethod
    def _accumulate_edges(betweenness, S, P, sigma, s):
        # betweenness[s] += len(S) - 1
        delta = utils(S, value=0)
        while S:
            w = S.pop()
            coeff = (1.0 + delta[w]) / sigma[w]
            for v in P[w]:
                c = sigma[v] * coeff
                if (v, w) not in betweenness:
                    betweenness[(w, v)] += c
                else:
                    betweenness[(v, w)] += c
                delta[v] += c
            if w != s:
                betweenness[w] += delta[w]

        return betweenness
    @staticmethod
    def _rescale_e(betweenness, n):
        if n <= 1:
            scale = None  # no normalization b=0 for all nodes
        else:
            scale = 1.0 / (n * (n - 1))
        
        if scale is not None:
            for v in betweenness:
                betweenness[v] *= scale
        return betweenness

    def modularity(partition, g):
        inc = dict([])
        deg = dict([])
        links = g.weights()
        
        if links == 0:
            return 0
        for node in g.graph:
            com = partition[node]
            deg[com] = deg.get(com, 0.) + len(g.graph[node])
            for neighbor, w in g.graph[node]:
                edge_weight = w
                if partition[neighbor] == com:
                    inc[com] = inc.get(com, 0.) + float(edge_weight)
                else:
                    inc[com] = inc.get(com, 0.) + float(edge_weight) / 2.
        res = 0
        for com in set(partition.values()):
            res += (inc.get(com, 0.) / links) - (deg.get(com, 0.) / (2. * links)) ** 2
        return res 

    def remove(self, g_b):
        g_a = self.calBetweenness(g_b)
        items = g_a.getEdges(get_weight='True')
        sort_items = sorted(items, key=lambda item: item[2], reverse=True)
        remove_v = sort_items[0][2]
        r_s_remove = []
        for s_item in sort_items:
            if s_item[2] == remove_v:
                r_s_remove.append(s_item)

        for r in r_s_remove:
            g_a.removeEdges(r)
            sort_items.remove(r)

        return g_a

    def implementation(self):
        duplicate_g = self.g
        original_partition = {}
        mods = []
        for node in duplicate_g.graph:
            original_partition[node] = 0
        original_mod = self.modularity(original_partition, self.g)
        mods.append([original_mod, original_partition])
        while len(duplicate_g.connectedComponents()) != len(self.g.graph):
            duplicate_g = self.remove(duplicate_g)
            subgraphs = duplicate_g.connectedComponents()
            partitions = {}
            num_sub = 0
            for subgraph in subgraphs:
                num_sub += 1
                for sub_g_node in subgraphs[subgraph]:
                    partitions[sub_g_node] = partitions.setdefault(sub_g_node, -1) + num_sub

            mod = self.modularity(partitions, self.g)
            mods.append([mod, partitions])

        mods_items = sorted(mods, key=lambda x: x[0], reverse=True)
        com_dic = mods_items[0]
        return com_dic[0]

g = Graph('sgb_words.txt', 800)
# g.printConnectedComponents()
gravinNewman = gravinNewman(g)
# print(gravinNewman.implementation())
