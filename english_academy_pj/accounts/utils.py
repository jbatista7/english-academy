import uuid

def generate_custom_id(UserX):
    custom_id = str(uuid.uuid4().int)[:5]

    try:
        id_exists = UserX.objects.get(id=custom_id)
        generate_custom_id()
    except:
        return custom_id