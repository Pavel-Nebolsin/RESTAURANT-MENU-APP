from sqlalchemy import Column, String, Float, ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
import uuid

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(UUID, ForeignKey('menu.id'))
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(precision=10, scale=2))
    submenu_id = Column(UUID, ForeignKey('submenu.id'))
    submenu = relationship('SubMenu', back_populates='dishes')
