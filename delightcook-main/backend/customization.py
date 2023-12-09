from fastapi import APIRouter, HTTPException, Depends, status, Request, Form
from fastapi.encoders import jsonable_encoder
import json
from pydantic import BaseModel
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from ingredients import check_ingredient
from authentication import *
from typing import List

class Ingredient(BaseModel):
    ingredient_id: int
    adjusted_quantity: float

class Customization_Item(BaseModel):
    custom_id: int
    Ingredients: List[Ingredient]
    order_id: int

json_filename="data/customization.json"

with open(json_filename,"r") as read_file:
    data = json.load(read_file)

router = APIRouter(tags=["Customization"])

@router.get('/')
async def read_all_customization(user: User = Depends(get_current_user)):
    return data

@router.post('/')
async def create_customization(customization_item: Customization_Item, user: User = Depends(get_current_user)):
    existing_custom_ids = [customization.get('custom_id', 0) for customization in data]
    new_custom_id = max(existing_custom_ids, default=0) + 1

    ingredients_encoded = jsonable_encoder(customization_item.Ingredients)  # Convert Ingredient objects to dict

    new_customization = {
        "custom_id": new_custom_id,
        "Ingredients": ingredients_encoded,  # Use the encoded ingredients
        "order_id": customization_item.order_id
    }
    data.append(new_customization)

    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=2)

    return new_customization

# @router.get('/order/{order_id}')
# async def read_order_customization(order_id: int, user: User = Depends(get_current_user)):
#     list_customization = []
#     order_found = 0
#     for customization_item in data['customization']:
#         print(customization_item)
#         if customization_item['order_id'] == order_id:
#             order_found += 1
#             list_customization.append(customization_item)
#     if order_found != 0:
#         return list_customization
#     else:
#         raise HTTPException(
#             status_code=404, detail=f'Order not found!'
#         )

# @router.get('/customer/{customer_id}')
# async def read_customer_customization(customer_id: int, user: User = Depends(get_current_user)):
#     list_customization = []
#     customer_found = 0
#     for customization_item in data['customization']:
#         print(customization_item)
#         if customization_item['customer_id'] == customer_id:
#             customer_found += 1
#             list_customization.append(customization_item)
#     if customer_found != 0:
#         return list_customization
#     else:
#         raise HTTPException(
#             status_code=404, detail=f'Customer not found!'
#         )

# @router.get('/ingredient/{ingredient_id}')
# async def read_ingredient_customization(ingredient_id: int, user: User = Depends(get_current_user)):
#     list_customization = []
#     ingredient_found = 0
#     for customization_item in data['customization']:
#         print(customization_item)
#         if customization_item['ingredient_id'] == ingredient_id:
#             ingredient_found += 1
#             list_customization.append(customization_item)
#     if ingredient_found != 0:
#         return list_customization
#     else:
#         raise HTTPException(
#             status_code=404, detail=f'Ingredient not found!'
#         )

# @router.post('/')
# async def add_customization(item: Customization_Item, user: User = Depends(get_current_user)):
#     item_dict = item.dict()
#     if check_ingredient(item_dict['ingredient_id']):
#         item_found = False
#         for customization_item in data['customization']:
#             if (customization_item['ingredient_id'] == item_dict['ingredient_id']):
#                 item_found = True
#                 update_customization(item)
#         if not item_found:
#             data['customization'].append(item_dict)
#             with open(json_filename, "w") as write_file:
#                 json.dump(data, write_file)
#             return item_dict
#         raise HTTPException(
#             status_code=404, detail=f'Item not found!'
#         )
#     else:
#         raise HTTPException(
#             status_code=404, detail=f'Ingredient ID not found!'
#         )

# @router.put('/')
# async def update_customization(item: Customization_Item, user: User = Depends(get_current_user)):
#     item_dict = item.dict()
#     item_found = False
#     for customization_idx, customization_item in enumerate(data['customization']):
#         if (customization_item['ingredient_id'] == item_dict['ingredient_id']):
#             item_found = True
#             data['customization'][customization_idx] = item_dict
#             with open(json_filename, "w") as write_file:
#                 json.dump(data, write_file)
#             return "Customization updated!"
#     if not item_found:
#         return "Ingredient ID not found!"
#     raise HTTPException(
#         status_code=404, detail=f'Item not found!'
#     )

# @router.delete('/{custom_id}')
# async def delete_customization(custom_id: int, user: User = Depends(get_current_user)):
# 	item_found = False
# 	for customization_idx, customization_item in enumerate(data['customization']):
# 		if customization_item['custom_id'] == custom_id:
# 			item_found = True
# 			data['customization'].pop(customization_idx)
			
# 			with open(json_filename,"w") as write_file:
# 				json.dump(data, write_file)
# 			return "Customization deleted!"
	
# 	if not item_found:
# 		return "Custom ID not found!"
# 	raise HTTPException(
# 		status_code=404, detail=f'Item not found!'
# 	)