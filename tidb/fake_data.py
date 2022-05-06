import pandas as pd
import random
from faker import Faker
from collections import defaultdict
from sqlalchemy import create_engine

fake = Faker()

fake_data = []
count = 100 * 1000
for _ in range(count):
    fake_data.append({
        'name': fake.name(),
        'email': fake.email(),
        'address': fake.address(),
        'job': fake.job(),
        'sex': random.choice(['F', 'M']),
        'age': random.randint(1, 100)
    })

df = pd.DataFrame(fake_data)
engine = create_engine('mysql://root:@127.0.0.1:4040/tests')
print("insert to db")
df.to_sql(
    'user',
    con=engine,
    index=False,
    if_exists='append',
    chunksize=1000
)
