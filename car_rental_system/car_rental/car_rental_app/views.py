from datetime import date, datetime
import sqlite3
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

from car_rental.settings import BASE_DIR
from .models import *
from django.db import connection

from django.db.models import Q


from django.utils import timezone


from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import auth,User,Group
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db import models
from django.core.files.storage import FileSystemStorage
from pprint import pprint
from django.core.mail import send_mail
from django.utils.timezone import datetime 
import random



# Create your views here.
def home(request):
    return render(request,'home.html')

def user_registration(request):
    if 'register' in request.POST:
        fname=request.POST['fname']
        sname=request.POST['sname']
        hname=request.POST['hname']
        place=request.POST['place']
        pincode=request.POST['pincode']
        phone=request.POST['phone']
        email=request.POST['email']
        adhar=request.POST['adhar']
        dfront=request.FILES['dfront']
        fs = FileSystemStorage()
        f_nam =fs.save(dfront.name, dfront)
        dback=request.FILES['dback']
        bs = FileSystemStorage()
        b_nam =fs.save(dback.name, dback)
        image=request.FILES['image']
        ls = FileSystemStorage()
        l_nam =fs.save(image.name, image)
        username=request.POST['username']
        password=request.POST['password']
        lati=request.POST['latitude']
        longi=request.POST['longitude']
        
        qry=login(username=username,password=password,usertype='user')
        l=qry.save()
        print(f_nam,l_nam,b_nam)
        qry2=users(first_name=fname,second_name=sname,house_name=hname,place=place,pincode=pincode,email=email,adhar_card=adhar,driving_license_back=b_nam,driving_license_front=f_nam,picture=l_nam,latitude=lati,logitu=longi,login_id=qry.pk,phone=phone)
        qry2.save()
        return HttpResponse("<script>alert('Registration Success');window.location='login'</script>")
        
    return render(request,'user_registration.html')


def loginpage(request):
    if 'login' in request.POST:
        username=request.POST['username']
        password=request.POST['password']
        try:
            lg=login.objects.get(username=username,password=password)
            print(lg)
            request.session['login_id']=lg.pk
            if lg.usertype == 'admin':
                return HttpResponse("<script>alert('Login Success');window.location='admin_home'</script>")
            elif lg.usertype == 'user':
                ab=users.objects.get(login_id=request.session['login_id'])
                request.session['uid']=ab.pk
                request.session['uname']=ab.first_name
                return HttpResponse("<script>alert('Login Success');window.location='userhome'</script>")
            elif lg.usertype == 'owner':
                cd=owners.objects.get(login_id=request.session['login_id'])
                request.session['oid']=cd.pk
                request.session['oname']=cd.first_name
                return HttpResponse("<script>alert('Login Success');window.location='ownerhome'</script>")
            
        except:
            return HttpResponse("<script>alert('Invalid Username or Password');window.location='login'</script>")
    return render(request,'login.html')


def owner_registration(request):
    if 'ok' in request.POST:
        fname=request.POST['fname']
        sname=request.POST['sname']
        place=request.POST['place']
        phone=request.POST['phone']
        email=request.POST['email']
        image=request.FILES['image']
        fs = FileSystemStorage()
        f_nam =fs.save(image.name, image)
        username=request.POST['username']
        password=request.POST['password']
        
        qry=login(username=username,password=password,usertype='owner')
        qry.save()
        
        qry2=owners(first_name=fname,second_name=sname,place=place,phone=phone,email=email,image=f_nam,login_id=qry.pk)
        qry2.save()
        return HttpResponse("<script>alert('Registration Success');window.location='login'</script>")

    return render(request,'owner_registration.html')
        


####################################################################################################


def adminhome(request):
	return render(request,"adminhome.html")

def admin_view_users(request):
    obj=users.objects.all()
    return render(request,'admin_view_users.html',{'obj':obj})

def admin_view_owners(request):
    obj=owners.objects.all()
    if 'filter' in request.POST:
        search_term = request.POST['search']
        # place = f'%{search_term}%'
        # print(place)
        obj = owners.objects.filter(place__contains=search_term)
        # print(ob.query)  # Print the generated SQL query
        # print(obj)
    else:
       obj=owners.objects.all()    
    
    return render(request,'admin_view_owners.html',{'obj':obj})

