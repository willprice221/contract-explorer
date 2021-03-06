from copy import copy
import numpy as np
import pandas as pd
from google.cloud import bigquery
client = bigquery.Client()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
import pickle
import json

terminal = []
class Node:

    def __repr__(self):
        if len(self.children) == 0:
            return self.name
        else:
            return f'( {self.name} '+ (' '.join([str(c) for c in self.children]))+' )'

    def __init__(self, exp, parent=None):
        self.parent = parent
        self.children = []

        if type(exp) == list and len(exp)>0:
            self.name = exp[0] if type(exp[0]) == str else 'list'
            if self.name != 'list':
                for e in exp[1:]:
                    self.children.append(Node(e, parent=self))
            else:
                for e in exp:
                    self.children.append(Node(e, parent=self))

        else:
            self.name=str(exp)
            global terminal
            terminal.append(self)

    def downward_paths(self, max_len= None ):
        result = []
        vocab = set()

        def dfs(node, path_so_far, ignore):

            path_so_far = copy(path_so_far)
            path_so_far.append(node.name)
                
            if len(node.children) == 0:
                result = [path_so_far]
            else:
                result = []
            
            for c in node.children:
                if c is not ignore:
                    result.extend(dfs(c, path_so_far, node))

            return result

        psf = []
        return dfs(self, psf, None)
    

flatten = lambda l: [item for sublist in l for item in sublist]

def preprocess(tree):
    tree = json.loads(tree)
    paths = Node(tree).downward_paths()
    flat = flatten(paths)
    result =  ' '.join(flat)
    return result.replace('list', '')


class Preprocess:
    
    def __init__(self):
        pass
    
    def fit_transform(self, trees, y=0):
        self.features = []
        for t in trees:
            feats = preprocess(t)
            self.features.append(feats)
        return self.features
    
    def transform(self):
        return self.features



class ToArray:
    
    def __init__(self):
        pass
    
    def fit_transform(self, X, y=0):
        return X.toarray()
    
    def transform(self, X):
        return X.toarray()
    
    def fit(self, X, y=0):
        return X.toarray()
    
def load_from_bigquery(table, limit=''):
    sql = '''
    SELECT *  FROM `{}` {}
    '''.format(table, limit)

    df = client.query(sql, location='europe-west2').to_dataframe()
    return df