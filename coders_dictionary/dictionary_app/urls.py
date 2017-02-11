from django.conf.urls import patterns, url 
from dictionary_app import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^$', views.index, name='main'),
	url(r'^word/(?P<word_name_slug>[\w\-]+)/$', views.word, name='word'),
	url(r'^add-word/', views.add_word, name="add-word"),
	url(r'^word/(?P<word_name_slug>[\w\-]+)/add-definition/$', views.add_definition, name='add-definition'),
	url(r'^register/', views.register, name='register'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^logout/', views.user_logout, name='logout'),
	url(r'^user/(?P<user_username>[\w\-]+)/$', views.user_profile, name='profile'),
	url(r'^user/(?P<user_username>[\w\-]+)/edit/$', views.edit_profile, name='edit_profile'),
	url(r'^like_category/$', views.like_category, name='like_category'),
	url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
	url(r'^recover-password/$', views.PasswordRecoveryView.as_view(), name='recover-password'),
	)