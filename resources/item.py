from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'store_id',
        type=float,
        required=True,
        help="Every item needs a store_id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @classmethod
    def post(cls, name):
        if ItemModel.find_by_name(name):
            return {'message': "an item with name %s already exists!" % name}, 400

        data = cls.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        
        return {"item": item.json()}, 201

    @staticmethod
    def delete(name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "Item deleted"}
        else:
            return {'message': "No item with name %s" % name}
            
    @classmethod
    def put(cls, name):
        data = cls.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return {'item': item.json()}
    

class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}

