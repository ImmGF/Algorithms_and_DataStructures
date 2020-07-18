#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math as mth

#return a editing cost between two sumbols of two respective sequence
def Coster(symbol1,symbol2):
    if symbol1 == symbol2:
        return(0)
    elif symbol1 == '-': 
        return(1)
    elif symbol2 == '-':
        return(1)
    else:
        return(1)

#Calculate editinig distance between two sequences
def EditDistance(seq1, seq2, cost_function = Coster):
    
    EditScoreMatrix = np.zeros((len(seq1) + 1, len(seq2) + 1), dtype=int)
    MoveMatrix = np.empty((len(seq1) + 1, len(seq2) + 1), dtype=str)
    aln_seq1 = ''
    aln_seq2 = ''
    
    for i in range(1,len(seq1)+1):
        EditScoreMatrix[i,0] = EditScoreMatrix[i-1,0] + cost_function(seq1[i-1], '-')
        MoveMatrix[i,0] = 'g'
    for j in range(1,len(seq2)+1):
        EditScoreMatrix[0,j] = EditScoreMatrix[0,j-1] + cost_function('-', seq2[j-1])
        MoveMatrix[0,j] = 'l'
    for i in range(1,len(seq1)+1):
        for j in range(1,len(seq2)+1):
            EditScoreMatrix[i,j] = min(EditScoreMatrix[i-1,j  ] + cost_function(seq1[i-1], '-'),
                                       EditScoreMatrix[i  ,j-1] + cost_function('-', seq2[j-1]),
                                       EditScoreMatrix[i-1,j-1] + cost_function(seq1[i-1], seq2[j-1])
                                       )
            if EditScoreMatrix[i,j] == EditScoreMatrix[i-1,j  ] + cost_function(seq1[i-1], '-'):
                MoveMatrix[i,j] = 'g'
            elif EditScoreMatrix[i,j] == EditScoreMatrix[i  ,j-1] + cost_function('-', seq2[j-1]):
                MoveMatrix[i,j] = 'l'
            elif EditScoreMatrix[i,j] == EditScoreMatrix[i-1,j-1] + cost_function(seq1[i-1], seq2[j-1]):
                MoveMatrix[i,j] = 'u'
    bigger_seq = max(len(seq1), len(seq2))
    x = len(seq1)
    y = len(seq2)
    a = 0
    b = 0
    for k in range(bigger_seq, -1, -1):
        if MoveMatrix[x,y] == 'u':
            aln_seq1 += seq1[len(seq1) - 1 - a]
            aln_seq2 += seq2[len(seq2) - 1 - b]
            a += 1
            b += 1
            x -= 1
            y -= 1
        elif MoveMatrix[x,y] == 'g':
            
            aln_seq1 += seq1[len(seq1) - 1 - a]
            aln_seq2 += '-'
            a += 1
            x -= 1
        elif MoveMatrix[x,y] == 'l':
            aln_seq1 += '-'
            aln_seq2 += seq2[len(seq2) -1 - b]
            b += 1
            y -= 1
        #print("k: ", k, "a: ", a, "b: ", b)

    return(EditScoreMatrix[len(seq1), len(seq2)]) #, aln_seq1[::-1], aln_seq2[::-1])


class PhylNode:
    def __init__(self, distance = None, sequence = None, children = []):
        self.distance = distance
        self.sequence = sequence
        self.children = children

    #return a list of children
    def get_children(self):
        return(self.children)

    #return a distance between a node and its' parent
    def get_distance(self):
        if self.distance:
            return(self.distance)
        else:
            return(None)

    #return a sequence of the node
    def get_sequence(self):
        if self.sequence:
            return(self.sequence)
        else:
            return(None)

    #set the distance between the node and its' parent
    def set_distance(self, distance):
        self.distance = distance

    #set the sequence of the node
    def set_sequence(self, sequence):
        self.sequence = sequence
        
    def distance_sumNode(self, summa):
        summa.append(self.distance)
        
        for child in self.children:
            child.distance_sumNode(summa)
            
        return(sum(summa))
        

    def get_sequencesNode(self, lst):
        lst.append(self.sequence)

        for child in self.children:
            child.get_sequencesNode(lst)

        return(lst)
    
    def calculate_distancesNode(self, parent_sequence, dist_function, lst = []):
        if parent_sequence:
            self.distance = dist_function(self.sequence, parent_sequence)
            #lst.append(self.sequence)
            print("parent: ", parent_sequence,"child: ", self.sequence, " ==== ", self.distance)
        
        for child in self.children:
            child.calculate_distancesNode(self.sequence, dist_function)
            



