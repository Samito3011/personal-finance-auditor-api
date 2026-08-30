"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from audits.views import (
    TransactionViewSet,
    InsightsView,
    CategoryAnalysisView,
    AuditAlertsView,
    LargeTransactionView,
    DuplicateTransactionView,
    UnusualTransactionView,
    AuditSummaryView,
)


router = DefaultRouter()

router.register(
    r'transactions',
    TransactionViewSet,
    basename='transaction'
)


urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Transaction API
    path('api/', include(router.urls)),

    # Audit & Insights APIs
    path(
        'api/insights/',
        InsightsView.as_view()
    ),

    path(
        'api/insights/categories/',
        CategoryAnalysisView.as_view()
    ),

    path(
        'api/insights/alerts/',
        AuditAlertsView.as_view()
    ),

    path(
        'api/insights/large-transactions/',
        LargeTransactionView.as_view()
    ),

    path(
        'api/insights/duplicates/',
        DuplicateTransactionView.as_view()
    ),

    path(
        'api/insights/unusual/',
        UnusualTransactionView.as_view()
    ),

    path(
        'api/insights/summary/',
        AuditSummaryView.as_view()
    ),

    # API Documentation
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),
]