import operator
from functools import reduce
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import BaseFilterBackend
from rest_framework.compat import coreapi, coreschema


class TaskFilter(BaseFilterBackend):
    filter_title = _('Filter')
    lookup_prefixes = {
        '^': 'startswith',
        '=': 'exact',
        '@': 'search',
        '$': 'regex',
        '!': 'iregex',
        '~': 'in',
        '>': 'gt',
        '<': 'lt',
        '>=': 'gte',
        '<=': 'lte',
        '!=': 'ne',
        '==': 'iexact',
        '~~*': 'istartswith',
        '*~~': 'iendswith',
        '~~~': 'contains',
    }

    def get_start_index_of_field(self, field_name):
        i = 0
        if not (65 <= ord(field_name[0]) <= 90 or 97 <= ord(field_name[0]) <= 122):
            i = 1
        if not (65 <= ord(field_name[1]) <= 90 or 97 <= ord(field_name[1]) <= 122):
            i = 2
        if not (65 <= ord(field_name[2]) <= 90 or 97 <= ord(field_name[2]) <= 122):
            i = 3
        return i

    def construct_search(self, field_name):
        lu_field = None
        i = self.get_start_index_of_field(field_name)
        lu_field = field_name[0:i]
        lookup = self.lookup_prefixes.get(lu_field)
        if lookup:
            field_name = field_name[i:]
        else:
            lookup = 'icontains'
        return LOOKUP_SEP.join([field_name, lookup])

    def get_search_fields(self, view, request):
        return getattr(view, 'filter_fields', None)

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(view, request)

        # print('queryset:::::::', queryset)
        # print('search_fields::::::', search_fields)
        # print('search_terms:::::::', search_terms)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]
        
        # print('orm_lookups:::::::', orm_lookups)

        conditions = []
        i = 0
        for search_term in search_terms:
            queries = [
                Q(**{orm_lookups[i]: term}) for term in search_term
            ]
            i += 1
            # print('queries:::::::', queries)
            try:
                conditions.append(reduce(operator.or_, queries))
            except:
                pass
        # print('conditions:::::::', conditions)
        try:
            queryset = queryset.filter(reduce(operator.and_, conditions))
        except:
            pass
        queryset = queryset.distinct()
        # print('queryset:::::::', queryset)
        return queryset

    def get_search_terms(self, view, request):
        search_fields = self.get_search_fields(view, request)
        params = []
        for field in search_fields:
            param = request.query_params.get(field[self.get_start_index_of_field(field):], '')
            param = param.replace('\x00', '')  # strip null characters
            param = param.replace(',', ' ')
            params.append(param.split())
        return params

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        search_fields = self.get_search_fields(view, None)
        return [coreapi.Field(
                    name=f'{field[self.get_start_index_of_field(field):]}',
                    required=False,
                    location='query',
                    schema=coreschema.String(
                        title = force_str(self.filter_title),
                        description = force_str(f'Filter by {field[self.get_start_index_of_field(field):]}.')
                    )
                ) for field in search_fields]