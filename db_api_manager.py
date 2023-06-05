from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://maximbazant:storagepassword@storagecluster.gq3ddlp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
inventory_db = client["MaterialInventory"]
materials_db = inventory_db["Materials"]
placements_db = inventory_db["Placement"]


# functions
def get_material_detail(input):
    materials = materials_db.find()

    for material in materials:
        if str(material["code"]) == input or material["content"].lower() == input.lower():
            return material
    
    return False

def get_materials(value=None):
    all_materials = materials_db.find()
    return_materials = []
    if value: # user is searching a specific material
        for material in all_materials:
            if str(material["placement"]).lower() == value.lower():
                return_materials.append(material)
    else:
        return_materials = all_materials
    
    return return_materials

def delete_material(code:int):

    result = materials_db.find_one({"code": code})
    print(result)
    placement = result["placement"]
    placements_db.update_one({}, {"$pull": {"taken_places": placement}})

    materials_db.delete_one({"code": code})

def add_new_material(content, fragile, placement, instruction, units_available:int, unit):
    result = materials_db.find().sort('code', -1).limit(1)
    try:
        largest_code = result[0]['code'] + 1
    except Exception:
        largest_code = 1

    material = {
        "code": largest_code,
        "content": content,
        "fragile": fragile,
        "placement": placement,
        "instruction": instruction,
        "units_available": units_available,
        "unit": unit
    }

    materials_db.insert_one(material)
    placements_db.update_one({}, {"$push": {"taken_places": placement}})

def edit_units_available(code:int, quantity:int):
    item = materials_db.find_one({"code": code})

    # check if the new value will be greater than or equal to 0
    if item["units_available"] + quantity >= 0:
        # update the item's units_available value
        materials_db.update_one({"code": code}, {"$inc": {"units_available": quantity}})
        return True
    else:
        return False
    
def get_placements():
    return placements_db.find()[0]