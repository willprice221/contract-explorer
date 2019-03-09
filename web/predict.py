#
# Copied from /ml
#
from functions import *
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
