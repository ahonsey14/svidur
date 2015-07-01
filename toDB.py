import pandas as pd
from os import listdir 
from re import findall # regular expressions
from sqlalchemy import create_engine # your engine rears its ugly head

# the path where your downloaded files are
dir_path = '/Users/jamesquadrino/Desktop/competition_data/'
# files in that folder
files = listdir(dir_path)[1::]

engine = create_engine('mysql://root:@localhost:3306/cat')

#go through your files, read the csv, name the table according to filename, add table to cat
for fi in files:
    filename = pd.read_csv(dir_path + fi)
    name = findall("\w*(?=.csv)",fi)[0]
    filename.to_sql(name = name,con = engine, flavor = "mysql", if_exists = "replace")
    

