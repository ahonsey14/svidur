#pandas is for r dataframe like structures in python, highly recommended generally
import pandas as pd
import numpy as np 
from sklearn import preprocessing
import sqlengine

def CatEncoder(col):
    t = col.astype("category")
    t_categories = list(t.cat.categories)
    original = dict((key, value) for (key, value) in zip(t_categories, range(len(t_categories))))
    t2 = t.cat.rename_categories(original.values())
    return t2, original
    
def fannwriter(dataframe, path):
    print "writing file"
    shape = dataframe.shape
    f = open(path, "w")
    text = str(shape[0]) + " " + str(shape[1]-1) + " " + str(1) + "\n"
    f.writelines(text)
    y = dataframe["cost"]
    x = dataframe.drop("cost",1)
    t1 = y.iloc[0]
    t2 = x.iloc[0,]
    f.writelines((" ".join([str(l) for l in t2.values])) + "\n" + str(t1) + "\n")
    for i in np.arange(1,shape[0]):
      f.writelines((" ".join([str(l) for l in x.iloc[i,].values])) + "\n" + str(y.iloc[i]) + "\n")
    f.close()
    return "file successfully written"
    
engine = sqlengine.connect_to_db("ubuntu")

#query your DB using pandas, and your engine
print "Querying data..."
data = pd.read_sql(("SELECT train.tube_assembly_id, train.supplier, train.quote_date, \
train.annual_usage, train.min_order_quantity, train.bracket_pricing, train.quantity, \
train.cost, tube.material_id, tube.diameter, tube.material_id, tube.diameter, tube.wall,\
tube.length, tube.num_bends, tube.bend_radius, tube.end_a_1x, tube.end_a_2x, tube.end_x_1x,\
tube.end_x_2x, tube.end_a, tube.end_x, tube.num_boss, tube.num_bracket, tube.other,\
specs.spec1, specs.spec2, specs.spec3, specs.spec4, specs.spec5, specs.spec6,\
specs.spec7, specs.spec8, specs.spec9, specs.spec10 \
FROM train_set as train JOIN tube ON train.tube_assembly_id = tube.tube_assembly_id JOIN specs ON train.tube_assembly_id = specs.tube_assembly_id"),
engine)

print "cleaning/processing data"
#replace nas with 0
data = data.fillna(0)

#seperate numerical and categorical
numerical = data.select_dtypes(include = [np.float64, np.int64]) # sub out those that equal int64, float64
categorical = data.select_dtypes(exclude = [np.float64, np.int64])
cat_names = list(categorical.columns.values)

#replace categorical
# matrix of same size as categorical
size = categorical.shape
res = np.zeros(size)
d = {}

#change categorical values to numeric encoding
#need categorical names?
for i in range(categorical.shape[1]):
    temp = CatEncoder(categorical.iloc[::,i])
    res[:,i] = temp[0]
    d[categorical.iloc[::,i].name] = temp[1] #save the dictionary so we can perform same conversion on all data

categorical = pd.DataFrame(res)
categorical.columns = cat_names # this isnt matching up

#join the 2 matrices into a dataframe, need to check column names

data_trans = pd.concat((numerical,categorical),1)
n = data_trans.columns
data_trans = preprocessing.scale(data_trans)

#output in the FANN friendly format... yuck
#this takes forever, needs to be chunked up or something... but it works

data_trans = pd.DataFrame(data_trans)
data_trans.columns = n

msk = np.random.rand(len(data_trans)) < 0.8
train = data_trans[msk]
test  = data_trans[-msk]

fannwriter(train, "/home/ubuntu/svidur/data_train.data")
fannwriter(test, "/home/ubuntu/svidur/data_test.data")


