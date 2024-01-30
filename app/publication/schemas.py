from drf_yasg import openapi

top_params = [
    openapi.Parameter(
        "top",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description="Сортировать по рейтингу",
        default=10,
    ),
    openapi.Parameter(
        "created_at",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description="Строгое соответствие даты публикации",
    ),
    openapi.Parameter(
        "created_at__gte",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description="Дата публикации >= указанная дата",
    ),
    openapi.Parameter(
        "created_at__lte",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description="Дата публикации <= указанная дата",
    ),
    openapi.Parameter(
        "sorted_by_date",
        openapi.IN_QUERY,
        type=openapi.TYPE_BOOLEAN,
        description="Сортировать по дате",
    ),
    openapi.Parameter(
        "sorted_by_rating",
        openapi.IN_QUERY,
        type=openapi.TYPE_BOOLEAN,
        description="Сортировать по рейтингу",
    ),
]
