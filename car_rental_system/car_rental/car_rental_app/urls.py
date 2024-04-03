from django.urls import  path
from .import views

urlpatterns = [
   path('',views.home),
   path('user_registration',views.user_registration),
   path('login',views.loginpage),
   path('owner_registration',views.owner_registration),
   
   
   
   path('admin_home',views.adminhome),
   path('admin_view_users',views.admin_view_users),
   path('admin_view_owners',views.admin_view_owners),
   path('admin_approve_vehicles/<id>',views.admin_approve_vehicles),
   path('admin_accept_vehicle/<id>',views.admin_accept_vehicle),
   path('admin_reject_vehicle/<id>',views.admin_reject_vehicle),
   path('admin_view_images/<id>',views.admin_view_images),
   path('admin_view_booking',views.admin_view_booking),
   path('admin_view_payments/<id>',views.admin_view_payments),
   path('admin_view_feedback/<id>',views.admin_view_feedback),
   
   
   
   path('ownerhome',views.ownerhome),
   path('owner_manage_vehicles',views.owner_manage_vehicles),
   path('owner_vehicle_available/<id>',views.owner_vehicle_available),
   path('owner_vehicle_notavailable/<id>',views.owner_vehicle_notavailable),
   path('owner_delete_vehicle/<id>',views.owner_delete_vehicle),
   path('owner_update_vehicle/<id>',views.owner_update_vehicle),
   path('upload_img/<id>',views.upload_img),
   path('owner_delete_image/<id>',views.owner_delete_image),
   path('owner_view_pofile',views.owner_view_pofile),
   path('owner_manage_item',views.owner_manage_item),
   path('owner_delete_item/<id>',views.owner_delete_item),
   path('owner_update_item/<id>',views.owner_update_item),
   path('owner_view_booking',views.owner_view_booking),
   path('owner_view_user_details/<id>',views.owner_view_user_details),
   path('owner_accept_booking/<id>',views.owner_accept_booking),
   path('owner_reject_booking/<id>',views.owner_reject_booking),
   path('owner_view_payments/<id>',views.owner_view_payments),
   path('owner_view_payments/<id>',views.owner_view_payments),
   path('ready_to_deliver/<id>',views.ready_to_deliver),
   path('delivered/<id>',views.delivered),
   path('owner_view_feedback/<id>',views.owner_view_feedback),
   path('owner_accept_return/<fdate>/<tdate>/<rdate>/<bamt>/<bid>/<id>/<type>',views.owner_accept_return),
   path('owner_view_user',views.owner_view_user),
   path('owner_chats/<id>',views.owner_chats),
   path('owner_viewmsg',views.owner_viewmsg),
   path('owner_insert_chat/<msg>',views.owner_insert_chat),
   

   
   
   
   
   
   
   path('userhome',views.userhome),
   path('user_view_vehicles',views.user_view_vehicles),
   path('user_view_owners/<id>',views.user_view_owners),
   path('user_booking/<id>/<amt>',views.user_booking),
   path('user_payment/<type>/<amt>/<id1>',views.user_payment),
   path('user_return_vehicle/<id>/<id1>',views.user_return_vehicle),
   path('user_return_payment/<id>',views.user_return_payment,name='user_return_payment'),
   path('user_feedback/<id>',views.user_feedback),
   path('user_view_items',views.user_view_items),
   path('user_booking_item/<id>/<amt>',views.user_booking_item),
   path('user_return_req/<id>/<id1>',views.user_return_req),
   path('user_vehicle_booking',views.user_vehicle_booking),
   path('user_item_booking',views.user_item_booking),
   path('user_chat',views.user_chat),
   # path('user_chat_owner/<id>',views.user_chat_owner),
   path('user_vehicle_details/<id>',views.user_vehicle_details),
   path('user_item_details/<id>',views.user_item_details),
   
   path('user_chats/<id>',views.user_chats),
   path('user_viewmsg',views.user_viewmsg),
   path('user_insert_chat/<msg>',views.user_insert_chat),

]