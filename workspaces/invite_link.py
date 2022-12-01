import random
from .models import WorkSpace, Board


def encode(object: WorkSpace | Board) -> str:
    id_encoded = f'6289{object.pk}'
    name_encoded = ''.join([chr(int(c) + 97) for c in str(hash(object.name) % 100000)])
    range_nums = [i for i in range(48, 58)] + [i for i in range(65, 91)] + [i for i in range(97, 123)]
    # random_part = ''.join([chr(random.choice(range_nums)) for _ in range(8)])
    random_part = ''.join([str(i+5) for i in range(4)])
    type_encoded = 'workspace' if isinstance(object, WorkSpace) else 'board'
    return f'{name_encoded}{type_encoded}-{id_encoded}${object.name}{random_part}'


def decode(token) -> WorkSpace | Board:
    id_encoded = token.split('$')[0].split('-')[1]
    instance_id = int(id_encoded[4:])
    model_name = token.split('$')[0].split('-')[0][-5::]
    model = Board if model_name == 'board' else WorkSpace
    try:
        instance = model.objects.get(pk=instance_id)
    except:
        instance = None
    return instance