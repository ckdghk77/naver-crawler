'''
Created on Jul 1, 2016

@author: TYchoi
'''
import pickle

def pickleSaver(wantToSave, name):
    with open(name+'.pkl','wb') as pickle_file:
        pickle.dump(wantToSave, pickle_file)
        
def pickleLoader(name):
    with open(name+'.pkl','rb') as pickle_load:
        wantToLoadAs = pickle.load(pickle_load)   
    return wantToLoadAs
    