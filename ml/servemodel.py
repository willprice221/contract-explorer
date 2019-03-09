

#given a tree and pickled model, predict top N probabilities and classes
from functions import *

#unpickle processing pipeline and model
rf = pd.read_pickle('pickle/rf.p')
pipe = pd.read_pickle('pickle/pipe.p')

#example data
example = [["IF", ["ISZERO", ["EQ", ["STORAGE", 160, 0, 0], "CALLER"]], [["REVERT", 0]], [["IF", ["ISZERO", ["EXTCODESIZE", ["MASK_SHL", 160, 0, 0, ["cd", 4]]]], [["REVERT", 0]], [["CALL", ["ADD", -710, "GAS"], ["MASK_SHL", 160, 0, 0, ["cd", 4]], 0, 1981353871, 'null'], ["IF", ["ISZERO", "ext_call.success"], [["REVERT", 0]], [["IF", ["ISZERO", "ext_call.return_data"], [["REVERT", 0]], [["STORE", 160, 0, 12, [], ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["STOP"]]]]]]]]]]

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


print(predict_model(example, N=3))