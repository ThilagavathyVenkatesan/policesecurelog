import pandas as pd
from sqlalchemy import create_engine

# ✅ Read cleaned CSV
df = pd.read_csv("cleaned_traffic_data.csv", low_memory=False)

# ✅ MySQL connection using SQLAlchemy
engine = create_engine("mysql+pymysql://root:@localhost/securecheck1")

# ✅ Insert into MySQL
df.to_sql(name="traffic_stops", con=engine, if_exists="fail", index=False)

print("✅ Data inserted into 'securecheck.traffic_stops' successfully.")
