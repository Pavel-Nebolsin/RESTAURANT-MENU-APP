import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__: str = 'menu'

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title: str = Column(String, unique=True, nullable=False)
    description: str = Column(String, nullable=False)
    submenus: list['SubMenu'] = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenu(Base):
    __tablename__: str = 'submenu'

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title: str = Column(String, unique=True, nullable=False)
    description: str = Column(String, nullable=False)
    menu_id: uuid.UUID = Column(UUID, ForeignKey('menu.id'))
    menu: 'Menu' = relationship('Menu', back_populates='submenus')
    dishes: list['Dish'] = relationship('Dish', back_populates='submenu', cascade='all, delete')


class Dish(Base):
    __tablename__: str = 'dish'

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title: str = Column(String, unique=True, nullable=False)
    description: str = Column(String, nullable=False)
    price: float = Column(Numeric(precision=10, scale=2))
    submenu_id: uuid.UUID = Column(UUID, ForeignKey('submenu.id'))
    submenu: 'SubMenu' = relationship('SubMenu', back_populates='dishes')