def admin_approve_vehicles(request,id):
    obj=vehicles.objects.filter(owner_id=id)
    return render(request,'admin_approve_vehicles.html',{'obj':obj})

def admin_accept_vehicle(request,id):
    obj=vehicles.objects.get(vehicle_id=id)
    obj.car_status='APPROVED'
    obj.save()
    return HttpResponse("<script>alert('Accepted');window.location='/admin_view_owners'</script>")

def admin_reject_vehicle(request,id):
    obj=vehicles.objects.get(vehicle_id=id)
    obj.car_status='REJECTED'
    obj.save()
    return HttpResponse("<script>alert('Rejected');window.location='/admin_view_owners'</script>")

def admin_view_images(request,id):
    obj=images.objects.filter(vehicle_id=id)
    return render(request,'admin_view_images.html',{'obj':obj})

def admin_view_booking(request):
    obj=booking.objects.all()
    return render(request,'admin_view_booking.html',{'obj':obj})


def admin_view_payments(request,id):
    obj=payment.objects.get(booking_id=id)
    adpay=obj.amount
    commission=(int(adpay)*5)/100
    return render(request,'admin_view_payments.html',{'obj':obj,'amt':commission})

def admin_view_feedback(request,id):
    obj=feedback.objects.filter(booking_id=id)
    return render(request,'admin_view_feedback.html',{'obj':obj})

#########################################################################################

def ownerhome(request):
    return render(request,'ownerhome.html')

def owner_manage_vehicles(request):
    obj=vehicles.objects.filter(owner_id=request.session['oid'])
    if 'upload' in request.POST:

        brand=request.POST['brand']
        model=request.POST['model']
        colour=request.POST['colour']
        seats=request.POST['seats']
        description=request.POST['description']
        rent=request.POST['rent']
        image=request.FILES['img1']
        fs = FileSystemStorage()
        f_nam =fs.save(image.name, image)
        
        ab=vehicles(brand=brand,model=model,colour=colour,no_seat=seats,description=description,per_day_rent=rent,car_status='pending',vehicle_image=f_nam,owner_id=request.session['oid'])
        ab.save()
        return HttpResponse("<script>alert('Added');window.location='/owner_manage_vehicles'</script>")
        
    return render(request,'owner_manage_vehicles.html',{'obj':obj})

def owner_vehicle_available(request,id):
    obj=vehicles.objects.get(vehicle_id=id)
    obj.car_status='Available'
    obj.save()
    return HttpResponse("<script>alert('Available');window.location='/owner_manage_vehicles'</script>")


def owner_vehicle_notavailable(request,id):
    obj=vehicles.objects.get(vehicle_id=id)
    obj.car_status='Not Available'
    obj.save()
    return HttpResponse("<script>alert('Not Available');window.location='/owner_manage_vehicles'</script>")

def owner_delete_vehicle(request,id):
    obj=vehicles.objects.get(vehicle_id=id)
    obj.delete()
    return HttpResponse("<script>alert('Deleted');window.location='/owner_manage_vehicles'</script>")

def owner_update_vehicle(request,id):
    obj2=vehicles.objects.get(vehicle_id=id)
    if 'update' in request.POST:
        brand = request.POST['brand']
        model = request.POST['model']
        colour = request.POST['colour']
        seats = request.POST['seats']
        rent=request.POST['rent']
        description = request.POST['description']
        image = request.FILES['img1']
        fs = FileSystemStorage()
        f_nam =fs.save(image.name, image)
        
        obj2.brand=brand
        obj2.model=model
        obj2.colour=colour
        obj2.no_seat=seats
        obj2.per_day_rent=rent
        obj2.description=description
        obj2.vehicle_image=f_nam
        obj2.save()
        return HttpResponse("<script>alert('Updated');window.location='/owner_manage_vehicles'</script>")
        
    return render(request,'owner_manage_vehicles.html',{'obj2':obj2})

def upload_img(request,id):
    obj2=images.objects.filter(vehicle_id=id)
    if 'upload' in request.POST:
        print("fghjhgf")
        title=request.POST['title']
        image=request.FILES['img1']
        fs = FileSystemStorage()
        f_nam =fs.save(image.name, image)
        
        a=images(img=f_nam,title=title,vehicle_id=id)
        a.save()
        return HttpResponse("<script>alert('Added');window.location='/owner_manage_vehicles'</script>")
        
    return render(request,'upload_img.html',{'obj2':obj2})


