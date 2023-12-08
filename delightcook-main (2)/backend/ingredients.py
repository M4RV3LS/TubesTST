from fastapi import APIRouter, HTTPException, Depends, status, Request, Form
from fastapi.encoders import jsonable_encoder
import json
from pydantic import BaseModel
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from authentication import *

class Ingredient_Item(BaseModel):
    ingredient_id: int
    ingredient_name: str

json_filename = "data/ingredients.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter(tags=["Ingredients"])

@router.get('/')
async def read_all_ingredients(user: User = Depends(get_current_user)):
	return data['ingredients']

@router.get('/check/{ingredient_id}')
async def check_ingredient(ingredient_id: int, user: User = Depends(get_current_user)):
	ingredient_found = False
	for ingredient_item in data['ingredients']:
		print(ingredient_item)
		if ingredient_item['ingredient_id'] == ingredient_id:
			ingredient_found = True
	return ingredient_found

@router.get('/{ingredient_id}')
async def read_ingredient(ingredient_id: int, user: User = Depends(get_current_user)):
	for ingredient_item in data['ingredients']:
		print(ingredient_item)
		if ingredient_item['ingredient_id'] == ingredient_id:
			return ingredient_item
	raise HTTPException(
		status_code=404, detail=f'Ingredient not found!'
    )

@router.post('/')
async def add_ingredient(item: Ingredient_Item, user: User = Depends(get_current_user)):
	item_dict = item.dict()
	item_found = False
	for ingredient_item in data['ingredients']:
		if ingredient_item['ingredient_id'] == item_dict['ingredient_id']:
			item_found = True
			return "Ingredient ID "+str(item_dict['ingredient_id'])+" exists."
	
	if not item_found:
		data['ingredients'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'Item not found!'
	)

@router.put('/')
async def update_ingredient(item: Ingredient_Item, user: User = Depends(get_current_user)):
	item_dict = item.dict()
	item_found = False
	for ingredient_idx, ingredient_item in enumerate(data['ingredients']):
		if ingredient_item['ingredient_id'] == item_dict['ingredient_id']:
			item_found = True
			data['ingredients'][ingredient_idx] = item_dict
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Ingredient updated!"
	if not item_found:
		return "Ingredient ID not found!"
	raise HTTPException(
		status_code=404, detail=f'Item not found!'
    )

@router.delete('/{ingredient_id}')
async def delete_ingredient(ingredient_id: int, user: User = Depends(get_current_user)):
	item_found = False
	for ingredient_idx, ingredient_item in enumerate(data['ingredients']):
		if ingredient_item['ingredient_id'] == ingredient_id:
			item_found = True
			data['ingredients'].pop(ingredient_idx)
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Ingredient deleted!"
	if not item_found:
		return "Ingredient ID not found!"
	raise HTTPException(
		status_code=404, detail=f'Item not found!'
    )