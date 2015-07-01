#pandas is for r dataframe like structures in python, highly recommended generally
import pandas as pd
from sqlalchemy import create_engine #sql alchemy module, to connect to your database
from fann2 import libfann #neural net, not implemented yet

#create an engine to connect/add tables/read from sql
#requires credentials for your db, the ones i have entered are default for a database named cat
engine = create_engine('mysql://root:@localhost:3306/cat')

#query your DB using pandas, and your engine
data = pd.read_sql("SELECT train.tube_assembly_id, train.supplier, train.quote_date, train.annual_usage, train.min_order_quantity, train.bracket_pricing, train.quantity, train.cost, tube.material_id, tube.diameter, tube.material_id, tube.diameter, tube.wall, tube.length, tube.num_bends, tube.bend_radius, tube.end_a_1x, tube.end_a_2x, tube.end_x_1x, tube.end_x_2x, tube.end_a, tube.end_x, tube.num_boss, tube.num_bracket, tube.other, specs.spec1, specs.spec2, specs.spec3, specs.spec4, specs.spec5, specs.spec6, specs.spec7, specs.spec8, specs.spec9, specs.spec10 FROM train JOIN tube ON train.tube_assembly_id = tube.tube_assembly_id JOIN specs ON train.tube_assembly_id = specs.tube_assembly_id",
                  engine)
#replace nas with 0
data = data.fillna(0)