def owner_delete_image(request,id):
    ob=images.objects.get(img_id=id)
    ob.delete()
    return HttpResponse("<script>alert('Deleted');window.location='/owner_manage_vehicles'</script>")


def owner_view_pofile(request):
    obj=owners.objects.filter(owner_id=request.session['oid'])
    return render(request,'owner_view_pofile.html',{'obj':obj})

def owner_manage_item(request):
    obj=items.objects.filter(owner_id=request.session['oid'])
    if 'upload' in request.POST:

        iname = request.POST['iname']
        quantity = request.POST['quantity']
        rent_per_item = request.POST['rent_per_item']
        description = request.POST['description']
        
        image=request.FILES['img1']
        
        fs = FileSystemStorage()
        f_nam =fs.save(image.name, image)
        
        a=items(item_name=iname,quantity=quantity,rent_per_item=rent_per_item,description=description,image=f_nam,owner_id=request.session['oid'])
        a.save()
        return HttpResponse("<script>alert('Added');window.location='/owner_manage_item'</script>")

    return render(request,'owner_manage_item.html',{'obj':obj})

def owner_delete_item(request,id):
    ob=items.objects.get(item_id=id)
    ob.delete()
    return HttpResponse("<script>alert('Deleted');window.location='/owner_manage_item'</script>")
   
def owner_update_item(request,id):
    obj2=items.objects.get(item_id=id)
    if 'update' in request.POST:
        iname = request.POST['iname']
        quantity = request.POST['quantity']
        rent_per_item = request.POST['rent_per_item']
        description = request.POST['description']
        
        image = request.FILES['img1']
        
        fs = FileSystemStorage()
        f_nam =fs.save(image.name, image)
        
        obj2.item_name=iname
        obj2.quantity=quantity
        obj2.rent_per_item=rent_per_item
        obj2.description=description
        obj2.image=f_nam
        obj2.save()
        return HttpResponse("<script>alert('Updated');window.location='/owner_manage_item'</script>")
      
    return render(request,'owner_manage_item.html',{'obj2':obj2})


def owner_view_booking(request):

    owner_id = request.session['oid']

    query = """
        SELECT
            car_rental_app_users.first_name || ' ' || car_rental_app_users.second_name AS username,
            car_rental_app_users.latitude,
            car_rental_app_users.logitu,
            from_date,
            from_time,
            to_date,
            to_time,
            returned_date,
            booking_status,
            booked_datetime,
            book_for_type,
            booking_id,
            book_for_id,
            user_id,
            balance_amount,
            driver
        FROM car_rental_app_booking
        INNER JOIN car_rental_app_vehicles ON car_rental_app_vehicles.vehicle_id = car_rental_app_booking.book_for_id
        INNER JOIN car_rental_app_users USING(user_id)
        WHERE owner_id = ? AND book_for_type = 'vehicle'
        UNION
        SELECT
            car_rental_app_users.first_name || ' ' || car_rental_app_users.second_name AS username,
            car_rental_app_users.latitude,
            car_rental_app_users.logitu,
            from_date,
            from_time,
            to_date,
            to_time,
            returned_date,
            booking_status,
            booked_datetime,
            book_for_type,
            booking_id,
            book_for_id,
            user_id,
            balance_amount,
            driver
        FROM car_rental_app_booking
        INNER JOIN car_rental_app_items ON car_rental_app_items.item_id = car_rental_app_booking.book_for_id
        INNER JOIN car_rental_app_users USING(user_id)
        WHERE owner_id = ? AND book_for_type = 'item'
    """

    with sqlite3.connect('db.sqlite3') as connection:
        cursor = connection.cursor()
        cursor.execute(query, (owner_id, owner_id))
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]


    print(results)
    return render(request, 'owner_view_booking.html', {'results': results})



def owner_view_user_details(request,id):
    obj=users.objects.filter(user_id=id)
    return render(request,'owner_view_user_details.html',{'obj':obj})

def owner_accept_booking(request,id):
    obj=booking.objects.get(booking_id=id)
    obj.booking_status='APPROVED'
    obj.save()
    
    
    send_mail('Car Rental','Your Booking Confirmed','anushkaprashanth22@gmail.com',[obj.user.email],fail_silently=False)

    return HttpResponse("<script>alert('APPROVED');window.location='/owner_view_booking'</script>")

