from django.conf.urls.defaults import *
from django.contrib.auth.views import login, password_change, password_change_done, password_reset, password_reset_confirm, password_reset_complete, password_reset_done
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('apps.users.views',
    url('login/$', 'login_plus_remember_me', {'template_name': 'users/login.html'}, 'user-login'),
    url(r'^profile/employee/(?P<user_id>(\d+))?$', 'employee_profile', name='employee-profile'),
    url(r'^profile/student/(?P<user_id>(\d+))?$', 'student_profile', name='student-profile'),
    url('^$', 'my_profile', name='my-profile'),
    url('email-change/', 'email_change', name='email-change'),
    url('password-change/', password_change, {'template_name' : 'users/password_change_form.html', 'post_change_redirect' : '/users/password-change-done/'}, name='password-change'),
    url('password-change-done/', 'password_change_done', name='password-change-done'),
    url('password-reset/', password_reset, {'template_name': 'users/password_reset_form.html'}, name='password-reset'),
    url('password-reset-done/', password_reset_done, {'template_name': 'users/password_reset_done.html'}, name='password-reset-done'),
    url('password-reset-confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'users/password_reset_confirm.html'}, name='password-reset-confirm'),
    url('password-reset-complete/', password_reset_complete, {'template_name': 'users/password_reset_complete.html'}, name='password-reset-complete'),
    url('logout/$', 'logout', name='user-logout'),
    url('^employees/', 'employees_list', name='employees-list'),
    url('^students/', 'students_list', name='students-list'),
)