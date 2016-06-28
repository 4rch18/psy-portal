from django.shortcuts import render
from django.core.mail.backends import console
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime



import json


from .models import User, Query, OfficeHour, TimeSlot, Appointment


def index(request):
    context={}
    return render(request, 'portal/index.html', context)


def home(request):
    flag=request.POST.get('login_flag')
    
    if(flag=='signup'):
        uname = request.POST.get('username')
        pword1 = request.POST.get('password1')
        pword2 = request.POST.get('password2')
        
        tempUser=User.objects.filter(username=uname)
        if tempUser:                                            ########### use tempUser[0]
            context={
                'err': 'Username is not valid. Please try a different one',
            }
            return render(request, 'portal/error.html', context)

        if (pword1 == pword2):
            allAdmins = User.objects.filter(is_admin=True)
            currentClient = User.objects.create(username=uname, password=pword1, is_online=True)
            appointment_time=''
            context={
                'client':currentClient,
                'all':allAdmins,
                'message':'you just made a new account, get excited',

            }
            return render(request, 'portal/home.html', context)

        else:
            context={
                'err': 'Your passwords didn\'t match',
            }
            return render(request, 'portal/error.html', context)
    
    elif(flag=='login'):
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        
        tempUser = User.objects.filter(username=uname)

        if not tempUser:
            return render(request, 'portal/error.html', {'err': 'Username doesn\'t exist'})
        
        elif tempUser[0].password != pword:
            return render(request, 'portal/error.html', {'err': 'Incorrect password'})
        
        elif tempUser[0].is_admin:
            currentAdmin=tempUser[0]
            User.objects.filter(username=currentAdmin.username).update(is_online=True)
            officeHours= OfficeHour.objects.filter(admin=currentAdmin)
            allClients = User.objects.filter(is_admin=False)
            context={
                'admin':currentAdmin,
                'all':allClients,
                'office_hours':officeHours,

            }
            return render(request, 'portal/admin_home.html', context)

        elif not tempUser[0].is_admin :
            currentClient=tempUser[0]
            User.objects.filter(username=currentClient.username).update(is_online=True)
            appointment_time='';
            allAdmins = User.objects.filter(is_admin=True)
            context={
                'client':currentClient,
                'all':allAdmins,
                'message':'you are logged in',

            }
            return render(request, 'portal/home.html', context)

    elif(flag=='redirect'):
        clientID=request.POST.get('clientID')
        adminID=request.POST.get('adminID')
        currentClient=User.objects.get(pk=clientID)
        
        allAdmins= User.objects.filter(is_admin=True)
        slot_booked=request.POST.get('slot_time')                                                       #0

        currentAdmin=User.objects.get(pk=adminID)                                                       #1
        office_hours=OfficeHour.objects.filter(admin=currentAdmin)                                      #2
        time_slot=TimeSlot.objects.filter(display=slot_booked,office_hours=office_hours)                #3
        #time_slot (filter) will give a list

        TimeSlot.objects.filter(display=time_slot[0].display,office_hours=office_hours).update(is_booked=True)
        Appointment.objects.create(client=currentClient, admin=currentAdmin, slot= time_slot[0])        #4

        context={
            'client':currentClient,
            'all':allAdmins,
            'message':'you are logged in',

        }
        return render(request, 'portal/home.html', context)


def logout(request, userID):
    currentUser = User.objects.get(pk=userID)
    currentUser.is_online = False
    User.objects.filter(pk=userID).update(is_online=False)
    context = {
        'user': currentUser
    }
    return render(request, 'portal/logout.html', context)


def addHours(request, adminID):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    
    currentAdmin=User.objects.get(pk=adminID)
    hours=OfficeHour.objects.create(admin=currentAdmin,start_time=start_time,end_time=end_time,display=start_time+' to '+end_time)
    start_hour=''
    start_min=''
    start_m=''
    end_hour=''
    end_min=''
    end_m=''
    
    
    for x in range(8):
        if x < 2:
            start_hour+=start_time[x]
            end_hour+=end_time[x]
        elif x>2 and x<5:
            start_min+=start_time[x]
            end_min+=end_time[x]
        elif x>5:
            start_m+=start_time[x]
            end_m+=end_time[x]

    createTimeSlots(currentAdmin,hours,start_hour,start_min,start_m,end_hour,end_min,end_m)

    allClients = User.objects.filter(is_admin=False)
    office_hours= OfficeHour.objects.filter(admin=currentAdmin)
    context={
            'admin':currentAdmin,
            'all':allClients,
            'office_hours':office_hours,
        }
    return render(request, 'portal/admin_home.html', context)


