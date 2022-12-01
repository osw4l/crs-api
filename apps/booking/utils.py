from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from collections import OrderedDict
from rest_framework import filters
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('current_page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class BaseViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    custom_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            if hasattr(self, 'list_serializer_class'):
                return self.list_serializer_class
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def get_custom_serializer(self, *args, **kwargs):
        custom_serializer_class = self.get_custom_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return custom_serializer_class(*args, **kwargs)

    def get_custom_serializer_class(self):
        assert self.custom_serializer_class is not None, (
                "'%s' should either include a `custom_serializer` attribute, "
                "or override the `get_custom_serializer_class()` method."
                % self.__class__.__name__
        )
        return self.custom_serializer_class


class CrudModelViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       BaseViewSet):
    pass