def owner_reject_booking(request,id):
    obj=booking.objects.get(booking_id=id)
    obj.booking_status='REJECTED'
    obj.save()
    return HttpResponse("<script>alert('REJECTED');window.location='/owner_view_booking'</script>")

def owner_view_payments(request,id):
    obj=payment.objects.get(booking_id=id)
    if obj:
        adpay=obj.amount
        commission=(int(adpay)*5)/100
    return render(request,'owner_view_payments.html',{'obj':obj,'amt':commission})


def ready_to_deliver(request,id):
    obj=booking.objects.get(booking_id=id)
    obj.booking_status='Your Vehicle Is Ready To Deliver'
    obj.save()
    return HttpResponse("<script>alert('READY TO DELIVER');window.location='/owner_view_booking'</script>")
   
def delivered(request,id):
    obj=booking.objects.get(booking_id=id)
    obj.booking_status='Delivered'
    obj.save()
    return HttpResponse("<script>alert('DELIVERED');window.location='/owner_view_booking'</script>")

def owner_accept_return(request,fdate,tdate,rdate,bamt,bid,id,type):
    if type=='vehicle':
        obj=vehicles.objects.get(vehicle_id=bid)
        vrent=obj.per_day_rent
    elif type=='item':
        obj=items.objects.get(item_id=bid)
        vrent=obj.rent_per_item

    date_format = "%Y-%m-%d"
    c = datetime.strptime(fdate, date_format)
    a = datetime.strptime(tdate, date_format)
    b = datetime.strptime(rdate, date_format)
    delta = b - a
    delta1 =b - c
    delt=delta1.days
    print(delta1.days)
    print(delt)
    print(vrent)
    print(bamt)
    # brent_amount=(int(delta.days)*int(vrent))+int(bamt)
    brent_amt = abs(int(delta1.days) * int(vrent)) - abs(int(bamt))

    brent_amount=abs(brent_amt)

    print(brent_amount)
    
    if 'bal' in request.POST:
        ob=booking.objects.get(booking_id=id)
        ob.balance_amount=brent_amount
        ob.booking_status='Return Req Accepted'
        ob.save()
        return HttpResponse("<script>alert('RETURN REQUEST ACCEPTED');window.location='/owner_view_booking'</script>")
   
    return render(request,'owner_accept_return.html',{'fdate':fdate,'tdate':tdate,'rdate':rdate,'delta1':delt,'bal_amount':bamt,'per_day':vrent,'brent_amount':brent_amount})




def owner_view_feedback(request,id):
    obj=feedback.objects.filter(booking_id=id)
    return render(request,'owner_view_feedback.html',{'obj':obj})



def owner_view_user(request):
    obj=users.objects.all()
    return render(request,'owner_view_user.html',{'obj':obj})


def owner_chats(request,id):
    user_id=id
    request.session["user_id"]=user_id
    from_id=request.session['login_id']
    
    return render(request,"chat_owner.html",{"toid":id})

def owner_viewmsg(request):
    current_user_id = request.session['login_id']
    a=[]
    chat_messages = chatz.objects.filter(
        Q(from_id=current_user_id, to_id=request.session['user_id']) | Q(from_id=request.session['user_id'], to_id=current_user_id)
    )
    for i in chat_messages:
        a.append({"chat_id":i.chat_id,"from_id":i.from_id.login_id,"message":i.message,"date_time":i.date_time})
    p=users.objects.get(login_id=request.session["user_id"])
    print(chat_messages,p.first_name)
    first_name=p.first_name+" "+p.second_name
    print(a)
    b=p.picture
    return JsonResponse({'data':a,'first_name':first_name,'photo':"/static/profile.png"})
    


def owner_insert_chat(request,msg):
    print("wwwwwwwwwwww")
    import datetime
    ry=chatz(from_id_id=request.session['login_id'],to_id_id=request.session['user_id'],message=msg,date_time=datetime.datetime.now())
    ry.save()
    return JsonResponse({'status':"ok"})


#######################################################################################


def userhome(request):

    obj=booking.objects.filter(user_id=request.session['uid'],to_date=date.today())
    print(obj)
    for i in obj:
        print("##############",i)
        send_mail('Car Rental','Today is Your Car Return Date','anushkaprashanth22@gmail.com',[i.user.email],fail_silently=False)

    return render(request,'userhome.html')

