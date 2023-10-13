from sqlalchemy.engine import result
from sqlalchemy.sql.expression import null
from app.ext.rest import HttpStatus, Rest
from app.ext.resource_handler import ResourceHandler

from app import db

from app.adn.models.Adns import Adn



class ViewStatistics(ResourceHandler):


    def get(self, id=0):

        if id > 0:
            return Rest.response( 405, HttpStatus.RESOURCE_NOT_EXIST )
        else:
            try:

                mutant_dna = db.session.query(Adn.id).filter_by(is_valid=1).count()
                human_dna = db.session.query(Adn.id).filter_by(is_valid=0).count()
                ratio = "{0:.1f}".format(float(human_dna / mutant_dna))

                result = {
                    "count_mutant_dna": mutant_dna,
                    "count_human_dna": human_dna,
                    "ratio": float(ratio)
                }

                return Rest.response(200, HttpStatus.OK, result)

            except Exception as e:
                reason = "ViewStatus Exception: {0}".format(e)
                print(reason)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(reason)})

