"""
noGO SqlAlchemy ORM specification file
@author dpb
@date   7/11/2013
"""

from sqlalchemy import *
from sqlalchemy.orm import relation
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

url = "mysql://dpb:dpb_nyu@handbanana.bio.nyu.edu:3306/"

def setup(db="noGO", echo=False, recycle=3600):
    e = create_engine(url+db, echo=echo, pool_recycle=recycle)
    b = declarative_base(bind=e)
    s = sessionmaker(bind=e)
    return e,b,s
Engine, Base, Session = setup()

def push_to_db(session, object, exception_str=None, raise_on_duplicate=True):
    """
    A simple utility function to do the session add-flush-catch-refresh blocks.
    If raise_on_duplicate is true, will raise exception on IntegrityError. If false, will rollback and continue
        session - the Session to push ORM objects into
        object  - the ORM object to add to the session (and DB)
        exception_str   - a string to print when flushing the session fails (DB error)
    """
    if not exception_str:
        exception_str = "Failed to add object {0} to DB".format(object)

    session.add(object)
    try: 
        session.flush()
    except IntegrityError:
        print "Given object already exists in DB"
        if raise_on_duplicate:
            session.rollback()
            print exception_str
            raise
        else:
            print "Rolling back, returning None"
            session.rollback()
            return None 
    except Exception:
        print exception_str
        raise
    session.refresh(object)
    return object


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

class Version(Base):
    """
    Table representing the Version information in the database. Holds GO date and the date of the GO 
    set used for validation
    """
    __tablename__ = "version"
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['human9606.version_id']),
        ForeignKeyConstraint(['id'], ['mouse10090.version_id']),
        ForeignKeyConstraint(['id'], ['yeast4932.version_id']),
        ForeignKeyConstraint(['id'], ['worm6239.version_id']),
        ForeignKeyConstraint(['id'], ['arabidopsis3702.version_id']),
        ForeignKeyConstraint(['id'], ['rice39947.version_id']),
        {'autoload': True}
    )
    
    def __repr__(self, ):
        return "<Version {0}: GO {1}, Validation {2}>".format(self.id, self.go_date, self.validation_date)

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
    version = relation(Version, primaryjoin="Human9606.version_id==Version.id", uselist=False)

    def __repr__(self, ):
        return "<Human9606 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm_id, self.rank)

class Mouse10090(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "mouse10090"
    __table_args__ = (
        ForeignKeyConstraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Mouse10090.algorithm_id==Algorithm.id", uselist=False)
    version = relation(Version, primaryjoin="Mouse10090.version_id==Version.id", uselist=False)

    def __repr__(self, ):
        return "<Mouse10090 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm_id, self.rank)

class Yeast4932(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "yeast4932"
    __table_args__ = (
        ForeignKeyConstraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Yeast4932.algorithm_id==Algorithm.id", uselist=False)
    version = relation(Version, primaryjoin="Yeast4932.version_id==Version.id", uselist=False)

    def __repr__(self, ):
        return "<Yeast4932 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm_id, self.rank)

class Worm6239(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "worm6239"
    __table_args__ = (
        ForeignKeyConstraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Worm6239.algorithm_id==Algorithm.id", uselist=False)
    version = relation(Version, primaryjoin="Worm6239.version_id==Version.id", uselist=False)

    def __repr__(self, ):
        return "<Worm6239 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm_id, self.rank)

class Arabidopsis3702(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "arabidopsis3702"
    __table_args__ = (
        ForeignKeyConstraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Arabidopsis3702.algorithm_id==Algorithm.id", uselist=False)
    version = relation(Version, primaryjoin="Arabidopsis3702.version_id==Version.id", uselist=False)

    def __repr__(self, ):
        return "<Arabidopsis3702 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm_id, self.rank)


class Rice39947(Base):
    """
    Table representing the negative examples of genes per GO term in Human 9606
    """
    __tablename__  = "rice39947"
    __table_args__ = (
        ForeignKeyConstraint(['algorithm_id'], ['algorithm.id']),
        {'autoload': True}
    )
    algorithm = relation(Algorithm, primaryjoin="Rice39947.algorithm_id==Algorithm.id", uselist=False)
    version = relation(Version, primaryjoin="Rice39947.version_id==Version.id", uselist=False)

    def __repr__(self, ):
        return "<Rice39947 NegEG: {0}, gene {1}, algorithm {2}, rank {3}>".format(self.go_id, self.gene_symbol, self.algorithm_id, self.rank)

