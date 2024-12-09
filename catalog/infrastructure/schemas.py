"""
Provides Marshmallow schemas to help with the serialization of models across
the network.
"""

from catalog.domain import Money, Name, PartOption, PartOptionId, \
    Product, ProductId, ProductPart, ProductPartId, Units

from marshmallow import Schema, fields, post_load

class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()

    @post_load
    def load_product(self, data, **_) -> Product:
        return Product(
            id=ProductId(data['id']),
            name=Name(data['name']))

class ProductPartSchema(Schema):
    id = fields.Int()
    product_id = fields.Int()
    name = fields.Str()

    @post_load
    def load_product_part(self, data, **_) -> ProductPart:
        return ProductPart(
            id=ProductPartId(data['id']),
            product_id=ProductId(data['product_id']),
            name=Name(data['name']))

class PartOptionSchema(Schema):
    id = fields.Int()
    part_id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    available_units = fields.Int()

    @post_load
    def load_part_option(self, data, **_) -> PartOption:
        return PartOption(
            id=PartOptionId(data['id']),
            part_id=ProductPartId(data['part_id']),
            name=Name(data['name']),
            price=Money(data['price']),
            available_units=Units(data['available_units']))
