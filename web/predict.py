#
# Copied from /ml
#
from copy import copy
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
import pickle

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
    paths = Node(tree).downward_paths()
    flat = flatten(paths)
    return ' '.join(flat)


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

rf = pd.read_pickle('models/rf.p')
pipe = pd.read_pickle('models/pipe.p')

def predict_model(tree, N=3):
    '''
    Input: JSON tree, N
    Output: Top N probabilities, Top N classes (lists)'''

    #run data preprocessing pipeline
    pp = Preprocess().fit_transform(tree)
    result_test = pipe.transform(pp)

    #make prediction, sort indices by highest probability
    probs = rf.predict_proba(result_test)
    indices = np.argsort(probs, axis=1)[:,-N:]
    p = copy(probs)
    p.sort(axis=1)

    #sort in reverse order, flatten to 1D array (don't do flatten if predicting multiple points at once)
    top_n_probs = p[:,-N:][:,::-1].flatten()
    top_n_classes = rf.classes_[indices][:,::-1].flatten()

    return list(top_n_probs), list(top_n_classes)
