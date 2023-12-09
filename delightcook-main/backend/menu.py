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
	menu_url: str

json_filename="data/menu_items.json"
json_filename1="data/ingredients.json"
json_filename2="data/composition.json"
json_filename3="data/customization.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)
with open(json_filename1,"r") as read_file:
	data1 = json.load(read_file)
with open(json_filename2,"r") as read_file:
	data2 = json.load(read_file)
with open(json_filename3,"r") as read_file:
	data3 = json.load(read_file)

menu_stack = Stack()
menu_stack.push(data['menu_items'])  # Initial state

router = APIRouter(tags=["Menu"])

@router.get('/')
async def read_all_menu(sort_by: str = None):
    menu_items = menu_stack.items[-1]

    if sort_by:
        if sort_by not in menu_items[0]:
            raise HTTPException(
                status_code=400, detail=f'Invalid key for sorting: {sort_by}'
            )

        menu_items.sort(key=lambda x: x[sort_by])

    return menu_items

@router.get('/check/{menu_id}')
async def check_menu(menu_id: int):
	menu_found = False
	for menu_item in data['menu_items']:
		print(menu_item)
		if menu_item['menu_id'] == menu_id:
			menu_found = True
	print(f"Menu ID {menu_id} found: {menu_found}")
	return menu_found

@router.post('/')
async def add_menu(item: Menu_Item, user: User = Depends(get_current_user)):
    # Get the highest menu_id from the data or 0 if no menu items exist
    max_menu_id = max([menu_item['menu_id'] for menu_item in data['menu_items']], default=0)
    # Increment the menu_id by 1 to get a new unique menu_id
    new_menu_id = max_menu_id + 1

    # Update the item_dict with the new menu_id
    item_dict = item.dict()
    item_dict['menu_id'] = new_menu_id

    # Append the new menu item to the menu data
    data['menu_items'].append(item_dict)
    # Write the updated menu items back to the JSON file
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)

    # Update the stack
    menu_stack.push(data['menu_items'])

    return item_dict

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

@router.get('/{menu_id}')
async def read_menu(menu_id: int):
    menu_item = next((item for item in data['menu_items'] if item['menu_id'] == menu_id), None)

    if menu_item is None:
        raise HTTPException(status_code=404, detail='Menu not found!')

    menu_composition = [comp for comp in data2['composition'] if comp['menu_id'] == menu_id]

    ingredients_list = []
    for comp in menu_composition:
        ingredient_id = comp['ingredient_id']
        ingredient = next((ing for ing in data1['ingredients'] if ing['ingredient_id'] == ingredient_id), None)
        if ingredient:
            ingredient_data = {
                'ingredient_id': ingredient_id,
                'ingredient_name': ingredient['ingredient_name'],
                'default_quantity': comp['default_quantity'],
                'unit': comp['unit']
            }
            ingredients_list.append(ingredient_data)

    result = {
        'menu_id': menu_item['menu_id'],
        'menu_name': menu_item['menu_name'],
        'price': menu_item['price'],
        'duration': menu_item['duration'],
        'calories': menu_item['calories'],
        'level': menu_item['level'],
        'description': menu_item['description'],
		'menu_url': menu_item['menu_url'],
        'ingredients': ingredients_list
    }

    return result