import pandas as pd
from copy import copy
from google.oauth2 import service_account

test = ['if','sth',['add',2,3]]
example = [["IF", ["ISZERO", ["EQ", ["STORAGE", 160, 0, 0], "CALLER"]], [["REVERT", 0]], [["IF", ["ISZERO", ["EXTCODESIZE", ["MASK_SHL", 160, 0, 0, ["cd", 4]]]], [["REVERT", 0]], [["CALL", ["ADD", -710, "GAS"], ["MASK_SHL", 160, 0, 0, ["cd", 4]], 0, 1981353871, 'null'], ["IF", ["ISZERO", "ext_call.success"], [["REVERT", 0]], [["IF", ["ISZERO", "ext_call.return_data"], [["REVERT", 0]], [["STORE", 160, 0, 12, [], ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["STOP"]]]]]]]]]]
terminal = []

# Preprocessing
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

credentials = service_account.Credentials.from_service_account_file('/home/ankit//service.json',)
# data query
from google.cloud import bigquery
client = bigquery.Client()
table = 'contract-explorer-233919.ethparis.functions3'  
sql = '''
SELECT *  FROM `{}`
'''.format(table)
data = client.query(sql, location='europe-west2').to_dataframe()

target = data.hash
trees = data.tree

features = []
for t in trees:
    feats = preprocess(t)
    features.append(feats)


# Training
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import time

start = time.time()
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X = vectorizer.fit_transform(features)
X_train, X_test, y_train, y_test = train_test_split(X, target, test_size=0.33)
rf = RandomForestClassifier(n_estimators=50, n_jobs=60).fit(X_train,y_train)
print(rf.score(X_test, y_test))
end = time.time()
print('time {}s'.format(end-start))
