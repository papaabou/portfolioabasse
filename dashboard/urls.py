from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm

urlpatterns = [
    path("", views.dashboard_index, name="dashboard_index"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Password Reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='dashboard/password_reset.html',
            email_template_name='dashboard/password_reset_email.html',
            success_url='/admin/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='dashboard/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Use path converter to capture full token including "=" and "/"
    path(
        'password-reset-confirm/<uidb64>/<path:token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='dashboard/password_reset_confirm.html',
            form_class=CustomSetPasswordForm,
            success_url='/admin/password-reset-complete/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='dashboard/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path("messages/", views.messages_list, name="dashboard_messages"),
    path("messages/<int:pk>/", views.message_view, name="dashboard_message_view"),
    path("projects/", views.projects_list, name="dashboard_projects"),
    path("projects/new/", views.project_create, name="dashboard_project_create"),
    path("projects/<int:pk>/edit/", views.project_edit, name="dashboard_project_edit"),
    path("projects/<int:pk>/images/add/", views.project_image_add, name="dashboard_project_image_add"),
    path("projects/<int:pk>/images/<int:image_pk>/delete/", views.project_image_delete, name="dashboard_project_image_delete"),

    path("testimonials/", views.testimonials_list, name="dashboard_testimonials"),
    path("testimonials/<int:pk>/approve/", views.testimonial_approve, name="dashboard_testimonial_approve"),
    path("testimonials/<int:pk>/decline/", views.testimonial_decline, name="dashboard_testimonial_decline"),
    path("testimonials/<int:pk>/delete/", views.testimonial_delete, name="dashboard_testimonial_delete"),

    path("blog/", views.blog_list, name="dashboard_blog"),
    path("blog/new/", views.blog_create, name="dashboard_blog_create"),
    path("blog/<int:pk>/edit/", views.blog_edit, name="dashboard_blog_edit"),

    path("services/", views.services_list, name="dashboard_services"),
    path("services/<int:pk>/edit/", views.service_edit, name="dashboard_service_edit"),
]
