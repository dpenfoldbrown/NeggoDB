"""
NeggoDB SqlAlchemy ORM specification file
@author dpb
@date   7/11/2013
"""

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

url = "mysql://dpb:dpb_nyu@handbanana.bio.nyu.edu:3306"

def setup(db="neggoDB", echo=False, recycle=3600):
    e = create_engine(url+db, echo=echo, pool_recycle=recycle)
    b = declarative_base(bind=e)
    s = sessionmaker(bind=e)
    return e,b,s
Engine, Base, Session = setup()


class Algorithm(Base):
    """
    Table representing Algorithm in NeggoDB database. ID and description of algorithms
    """
    __tablename__  = "algorithm"
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['human9606.algorithm_id']),
        ForeignKeyConstraint(['id'], ['mouse10090.algorithm_id']),
        ForeignKeyConstraint(['id'], ['yeast4932.algorithm_id']),
        ForeignKeyConstraint(['id'], ['worm6239.algorithm_id']),
        ForeignKeyConstraint(['id'], ['arabidopsis3702.algorithm_id']),
        ForeignKeyConstraint(['id'], ['rice39947.algorithm_id']),
        {'autoload': True}
    )

    def __repr__(self, ):
        return "<Algorithm id: {0}, name: {1}>".format(self.id, self.name)

#class Human9606(Base):
#    """
#    Table representing the negative examples of genes per GO term in Human 9606
#    """
    

