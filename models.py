from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref, declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
Database_URL = "sqlite:///theater.db"
engine = create_engine(Database_URL)
session = sessionmaker(bind=engine)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)

    auditions = relationship("Audition", back_populates="role")

    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired_audition = [audition for audition in self.auditions if audition.hired]
        return hired_audition[0] if hired_audition else "no actor has been hired for this role"
     
    
    def understudy(self):
        hired_audition = [audition for audition in self.auditions if audition.hired]
        return hired_audition[1] if len(hired_audition) > 1 else "no actor has been hired for understudy for this role"

class Audition(Base):
    __tablename__ = "auditions"

    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    hired = Column(Boolean, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = True

session = session()
 
# role1 = Role(character_name="The Narrator")
# session.add(role1)
# session.commit()

# audition1 = Audition(actor="Will Smith", location="New York", hired=False, role_id=role1.id)
# audition2 = Audition(actor="Tom Cruise", location="New York", hired=False, role_id=role1.id)
# session.add_all([audition1, audition2])
# session.commit()

# audition1.call_back()
# audition2.call_back()
# session.commit()

# print(role1.actors())
# print(role1.locations())
# print(role1.lead())
# print(role1.understudy())