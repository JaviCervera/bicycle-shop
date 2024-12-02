from typing import Iterable, Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Mapped, mapped_column, Session

from catalog.domain import PartOption, PartOptionRepository
from .sqlalchemy_base import SqlAlchemyBase

class PartOptionModel(SqlAlchemyBase):
  __tablename__ = 'part_options'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  part_id: Mapped[int]
  description: Mapped[str]
  price: Mapped[float]
  in_stock: Mapped[bool]


class OptionIncompatibilityModel(SqlAlchemyBase):
  __tablename__ = 'option_incompatibilities'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  option_id: Mapped[int]
  incompatible_option_id: Mapped[int]


class OptionPriceModifierModel(SqlAlchemyBase):
  __tablename__ = 'option_price_modifiers'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  part_id: Mapped[int]
  depending_option_id: Mapped[int]
  coef: Mapped[float]


class SqlAlchemyPartOptionRepository(PartOptionRepository):
  def __init__(self, engine: Engine):
    self._engine = engine
    self._session = Session(engine)

  def list(self, part_id: int = None) -> Iterable[int]:
    stmt = select(PartOptionModel.id)
    if part_id:
      stmt = stmt.where(PartOptionModel.part_id == part_id)
    return [row.id for row in self._session.execute(stmt).all()]

  def get(self, id: int) -> Optional[PartOption]:
    result = self._session.scalars(
      select(PartOptionModel) \
        .where(PartOptionModel.id == id)).first()
    return PartOption(
      id=result.id,
      part_id=result.part_id,
      description=result.description,
      price=result.price,
      in_stock=result.in_stock) if result else None

  def create(self, part_id: int, description: str, price: float, in_stock: bool) -> PartOption:
    model = PartOptionModel(
      part_id=part_id,
      description=description,
      price=price,
      in_stock=in_stock)
    self._session.add(model)
    self._session.flush()
    return PartOption(
      id=model.id,
      part_id=model.part_id,
      description=model.description,
      price=model.price,
      in_stock=model.in_stock)

  def list_incompatibilies(self, id: int) -> Iterable[int]:
    result = self._session.execute(
      select(OptionIncompatibilityModel.incompatible_option_id) \
        .where(OptionIncompatibilityModel.option_id == id)).all()
    return [row.incompatible_option_id for row in result]
  
  def create_incompatibility(
      self, option_id: int, incompatible_option_id: int) -> None:
    self._session.add(OptionIncompatibilityModel(
      option_id=option_id,
      incompatible_option_id=incompatible_option_id))
    self._session.flush()

  def list_depending_options(self, part_id: int) -> Iterable[int]:
    result = self._session.execute(
      select(OptionPriceModifierModel.depending_option_id) \
        .where(OptionPriceModifierModel.part_id == part_id)).all()
    return [row.depending_option_id for row in result]

  def get_depending_option_price_coef(
      self, part_id: int, depending_option_id: int) -> float:
    result = self._session.scalars(
      select(OptionPriceModifierModel.coef) \
        .where(OptionPriceModifierModel.part_id == part_id \
                and OptionPriceModifierModel.depending_option_id \
                == depending_option_id)).first()
    return result or 1.0
  
  def create_depending_option(
      self, part_id: int, depending_option_id: int, coef: float) -> None:
    model = OptionPriceModifierModel(
      part_id=part_id,
      depending_option_id=depending_option_id,
      coef=coef)
    self._session.add(model)
    self._session.flush()

  def commit(self) -> None:
    self._session.commit()
  
  def close(self) -> None:
    self._session.close()

  def __enter__(self) -> 'SqlAlchemyPartOptionRepository':
    return self
  
  def __exit__(self) -> None:
    self.close()