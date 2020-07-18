#!/usr/bin/env python
# coding: utf-8


class PhylNode:
    def __init__ (self, distance, children = [], aggregate_max = 0, aggregate_min = 0):
        #self.name = name
        self.distance = distance
        self.distance_dummy = distance
        self.children = children
        self.aggregate_max = aggregate_max
        self.aggregate_min = aggregate_min

    #return list of children
    def get_children(self):
        return(self.children)

    #return a distance from a node to the root
    def get_distance(self):
        return(self.distance)

    #set sequence of a node
    def set_distance(self, distance):
        self.distance = distance

    #get median path distance from all nodes to the root
    def get_median(self, all_paths, path):
        if not self.children:
            all_paths.append(path)
            
        for child in self.children:
            child.get_median(all_paths, path + child.distance)
        
        if len(all_paths) > 0:
            med_lst = all_paths
            med_lst.sort()
        
        if len(med_lst) % 2 != 0:
            median = med_lst[(int((len(med_lst)-1)/2))]
        else:
            median = (med_lst[(int((len(med_lst))/2))] + med_lst[(int((len(med_lst))/2)) - 1])/2
        
        return(median)

    #get average path distance from all nodes to the root
    def get_avg(self, cur_path, all_paths):
        if not self.children:
            all_paths.append(cur_path)
            
        for child in self.children:
            child.get_avg(cur_path + child.distance, all_paths)
                
        return(sum(all_paths)/len(all_paths))

    #get minimum path distance from all nodes to the root
    def get_min(self):
        min_value = 0.0
        
        for child in self.children:
            value = child.get_min() + child.get_distance()
            if min_value == 0 or min_value > value:
                min_value = value
                
        return(min_value)

    #get maximum path distance from all nodes to the root
    def get_max(self):
        max_value = 0
        
        for child in self.children:
            value = child.get_max() + child.get_distance()
            if max_value < value:
                max_value = value
            
        return(max_value)

    def elongate(self,remainder):
        
        for child in self.children:
            child.distance = remainder - child.aggregate_max + child.distance_dummy
            child.elongate(remainder - child.distance)
            
        return(self.distance)
    
    def truncate(self,remainder):
        
        for child in self.children:
            if remainder > 0:
                if child.distance >= remainder:
                    child.distance = remainder
                    child.nullifier()
                elif child.distance < remainder:
                    child.truncate(remainder - child.distance)
            
        return(self.distance)
    
    def nullifier(self):
        for child in self.children:
            child.distance = 0
            child.nullifier()
    
    def unify(self, cur_path, threshold):
        if cur_path + self.distance > threshold:
            self.distance += threshold - cur_path
            self.nullifier()
            return(True)
        if cur_path + self.distance < threshold and not self.children:
            self.distance += threshold - cur_path
        
        for child in self.children:
            child.unify(cur_path + child.distance, threshold)
            
        return(self.distance)
    
    def get_aggregate_max(self, value = 0):
        if not self.children:
            value = self.distance
            self.aggregate_max = value
        
        for child in self.children:
            if self.aggregate_max == 0 or self.aggregate_max < child.get_aggregate_max() + self.distance:
                self.aggregate_max = child.get_aggregate_max() + self.distance
                
        return(self.aggregate_max)
    
    def get_aggregate_min(self, value = 0):
        if not self.children:
            value = self.distance
            self.aggregate_min = value
        
        for child in self.children:
            if self.aggregate_min == 0 or self.aggregate_min >= child.get_aggregate_min() + self.distance:
                self.aggregate_min = child.get_aggregate_min() + self.distance
                
        return(self.aggregate_min)
    
    def show_aggregate_max(self, cur_path = float, all_paths = float):
        if not self.children:
            all_paths.append(cur_path)
            
        for child in self.children:
            child.show_aggregate_max(cur_path +[child.aggregate_max], all_paths)
                
        return(all_paths)
    
    def show_aggregate_min(self, cur_path, all_paths):
        if not self.children:
            all_paths.append(cur_path)
            
        for child in self.children:
            child.show_aggregate_min(cur_path +[child.aggregate_min], all_paths)
                
        return(all_paths)
    
    def show_paths(self, cur_path, all_paths):
        if not self.children:
            all_paths.append(cur_path)
            
        for child in self.children:
            child.show_paths(cur_path +[child.distance], all_paths)
                
        return(all_paths)



class PhylTree:
    def __init__(self,node = None):
        self.root = node;
        
    def root(self):
        return(self.root)
    
    def average_leaf_distance(self):
        if self.root != None: 
            value = 0.0
            lst = []
            leaf = self.root.get_avg(value,lst)
            return(leaf)
    
    def min_leaf_distance(self):
        if self.root != None: 
            leaf = self.root.get_min()
            return(leaf)
    
    def max_leaf_distance(self):
        if self.root != None: 
            leaf = self.root.get_max()
            return(leaf)

    #modify edge weights so that all combined distances from root to
    #the leaves were equal, with neither weight being reduced
    def elongate_distances(self):
        if self.root != None:
            self.root.get_aggregate_max()
            longest_path = self.root.get_max()
            leaf = self.root.elongate(longest_path)
            return(leaf)

    #modify edge weights so that all combined distances from root to
    #the leaves were equal, with neither weight being increased
    def truncate_distances(self):
        if self.root != None:
            self.root.get_aggregate_min()
            shortest_path = self.root.get_min()
            leaf = self.root.truncate(shortest_path)
            return(leaf)

    #modify edge weights so that all cumulative distances from root to leaf
    #were equal
    def unify_distances(self):
        if self.root != None:
            all_paths = []
            path = 0
            threshold = self.root.get_median(all_paths, path)
            cur_path = 0
            self.root.unify(cur_path, threshold)
    
    def show_tree(self):
        if self.root != None:
            cur_path = [] 
            all_paths = []
            tree = self.root.show_paths(cur_path, all_paths)
            return(tree)

