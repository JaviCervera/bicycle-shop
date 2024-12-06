from typing import Iterable, Optional

from sqlalchemy import  select
from sqlalchemy.orm import Mapped, mapped_column

from catalog.domain import Description, Money, PartOption, PartOptionId, \
    PartOptionRepository, ProductPartId
from .sqlalchemy_base import SqlAlchemyBase
from .sqlalchemy_base_repository import SqlAlchemyBaseRepository


class PartOptionModel(SqlAlchemyBase):
    __tablename__ = 'part_options'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    part_id: Mapped[int]
    description: Mapped[str]
    price: Mapped[float]
    in_stock: Mapped[bool]


class OptionIncompatibilityModel(SqlAlchemyBase):
    __tablename__ = 'option_incompatibilities'
    option_a: Mapped[int] = mapped_column(primary_key=True)
    option_b: Mapped[int] = mapped_column(primary_key=True)


class OptionPriceModifierModel(SqlAlchemyBase):
    __tablename__ = 'option_price_modifiers'
    part_id: Mapped[int] = mapped_column(primary_key=True)
    depending_option_id: Mapped[int] = mapped_column(primary_key=True)
    coef: Mapped[float]


class SqlAlchemyPartOptionRepository(PartOptionRepository, SqlAlchemyBaseRepository):
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
            description=Description(result.description),
            price=Money(result.price),
            in_stock=result.in_stock) if result else None

    def create(
            self,
            part_id: ProductPartId,
            description: Description,
            price: float,
            in_stock: bool) -> PartOption:
        model = PartOptionModel(
            part_id=int(part_id),
            description=str(description),
            price=float(price),
            in_stock=in_stock)
        self._session.add(model)
        self._session.flush()
        return PartOption(
            id=PartOptionId(model.id),
            part_id=ProductPartId(model.part_id),
            description=Description(model.description),
            price=Money(model.price),
            in_stock=model.in_stock)

    def list_incompatibilities(
            self, id_: PartOptionId) -> Iterable[PartOptionId]:
        result_a = self._session.execute(
            select(OptionIncompatibilityModel.option_a) \
                .where(OptionIncompatibilityModel.option_b == int(id_))).all()
        result_b = self._session.execute(
            select(OptionIncompatibilityModel.option_b) \
                .where(OptionIncompatibilityModel.option_a == int(id_))).all()
        return set([PartOptionId(row.option_a) for row in result_a]
                   + [PartOptionId(row.option_b) for row in result_b])

    def create_incompatibility(
            self,
            option_a: PartOptionId,
            option_b: PartOptionId) -> None:
        self._session.add(OptionIncompatibilityModel(
            option_a=min(int(option_a), int(option_b)),
            option_b=max(int(option_a), int(option_b))))
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
            select(OptionPriceModifierModel.coef) \
                .where(OptionPriceModifierModel.part_id == int(part_id) \
                       and OptionPriceModifierModel.depending_option_id \
                       == int(depending_option_id))).first()
        return result or 1.0

    def create_depending_option(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId,
            coef: float) -> None:
        model = OptionPriceModifierModel(
            part_id=int(part_id),
            depending_option_id=int(depending_option_id),
            coef=coef)
        self._session.add(model)
        self._session.flush()
