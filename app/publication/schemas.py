from drf_yasg import openapi

top_params = [
        openapi.Parameter(
            "top",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            default=10,
        ),
    ]
