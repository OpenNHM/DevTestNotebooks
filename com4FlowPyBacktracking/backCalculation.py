#/usr/bin/python3

from matplotlib import pyplot as plt

def backTracking(topologyDict, valDict):
    '''
    performs the "back-tracking"

    Parameters
    -----------
    topologyDict: dictionary
        graph topology
    
    valDict: dictionary
        (infrastructure) values associated with each node
    '''

    # sort valDict (so we start traversing from highest infrastructure cells first)
    valDictSorted = {k: v for k, v in sorted(valDict.items(), key= lambda item: item[1], reverse=True)}
    # reverse the graph topology, so "parents" become "children"
    reverseGraph = reverseTopology(topologyDict)
    #print(valDictSorted)
    
    def propagateInfraVal(node, valToPropagate, visited):
        '''
        this is the main concept behind the 'back-tracking' functionality

        Parameters:
        -----------
        node: dictionary key
            current node        
        valToPropagate: int
            (infrastructure) value to propagate
        visited: set()
            set of keys/nodes indicating if node has been visited

        '''
        if node in visited:
            print("already visited %i (val:%i) - current propagation val is: %i" %(node,
                                                                                   valDict.get(node, 0),
                                                                                   valToPropagate))
            return
        elif (valDict.get(node, 0) >= valToPropagate) and bool(visited):
            print("found higher val in %i (val:%i) - current propagation val is: %i" %(node,
                                                                                   valDict.get(node, 0),
                                                                                   valToPropagate))
            return
            
        
        print("current node: %i - valToPropagate: %i"%(node, valToPropagate))
        valDict[node] = max(valDict[node], valToPropagate)
        visited.add(node)

        for parentNode in reverseGraph.get(node, []):
            print("next Parent: %i"%parentNode)
            propagateInfraVal(parentNode, valToPropagate, visited)
    

    for node, val in valDictSorted.items():
        
        if val > 0:
            propagateInfraVal(node, val, set())
    
    return valDict
    
def reverseTopology(graphDict):
    '''
    reverse graph topology, i.e. switch directions of edges in the dir graph

    Parameters
    -----------
    graphDict: python dictionary
        dictonary containing the dir-graph topology
        graph nodes are keys and edges to child-nodes are stored in a list of keys for each key
    '''
    reverseGraph = {}

    for node, children in graphDict.items():
        childSet = set(children)
        if node not in reverseGraph:
            reverseGraph[node] = []
        for child in childSet:
            if child not in reverseGraph:
                reverseGraph[child] = []
            reverseGraph[child].append(node)

    return reverseGraph


def plotGraph(topology, values, positions, nDim = (5,5)):
    '''
    simple plotting function
    '''
    
    colorsInfra = ['white','#fde0dd','#dd3497','#7a0177']
    colorsText  = ['k','k','white','white']
    
    #### draw grid
    fig, ax = plt.subplots()

    for i in range(nDim[0]):
        for j in range(nDim[1]):
            ax.plot(i,j, marker='+', lw=0,
                    markerfacecolor='None',
                    markeredgecolor='k',
                    markersize=10,
                    alpha=.5)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.set_aspect('equal')

    ax.set_xticks(range(nDim[0]))
    ax.set_yticks(range(nDim[1]))
    ax.set_xlim(-0.5,nDim[0]-0.5)
    ax.set_ylim(-0.5,nDim[1]-0.5)
    
    for parent, children in topology.items():
        
        ax.plot(positions[parent][0], positions[parent][1],
                marker='o',
                lw=0,markerfacecolor=colorsInfra[values[parent]],
                markeredgecolor='k',
                markersize=25)
        ax.text(positions[parent][0], positions[parent][1],
                s='%i'%parent, va='center', ha='center',
                color=colorsText[values[parent]], fontsize=12)
        
        
        for child in children:
            ax.annotate('',
                        xy=(positions[child][0], positions[child][1]),
                        xytext=(positions[parent][0], positions[parent][1]),
                        arrowprops=dict(facecolor='k', edgecolor='k',
                                        arrowstyle='->', linewidth=1.,
                                        shrinkA=10, shrinkB=10)
                       )
    ax.set_xlabel('x')
    ax.set_ylabel('y')