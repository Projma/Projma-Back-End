from django.core.management.base import BaseCommand, CommandError
from ...views.templates import create_template
from ...models import Board


class BaseTemplate:
    def __init__(self, t_params, tl_params, l_params) -> None:
        self.template_params = t_params
        self.tasklists_params = tl_params
        self.labels_params = l_params


class Command(BaseCommand):
    help = "Create templates"

    templates = {
        "project management": BaseTemplate(
            t_params={'name': 'Project Management', 'description': 'Project Management Template'},
            tl_params=[{'title': 'Project Resources'}, \
                {'title': 'Questions For Next Meeting'}, \
                {'title': 'Project Progress'}, \
                {'title': 'To Do'}, \
                {'title': 'Pending'}, \
                {'title': 'Blocked'}, \
                {'title': 'Done'}],
            l_params=[{'title': 'Copy Request', 'color': '#D6FF36'}, \
                {'title': 'Priority', 'color': '#FF8980'}, \
                {'title': 'Design Team', 'color': '#C71287'}]
        ),
        "kanban":BaseTemplate(
            t_params={'name': 'Kanban', 'description': 'Kanban Template'},
            tl_params=[{'title': 'Backlog'}, \
                {'title': 'Design'}, \
                {'title': 'To Do'}, \
                {'title': 'Doing'}, \
                {'title': 'Code Review'}, \
                {'title': 'Testing'},
                {'title': 'Done'}],
            l_params=[{'title': 'In Queue', 'color': '#FF7896'}, \
                {'title': 'In Progress', 'color': '#FFCD26'}, \
                {'title': 'Completed', 'color': '#66FF96'}]
        ),
        "agile board": BaseTemplate(
            t_params={'name': 'Agile Board', 'description': 'Agile Board Template'},
            tl_params=[{'title': 'Done'}, \
                {'title': 'Current Sprint'}, \
                {'title': 'In Progress'}, \
                {'title': 'On Hold'}, \
                {'title': 'Next Up'}, \
                {'title': 'Questions'}],
            l_params=[{'title': 'Demand Marketing', 'color': '#E21F96'}, \
                {'title': 'Planning', 'color': '#5EFF96'}, \
                {'title': 'Happiness', 'color': '#F3F396'}, \
                {'title': 'Government', 'color': '#14FF96'},\
                {'title': 'Partners', 'color': '#1C9F96'}]
        ),
        "simple template": BaseTemplate(
            t_params = {'name': 'Simple Template', 'description': 'Simple Board Template'},
            tl_params = [{'title': 'Brainstorm'}, \
                {'title': 'To Do'}, \
                {'title': 'Doing'},\
                {'title': 'Done'}],
            l_params = []
        )
    }

    def handle(self, *args, **options):
        length = len(Board.objects.filter(is_template=True).all())
        if length == len(self.templates):
            self.stdout.write(self.style.WARNING("Templates were created before"))
        else:
            for key, value in self.templates.items():
                try:
                    create_template(value.template_params, value.tasklists_params, value.labels_params)
                    self.stdout.write("%s template " %key + self.style.SUCCESS("created successfully"))
                except:
                    raise CommandError("Fail to create %s template" %key)