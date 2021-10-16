import pickle
import configparser
import json
import os
import random
from multiprocessing import Process

with open('G:/lol/Evaluation/7dabcf7f-7a35-438e-89ce-87e12a3f659e.pickle', 'rb') as f:
    evalf = pickle.load(f)
    print(evalf)