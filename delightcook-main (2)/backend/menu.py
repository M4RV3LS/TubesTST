from fastapi import APIRouter, HTTPException, Depends, status, Request, Form
from fastapi.encoders import jsonable_encoder
import json
from pydantic import BaseModel
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from authentication import *

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(json.loads(json.dumps(item)))

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

class Menu_Item(BaseModel):
	menu_id: int
	menu_name: str
	price: int
	duration: int
	calories: float
	level: str
	description: str

json_filename="data/menu_items.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

menu_stack = Stack()
menu_stack.push(data['menu_items'])  # Initial state

router = APIRouter(tags=["Menu"])

@router.get('/')
async def read_all_menu(sort_by: str = None, user: User = Depends(get_current_user)):
    menu_items = menu_stack.items[-1]

    if sort_by:
        if sort_by not in menu_items[0]:
            raise HTTPException(
                status_code=400, detail=f'Invalid key for sorting: {sort_by}'
            )

        menu_items.sort(key=lambda x: x[sort_by])

    return menu_items

@router.get('/{menu_id}')
async def read_menu(menu_id: int, user: User = Depends(get_current_user)):
	for menu_item in data['menu_items']:
		print(menu_item)
		if menu_item['menu_id'] == menu_id:
			return menu_item
	raise HTTPException(
		status_code=404, detail=f'Menu not found!'
	)

@router.get('/check/{menu_id}')
async def check_menu(menu_id: int, user: User = Depends(get_current_user)):
	menu_found = False
	for menu_item in data['menu_items']:
		print(menu_item)
		if menu_item['menu_id'] == menu_id:
			menu_found = True
	print(f"Menu ID {menu_id} found: {menu_found}")
	return menu_found

@router.post('/')
async def add_menu(item: Menu_Item, user: User = Depends(get_current_user)):
	item_dict = item.dict()
	item_found = False
	for menu_item in data['menu_items']:
		if menu_item['menu_id'] == item_dict['menu_id']:
			item_found = True
			return "Menu ID "+str(item_dict['menu_id'])+" exists."
	
	if not item_found:
		data['menu_items'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)
		menu_stack.push(data['menu_items'])
		return item_dict
	
	raise HTTPException(
		status_code=404, detail=f'Item not found!'
	)

@router.put('/')
async def update_menu(item: Menu_Item, user: User = Depends(get_current_user)):
	item_dict = item.dict()
	item_found = False
	for menu_idx, menu_item in enumerate(data['menu_items']):
		if menu_item['menu_id'] == item_dict['menu_id']:
			item_found = True
			data['menu_items'][menu_idx]=item_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			menu_stack.push(data['menu_items'])
			return "Menu updated!"
	
	if not item_found:
		return "Menu ID not found!"
	raise HTTPException(
		status_code=404, detail=f'Item not found!'
	)

@router.delete('/{menu_id}')
async def delete_menu(menu_id: int, user: User = Depends(get_current_user)):
	item_found = False
	for menu_idx, menu_item in enumerate(data['menu_items']):
		if menu_item['menu_id'] == menu_id:
			item_found = True
			data['menu_items'].pop(menu_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			menu_stack.push(data['menu_items'])
			return "Menu deleted!"
	
	if not item_found:
		return "Menu ID not found!"
	raise HTTPException(
		status_code=404, detail=f'Item not found!'
	)