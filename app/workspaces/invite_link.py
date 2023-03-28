from .models import WorkSpace, Board


def encode(object) -> str:
    id_encoded = f'6289{object.pk}'
    # name_encoded = ''.join([chr(int(c) + 97) for c in str(hash(object.name) % 100000)])
    print(str(hash(object.name) % 100000))
    type_encoded = 'workspace' if isinstance(object, WorkSpace) else 'board'
    name_encoded = object.owner.user.username if isinstance(object, WorkSpace) else object.workspace.owner.user.username
    return f'{name_encoded}{type_encoded}-{id_encoded}${object.name}{len(object.members.all())}'


def decode(token):
    try:
        id_encoded = token.split('$')[0].split('-')[1]
        instance_id = int(id_encoded[4:])
        first_part = token.split('$')[0].split('-')[0]
        second_part = token.split('$')[1]
        model_type = first_part[-5::]
        model = Board if model_type == 'board' else WorkSpace
        instance = model.objects.get(pk=instance_id)
        instance_members_len = str(len(instance.members.all()))
        instance_name = second_part[0:len(second_part) - len(instance_members_len)]
        owner = instance.owner.user.username if isinstance(instance, WorkSpace) else instance.workspace.owner.user.username
        owner_username = first_part[0:len(first_part) - 5] if model_type == 'board' else first_part[0:len(first_part) - 9]
        if instance_name != instance.name or str(len(instance.members.all())) != second_part[-len(instance_members_len)::] or \
            id_encoded[0:4] != '6289' or model_type not in ['board', 'space'] or owner != owner_username:
            raise ModuleNotFoundError
    except:
        instance = None
    return instance