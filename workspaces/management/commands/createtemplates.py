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
            t_params={'name': 'مدیریت پروژه', 'description': 'قالب مدیریت پروژه', 'background_pic': '../../template/static/project-management-pic.jpg'},
            tl_params=[{'title': 'منابع پروژه'}, \
                {'title': 'سوالات جلسه بعدی'}, \
                {'title': 'پیشرفت پروژه'}, \
                {'title': 'انجام دادن'}, \
                {'title': 'در انتظار'}, \
                {'title': 'مسدود'}, \
                {'title': 'انجام شده'}],
            l_params=[{'title': 'درخواست کپی', 'color': '#D6FF36'}, \
                {'title': 'اولویت', 'color': '#FF8980'}, \
                {'title': 'تیم طراحی', 'color': '#C71287'}]
        ),
        "kanban":BaseTemplate(
            t_params={'name': 'کنبان(kanban)', 'description': 'قالب کنبان', 'background_pic': '../../template/static/kanban-pic.jpg'},
            tl_params=[{'title': 'جمع شدن'}, \
                {'title': 'طراحی'}, \
                {'title': 'انجام دادن'}, \
                {'title': 'در حال انجام'}, \
                {'title': 'بررسی کد'}, \
                {'title': 'آزمایش کردن'},
                {'title': 'انجام شده'}],
            l_params=[{'title': 'در صف', 'color': '#FF7896'}, \
                {'title': 'در حال پیشرفت', 'color': '#FFCD26'}, \
                {'title': 'تکمیل شده', 'color': '#66FF96'}]
        ),
        "agile board": BaseTemplate(
            t_params={'name': 'صفحه چابک', 'description': 'قالب صفحه چابک', 'background_pic': '../../template/static/agile-board-pic.jpg'},
            tl_params=[{'title': 'انجام شده'}, \
                {'title': 'اسپرینت فعلی'}, \
                {'title': 'در حال پیش رفت'}, \
                {'title': 'در انتظار'}, \
                {'title': 'بعدی'}, \
                {'title': 'سوالات'}],
            l_params=[{'title': 'بازاریابی تقاضا', 'color': '#E21F96'}, \
                {'title': 'برنامه ریزی', 'color': '#5EFF96'}, \
                {'title': 'خوشحالی', 'color': '#F3F396'}, \
                {'title': 'دولت', 'color': '#14FF96'},\
                {'title': 'شرکا', 'color': '#1C9F96'}]
        ),
        "simple template": BaseTemplate(
            t_params = {'name': 'صفحه ساده', 'description': 'قالب صفحه ساده', 'background_pic': '../../template/static/simple-pic.jpg'},
            tl_params = [{'title': 'ایده پردازی'}, \
                {'title': 'انجام دادن'}, \
                {'title': 'در حال انجام'},\
                {'title': 'انجام شده'}],
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