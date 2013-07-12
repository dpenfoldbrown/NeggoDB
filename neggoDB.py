"""
NeggoDB SqlAlchemy ORM specification file
@author dpb
@date   7/11/2013
"""

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = "mysql://dpb:dpb_nyu@handbanana.bio.nyu.edu:3306/"

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

class Human9606(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "human9606"
    __table_args__ = (
        ForeignKeyConstraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Human9606.algorithm_id==Algorithm.id", uselist=False)

    def __repr__(self, ):
        return "<Human9606 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm.name, self.rank)

class Mouse10090(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "Mouse10090"
    __table_args__ = (
        ForeignKeyContraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Mouse10090.algorithm_id==Algorithm.id", uselist=False)

    def __repr__(self, ):
        return "<Mouse10090 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm.name, self.rank)

class Yeast4932(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "Yeast4932"
    __table_args__ = (
        ForeignKeyContraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Yeast4932.algorithm_id==Algorithm.id", uselist=False)

    def __repr__(self, ):
        return "<Yeast4932 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm.name, self.rank)

class Worm6293(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "Worm6293"
    __table_args__ = (
        ForeignKeyContraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Worm6293.algorithm_id==Algorithm.id", uselist=False)

    def __repr__(self, ):
        return "<Worm6293 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm.name, self.rank)

class Arabidopsis3702(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "Arabidopsis3702"
    __table_args__ = (
        ForeignKeyContraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Arabidopsis3702.algorithm_id==Algorithm.id", uselist=False)

    def __repr__(self, ):
        return "<Arabidopsis3702 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm.name, self.rank)


class Rice39947(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "Rice39947"
    __table_args__ = (
        ForeignKeyContraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Rice39947.algorithm_id==Algorithm.id", uselist=False)

    def __repr__(self, ):
        return "<Rice39947 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm.name, self.rank)

