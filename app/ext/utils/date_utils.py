# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from app.config.local_settings import STDR_UTC_HOUR
from dateutil.relativedelta import relativedelta
import calendar


class DateUtils:

    @staticmethod
    def get_timestamp():
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
        timestamp = now.strftime('%Y%m%d%H%M%S')
        return timestamp

    @staticmethod
    def today(format_date=None, type_format='str'):
        format_date = '%Y-%m-%d' if format_date is None else format_date
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)

        if type_format is 'str':
            current_date = now.strftime(format_date)
            return current_date
        elif type_format is 'date':
            return now
        return None

    @staticmethod
    def str_to_datetime(date_time=None, format_date=None):
        if date_time is None or format_date is None:
            return None

        to_datetime = datetime.strptime(date_time,format_date)
        return to_datetime

    @staticmethod
    def datetime_to_str(date_time=None, format_date=None):
        if date_time is None or format_date is None:
            return None

        to_datetime = datetime.strftime(date_time,format_date)
        return to_datetime

    @staticmethod
    def dif_hms(init_date=None, end_date=None):
        """fechas deben ser en formato datetime %Y-%m-%d %H:%M:%S"""
        if init_date is None or end_date is None:
            return None

        date_diff = end_date - init_date

        days, seconds = date_diff.days, date_diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        total_time = "{0:02d}:{1:02d}:{2:02d}".format(hours,minutes,seconds)
        return total_time

    @staticmethod
    def get_current_time():
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        return current_time

    @staticmethod
    def compare_dates(init_date=None, end_date=None, compare='eq'):
        if init_date is None:
            return None
        if end_date is None:
            return None
        try:
            _init = datetime.strptime(init_date, '%Y-%m-%d')
            _end = datetime.strptime(end_date, '%Y-%m-%d')

            if compare is 'eq':
                if _init == _end:
                    return True
                else:
                    return False
            elif compare is 'gr':
                if _init > _end:
                    return True
                else:
                    return False
            elif compare is 'le':
                if _init < _end:
                    return True
                else:
                    return False
            elif compare is 'gt':
                if _init >= _end:
                    return True
                else:
                    return False
            elif compare is 'lt':
                if _init <= _end:
                    return True
                else:
                    return False
        except Exception as e:
            print("compare_dates Exception: an invalid date has been entered")
            print("compare_dates Exception:", e)
            return None
        return None

    @staticmethod
    def fix_time(_time=None):
        n_time = None

        if _time is None:
            return None

        try:
            _init = datetime.strptime(str(_time), '%H:%M:%S')
            n_time = datetime.strftime(_init, '%H:%M')
            return n_time
        except Exception:
            try:
                _init = datetime.strptime(str(_time), '%H:%M')
                n_time = datetime.strftime(_init, '%H:%M')
                return n_time
            except Exception:
                print("fix_time Exception: can not convert this time format", _time)
                return None
            return None

    @staticmethod
    def compare_times(init_time=None, end_time=None, compare='eq', format_time="%H:%M"):
        if init_time is None:
            return None

        if end_time is None:
            return None

        try:
            _init = datetime.strptime(init_time, format_time)
            _end = datetime.strptime(end_time, format_time)

            if compare is 'eq':
                if _init == _end:
                    return True
                else:
                    return False
            elif compare is 'gr':
                if _init > _end:
                    return True
                else:
                    return False
            elif compare is 'le':
                if _init < _end:
                    return True
                else:
                    return False
            elif compare is 'gt':
                if _init >= _end:
                    return True
                else:
                    return False
            elif compare is 'lt':
                if _init <= _end:
                    return True
                else:
                    return False
        except Exception as e:
            print("compare_times Exception: an invalid time has been entered")
            print("compare_times Exception:", e)
            return None
        return None

    @staticmethod
    def get_current_unix_time():
        try:
            unix_time = int(time.time() - STDR_UTC_HOUR)
            return unix_time
        except Exception as e:
            print("get_current_unix_time Exception:", e)
            return None

    @staticmethod
    def from_unix_time(unix_time):
        try:
            to_date = datetime.fromtimestamp(unix_time)
            formated_date = to_date.strftime('%Y-%m-%d %H:%M:%S')
            return formated_date
        except Exception as e:
            print("from_unix Exception:", e)
            return None

    @staticmethod
    def to_unix_time(init_date, init_hour=None):
        if init_date is None:
            return None

        if init_hour is None:
            init_hour = '00:00:00'

        try:
            y, m, d = init_date.split('-')
            H, M, S = init_hour.split(':')

            to_dt = datetime(int(y), int(m), int(d), int(H), int(M), int(S))
            unix_time = time.mktime(to_dt.timetuple())
            # or
            # unix_time = int(to_dt.strftime("%s"))
            return unix_time
        except Exception as e:
            print("to_unix_time Exception:", e)
            return None

    @staticmethod
    def day_of_week(init_date):
        if init_date is None:
            return None

        y, m, d = init_date.split('-')
        week_day = date(int(y), int(m), int(d)).weekday()
        calendar_day = calendar.day_name[week_day]
        return {'calendar_day': calendar_day, 'week_day': (week_day + 1)}

    @staticmethod
    def to_date(current_date, current_format, new_format=None, type_format='str'):
        if current_date is None:
            return None

        if current_format is None:
            return None

        new_format = '%Y-%m-%d' if new_format is None else new_format

        try:
            _date = datetime.strptime(current_date, current_format)

            if type_format is 'str':
                new_date = _date.strftime(new_format)
                return new_date
            elif type_format is 'date':
                return _date
        except Exception as e:
            print("to_date Exception:", e)
            return None

    @staticmethod
    def add_months(add_months=1, init_date=None):
        added_months = None
        if init_date is None:
            next_month = date.today() + relativedelta(months=+add_months)
            added_months = datetime.strftime(next_month, "%Y-%m-%d")
        else:
            next_month = datetime.strptime(init_date, '%Y-%m-%d') + relativedelta(months=+add_months)
            added_months = datetime.strftime(next_month, "%Y-%m-%d")
        return added_months

    @staticmethod
    def add_days(current_date, num_days=None):

        if current_date is None:
            return None

        if num_days is None:
            return None

        try:
            _init = datetime.strptime(current_date, '%Y-%m-%d')
            resp = _init + timedelta(days=num_days)
            early_date = datetime.strftime(resp, '%Y-%m-%d')

            if early_date is None:
                return None
            return early_date
        except Exception as e:
            print("add_days Exception:", e)
            return None

    @staticmethod
    def add_hours(current_date=None, num_hours=None):

        if current_date is None:
            current_date = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)

        if num_hours is None:
            return None

        try:
            resp = current_date + timedelta(hours=num_hours)

            early_date = datetime.strftime(resp, '%Y%m%d%H%M%S')

            if early_date is None:
                return None
            return early_date
        except Exception as e:
            print("add_hours Exception:", e)
            return None

    @staticmethod
    def add_seconds(current_date=None, format_date=None, num_seconds=None, type_format='str'):
        if num_seconds is None:
            return None

        format_date = '%Y-%m-%d %H:%M:%S' if format_date is None else format_date
        if current_date is None:
            now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
            add_seconds = now + timedelta(seconds=num_seconds)
        else:
            current_date=datetime.strptime(current_date, format_date)
            add_seconds = current_date + timedelta(seconds=num_seconds)

        if type_format is 'str':
            current_date = add_seconds.strftime(format_date)
            return current_date
        elif type_format is 'date':
            return add_seconds
        return None

    @staticmethod
    def add_minutes(current_date=None, format_date=None, num_minutes=None, type_format='str'):
        if num_minutes is None:
            return None

        format_date = '%Y-%m-%d %H:%M:%S' if format_date is None else format_date
        if current_date is None:
            now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
            add_minutes = now + timedelta(minutes=num_minutes)
        else:
            current_date=datetime.strptime(current_date, format_date)
            add_minutes = current_date + timedelta(minutes=num_minutes)

        if type_format is 'str':
            current_date = add_minutes.strftime(format_date)
            return current_date
        elif type_format is 'date':
            return add_minutes
        return None

    @staticmethod
    def get_next_month(init_date=None):

        if init_date is None:
            return None

        try:
            y1, m1, d1 = init_date.split('-')
            _initd = date(int(y1), int(m1), int(d1))

            new_month = _initd + datetime.timedelta(days=calendar.monthrange(_initd.year, _initd.month)[1])
            next_month = datetime.datetime.strftime(new_month, "%Y-%m-%d")

            return next_month
        except Exception as e:
            print("get_next_month Exception:", e)
            return None

    @staticmethod
    def validate_time(time=None):
        """Valida si una hora es valida, retorna True si es correcta"""
        if time is None:
            return None,""

        try:
            datetime.strptime(time, "%H:%M:%S")
            return True,""
        except Exception as e:
            print("validate_time Exception:", e)
            return None,str(e)

    @staticmethod
    def validate_date(date=None):
        """Valida si una fecha es valida, retorna True si es correcta"""
        if date is None:
            return None,""

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True,""
        except Exception as e:
            print("validate_date Exception:", e)
            return None,str(e)

    @staticmethod
    def hms_to_s(time=None):
        """recibe un tiempo en formato %H:%M:%S, retorna el total del tiempo en segundos"""
        if time is None:
            return None

        h, m, s = [int(i) for i in time.split(':')]
        return 3600*h + 60*m + s

    @staticmethod
    def validate_date_time(init_date=None,end_date=None,init_hour=None,end_hour=None):
        """Valida fecha inicio y fin hora inicio y fin que sea mayor a la actual"""
        if init_date is None or end_date is None or init_hour is None or end_hour is None:
            return None

        try:
            error = None

            init_date_validate, error_init_date = DateUtils.validate_date(init_date)
            if init_date_validate is None:
                error = error_init_date

            end_date_validate, error_end_date = DateUtils.validate_date(end_date)
            if end_date_validate is None:
                error = error_end_date

            init_hour_validate, error_init_hour = DateUtils.validate_time(init_hour)
            if init_hour_validate is None:
                error = error_init_hour

            end_hour_validate, error_end_hour = DateUtils.validate_time(end_hour)
            if end_hour_validate is None:
                error = error_end_hour


            compare_times_validate = DateUtils.compare_times(init_hour,end_hour,'gt')
            if compare_times_validate is True or compare_times_validate is None:
                error = 'init_hour greater than end_hour'

            current_day = DateUtils.today('%Y-%m-%d')
            #valida que la fecha inicio sea mayor a fecha fin
            date_validate_gt = DateUtils.compare_dates(end_date,init_date,'gt')
            if not date_validate_gt:
                error = "end_date must be greater than init_date"
            #valida que la fecha inicio sea mayor a la actual
            compare_date_validate_le = DateUtils.compare_dates(current_day,init_date,'le')
            if not compare_date_validate_le:
                #valida que la fecha de inicio sea igual a la de hoy
                compare_date_validate_eq = DateUtils.compare_dates(current_day,init_date,'eq')
                #si no es igual a hoy la fecha ya paso
                if not compare_date_validate_eq:
                    error = 'init_date less than current date'
                else:
                    #si la fecha es igual a hoy
                    current_time = DateUtils.today('%H:%M:%S')
                    compare_compare_times_gt = DateUtils.compare_times(init_hour,current_time,'gt')
                    #validar que la hora de inicio sea mayor a la hora actual
                    if not compare_compare_times_gt:
                        error = 'init_hour less than current time'

            return error
        except Exception as e:
            print("validate_date_time Exception:", e)
            return None

    @staticmethod
    def days_between_dates(init_date, end_date):
        if init_date is None:
            return None

        if end_date is None:
            return None

        try:
            i_y, i_m, i_d = init_date.split('-')
            f_date = date(int(i_y), int(i_m), int(i_d))

            e_y, e_m, e_d = end_date.split('-')
            l_date = date(int(e_y), int(e_m), int(e_d))

            delta = (l_date - f_date)
            print("days_between_dates delta.days:", delta.days)

            return delta.days
        except Exception as e:
            print("days_between_dates Exception:", e)
            return None
