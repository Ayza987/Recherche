from app.database.database import Base
from app.database.database import engine

from app.database.models import *

Base.metadata.create_all(bind=engine)

print("Tables créées")