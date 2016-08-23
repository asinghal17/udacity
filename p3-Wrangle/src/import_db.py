import sqlite3
import pandas as pd

db = sqlite3.connect('sqlite/openstreetmap.db')
db.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

#DF
nodes_df = pd.read_csv(NODES_PATH)
node_tags_df =pd.read_csv(NODE_TAGS_PATH)
ways_df=pd.read_csv(WAYS_PATH)
way_nodes_df=pd.read_csv(WAY_NODES_PATH)
way_tags_df=pd.read_csv(WAY_TAGS_PATH)

#TO SQL
nodes_df.to_sql('nodes',db,index=True, if_exists='append',chunksize=1000)
node_tags_df.to_sql('node_tags',db,index=True, if_exists='append',chunksize=1000)
ways_df.to_sql('ways',db,index=True, if_exists='append',chunksize=1000)
way_nodes_df.to_sql('way_nodes',db,index=True, if_exists='append',chunksize=1000)
way_tags_df.to_sql('way_tags',db,index=True, if_exists='append',chunksize=1000)

db.commit()
db.close()