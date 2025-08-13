from flask import request, jsonify, Blueprint
from project.models import db, Item
from flask_jwt_extended import jwt_required

items_bp = Blueprint('items', __name__)

#Add Item 
@items_bp.route("/items", methods=['POST'])
@jwt_required()
def items():
    incoming_data = request.get_json()

    new_item = Item(name=incoming_data['name'], quantity=incoming_data['quantity'])
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message' : f"Item '{new_item.name}' added successfully"}), 201

#Get Item
@items_bp.route("/items", methods=['GET'])
def get_items():
    items = Item.query.all()
    item_list = []
    for item in items:
        item_data = {'name' : item.name, 'quantity' : item.quantity}
        item_list.append(item_data)
    
    return jsonify({'items' : item_list})