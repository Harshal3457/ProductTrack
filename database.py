
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:root@localhost:5432/harry"

engine=create_engine(db_url)
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)