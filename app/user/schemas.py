from drf_yasg import openapi


token_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "access": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
    },
)

registration_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
    },
)
