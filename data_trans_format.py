#pandas is for r dataframe like structures in python, highly recommended generally
import pandas as pd
import numpy as np
from sqlalchemy import create_engine #sql alchemy module, to connect to your database

def CatEncoder(col):
    t = col.astype("category")
    t_categories = list(t.cat.categories)
    original = dict((key, value) for (key, value) in zip(t_categories, range(len(t_categories))))
    t2 = t.cat.rename_categories(original.values())
    return t2, original

#create an engine to connect/add tables/read from sql
#requires credentials for your db, the ones i have entered are default for a database named cat
engine = create_engine('mysql://root:@localhost:3306/cat')

#query your DB using pandas, and your engine
data = pd.read_sql("SELECT train.tube_assembly_id, train.supplier, train.quote_date, train.annual_usage, train.min_order_quantity, train.bracket_pricing, train.quantity, train.cost, tube.material_id, tube.diameter, tube.material_id, tube.diameter, tube.wall, tube.length, tube.num_bends, tube.bend_radius, tube.end_a_1x, tube.end_a_2x, tube.end_x_1x, tube.end_x_2x, tube.end_a, tube.end_x, tube.num_boss, tube.num_bracket, tube.other, specs.spec1, specs.spec2, specs.spec3, specs.spec4, specs.spec5, specs.spec6, specs.spec7, specs.spec8, specs.spec9, specs.spec10 FROM train JOIN tube ON train.tube_assembly_id = tube.tube_assembly_id JOIN specs ON train.tube_assembly_id = specs.tube_assembly_id",
                  engine)

#replace nas with 0
data = data.fillna(0)

#dummy vars
numerical = data.select_dtypes(include = [np.float64, np.int64]) # sub out those that equal int64, float64
categorical = data.select_dtypes(exclude = [np.float64, np.int64])

#replace categorical
# matrix of same size as categorical
size = categorical.shape
res = np.zeros(size)
d = {}

#change categorical values to numeric encoding
for i in range(categorical.shape[1]):
    temp = CatEncoder(categorical.iloc[::,i])
    res[:,i] = temp[0]
    d[categorical.iloc[::,i].name] = temp[1] #save the dictionary so we can perform same conversion on all data

#join the 2 matrices into a numpy matrix
numerical = numerical.as_matrix()
data_trans = np.concatenate((numerical,res),1)

for i in range(2):
    string = " "
    print string.join(str(data.iloc[::,1]))