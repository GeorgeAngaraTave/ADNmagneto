from app.ext.rest import HttpStatus, Rest
from app.ext.resource_handler import ResourceHandler

from app.adn.models.Adns import Adn

from app import db

from flask import request, escape



class ViewAdn(ResourceHandler):

    def post(self):
        content = request.get_json()
        try:
            dna = content.get('adn')
            is_mutant = self.is_mutant(dna)

            if is_mutant == True:
                return Rest.response(200, HttpStatus.OK, "Is  mutant")
            else:
                return Rest.response(403, HttpStatus.FORBIDDEN, "Is not mutant")

        except Exception as e:
            reason = "ViewAdn Exception: {0}".format(e)
            print(reason)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(reason)})


    def is_mutant (self, dna)-> bool:
        result = False
        file   = len(dna)
        column = len(dna[0])
        ran = int(column)-1
        list_json = []

        suma = 0
        # primer nivel
        for f in range(file):

            is_valid = self.is_valid_strucrt(dna[f])
            if is_valid ==  False:
                return is_valid

            suma += self.validate_adn(dna[f])
            cal = []
            dig1 = []
            for c in range(column):
                if f+c <= ran:
                    dig1.append(dna[f+c][c])
                cal.append(dna[f][c])

            string_column = "".join(cal)
            suma += self.validate_adn(string_column)
            string_dig1 = "".join(dig1)
            suma +=  self.validate_adn(string_dig1)
        # Segundo nivel
        file   = file - 1
        column = ran
        for i in range(0,file+1):
            cont = 0
            larger_array = []
            for j in range(i,column+1):
                if cont != j:
                    if j <= column:
                        larger_array.append(dna[cont][j])
                cont =  cont + 1

            string_column = "".join(larger_array)
            suma += self.validate_adn(string_column)


        if suma > 1:
            result = True
        else:
            result = result

        to_adn = Adn.get_by('sequence', str(dna))

        if to_adn is None:
            list_json.append({
                'sequence': str(dna),
                'is_valid': result
            })

            db.engine.execute(Adn.__table__.insert(), list_json)
            db.session.commit()


        return  result

    def is_valid_strucrt (self, cadena)-> bool:
        result = True
        _len = len(cadena)
        expression = "ATCG"

        for item in range(_len):
            if expression.count(cadena[item]) < 1:
                result = False

        return  result

    def validate_adn(self, cadena) -> int:
        count = 0

        if cadena.count('AAAA') == 1:
            count = count +1
        elif cadena.count('TTTT') == 1:
            count = count +1
        elif cadena.count('CCCC') == 1:
            count = count +1
        elif cadena.count('GGGG') == 1:
            count = count +1

        return int(count)