class PhylTree:
    def __init__(self, node = None):
        self.wooden_root = node

    #return root of the tree
    def root(self):
        return(self.wooden_root)

    #return the sum of all distances in the tree (including root distance from
    #his parent)
    def distance_sum(self):
        summa = []
        
        if self.root != None:
            leaf = self.wooden_root.distance_sumNode(summa)
            
        return(leaf)

    #return a list of sequences from all vertices of the tree, sorted by prefix
    #(first a given vertex, then the first son with descendants, the second son with descendants, etc.)
    def get_sequences(self, lst = []):
        
        if self.root != None:
            self.wooden_root.get_sequencesNode(lst)
            
        return(lst)

    #give all vertices a distance from parents designated with dist_function (default is EditDistance; functions should be
    #apply to vertex labels or sequences); the root should be given a distance of 0 from the parent
    def calculate_distances(self, dist_function = EditDistance):
        
        if self.root != None:
            self.wooden_root.calculate_distancesNode(self.wooden_root.sequence, dist_function)



#Additional functions that help implementing BuilTree() function:
#1.distancer - computes distances between sequences in the list and returns distance matrix
#2.checkAncestors - checks ancestors of the sequence in the tree (tree presented as dictionary)
#3.SeedTree - function that build phylogenetic tree with overall lowest sum of distances for a given sequence list as dictionary
#4.getKeyAsRoot - returns a value which is a root in a given phylogenetic tree (as a dictionary)
#5.build_tree_from_dictionary - builds a tree as a list of lists of PhylNodes objects

#1.
def distancer(seq_lst, max_len_seq, dist_function):
    SequenceDistanceMatrix = np.ones((len(seq_lst), len(seq_lst)), dtype=int)
    SequenceDistanceMatrix *= max_len_seq*5
    
    for i in range(len(seq_lst)):
        for j in range(len(seq_lst)):
            if i != j:
                SequenceDistanceMatrix[i,j] = dist_function(seq_lst[i], seq_lst[j])
            
    return(SequenceDistanceMatrix)
            
#2.
def checkAncestors(dic, value, lst):
    
    lst.append(value)
    for k in dic:
        for v in dic[k]:
            if value == v[0]:
                checkAncestors(dic,k,lst)
    
    return(lst)

#3.
def SeedTree(lst, dist_function):
    
    max_len = 0
    for seq in lst:
        if max_len < len(seq):
            max_len = len(seq)
    
    distance_matrix = distancer(lst, max_len, dist_function)
    
    tree_dic = {}
    for i in range(len(lst)):
        tree_dic[lst[i]] = []
    
    count = 0
    while distance_matrix.min() != max_len*5:
        row = np.where(distance_matrix == distance_matrix.min())[0][0] #parent
        column = np.where(distance_matrix == distance_matrix.min())[1][0] #child
        if count == 0:
            distance_matrix[:,row] = 1
            distance_matrix[:,row] *= max_len*5
                    
        tree_dic[lst[row]].append((lst[column],distance_matrix.min()))
        
        
        
        for key in tree_dic:
            for value in tree_dic[key]:
                empty_ancestors = []
                ancestors = checkAncestors(tree_dic,value[0],empty_ancestors)

                for ancestor1 in ancestors:
                    for ancestor2 in ancestors:
                        x = lst.index(ancestor1)
                        y = lst.index(ancestor2)
                        distance_matrix[x,y] = 1
                        distance_matrix[x,y] = max_len*5
        
        distance_matrix[:,column] = 1
        distance_matrix[:,column] *= max_len*5
        
        #distance_matrix[:,row] = 1
        #distance_matrix[:,row] *= max_len*5
        
        #distance_matrix[column,:] = 1
        #distance_matrix[column,:] *= max_len*5
        
        count += 1
        
    return(tree_dic)

#4.
def getKeyAsRoot(dictionary):
    
    children = [] #list of nodes that are children
    parents = [] #list of nodes that are parents
    
    for key in dictionary:
        parents.append(key)
        values = dictionary[key]
        for value in values:
            children.append(value[0])
    
    children = set(children)
    parents = set(parents)
    
    parent_of_parents = parents.difference(children)
    parent_of_parents = sorted(parent_of_parents)
    
    return(parent_of_parents[0])
            
#5.
def build_tree_from_dictionary(root, dictionary):
    for child in dictionary[root.sequence]:
        ChildDistance = 0 #child[1]
        ChildSequence = child[0]
        ChildNode = PhylNode(distance = ChildDistance, sequence = ChildSequence, children=[])
        root.children.append(ChildNode)
        build_tree_from_dictionary(ChildNode,dictionary)
    return(root)


#function that returns a phylogenetic tree for sequences from the sequences
#list with distances specified with dist_function; the tree should
#be constructed so that the sum of all distances is as small as possible.
def BuildTree(sequences, dist_function=EditDistance):
    
    tree_as_dictionary = SeedTree(sequences, dist_function)
    
    dictionary_root = getKeyAsRoot(tree_as_dictionary)

    TreeRoot = PhylNode(distance = 0, sequence=dictionary_root, children=[])
    tree_from_dictionary_Node = build_tree_from_dictionary(TreeRoot, tree_as_dictionary)
    tree_from_dictionary = PhylTree(node=tree_from_dictionary_Node)
    
    return(tree_from_dictionary)
    

