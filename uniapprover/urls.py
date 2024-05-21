from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import authentication, permissions


# from django.conf.urls.static import static


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        return swagger


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Ideas Api",
        default_version="1.0.0",
        description="API Documentation of Ideas Application",
        contact=openapi.Contact(email="info@ideas.com"),
    ),
    public=False,
    authentication_classes=[authentication.BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated],
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("account/", include("account.urls")),
                path("universityapp/", include("universityapp.urls")),
                # path("component3/", include("core_apps.component3.urls")),
                path(
                    "swagger/schema/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="swagger-schema",
                ),
                path(
                    "redoc/",
                    schema_view.with_ui("redoc", cache_timeout=0),
                    name="schema-redoc",
                ),

            ]
        ),
    ),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "UniApproval API Admin"

admin.site.site_title = "UniApproval API Admin Portal"

admin.site.index_title = "Welcome to UniApproval API Portal"
