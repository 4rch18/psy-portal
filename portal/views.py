from django.shortcuts import render
from django.core.mail.backends import console
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User

import json


from .models import MyUser, Query, OfficeHour, TimeSlot, Appointment


def index(request):
    context={}
    return render(request, 'portal/index.html', context)


def home(request, clientID_from_url=None):
    
    if clientID_from_url is None :
        flag=request.POST.get('login_flag')
        

        if(flag=='signup'):
            

            uname = request.POST.get('username')
            pword1 = request.POST.get('password1')
            pword2 = request.POST.get('password2')
            

            

            tempUser=MyUser.objects.filter(username=uname)
            if tempUser:                                            ########### use tempUser[0]
                context={
                    'err': 'Username is not valid. Please try a different one',
                }
                return render(request, 'portal/error.html', context)

            if (pword1 == pword2):
                allAdmins = MyUser.objects.filter(is_admin=True)
                currentClient = MyUser.objects.create(username=uname, password=pword1, is_online=True)
                
                request.session['user_id'] = currentClient.id

                allAppointments=Appointment.objects.filter(client=currentClient)

                user = User.objects.create_user(uname, None, pword1)

                context={
                    'client':currentClient,
                    'all':allAdmins,
                    'message':'you just made a new account, get excited',
                    'allAppointments': allAppointments,
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
            
            tempUser = MyUser.objects.filter(username=uname)


            user = authenticate(username=uname, password=pword)

            if user is None:
                if not tempUser:
                    return render(request, 'portal/error.html', {'err': 'Username doesn\'t exist'})
                
                elif tempUser[0].password != pword:
                    return render(request, 'portal/error.html', {'err': 'Incorrect password'})
            
            elif user is not None:
                
                request.session['user_id'] = tempUser[0].id
                
                if tempUser[0].is_admin:
                    currentAdmin=tempUser[0]
                    MyUser.objects.filter(username=currentAdmin.username).update(is_online=True)
                    officeHours= OfficeHour.objects.filter(admin=currentAdmin)
                    allClients = MyUser.objects.filter(is_admin=False)
                    allAppointments=Appointment.objects.filter(admin=currentAdmin)

                    context={
                        'admin':currentAdmin,
                        'all':allClients,
                        'office_hours':officeHours,
                        'allAppointments':allAppointments,

                    }
                    return render(request, 'portal/admin_home.html', context)

                elif not tempUser[0].is_admin :
                    currentClient=tempUser[0]
                    MyUser.objects.filter(username=currentClient.username).update(is_online=True)
                    appointment_time='';
                    allAdmins = MyUser.objects.filter(is_admin=True)
                    allAppointments=Appointment.objects.filter(client=currentClient)
                    context={
                        'a':request.session['user_id'],
                        'b':tempUser[0].id,
                        'client':currentClient,
                        'all':allAdmins,
                        'message':'you are logged in',
                        'allAppointments': allAppointments,

                    }
                    return render(request, 'portal/home.html', context)

        elif(flag=='redirect'):
            try:
                t=request.session['user_id']
            except KeyError:
                context1={
                    'err':'Please login to access the portal',
                    'link':"portal:index",
                }
                return render(request, 'portal/error.html', context1)
            clientID=request.POST.get('clientID')
            if str(request.session['user_id']) == str(clientID):

                adminID=request.POST.get('adminID')
                slot_display=request.POST.get('slot_time')
                currentClient=MyUser.objects.get(pk=clientID)
                currentAdmin=MyUser.objects.get(pk=adminID)

                office_hours=OfficeHour.objects.filter(admin=currentAdmin)
                
                if office_hours:
                    TimeSlot.objects.filter(display = slot_display, office_hours = office_hours).update(is_free = False, client = currentClient)
                    
                    tempTimeSlot=TimeSlot.objects.filter(display = slot_display, office_hours = office_hours)

                    Appointment.objects.create(client=currentClient, admin=currentAdmin, slot= tempTimeSlot[0]) 
                    MyUser.objects.filter(pk=clientID).update(status_appointment_changed=True)
                    MyUser.objects.filter(pk=adminID).update(status_appointment_changed=True)
                return HttpResponseRedirect(reverse('portal:home', args=(clientID,)))
            else:
                context={
                    'err':'Invalid authorization'
                }
                return render(request, 'portal/error.html', context)
            

    else:
        try:
            t=request.session['user_id']
        except KeyError:
            context1={
                'err':'Please login to access the portal',
                'link':"portal:index",
            }
            return render(request, 'portal/error.html', context1)

        clientID=clientID_from_url
        if str(request.session['user_id']) == str(clientID):
            currentClient=MyUser.objects.get(pk=clientID)
            
            allAdmins= MyUser.objects.filter(is_admin=True)                                                             
            allAppointments=Appointment.objects.filter(client=currentClient)     

            context={
                'client':currentClient,
                'all':allAdmins,
                'message':'you are logged in',
                'allAppointments':allAppointments,
            }
            return render(request, 'portal/home.html', context)
        else:
            context={
                'err':'Invalid authorization'
            }
            return render(request, 'portal/error.html', context)





def addHours(request, adminID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(adminID):
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        currentAdmin=MyUser.objects.get(pk=adminID)
        if start_time is not None and start_time != '' and end_time is not None and end_time != '' :
        
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
            return HttpResponseRedirect(reverse('portal:addHOurs', args=(adminID,)))

        allClients = MyUser.objects.filter(is_admin=False)
        office_hours= OfficeHour.objects.filter(admin=currentAdmin)
        allAppointments=Appointment.objects.filter(admin=currentAdmin)
        context={
                'admin':currentAdmin,
                'all':allClients,
                'office_hours':office_hours,
                'allAppointments':allAppointments,
            }
        return render(request, 'portal/admin_home.html', context)
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)


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
        temp=TimeSlot.objects.create(office_hours = office_hours, display = regex)
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


def acceptRequest(request, clientID, adminID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(adminID):
        flag=request.POST.get('accept_flag')
        

        currentAdmin=MyUser.objects.get(pk=adminID)
        allClients = MyUser.objects.filter(is_admin=False)
        office_hours= OfficeHour.objects.filter(admin=currentAdmin)
        allAppointments=Appointment.objects.filter(admin=currentAdmin)
        

        if flag=='accept':
            if office_hours:
                currentClient=MyUser.objects.get(pk=clientID)
                TimeSlot.objects.filter(client = currentClient, office_hours=office_hours).update(is_free = False)
                Appointment.objects.filter(admin = currentAdmin, client = currentClient).update(status = 'booked')
                MyUser.objects.filter(pk=clientID).update(status_appointment_changed=True)
            return HttpResponseRedirect(reverse('portal:acceptRequest', args=(clientID,adminID)))
        
        elif flag=='decline':
            if office_hours:
                currentClient=MyUser.objects.get(pk=clientID)
                TimeSlot.objects.filter(client = currentClient, office_hours=office_hours).update(is_free = True)   #dont free if double request
                Appointment.objects.filter(admin = currentAdmin, client = currentClient).delete()
                MyUser.objects.filter(pk=clientID).update(status_appointment_changed=True)
            return HttpResponseRedirect(reverse('portal:acceptRequest', args=(clientID,adminID)))
        
        context={
            'admin':currentAdmin,
            'all':allClients,
            'office_hours':office_hours,
            'allAppointments':allAppointments,
        }
        return render(request, 'portal/admin_home.html', context)
    
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)  


def chat(request, clientID, adminID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(clientID):
        currentClient=MyUser.objects.get(pk=clientID)
        currentAdmin=MyUser.objects.get(pk=adminID)
        new_msg=request.POST.get('new_msg')
        date=datetime.now()
        if new_msg is not None and new_msg != '':
            tempQuery = Query.objects.create(client=currentClient, admin=currentAdmin, pub_date=date, text=new_msg, by_admin=False)
            MyUser.objects.filter(pk=clientID).update(sent_new_text=True)
            return HttpResponseRedirect(reverse('portal:chat', args=(clientID,adminID,)))
        
        allQueries=Query.objects.filter(admin_id=adminID,client_id=clientID)
        context={
            'all':allQueries,
            'client':currentClient,
            'admin':currentAdmin,
            'isAdmin': False,
        }
        return render(request, 'portal/p_chat.html', context)
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)


def admin_chat(request, clientID, adminID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(adminID):
        currentClient=MyUser.objects.get(pk=clientID)
        currentAdmin=MyUser.objects.get(pk=adminID)
        new_msg=request.POST.get('new_msg')
        date=datetime.now()
        if new_msg is not None and new_msg != '':
            tempQuery = Query.objects.create(client=currentClient, admin=currentAdmin, pub_date=date, text=new_msg, by_admin=True)
            MyUser.objects.filter(pk=adminID).update(sent_new_text=True)
            return HttpResponseRedirect(reverse('portal:admin_chat', args=(clientID,adminID,)))
        
        allQueries=Query.objects.filter(admin_id=adminID,client_id=clientID)
        context={
            'all':allQueries,
            'client':currentClient,
            'admin':currentAdmin,
            'isAdmin': True,
        }
        return render(request, 'portal/p_chat.html', context)
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)


def book(request, clientID, adminID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(clientID):
        currentAdmin=MyUser.objects.get(pk=adminID)
        currentClient=MyUser.objects.get(pk=clientID)
        office_hours=OfficeHour.objects.filter(admin=currentAdmin)
        time_slots=TimeSlot.objects.filter(office_hours=office_hours)

        #to check if already booked
        tempAppointment=Appointment.objects.filter(client=currentClient,admin=currentAdmin)

        if tempAppointment :
            appointment_with=True
            currentAppointment=tempAppointment[0]
        else:
            appointment_with=False
            currentAppointment=None
        context={
            'client':currentClient,
            'admin':currentAdmin,
            # 'hours':office_hours,
            'slots':time_slots,
            'flag':appointment_with,
            'appointment_at':currentAppointment,
        }
        return render(request, 'portal/book.html', context)
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)


def deleteHours(request, adminID, officeHoursID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(adminID):
        OfficeHour.objects.get(pk=officeHoursID).delete()
        data={'type':'1','sub-type':'blank'}
        return HttpResponse(json.dumps(data))
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)


def call(request, clientID, adminID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(clientID):
        currentClient=MyUser.objects.get(pk=clientID)
        currentAdmin=MyUser.objects.get(pk=adminID)
        context={
            'client':currentClient,
            'admin':currentAdmin,
        }
        return render(request, 'portal/call.html', context)
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)


def admin_call(request, clientID, adminID):
    try:
        t=request.session['user_id']
    except KeyError:
        context1={
            'err':'Please login to access the portal',
            'link':"portal:index",
        }
        return render(request, 'portal/error.html', context1)
    if str(request.session['user_id']) == str(adminID):
        currentClient=MyUser.objects.get(pk=clientID)
        currentAdmin=MyUser.objects.get(pk=adminID)
        context={
            'client':currentClient,
            'admin':currentAdmin,
        }
        return render(request, 'portal/admin_call.html', context)
    else:
        context={
            'err':'Invalid authorization'
        }
        return render(request, 'portal/error.html', context)

def my_logout(request):
    context={}
    try:
        del request.session['user_id']
    except KeyError:
        pass
    
    return render(request, 'portal/index.html',context)


def getData(request, clientID, adminID):

    
    temp2=MyUser.objects.get(pk=adminID)
    
    if(temp2.sent_new_text == False):
        data={'type':'1','sub-type':'blank'}
    else:
        MyUser.objects.filter(pk=adminID).update(sent_new_text=False)
        data={'type':'2','sub-type':'blank'}

    return HttpResponse(json.dumps(data))


def admin_getData(request, clientID, adminID):
    temp=MyUser.objects.get(pk=clientID)

    if(temp.sent_new_text == False):
        data={'type':'1','sub-type':'blank'}
    else:
        MyUser.objects.filter(pk=clientID).update(sent_new_text=False)
        data={'type':'2','sub-type':'blank'}

    return HttpResponse(json.dumps(data))


def polling_home(request, clientID):
    currentClient=MyUser.objects.get(pk=clientID)
    if currentClient.status_appointment_changed == False:
        data={'type':'1','sub-type':'blank'}
    else:
        MyUser.objects.filter(pk=clientID).update(status_appointment_changed=False)
        data={'type':'2','sub-type':'blank'}

    return HttpResponse(json.dumps(data))


def admin_polling_home(request, adminID):
    currentAdmin=MyUser.objects.get(pk=adminID)
    if currentAdmin.status_appointment_changed == False:
        data={'type':'1','sub-type':'blank'}
    else:
        MyUser.objects.filter(pk=adminID).update(status_appointment_changed=False)
        data={'type':'2','sub-type':'blank'}

    return HttpResponse(json.dumps(data))