def user_view_vehicles(request):
    obj = vehicles.objects.filter(car_status='Available')
    if 'filter' in request.POST:
        search_term = request.POST['search']
       
        obj = vehicles.objects.filter(
            Q(brand__contains=search_term) | Q(colour__contains=search_term) | Q(model__contains=search_term)
        )       
    else:
       obj=vehicles.objects.filter(car_status='Available')
    return render(request,'user_view_vehicles.html',{'obj':obj})

def user_view_owners(request,id):
    obj=owners.objects.filter(owner_id=id)
    return render(request,'user_view_owners.html',{'obj':obj})


def user_booking(request, id, amt):
    obj = booking.objects.filter(book_for_id=id)

    if 'ok' in request.POST:
        fdate = request.POST['fdate']
        ftime = request.POST['ftime']
        tdate = request.POST['tdate']
        ttime = request.POST['ttime']
        dri = request.POST['dri']

        # Convert date strings to datetime objects
        today = datetime.now().date()
        d1 = datetime.strptime(fdate, '%Y-%m-%d').date()
        d2 = datetime.strptime(tdate, '%Y-%m-%d').date()

        # Check if the selected dates are not in the past
        if d1 < today or d2 < today:
            return HttpResponse("<script>alert('Please select present or future dates only.');window.location='/user_view_vehicles'</script>")

        totaldate = abs((d2 - d1).days)
        totalrent = int(amt) * totaldate
        half_rent = totalrent / 2
        gh = int(half_rent)
        request.session['vamt'] = gh

        b = booking(
            book_for_id=id,
            book_for_type='vehicle',
            from_date=fdate,
            from_time=ftime,
            to_date=tdate,
            to_time=ttime,
            b_quantity='NA',
            driver=dri,
            balance_amount=gh,
            booking_status='pending',
            booked_datetime=datetime.now(),  # Use datetime.now() instead of date.today() to include time
            user_id=request.session['uid']
        )
        b.save()

        return HttpResponse("<script>alert('BOOKED');window.location='/user_view_vehicles'</script>")

    return render(request, 'user_booking.html', {'obj': obj, 'amt': amt, 'id': id})

def user_payment(request,type,amt,id1):
    if type=='vehicle':
        obj=vehicles.objects.get(vehicle_id=amt)
        # am=obj.per_day_rent
        am=request.session['vamt']
    elif type=='item':
        obj=items.objects.get(item_id=amt)
        # am=obj.rent_per_item
        am=request.session.get('iamt')
    a=booking.objects.get(booking_id=id1)
    jm=a.balance_amount
    if 'ok' in request.POST:
        
        b=booking.objects.get(booking_id=id1)
        b.booking_status='advance paid'
        b.save()
        aa=b.balance_amount
        a=payment(payment_type='advance payment',amount=aa,datetime=datetime.now(),booking_id=id1)
        a.save()
        return HttpResponse("<script>alert('PAID');window.location='/userhome'</script>")

    return render(request,'user_payment.html',{'amt':jm})

def user_return_vehicle(request,id,id1):
    obj=vehicles.objects.get(vehicle_id=id)
    ob=booking.objects.get(booking_id=id1)
    if 'pay' in request.POST:
        return redirect('user_return_payment', b_id=id)
    return render(request,'user_return_vehicle.html',{'obj':obj,'amt':ob,'id1':id1})

def user_return_payment(request,id):
    obj=payment.objects.get(booking_id=id)
    h=obj.amount
    
    ob=booking.objects.get(booking_id=id)
    j=ob.balance_amount
    full_amt=int(h)+int(j)
    
    if 'ok' in request.POST:
        a=booking.objects.get(booking_id=id)
        a.booking_status='returned'
        a.returned_date=datetime.now()
        a.save()
        obj.payment_type='FULLY PAID'
        obj.amount=full_amt
        obj.save()
        return HttpResponse("<script>alert('FULLY PAID');window.location='/user_view_vehicles'</script>")
   
    return render(request,'user_return_payment.html',{'amt':j})


def user_feedback(request,id):
    obj=feedback.objects.filter(booking_id=id)
    if 'send' in request.POST:
        rating=request.POST['rating']
        description=request.POST['feedback']
        
        a=feedback(rating=rating,description=description,datetime=datetime.now(),booking_id=id)
        a.save()
        return HttpResponse("<script>alert('FEEDBACK SENT');window.location='/user_view_vehicles'</script>")
       
    return render(request,'user_feedback.html',{'obj':obj})


