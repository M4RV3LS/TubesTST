from fastapi import APIRouter, HTTPException, Depends, status, Request, Form
from fastapi.encoders import jsonable_encoder
import json
from pydantic import BaseModel
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from authentication import *

class Order_Item(BaseModel):
	order_id: int
	customer_id: int
	menu_id: int
	menu_quantity: int

json_filename = "data/order.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter(tags=["Order"])

@router.get('/')
async def read_all_order(user: User = Depends(get_current_user)):
	return data['order']

@router.get('/{order_id}')
async def read_order(order_id: int, user: User = Depends(get_current_user)):
	for order_item in data['order']:
		print(order_item)
		if order_item['order_id'] == order_id:
			return order_item
	raise HTTPException(
		status_code=404, detail=f'Order not found!'
    )

@router.post('/')
async def add_order(item: Order_Item, user: User = Depends(get_current_user)):
    # Get the highest order_id from the data or 0 if no orders exist
    max_order_id = max([order_item['order_id'] for order_item in data['order']], default=0)
    # Increment the order_id by 1 to get a new unique order_id
    new_order_id = max_order_id + 1
    # Set the new order_id to the item
    item_dict = item.dict()
    item_dict['order_id'] = new_order_id
    # Append the new order item to the order data
    data['order'].append(item_dict)
    # Write the updated orders back to the JSON file
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)

    return item_dict