def createTimeSlots(admin_object,office_hours,a,b,c,d,e,f):
    a1=int(a)
    b1=int(b)
    d1=int(d)
    e1=int(e)
    
    while a1 < d1 or (c=='AM' and f=='PM'):
        a2=str(a1)
        b2=str(b1)
        if 8<a1 and a1<13:
            c2='AM'
        else:
            c2='PM'
        if b1==00:
            b1=30
            d2=str(a1)
            e2=str(b1)
            if 8<a1 and a1<13:
                f2='AM'
            else:
                f2='PM' 
        else:
            if a1==12:
                a1=1
            else:
                a1+=1
            b1=00
            d2=str(a1)
            e2=str(b1)
            if 8<a1 and a1<13:
                f2='AM'
            else:
                f2='PM'

        if(b2=='0'):
            b2='00'
        if(e2=='0'):
            e2='00'
        if(a2=='12'):
            c2='PM'
        if(d2=='12'):
            f2='PM'

        regex=a2+':'+b2+' '+c2+' - '+d2+':'+e2+' '+f2
        temp=TimeSlot.objects.create(office_hours=office_hours,display=regex)
        if 8<a1 and a1<13:
            c='AM'
        else:
            c='PM'
        if 8<d1 and d1<13:
            f='AM'
        else:
            f='PM'
    

    if a1==d1:
        if e1==30:
            a2=str(a1)
            b2=str(b1)
            d2=str(a1)
            e2=str(e1)
            if 8<a1 and a1<13:
                c2='AM'
                f2='AM'
            else:
                c2='PM'
                f2='PM'

            if(b2=='0'):
                b2='00'
            if(e2=='0'):
                e2='00'
            if(a2=='12'):
                c2='PM'
            if(d2=='12'):
                f2='PM'

            regex=a2+':'+b2+' '+c2+' - '+d2+':'+e2+' '+f2
            temp=TimeSlot.objects.create(office_hours=office_hours,display=regex)


def chat(request, clientID, adminID):
    currentClient=User.objects.get(pk=clientID)
    currentAdmin=User.objects.get(pk=adminID)
    new_msg=request.POST.get('new_msg')
    date=datetime.now()
    if new_msg is not None and new_msg != '':
        tempQuery = Query.objects.create(client=currentClient, admin=currentAdmin, pub_date=date, text=new_msg, by_admin=False)
        User.objects.filter(pk=clientID).update(sent_new_text=True)
        return HttpResponseRedirect(reverse('portal:chat', args=(clientID,adminID,)))
    
    allQueries=Query.objects.filter(admin_id=adminID,client_id=clientID)
    context={
        'all':allQueries,
        'client':currentClient,
        'admin':currentAdmin,
        'isAdmin': False,
    }
    return render(request, 'portal/chat.html', context)

def admin_chat(request, clientID, adminID):
    currentClient=User.objects.get(pk=clientID)
    currentAdmin=User.objects.get(pk=adminID)
    new_msg=request.POST.get('new_msg')
    date=datetime.now()
    if new_msg is not None and new_msg != '':
        tempQuery = Query.objects.create(client=currentClient, admin=currentAdmin, pub_date=date, text=new_msg, by_admin=True)
        User.objects.filter(pk=adminID).update(sent_new_text=True)
        return HttpResponseRedirect(reverse('portal:admin_chat', args=(clientID,adminID,)))
    
    allQueries=Query.objects.filter(admin_id=adminID,client_id=clientID)
    context={
        'all':allQueries,
        'client':currentClient,
        'admin':currentAdmin,
        'isAdmin': True,
    }
    return render(request, 'portal/admin_chat.html', context)


def book(request, clientID, adminID):
    currentAdmin=User.objects.get(pk=adminID)
    currentClient=User.objects.get(pk=clientID)
    office_hours=OfficeHour.objects.filter(admin=currentAdmin)
    time_slots=TimeSlot.objects.filter(office_hours=office_hours)
    context={
        'client':currentClient,
        'admin':currentAdmin,
        'hours':office_hours,
        'slots':time_slots,
    }
    return render(request, 'portal/book.html', context)



#########################################################################################################

# APIs

def deleteHours(request, adminID, officeHoursID):
    currentOfficeHours=OfficeHour.objects.get(pk=officeHoursID)
    currentOfficeHours.delete()
    data={'type':'1','sub-type':'blank'}
    return HttpResponse(json.dumps(data))


