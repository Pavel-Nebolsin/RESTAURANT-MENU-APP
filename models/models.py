import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__: str = 'menu'

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = Column(String, unique=True, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    submenus: Mapped[list['SubMenu']] = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenu(Base):
    __tablename__: str = 'submenu'

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = Column(String, unique=True, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    menu_id: Mapped[uuid.UUID] = Column(UUID, ForeignKey('menu.id'))
    menu: Mapped['Menu'] = relationship('Menu', back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='submenu', cascade='all, delete')


class Dish(Base):
    __tablename__: str = 'dish'

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = Column(String, unique=True, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    price: Mapped[float] = Column(Numeric(precision=10, scale=2))
    submenu_id: Mapped[uuid.UUID] = Column(UUID, ForeignKey('submenu.id'))
    submenu: Mapped['SubMenu'] = relationship('SubMenu', back_populates='dishes')
