import datetime
import logging
from ckan.model.domain_object import DomainObject
from ckan.model import meta
from ckan import model
from sqlalchemy import Column, UniqueConstraint, ForeignKeyConstraint, ForeignKey, Table, types, DateTime
from sqlalchemy import desc

log = logging.getLogger(__name__)

security_member_table = None


def setup():
    if security_member_table is None:
        define_security_member_table()
        log.debug('Security_member table defined in memory')

    if model.member_table.exists():
        if not security_member_table.exists():
            security_member_table.create()
            log.debug('Security_member table create')
        else:
            log.debug('Security_member table already exists')
    else:
        log.debug('Security_member table creation deferred')


class SecurityMemberModel(object):
    @classmethod
    def filter(cls, session, **kwargs):
        return session.query(cls).filter_by(**kwargs)

    @classmethod
    def exists(cls, session, member_dict, dataset_type):
        if cls.filter(session, 
                      user_id=member_dict['table_id'], 
                      group_id=member_dict['group_id'], 
                      dataset_type=dataset_type).first():
            return True
        else:
            return False

    @classmethod
    def get(cls, session, **kwargs):
        instance = cls.filter(session, **kwargs).first()
        return instance

    @classmethod
    def create(cls, session, member_dict, dataset_type, classification):
        instance = cls()
        instance.member_id = member_dict['id'],
        instance.user_id = member_dict['table_id'],
        instance.group_id = member_dict['group_id'],
        instance.state = member_dict['state']
        instance.classification = classification
        instance.dataset_type = dataset_type

        session.add(instance)
        session.commit()
        return instance.as_dict()

    @classmethod
    def as_dict(self):
        return self.__dict__


class SecurityMember(SecurityMemberModel):
    @classmethod
    def get_all(cls, session, **kwargs):
        instances = cls.filter(session, **kwargs).all()
        return instances

    @classmethod
    def is_classification_for_member(cls, session, member_dict, classification, dataset_type):
        if cls.get(session, 
                   member_dict, 
                   classification=classification, 
                   dataset_type=dataset_type):
            return True
        else:
            return False


def define_security_member_table():
    global security_member_table

    security_member_table = Table(
        'security_member',
        meta.metadata,
        Column(
               'id',
               types.Integer,
               primary_key=True,
               autoincrement=True), 
        Column(
               'member_id',
               types.UnicodeText,
               primary_key=True, 
               nullable=False),
        Column('user_id',
               types.UnicodeText,
               nullable=False),
        Column('group_id',
               types.UnicodeText,
               nullable=False),
        Column('state',
               types.UnicodeText,
               nullable=False),
        Column('dataset_type',
               types.UnicodeText,
               nullable=False),
        Column('classification',
               types.UnicodeText,
               nullable=False),
        ForeignKeyConstraint(
                ['member_id'],
                ['member.id'],
                onupdate="CASCADE", ondelete="CASCADE"
        ),
        UniqueConstraint('member_id', 
                         'user_id', 
                         'group_id',
                         'dataset_type',
                         name='uix_1')
    )

    meta.mapper(SecurityMember, security_member_table)


def get_member_classification(session, member_id, dataset_type, classification="1"):
    return session.query(SecurityMemberModel).filter(
                    and_(SecurityMemberModel.member_id == member_id, 
                         SecurityMemberModel.classification == classification)).first()


def add_member_classification(session, member_dict, dataset_type, classification="1"):
    model = SecurityMemberModel()
    
    model.member_id = member_dict['id']
    model.user_id = member_dict['table_id']
    model.group_id = member_dict['group_id']
    model.state = member_dict['state']
    model.classification = classification
    model.dataset_type = dataset_type

    session.add(model)
    session.commit()  