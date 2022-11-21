import random
from .models import WorkSpace


def encode(workspace: WorkSpace) -> str:
    id_encoded = f'6289{workspace.pk}'
    name_encoded = ''.join([chr(int(c) + 97) for c in str(hash(workspace.name) % 100000)])
    range_nums = [i for i in range(48, 58)] + [i for i in range(65, 91)] + [i for i in range(97, 123)]
    random_part = ''.join([chr(random.choice(range_nums)) for _ in range(8)])
    return f'{name_encoded}-{id_encoded}${workspace.name}{random_part}'


def decode(token) -> WorkSpace:
    id_encoded = token.split('$')[0].split('-')[1]
    workspace_id = int(id_encoded[4:])
    try:
        workspace = WorkSpace.objects.get(pk=workspace_id)
    except:
        workspace = None
    return workspace