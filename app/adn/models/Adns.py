from app import db
from app.ext.generic_model import GenericModel

class Adn(GenericModel):
    __tablename__ = 'adns'

    id          = db.Column( db.Integer, primary_key=True )
    sequence    = db.Column( db.String(100), nullable=False )
    is_valid    = db.Column( db.Boolean, nullable=False )
    added_on    = db.Column( db.DateTime, nullable=False, server_default=db.FetchedValue() )
    update_on   = db.Column( db.DateTime )
