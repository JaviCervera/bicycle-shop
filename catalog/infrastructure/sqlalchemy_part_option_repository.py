from typing import Iterable, Optional

from sqlalchemy import  select
from sqlalchemy.orm import Mapped, mapped_column, Session

from catalog.domain import Money, Name, PartOption, PartOptionId, \
    PartOptionRepository, ProductPartId, Units
from .sqlalchemy_base import SqlAlchemyBase


class PartOptionModel(SqlAlchemyBase):
    __tablename__ = 'part_options'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    part_id: Mapped[int]
    name: Mapped[str]
    price: Mapped[float]
    available_units: Mapped[int]


class OptionIncompatibilityModel(SqlAlchemyBase):
    __tablename__ = 'option_incompatibilities'
    first_option_id: Mapped[int] = mapped_column(primary_key=True)
    second_option_id: Mapped[int] = mapped_column(primary_key=True)


class OptionPriceModifierModel(SqlAlchemyBase):
    __tablename__ = 'option_price_modifiers'
    part_id: Mapped[int] = mapped_column(primary_key=True)
    depending_option_id: Mapped[int] = mapped_column(primary_key=True)
    coefficient: Mapped[float]


class SqlAlchemyPartOptionRepository(PartOptionRepository):
    """ A SQLAlchemy-based implementation of PartOptionRepository. """
    def __init__(self, session: Session):
        self._session = session

    def list(
            self,
            part_id: Optional[ProductPartId] = None) -> Iterable[PartOptionId]:
        stmt = select(PartOptionModel.id)
        if part_id:
            stmt = stmt.where(PartOptionModel.part_id == int(part_id))
        return [PartOptionId(row.id)
                for row in self._session.execute(stmt).all()]

    def get(self, id_: PartOptionId) -> Optional[PartOption]:
        result = self._session.scalars(
            select(PartOptionModel) \
                .where(PartOptionModel.id == int(id_))).first()
        return PartOption(
            id=PartOptionId(result.id),
            part_id=ProductPartId(result.part_id),
            name=Name(result.name),
            price=Money(result.price),
            available_units=Units(result.available_units)) if result else None

    def create(
            self,
            part_id: ProductPartId,
            name: Name,
            price: Money,
            available_units: Units) -> PartOption:
        model = PartOptionModel(
            part_id=int(part_id),
            name=str(name),
            price=float(price),
            available_units=int(available_units))
        self._session.add(model)
        self._session.flush()
        return PartOption(
            id=PartOptionId(model.id),
            part_id=ProductPartId(model.part_id),
            name=Name(model.name),
            price=Money(model.price),
            available_units=Units(model.available_units))

    def list_incompatibilities(
            self, id_: PartOptionId) -> Iterable[PartOptionId]:
        result_a = self._session.execute(
            select(OptionIncompatibilityModel.first_option_id) \
                .where(OptionIncompatibilityModel.second_option_id == int(id_))).all()
        result_b = self._session.execute(
            select(OptionIncompatibilityModel.second_option_id) \
                .where(OptionIncompatibilityModel.first_option_id == int(id_))).all()
        return set([PartOptionId(row.first_option_id) for row in result_a]
                   + [PartOptionId(row.second_option_id) for row in result_b])

    def create_incompatibility(
            self,
            first_option_id: PartOptionId,
            second_option_id: PartOptionId) -> None:
        self._session.add(OptionIncompatibilityModel(
            first_option_id=min(int(first_option_id), int(second_option_id)),
            second_option_id=max(int(first_option_id), int(second_option_id))))
        self._session.flush()

    def list_depending_options(
            self, part_id: ProductPartId) -> Iterable[PartOptionId]:
        result = self._session.execute(
            select(OptionPriceModifierModel.depending_option_id) \
                .where(OptionPriceModifierModel.part_id == int(part_id))).all()
        return [PartOptionId(row.depending_option_id) for row in result]

    def get_depending_option_price_coef(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId) -> float:
        result = self._session.scalars(
            select(OptionPriceModifierModel.coefficient) \
                .where(OptionPriceModifierModel.part_id == int(part_id) \
                       and OptionPriceModifierModel.depending_option_id \
                       == int(depending_option_id))).first()
        return result or 1.0

    def create_depending_option(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId,
            coefficient: float) -> None:
        model = OptionPriceModifierModel(
            part_id=int(part_id),
            depending_option_id=int(depending_option_id),
            coefficient=coefficient)
        self._session.add(model)
        self._session.flush()