def user_view_items(request):
    obj=items.objects.all()
    if 'filter' in request.POST:
        search_term = request.POST['search']
        # place = f'%{search_term}%'
        # print(place)
        obj = items.objects.filter(item_name__contains=search_term)
        # print(ob.query)  # Print the generated SQL query
        # print(obj)
    else:
       obj=items.objects.all() 
    return render(request,'user_view_items.html',{'obj':obj})


def user_booking_item(request, id, amt):
    obj = booking.objects.filter(book_for_id=id)

    if 'ok' in request.POST:
        fdate = request.POST['fdate']
        qty = request.POST['qty']
        ftime = request.POST['ftime']
        tdate = request.POST['tdate']
        ttime = request.POST['ttime']

        # Convert date strings to datetime objects
        today = datetime.now().date()
        d1 = datetime.strptime(fdate, '%Y-%m-%d').date()
        d2 = datetime.strptime(tdate, '%Y-%m-%d').date()

        # Check if the selected dates are not in the past
        if d1 < today or d2 < today:
            return HttpResponse("<script>alert('Please select present or future dates only.');window.location='/user_booking_item'</script>")

        totaldate = abs((d2 - d1).days)
        totalrent = (int(amt) * int(qty)) * totaldate
        half_rent = totalrent / 2
        gh = int(half_rent)

        b = booking(
            book_for_id=id,
            book_for_type='item',
            b_quantity=qty,
            from_date=fdate,
            from_time=ftime,
            to_date=tdate,
            to_time=ttime,
            balance_amount=gh,
            booking_status='pending',
            booked_datetime=datetime.now(),  
            user_id=request.session['uid']
        )
        b.save()
        return HttpResponse("<script>alert('BOOKED');window.location='/user_view_items'</script>")
   
    return render(request, 'user_booking_item.html')

def user_return_req(request,id,id1):
    obj=booking.objects.get(booking_id=id1)
    obj.booking_status='Return Req'
    obj.returned_date=date.today()
    obj.save()
    return HttpResponse("<script>alert('RETURN REQUEST');window.location='/user_vehicle_booking'</script>")



def user_vehicle_booking(request):
    obj=booking.objects.filter(user_id=request.session['uid'],book_for_type='vehicle')
    print(obj)
    return render(request,'user_vehicle_booking.html',{'obj':obj})


def user_item_booking(request):
    obj=booking.objects.filter(user_id=request.session['uid'],book_for_type='item')
    print(obj)
    return render(request,'user_item_booking.html',{'obj':obj})

def user_chat(request):
    obj=owners.objects.all()
    return render(request,'user_chat.html',{'obj':obj})




def user_vehicle_details(request,id):
    obj=vehicles.objects.filter(vehicle_id=id)
    return render(request,'user_vehicle_details.html',{'obj':obj})

def user_item_details(request,id):
    obj=items.objects.filter(item_id=id)
    return render(request,'user_item_details.html',{'obj':obj})






def user_chats(request,id):
    owner_id=id
    request.session["owner_id"]=owner_id
    from_id=request.session['login_id']
    print("hiiiiiiiiii")
    return render(request,"chat.html",{"toid":id})

def user_viewmsg(request):
    current_user_id = request.session['login_id']
    a=[]
    chat_messages = chatz.objects.filter(
        Q(from_id=current_user_id, to_id=request.session['owner_id']) | Q(from_id=request.session['owner_id'], to_id=current_user_id)
    )
    for i in chat_messages:
        a.append({"chat_id":i.chat_id,"from_id":i.from_id.login_id,"message":i.message,"date_time":i.date_time})
    p=owners.objects.get(login_id=request.session["owner_id"])
    print(chat_messages,p.first_name)
    first_name=p.first_name+" "+p.second_name
    print(a)
    return JsonResponse({'data':a,'first_name':first_name,'photo':"/static/profile.png"})
    


def user_insert_chat(request,msg):
    print("wwwwwwwwwwww")
    import datetime
    ry=chatz(from_id_id=request.session['login_id'],to_id_id=request.session['owner_id'],message=msg,date_time=datetime.datetime.now())
    ry.save()
    return JsonResponse({'status':"ok"})