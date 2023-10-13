#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from app.ext.generic_model import GenericModel


class DbTransaction:
    """
    Class To Handle Database Transaction Using SQLAlchemy
    """

    def __init__(self, database_engine):
        self.database_engine = database_engine
        self.session = None
        # begin create session
        self.__create_session()

    def __create_session(self):
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

    def add(self, model: GenericModel):
        """
        Add an Item
        :param model:
        :return:
        """
        self.session.add(model)

    def update(self, model: GenericModel):
        """
        Update an Item
        :param model:
        :return:
        """
        self.session.add(model)

    def delete(self, model: GenericModel):
        """
        Delete an Item
        :param model: Item to delete
        :return: None
        """
        self.session.delete(model)

    def commit(self):
        """
        Apply Changes to Database
        :return: None
        :raises Exception: if commit fail.
        """
        try:
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex
        finally:
            self.session.close()

"""
transaction = DbTransaction(db.engine)
try:
    transaction.add(MyModel)
    transaction.commit()
except Exception as ex:
    print(ex)
"""
