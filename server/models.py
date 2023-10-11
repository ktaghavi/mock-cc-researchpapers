from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Research(db.Model, SerializerMixin):
    __tablename__ = 'researches'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    #Add Relationship
    researchauthors = db.relationship("ResearchAuthors", backref="research")

    #Add Seralization 
    serialize_rules = ('-researchauthors.research',)

    #Add Validation
    @validates('year')
    def validate_year(self, key, year):
        if len(str(year)) == 4:
            return year
        else:
            return ValueError('Invalid Year')

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    #Add Relationship
    researchauthors = db.relationship("ResearchAuthors", backref="author")

    #Add Seralization
    serialize_rules = ('-researchauthors.authors',)

    #Add Validation
    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        if field_of_study not in ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']:
            return ValueError('Invalid field of study!')

        else:
            return field_of_study

class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'researchauthors'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))


    #Add Seralization
    serialize_rules = ('-research', '-author')
