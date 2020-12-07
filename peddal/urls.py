
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name="home"),
    path('cycle-adminlist/',views.ListCycle,name="cycle_adminlist"),
    path('cycle-list/',views.CycleList,name="cycle_list"),
    path('admin-editcycle/<int:id>',views.EditCycle,name="edit_cycle"),
    path('cycle-detail/<int:id>/',views.DetailCycle,name="cycle_detail"),
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('customer-detail/',views.CustomerDetail,name='customerdetail'),
    path('rental/<int:id>',views.RentalDetail,name='rental'),
    path('payment/',views.Payment,name='payment'),
    path('delete/<int:id>/',views.DeleteCycle,name='delete'),
    path('cycleapi/',views.CsrfCycleApi,name='cycle-api'),
    path('cycleobjectapi/<int:id>',views.CsrfCycleObjectApi,)
]