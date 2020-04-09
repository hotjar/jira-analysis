from os.path import dirname, join, realpath

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


CURRENT_DIR = dirname(realpath(__file__))
ANALYSIS_FILE = "sqlite:///{}".format(join(CURRENT_DIR, "analysis.db"))

engine = create_engine(ANALYSIS_FILE)

_Session = sessionmaker(bind=engine)


def get_session():
    Base.metadata.create_all(engine)
    return _Session()
