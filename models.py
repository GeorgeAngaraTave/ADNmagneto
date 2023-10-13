# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Table, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    schedule_activity_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150, 'utf8_bin'))
    active_form = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    serviforms_form_id = db.Column(db.String(40, 'utf8_bin'))
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Activity.company_id == Company.id', backref='activities')



class Break(db.Model):
    __tablename__ = 'breaks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150))
    init_hour = db.Column(db.Time, nullable=False)
    end_hour = db.Column(db.Time, nullable=False)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Break.company_id == Company.id', backref='breaks')



class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    json_base = db.Column(db.JSON)
    typology_id = db.Column(db.ForeignKey('typology.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    typology = db.relationship('Typology', primaryjoin='Category.typology_id == Typology.id', backref='categories')



class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    address = db.Column(db.String(100, 'utf8_bin'))
    phone = db.Column(db.String(20, 'utf8_bin'))
    nit = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    date_init = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    contac_persons = db.Column(db.String(50, 'utf8_bin'))
    city = db.Column(db.String(50, 'utf8_bin'))
    country = db.Column(db.String(50, 'utf8_bin'))
    description = db.Column(db.String(150, 'utf8_bin'))
    realtionship = db.Column(db.Integer)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)



class ConfigCompany(db.Model):
    __tablename__ = 'config_company'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    type_config_id = db.Column(db.ForeignKey('type_config.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    config_json = db.Column(db.JSON, nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='ConfigCompany.company_id == Company.id', backref='config_companies')
    type_config = db.relationship('TypeConfig', primaryjoin='ConfigCompany.type_config_id == TypeConfig.id', backref='config_companies')



class Depot(db.Model):
    __tablename__ = 'depot'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(200))
    city = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    cx = db.Column(db.Float(asdecimal=True), nullable=False)
    cy = db.Column(db.Float(asdecimal=True), nullable=False)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Depot.company_id == Company.id', backref='depots')



class DivipolaCity(db.Model):
    __tablename__ = 'divipola_city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code_geo = db.Column(db.String(5), nullable=False)
    world_code = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.ForeignKey('divipola_department.id'), nullable=False, index=True)

    department = db.relationship('DivipolaDepartment', primaryjoin='DivipolaCity.department_id == DivipolaDepartment.id', backref='divipola_cities')



class DivipolaCountry(db.Model):
    __tablename__ = 'divipola_country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(5), nullable=False)
    centroid = db.Column(db.String(100), nullable=False)
    code_country = db.Column(db.String(20), nullable=False)



class DivipolaDepartment(db.Model):
    __tablename__ = 'divipola_department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    country_id = db.Column(db.ForeignKey('divipola_country.id'), nullable=False, index=True)

    country = db.relationship('DivipolaCountry', primaryjoin='DivipolaDepartment.country_id == DivipolaCountry.id', backref='divipola_departments')



class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    description = db.Column(db.String(150, 'utf8_bin'))
    city = db.Column(db.String(50, 'utf8_bin'))
    country = db.Column(db.String(50, 'utf8_bin'))
    cx = db.Column(db.Float, nullable=False)
    cy = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    dirtrad = db.Column(db.String(250, 'utf8_bin'))
    hour_init = db.Column(db.Time, nullable=False)
    hour_end = db.Column(db.Time)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    serviforms_group_id = db.Column(db.String(40, 'utf8_bin'))
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Group.company_id == Company.id', backref='groups')



class Layer(db.Model):
    __tablename__ = 'layer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status_id = db.Column(db.ForeignKey('status.id'), nullable=False, index=True)
    company_id = db.Column(db.ForeignKey('company.id'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Layer.company_id == Company.id', backref='layers')
    status = db.relationship('Status', primaryjoin='Layer.status_id == Status.id', backref='layers')



class Login(db.Model):
    __tablename__ = 'login'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.ForeignKey('resource.id'), nullable=False, index=True)
    email = db.Column(db.String(100, 'utf8_bin'), nullable=False)
    token = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    refresh_token = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    expires_token = db.Column(db.DateTime, nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    resource = db.relationship('Resource', primaryjoin='Login.resource_id == Resource.id', backref='logins')



class ManualDatum(db.Model):
    __tablename__ = 'manual_data'

    id = db.Column(db.Integer, primary_key=True)
    register = db.Column(db.JSON, nullable=False)
    validator = db.Column(db.JSON, nullable=False)
    upload_file_id = db.Column(db.ForeignKey('upload_file.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='ManualDatum.company_id == Company.id', backref='manual_data')
    upload_file = db.relationship('UploadFile', primaryjoin='ManualDatum.upload_file_id == UploadFile.id', backref='manual_data')



class ManualTappingVp(db.Model):
    __tablename__ = 'manual_tapping_vp'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    identification = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    address = db.Column(db.String(150, 'utf8_bin'))
    city = db.Column(db.String(150, 'utf8_bin'))
    country = db.Column(db.String(150, 'utf8_bin'))
    phone = db.Column(db.String(150, 'utf8_bin'))
    cx = db.Column(db.Float(asdecimal=True))
    cy = db.Column(db.Float(asdecimal=True))
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    status_id = db.Column(db.ForeignKey('status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='ManualTappingVp.company_id == Company.id', backref='manual_tapping_vps')
    status = db.relationship('Status', primaryjoin='ManualTappingVp.status_id == Status.id', backref='manual_tapping_vps')



class MasterVisitPoint(db.Model):
    __tablename__ = 'master_visit_point'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    identification = db.Column(db.String(30, 'utf8_bin'), nullable=False, unique=True)
    address = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    city = db.Column(db.String(150, 'utf8_bin'))
    country = db.Column(db.String(150, 'utf8_bin'))
    phone = db.Column(db.String(150, 'utf8_bin'))
    cx = db.Column(db.Float(asdecimal=True), nullable=False)
    cy = db.Column(db.Float(asdecimal=True), nullable=False)
    geo_hash = db.Column(db.String(45, 'utf8_bin'), nullable=False)
    unique_key = db.Column(db.String(100, 'utf8_bin'), nullable=False, unique=True)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    company_name = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    origin = db.Column(db.String(100, 'utf8_bin'), nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='MasterVisitPoint.company_id == Company.id', backref='master_visit_points')



class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8_bin'), nullable=False, index=True)
    description = db.Column(db.String(100, 'utf8_bin'))
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)



class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    lastname = db.Column(db.String(50, 'utf8_bin'))
    username = db.Column(db.String(50, 'utf8_bin'))
    email = db.Column(db.String(100, 'utf8_bin'), nullable=False, unique=True)
    identification = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    city = db.Column(db.String(150, 'utf8_bin'))
    address = db.Column(db.String(150, 'utf8_bin'))
    cx = db.Column(db.Float(asdecimal=True))
    cy = db.Column(db.Float(asdecimal=True))
    init_hour_window = db.Column(db.Time)
    end_hour_window = db.Column(db.Time)
    max_travel_distance = db.Column(db.Integer)
    max_travel_duration = db.Column(db.Time)
    first_capacity_name = db.Column(db.String(50, 'utf8_bin'))
    first_capacity = db.Column(db.Float(asdecimal=True))
    second_capacity_name = db.Column(db.String(50, 'utf8_bin'))
    second_capacity = db.Column(db.Float(asdecimal=True))
    third_capacity_name = db.Column(db.String(50, 'utf8_bin'))
    third_capacity = db.Column(db.Float(asdecimal=True))
    uid = db.Column(db.String(50, 'utf8_bin'))
    additional_info = db.Column(db.JSON)
    json_properties = db.Column(db.JSON)
    password = db.Column(db.String(160, 'utf8_bin'))
    code_recover_pass = db.Column(db.String(10, 'utf8_bin'))
    code_recover_date = db.Column(db.DateTime)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    role_id = db.Column(db.ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    typology_id = db.Column(db.ForeignKey('typology.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    status_id = db.Column(db.ForeignKey('status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Resource.company_id == Company.id', backref='resources')
    role = db.relationship('Role', primaryjoin='Resource.role_id == Role.id', backref='resources')
    status = db.relationship('Status', primaryjoin='Resource.status_id == Status.id', backref='resources')
    typology = db.relationship('Typology', primaryjoin='Resource.typology_id == Typology.id', backref='resources')


class ControlLogInOut(Resource):
    __tablename__ = 'control_log_in_out'

    resource_id = db.Column(db.ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    date_login = db.Column(db.DateTime)
    date_logout = db.Column(db.DateTime)
    total_session_time = db.Column(db.String(10))
    oauth_client_name = db.Column(db.String(45), nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)



class ResourceBreak(db.Model):
    __tablename__ = 'resource_breaks'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    breaks_id = db.Column(db.ForeignKey('breaks.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    breaks = db.relationship('Break', primaryjoin='ResourceBreak.breaks_id == Break.id', backref='resource_breaks')
    resource = db.relationship('Resource', primaryjoin='ResourceBreak.resource_id == Resource.id', backref='resource_breaks')



class ResourceDepot(db.Model):
    __tablename__ = 'resource_depot'

    id = db.Column(db.Integer, primary_key=True)
    point = db.Column(db.Integer, nullable=False)
    resource_id = db.Column(db.ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    depot_id = db.Column(db.ForeignKey('depot.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    depot = db.relationship('Depot', primaryjoin='ResourceDepot.depot_id == Depot.id', backref='resource_depots')
    resource = db.relationship('Resource', primaryjoin='ResourceDepot.resource_id == Resource.id', backref='resource_depots')



class ResourceGroupActivity(db.Model):
    __tablename__ = 'resource_group_activity'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    activity_id = db.Column(db.ForeignKey('activity.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    group_id = db.Column(db.ForeignKey('group.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    activity = db.relationship('Activity', primaryjoin='ResourceGroupActivity.activity_id == Activity.id', backref='resource_group_activities')
    group = db.relationship('Group', primaryjoin='ResourceGroupActivity.group_id == Group.id', backref='resource_group_activities')
    resource = db.relationship('Resource', primaryjoin='ResourceGroupActivity.resource_id == Resource.id', backref='resource_group_activities')



class ResourceSkill(db.Model):
    __tablename__ = 'resource_skill'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    skill_id = db.Column(db.ForeignKey('skills.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    resource = db.relationship('Resource', primaryjoin='ResourceSkill.resource_id == Resource.id', backref='resource_skills')
    skill = db.relationship('Skill', primaryjoin='ResourceSkill.skill_id == Skill.id', backref='resource_skills')



class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100, 'utf8_bin'), nullable=False, index=True)
    description = db.Column(db.String(150, 'utf8_bin'))
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)



class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    permission_id = db.Column(db.ForeignKey('permission.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    permission = db.relationship('Permission', primaryjoin='RolePermission.permission_id == Permission.id', backref='role_permissions')
    role = db.relationship('Role', primaryjoin='RolePermission.role_id == Role.id', backref='role_permissions')



class Route(db.Model):
    __tablename__ = 'route'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Route.company_id == Company.id', backref='routes')



class RouteVisitPoint(db.Model):
    __tablename__ = 'route_visit_point'

    id = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.Integer)
    route_date = db.Column(db.DateTime)
    route_id = db.Column(db.ForeignKey('route.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    visit_point_id = db.Column(db.ForeignKey('visit_point.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    route = db.relationship('Route', primaryjoin='RouteVisitPoint.route_id == Route.id', backref='route_visit_points')
    visit_point = db.relationship('VisitPoint', primaryjoin='RouteVisitPoint.visit_point_id == VisitPoint.id', backref='route_visit_points')



class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    visit_point_id = db.Column(db.Integer, nullable=False)
    has_repetition = db.Column(db.Integer, nullable=False)
    init_cx = db.Column(db.Float(asdecimal=True), server_default=db.FetchedValue())
    init_cy = db.Column(db.Float(asdecimal=True), server_default=db.FetchedValue())
    init_address = db.Column(db.String(150))
    init_city = db.Column(db.String(150))
    end_cx = db.Column(db.Float(asdecimal=True), server_default=db.FetchedValue())
    end_cy = db.Column(db.Float(asdecimal=True), server_default=db.FetchedValue())
    end_address = db.Column(db.String(150))
    end_city = db.Column(db.String(150))
    additional_info = db.Column(db.JSON)
    company_id = db.Column(db.Integer, nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)



class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.Float(asdecimal=True), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(150))
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='Skill.company_id == Company.id', backref='skills')



class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50, 'utf8_bin'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)



class StatusMobile(db.Model):
    __tablename__ = 'status_mobile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8_bin'), nullable=False)
    description = db.Column(db.String(150, 'utf8_bin'))
    active_form = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status_id = db.Column(db.ForeignKey('status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='StatusMobile.company_id == Company.id', backref='status_mobiles')
    status = db.relationship('Status', primaryjoin='StatusMobile.status_id == Status.id', backref='status_mobiles')



class TypeConfig(db.Model):
    __tablename__ = 'type_config'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    status_id = db.Column(db.ForeignKey('status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    json_base = db.Column(db.JSON, nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    status = db.relationship('Status', primaryjoin='TypeConfig.status_id == Status.id', backref='type_configs')



class Typology(db.Model):
    __tablename__ = 'typology'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(150, 'utf8_bin'), nullable=False, index=True)
    description = db.Column(db.String(150, 'utf8_bin'))
    company_id = db.Column(db.Integer, nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)



class UploadFile(db.Model):
    __tablename__ = 'upload_file'

    id = db.Column(db.Integer, primary_key=True)
    typology_id = db.Column(db.ForeignKey('typology.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    bucket_path = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    original_name = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    equivalent_fields = db.Column(db.JSON)
    process_state = db.Column(db.String(50, 'utf8_bin'))
    resource_id = db.Column(db.ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    is_public = db.Column(db.Integer, server_default=db.FetchedValue())
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    resource = db.relationship('Resource', primaryjoin='UploadFile.resource_id == Resource.id', backref='upload_files')
    typology = db.relationship('Typology', primaryjoin='UploadFile.typology_id == Typology.id', backref='upload_files')



t_view_category_typology = db.Table(
    'view_category_typology',
    db.Column('category_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('category_name', db.String(50)),
    db.Column('json_base', db.JSON),
    db.Column('typology_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('typology_name', db.String(150)),
    db.Column('company_id', db.Integer)
)



t_view_config_company = db.Table(
    'view_config_company',
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('config_company_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('company_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('company_name', db.String(150)),
    db.Column('config_json', db.JSON),
    db.Column('type_config_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('type_config_name', db.String(150)),
    db.Column('json_base', db.JSON)
)



t_view_divipola = db.Table(
    'view_divipola',
    db.Column('city_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('city_name', db.String(150)),
    db.Column('code_geo', db.String(5)),
    db.Column('world_code', db.String(50)),
    db.Column('department_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('department_name', db.String(150)),
    db.Column('country_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('country_name', db.String(100)),
    db.Column('country_code', db.String(5)),
    db.Column('centroid', db.String(100)),
    db.Column('country_code_country', db.String(20))
)



t_view_resource = db.Table(
    'view_resource',
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('name', db.String(50)),
    db.Column('lastname', db.String(50)),
    db.Column('username', db.String(50)),
    db.Column('email', db.String(100)),
    db.Column('identification', db.String(150)),
    db.Column('code_recover_pass', db.String(10)),
    db.Column('code_recover_date', db.DateTime),
    db.Column('additional_info', db.JSON),
    db.Column('company_id', db.Integer),
    db.Column('company_name', db.String(150)),
    db.Column('role_id', db.Integer),
    db.Column('role_name', db.String(100)),
    db.Column('typology_id', db.Integer),
    db.Column('typology_name', db.String(150)),
    db.Column('status_id', db.Integer),
    db.Column('status', db.String(50)),
    db.Column('uid', db.String(50)),
    db.Column('added_on', db.DateTime, server_default=db.FetchedValue()),
    db.Column('update_on', db.DateTime)
)



t_view_resource_group_activity = db.Table(
    'view_resource_group_activity',
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('resource_id', db.Integer),
    db.Column('resource_name', db.String(50)),
    db.Column('company_id', db.Integer),
    db.Column('activity_id', db.Integer),
    db.Column('schedule_activity_id', db.Integer),
    db.Column('group_id', db.Integer),
    db.Column('group_name', db.String(50))
)



t_view_role_permission = db.Table(
    'view_role_permission',
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('role_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('role_name', db.String(100)),
    db.Column('permission_id', db.Integer),
    db.Column('permission_name', db.String(50))
)



t_view_upload_file = db.Table(
    'view_upload_file',
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('bucket_path', db.String(200)),
    db.Column('original_name', db.String(200)),
    db.Column('equivalent_fields', db.JSON),
    db.Column('process_state', db.String(50)),
    db.Column('is_public', db.Integer, server_default=db.FetchedValue()),
    db.Column('added_on', db.DateTime, server_default=db.FetchedValue()),
    db.Column('update_on', db.DateTime),
    db.Column('typology_id', db.Integer),
    db.Column('typology_name', db.String(150)),
    db.Column('category_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('category_name', db.String(50)),
    db.Column('category_json_base', db.JSON),
    db.Column('resource_id', db.Integer),
    db.Column('resource_email', db.String(100)),
    db.Column('company_id', db.Integer),
    db.Column('company_name', db.String(150))
)



t_view_visit_point_resource = db.Table(
    'view_visit_point_resource',
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('sequence', db.Integer),
    db.Column('route_date', db.DateTime),
    db.Column('route_id', db.Integer),
    db.Column('route_name', db.String(50)),
    db.Column('visit_point_id', db.Integer),
    db.Column('visit_point_name', db.String(150)),
    db.Column('visit_point_identification', db.String(200)),
    db.Column('visit_point_address', db.String(150)),
    db.Column('visit_point_cx', db.Float(asdecimal=True)),
    db.Column('visit_point_cy', db.Float(asdecimal=True)),
    db.Column('company_id', db.Integer),
    db.Column('company_name', db.String(150))
)



class VisitPoint(db.Model):
    __tablename__ = 'visit_point'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(150, 'utf8_bin'), nullable=False)
    identification = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    address = db.Column(db.String(150, 'utf8_bin'))
    city = db.Column(db.String(150, 'utf8_bin'))
    country = db.Column(db.String(150, 'utf8_bin'))
    phone = db.Column(db.String(150, 'utf8_bin'))
    cx = db.Column(db.Float(asdecimal=True), nullable=False)
    cy = db.Column(db.Float(asdecimal=True), nullable=False)
    additional_info = db.Column(db.JSON)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    status_id = db.Column(db.ForeignKey('status.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    typology_id = db.Column(db.ForeignKey('typology.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    company = db.relationship('Company', primaryjoin='VisitPoint.company_id == Company.id', backref='visit_points')
    status = db.relationship('Status', primaryjoin='VisitPoint.status_id == Status.id', backref='visit_points')
    typology = db.relationship('Typology', primaryjoin='VisitPoint.typology_id == Typology.id', backref='visit_points')



class VisitPointResource(db.Model):
    __tablename__ = 'visit_point_resource'

    id = db.Column(db.Integer, primary_key=True)
    visit_point_id = db.Column(db.ForeignKey('visit_point.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    resource_id = db.Column(db.ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_on = db.Column(db.DateTime)

    resource = db.relationship('Resource', primaryjoin='VisitPointResource.resource_id == Resource.id', backref='visit_point_resources')
    visit_point = db.relationship('VisitPoint', primaryjoin='VisitPointResource.visit_point_id == VisitPoint.id', backref='visit_point_resources')
