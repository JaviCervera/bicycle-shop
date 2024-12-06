from catalog.domain import Description, PartOption, PartOptionId, Product, \
    ProductId, ProductPart, ProductPartId

from marshmallow import Schema, fields, post_load

class ProductSchema(Schema):
    id = fields.Int()
    description = fields.Str()

    @post_load
    def load_product(self, data, **_) -> Product:
        return Product(
            id=ProductId(data['id']),
            description=Description(data['description']))

class ProductPartSchema(Schema):
    id = fields.Int()
    product_id = fields.Int()
    description = fields.Str()

    @post_load
    def load_product_part(self, data, **_) -> ProductPart:
        return ProductPart(
            id=ProductPartId(data['id']),
            product_id=ProductId(data['product_id']),
            description=Description(data['description']))

class PartOptionSchema(Schema):
    id = fields.Int()
    part_id = fields.Int()
    description = fields.Str()
    price = fields.Float()
    in_stock = fields.Bool()

    @post_load
    def load_part_option(self, data, **_) -> PartOption:
        return PartOption(
            id=PartOptionId(data['id']),
            part_id=ProductPartId(data['part_id']),
            description=Description(data['description']),
            price=data['price'],
            in_stock=data['in_stock'])
