# -*- coding: utf-8 -*-

"""Python module of common functions."""

import re
import unicodedata
import json
import re
import time
from datetime import datetime, timedelta, date, time
from jsonschema import Draft7Validator, draft7_format_checker
from app.config.storage import ALLOWED_EXTENSIONS, ALLOWED_IMG_EXTS
from typing import List, Any


class customEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return (datetime.min + obj).time().isoformat()
        else:
            return super(customEncoder, self).default(obj)

        return json.JSONEncoder.default(self, obj)


class Commons:
    @staticmethod
    def validate(data, fields):
        if fields is None:
            return None

        obj = []
        try:
            for field in fields:
                if field not in data or data.get(field) is None:
                    obj.append(field)
                else:
                    pass
            return obj if len(obj) > 0 else None
        except Exception as e:
            print("validate Exception:", e)
            return None

    @staticmethod
    def validate_email(email):
        if email is None:
            return None

        try:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

            if match is None:
                return False
            else:
                return True
        except Exception as e:
            print("validate_email Exception:", e)
            return False

    @staticmethod
    def validate_url( url ):
        regex = re.compile (
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        return re.match( regex, url ) is not None

    @staticmethod
    def create_name_from_email(email):
        if email is None:
            return None

        try:
            return re.sub(r'_+|-+|\.+|\++', ' ', email.split('@')[0]).title()
        except Exception as e:
            print("create_name_from_email Exception:", e)
            return None

    @staticmethod
    def is_iterable(value):
        if value is None:
            return None

        return isinstance(value, (tuple, list))

    @classmethod
    def remove_accents(self, unicode_str):
        if unicode_str is None:
            return None

        try:
            return ''.join((char_at for char_at in unicodedata.normalize('NFD', unicode_str) if unicodedata.category(char_at) != 'Mn'))
        except Exception as e:
            print("remove_accents Exception:", e)
            return None

    @classmethod
    def sanity_check(self, dirty_str, upper=False, use_encode=False):
        if dirty_str is None:
            return None

        u_str = None

        try:
            if use_encode is True:
                u_str = dirty_str.encode("utf-8")
            else:
                u_str = dirty_str
        except Exception as e:
            print("sanity_check encode Exception:", e)
            return None

        normalize_str = self.remove_accents(u_str)
        clean_str = normalize_str.replace(" ", "_")

        if upper:
            return clean_str.upper()

        return clean_str

    @staticmethod
    def to_json(obj=None, sort=False, encoding_type='ISO-8859-1', response='json'):
        if obj is None:
            return None

        try:
            # str_result = json.dumps(obj, encoding=encoding_type, indent=4, sort_keys=sort, cls=customEncoder)
            str_result = json.dumps(obj, indent=4, sort_keys=sort, cls=customEncoder)

            if response == 'json':
                result = json.loads(str_result)
                return result
            elif response == 'str':
                return str_result
        except Exception as e:
            print("to_json Exception:", e)
            return None

    @staticmethod
    def get_file_size(file_size, format='B'):
        if file_size is None:
            return None

        if format is 'B':
            total_bytes = round(float(float(file_size)), 2)
            return total_bytes
        if format is 'Kb':
            kbs = round(float(float(file_size) / 1024), 2)
            return kbs
        elif format is 'Mb':
            megas = round(float(float(file_size) / 1024) / 1024, 2)
            return megas
        else:
            return None

    @staticmethod
    def allowed_files(filename=None):
        if filename is not None:
            if '.' in filename:
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in ALLOWED_EXTENSIONS:
                    return True, ext
        return False, None

    @staticmethod
    def allowed_images(filename=None):
        if filename is not None:
            if '.' in filename:
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in ALLOWED_IMG_EXTS:
                    return True, ext
        return False, None

    @staticmethod
    def clean_string(ugly_cad=None):
        if ugly_cad is None:
            return None

        special_list = [{"b": "á", "g": "a"}, {"b": "é", "g": "e"}, {"b": "í", "g": "i"}, {"b": "ó", "g": "o"},
                        {"b": "ú", "g": "u"}, {"b": "Á", "g": "A"}, {"b": "É", "g": "E"}, {"b": "Í", "g": "I"},
                        {"b": "Ó", "g": "O"}, {"b": "Ú", "g": "U"}, {"b": "ñ", "g": "n"}, {"b": "Ñ", "g": "N"},
                        {"b": "\xe1", "g": "a"}, {"b": "\xe9", "g": "e"}, {"b": "\xed", "g": "i"},
                        {"b": "\xf3", "g": "o"}, {"b": "\xfa", "g": "u"}, {"b": "\xc1", "g": "A"},
                        {"b": "\xc9", "g": "E"}, {"b": "\xcd", "g": "I"}, {"b": "\xd3", "g": "O"},
                        {"b": "\xda", "g": "U"}]

        try:
            for item in special_list:
                result = ugly_cad.replace(item['b'], item['g'])
                ugly_cad = result

            return ugly_cad

        except Exception as e:
            print("clean_string Exception:", e)
            return None

    @staticmethod
    def check_repeat(value=None, list_values=None):
        if value is None:
            return False

        if list_values is None:
            return False

        if value in list_values:
            return True
        else:
            return False

    @staticmethod
    def validator_jsonschema(jsonschema=None, data=None, identifier=None):
        if jsonschema is None:
            return None

        if data is None:
            return None

        validator = Draft7Validator(jsonschema, format_checker=draft7_format_checker)
        errors = sorted(validator.iter_errors(data), key=str)

        temporal_error = []
        for error in errors:
            obj_error = {
                "absolute_path": list(error.absolute_path),
                "message": error.message,
                "validator": error.validator
            }

            if 'description' in error.schema:
                obj_error['description'] = error.schema['description']

            if identifier is not None:
                obj_error['identifier'] = identifier

            temporal_error.append(obj_error)
        return temporal_error

    @staticmethod
    def validate_coordinates(cx=None, cy=None):
        if cx is None or cy is None:
            return False, False

        try:
            cx = float(cx)
        except Exception as e:
            print("validate_coords longitude Exception:", e)
            return False, e

        try:
            cy = float(cy)
        except Exception as e:
            print("validate_coords latitude Exception:", e)
            return False, e

        if -90.0 <= cy <= 90.0:
            validate_cy = True
        else:
            validate_cy = False

        if -180.0 <= cx <= 180.0:
            validate_cx = True
        else:
            validate_cx = False

        return validate_cx, validate_cy

    @staticmethod
    def isValidTime(data):
        try:
            time.strptime(data, "%H:%M:%S")
            return True
        except ValueError:
            return False

    @staticmethod
    def name_week_day(data):
        try:
            nombres_dias_semana = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
            fecha = datetime.strptime('2020-01-28', "%Y-%m-%d")
            return "{}.".format(nombres_dias_semana[fecha.weekday()])
        except ValueError:
            return False

    def is_int(value) -> bool:
        if isinstance(value, str):
            try:
                isnumeric = value.isnumeric()
                if isnumeric:
                    return int(value) >= 0
                return False
            except:
                return False
        if isinstance(value, (int, float)):
            return int(value) == value

    @staticmethod
    def is_float(_value: Any) -> bool:
        if isinstance(_value, str):
            try:
                float(_value)
                return True
            except Exception as ex:
                return False
        if isinstance(_value, (int, float)):
            return float(_value) == _value

    @staticmethod
    def is_bool(value) -> bool:
        return str(value).lower() in ["true", "false"]

    @staticmethod
    def get_bool(value) -> bool:
        return True if str(value).lower() == "true" else False

    @staticmethod
    def is_iterable(value):
        if value is None:
            return None

        return isinstance(value, (tuple, list))

    @staticmethod
    def chunks(_list: List, n: int):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(_list), n):
            yield _list[i:i + n]

    @classmethod
    def remove_accents(self, unicode_str):
        if unicode_str is None:
            return None

        try:
            return ''.join((char_at for char_at in unicodedata.normalize('NFD', unicode_str) if unicodedata.category(char_at) != 'Mn'))
        except Exception as e:
            print("remove_accents Exception:", e)
            return None
    @classmethod
    def list_of_days(cls, data=None, option="list"):
        lis_ = ""
        cont = 1
        name = ""
        M = ""
        TU = ""
        W  = ""
        TH = ""
        F = ""
        SA = ""
        SU = ""
        H = ""
        nivel_pro = []
        start = ""
        ends = ""
        if option == "letters": # Organiza la letas
            array_days = data.split("|")

            for item in array_days:
                pail_ = ""

                if str(item) == "M":
                    # if cont > 1:
                    #     pail_ = "|"
                    M = str(pail_)+"M"
                elif str(item) == "TU":
                    if len(array_days) > 1 and  "M" in array_days:
                        pail_ = "|"
                    TU = str(pail_)+"TU"
                elif str(item) == "W":
                    if len(array_days) > 1 and  "M" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TU" in array_days:
                        pail_ = "|"
                    W = str(pail_)+"W"
                elif str(item) == "TH":
                    if len(array_days) > 1 and  "M" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TU" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "W" in array_days:
                        pail_ = "|"
                    TH =  str(pail_)+"TH"
                elif str(item) == "F":
                    if len(array_days) > 1 and  "M" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TU" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "W" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TH" in array_days:
                        pail_ = "|"
                    F =  str(pail_)+"F"
                elif str(item) == "SA":
                    if len(array_days) > 1 and  "M" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TU" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "W" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TH" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "F" in array_days:
                        pail_ = "|"
                    SA =  str(pail_)+"SA"
                elif str(item) == "SU":
                    if len(array_days) > 1 and  "M" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TU" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "W" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TH" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "F" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "SA" in array_days:
                        pail_ = "|"
                    SU =  str(pail_)+"SU"
                elif str(item) == "H":
                    if len(array_days) > 1 and  "M" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TU" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "W" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "TH" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "F" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "SA" in array_days:
                        pail_ = "|"
                    elif len(array_days) > 1 and  "SU" in array_days:
                        pail_ = "|"
                    H =  str(pail_)+"H"

                days = "{0}{1}{2}{3}{4}{5}{6}{7}".format(M, TU, W, TH, F, SA, SU, H)
                cont = cont + 1

            val_day = {
                    "M": 1,
                    "TU": 2,
                    "W": 3,
                    "TH": 4,
                    "F": 5,
                    "SA": 6,
                    "SU": 7,
                    "H": 8,
                }

            array_days = days.split("|")
            print(array_days)
            if len(array_days) > 0 and len(array_days) <= 2:
                days = "{0} y {1}".format(array_days[0], array_days[1])
            elif len(array_days) > 0 and len(array_days) > 2:
                cont = 0
                list_seg = []
                list_sep = []
                div_ = ""
                end_ = ""
                for item in array_days:
                    #print(item)
                    #print(val_day[item])
                    cd = val_day[item]
                    #print(cont)
                    if cont < len(array_days)-1:
                        d = array_days[cont+1]
                        next_ = val_day[d]
                        if str(cd+1) == str(next_):
                            if array_days[cont] in  list_seg:
                                pass
                            else:
                                list_seg.append(array_days[cont])

                            if array_days[cont+1] in  list_seg:
                                pass
                            else:
                                list_seg.append(array_days[cont+1])

                        else:
                            if array_days[cont] in  list_sep:
                                print("else 1",array_days[cont])
                                pass
                            else:
                                if array_days[cont] in  list_seg:
                                    print("else 2",array_days[cont])
                                    div_ = array_days[cont]
                                    pass
                                else:
                                    list_sep.append(array_days[cont])
                    else:

                        if array_days[cont] in  list_sep:
                            print("else 3",array_days[cont])
                            pass
                        else:
                            if array_days[cont] in  list_seg:
                                print("else 4",array_days[cont])
                                end_ = array_days[cont]
                                pass
                            else:
                                list_sep.append(array_days[cont])


                    cont = cont + 1

                print("SEGUIDO ***", list_seg)
                print("ESPACIO ***", list_sep)
                # Aqui me quede
                # days = ""
                # if len(list_seg) > 0:
                #     if end_ and  div_:
                #         days = list_seg[0]+" a "+ (end_)+" y "



            lis_ = days

        elif option == "list": # Lista los días de la semana , con el letra y el nombre
            lis_ = [{
                "code": "M",
                "name": "Lunes"
            },{
                "code": "TU",
                "name": "Martes"
            },{
                "code": "W",
                "name": "Miércoles"
            },{
                "code": "TH",
                "name": "Jueves"
            },{
                "code": "F",
                "name": "Viernes"
            },{
                "code": "SA",
                "name": "Sábado"
            },{
                "code": "SU",
                "name": "Domingos"
            },{
                "code": "H",
                "name": "Festivoss"
            }]

        elif option == "struct": # agrupa un array por días
            for json_list in data:
                lis_ = []
                array_days = json_list['date_prog'].split("|")
                for item in array_days:
                    if str(item) == "M":
                        M = "M"
                        name = "Lunes"
                    elif str(item) == "TU":
                        TU = "TU"
                        name = "Martes"
                    elif str(item) == "W":
                        W = "W"
                        name = "Miercoles"
                    elif str(item) == "TH":
                        TH = "TH"
                        name = "Jueves"
                    elif str(item) == "F":
                        F = "F"
                        name = "Viernes"
                    elif str(item) == "SA":
                        SA = "SA"
                        name = "Sabado"
                    elif str(item) == "SU":
                        SU = "SU"
                        name = "Domingos"
                    elif str(item) == "H":
                        H = "H"
                        name = "Festivos"

                    lis_.append({
                        "name": name,
                        "init_hour": json_list['init_hour'],
                        "end_hour": json_list['end_hour'],
                    })

        elif  option == "rank": # oganiziza los día spor rango de días
            lis_ = []
            for json_list in data:
                if json_list['date_prog']:
                    array_days = json_list['date_prog'].split("|")
                    days = "0"
                    cont = 1
                    days_ = []
                    split_ = []
                    days = ""
                    M = ""
                    TU = ""
                    W  = ""
                    TH = ""
                    F = ""
                    SA = ""
                    SU = ""
                    H = ""

                    for item in array_days:
                        pail_ = ""
                        if str(item) == "M":
                            M = str(pail_)+"Lunes"
                        elif str(item) == "TU":
                            if len(array_days) > 1 and  "M" in array_days:
                                pail_ ="| a "

                            TU = str(pail_)+"Martes"
                        elif str(item) == "W":
                            if len(array_days) > 1 and  "M" in array_days and  "TU" in array_days:
                                pail_ ="| a "
                            elif len(array_days) > 1 and  "M" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TU" in array_days:
                                pail_ ="| y "

                            W = str(pail_)+"Miercoles"
                        elif str(item) == "TH":
                            if len(array_days) > 1 and  "M" in array_days and  "TU" in array_days and  "W" in array_days:
                                pail_ ="| a "
                            elif len(array_days) > 1 and  "M" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TU" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "W" in array_days:
                                pail_ ="| y "

                            TH =  str(pail_)+"Jueves"
                        elif str(item) == "F":

                            if len(array_days) > 1 and  "M" in array_days and  "TU" in array_days and  "W" in array_days and  "TH" in array_days:
                                    pail_ ="| a "
                            elif len(array_days) > 1 and  "M" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TU" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "W" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TH" in array_days:
                                pail_ ="| y "

                            F =  str(pail_)+"Viernes"
                        elif str(item) == "SA":
                            if len(array_days) > 1 and  "M" in array_days and  "TU" in array_days and  "W" in array_days and  "TH" in array_days and  "F" in array_days :
                                pail_ ="| a "
                            elif len(array_days) > 1 and  "M" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TU" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "W" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TH" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "F" in array_days:
                                pail_ ="| y "

                            SA =  str(pail_)+"Sábado"
                        elif str(item) == "SU":

                            if len(array_days) > 1 and  "M" in array_days and  "TU" in array_days and  "W" in array_days and  "TH" in array_days and  "F" in array_days and  "SA" in array_days:
                                pail_ ="| a "
                            elif len(array_days) > 1 and  "M" in array_days:
                                    pail_ ="| y "
                            elif len(array_days) > 1 and  "TU" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "W" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TH" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "F" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "SA" in array_days:
                                pail_ ="| y "

                            SU =  str(pail_)+"Domingo"
                        elif str(item) == "H":

                            if len(array_days) > 1 and  "M" in array_days and  "TU" in array_days and  "W" in array_days and  "TH" in array_days and  "F" in array_days and  "SA" in array_days and  "SU" in array_days:
                                pail_ ="| a"
                            if len(array_days) > 1 and  "M" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TU" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "W" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "TH" in array_days:
                                pail_ = "| y "
                            elif len(array_days) > 1 and  "F" in array_days:
                                pail_ ="| y "
                            elif len(array_days) > 1 and  "SA" in array_days:
                                pail_ = "|"
                            elif len(array_days) > 1 and  "SU" in array_days:
                                pail_ = "| y "

                            H =  str(pail_)+"Festivos"


                        cont = cont + 1
                    days = "{0}{1}{2}{3}{4}{5}{6}{7}".format(M, TU, W, TH, F, SA, SU, H)

                    days_ = days.split("|")
                    split_ = len(days_)

                    if split_ == 1:
                        days_ = "{0}".format(days_[0])

                    if split_ >=2:
                        if days_[split_-1] == " y Festivos" and len(array_days) == 2:
                            days_ = "{0}{1}".format(days_[0], days_[split_-1])
                        elif days_[split_-1] == " y Festivos":
                            days_ = "{0}{1}{2}".format(days_[0], days_[split_-2],  days_[split_-1])
                        else:

                            days_ = "{0}{1}".format(days_[0],  days_[split_-1])
                    ## ************
                    # val_day = {
                    #     "Lunes": 1,
                    #     "Martes": 2,
                    #     "Miercoles": 3,
                    #     "Jueves": 4,
                    #     "Viernes": 5,
                    #     "Sábado": 6,
                    #     "Domingo": 7,
                    #     "Festivo": 8,
                    # }

                    # array_days = days.split("|")
                    # print(array_days)
                    # if len(array_days) > 0 and len(array_days) == 2:
                    #     days = "{0} y {1}".format(array_days[0], array_days[1])
                    # elif len(array_days) > 0 and len(array_days) == 2:
                    #     days = "{0}".format(array_days[0])
                    # elif len(array_days) > 0 and len(array_days) > 2:
                    #     cont = 0
                    #     list_seg = []
                    #     list_sep = []
                    #     for item in array_days:
                    #         #print(item)
                    #         #print(val_day[item])
                    #         cd = val_day[item]
                    #         #print(cont)
                    #         if cont < len(array_days)-1:
                    #             d = array_days[cont+1]
                    #             next_ = val_day[d]
                    #             if str(cd+1) == str(next_):
                    #                 if array_days[cont] in  list_seg:
                    #                     pass
                    #                 else:
                    #                     list_seg.append(array_days[cont])

                    #                 if array_days[cont+1] in  list_seg:
                    #                     pass
                    #                 else:
                    #                     list_seg.append(array_days[cont+1])

                    #             else:
                    #                 if array_days[cont] in  list_sep:
                    #                     pass
                    #                 else:
                    #                     if array_days[cont] in  list_seg:
                    #                             pass
                    #                     else:
                    #                         list_sep.append(array_days[cont])
                    #         else:

                    #             if array_days[cont] in  list_sep:
                    #                 pass
                    #             else:
                    #                 if array_days[cont] in  list_seg:
                    #                         pass
                    #                 else:
                    #                     list_sep.append(array_days[cont])



                    #         cont = cont + 1
                    #     print("SEGUIDO ***", list_seg)
                    #     print("ESPACIO ***", list_sep)

                    lis_.append({
                        "id": json_list['id'],
                        "name": days_,
                        "init_hour": json_list['init_hour'],
                        "end_hour": json_list['end_hour'],
                    })


            lis_ = lis_

        elif  option == "byDay": # Organiza por día, para mostrar solo una programación
            lis_ = {}
            d = date.today()
            year, week, weekday = d.isocalendar()
            array_day_letter = ['M', 'TU', 'W', 'TH', 'F', 'SA', 'SU', 'H' ]
            array_day = ['Lunes', 'Martes', 'Miécoles', 'Jueves', 'Vienes', 'Sábado', 'Domingo', 'Festivo' ]

            _day = array_day_letter[int(weekday)-1]
            for json_list in data:
                if int(str(json_list['date_prog']).find(str(_day)))>=0:
                    #print(json_list['date_prog'], json_list['init_hour'], json_list['end_hour'])
                    now = datetime.now()+ timedelta(hours=-5)
                    if str(datetime.time(now)) >= json_list['end_hour']:
                        close = 'Cerrada'
                        status = 0
                    else:
                        close = 'Abierta'
                        status = 1
                    lis_ = {
                        "id": json_list['id'],
                        "name": str(array_day[int(weekday)-1]),
                        "init_hour": json_list['init_hour'],
                        "end_hour": json_list['end_hour'],
                        "status": status,
                        "status_name": close
                    }

            if lis_ == {}:
                lis_ = {
                    "name": str(array_day[int(weekday) - 1]),
                    "status": 0,
                    "status_name": 'Cerrada'
                }

        return lis_
