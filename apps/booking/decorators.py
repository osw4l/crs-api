from django.db import connection, reset_queries
from functools import wraps
from django.db.models import QuerySet
from rest_framework.response import Response
import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}", flush=True)
        print(f"Number of Queries : {end_queries - start_queries}", flush=True)
        print(f"Finished in : {(end - start):.2f}s", flush=True)
        return result

    return inner_func


def action_paginated(func):

    @wraps(func)
    def inner(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)
        assert isinstance(queryset, (list, QuerySet))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_custom_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_custom_serializer(queryset, many=True)
        return Response(serializer.data)
    return inner
