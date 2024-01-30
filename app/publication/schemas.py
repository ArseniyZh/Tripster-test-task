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
        description="Сортировать по дате публикации (timestamp)",
    ),
]
