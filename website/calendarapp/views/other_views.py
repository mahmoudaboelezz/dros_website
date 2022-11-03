# cal/views.py

from django.conf import settings
from django.shortcuts import render, redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from sitemessage.shortcuts import schedule_email, recipients, schedule_messages
from django.contrib import messages
from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm
from newsletter.models import Newsletter,QRCode
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core import mail
from django.utils.html import strip_tags

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        # html_cal = html_cal.replace("mon","الاثنين")
        # html_cal = html_cal.replace("tue","الثلاثاء")
        # html_cal = html_cal.replace("wed","الاربعاء")
        # html_cal = html_cal.replace("thu","الخميس")
        # html_cal = html_cal.replace("fri","الجمعة")
        # html_cal = html_cal.replace("sat","السبت")
        # html_cal = html_cal.replace("sun","الاحد")
        html_cal = html_cal.replace("Mon","الاثنين")
        html_cal = html_cal.replace("Tue","الثلاثاء")
        html_cal = html_cal.replace("Wed","الاربعاء")
        html_cal = html_cal.replace("Thu","الخميس")
        html_cal = html_cal.replace("Fri","الجمعة")
        html_cal = html_cal.replace("Sat","السبت")
        html_cal = html_cal.replace("Sun","الاحد")
        print(html_cal)
     
        
        
        
        context["calendar"] = mark_safe(_(html_cal))
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context
    
    


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='accounts:signin')
def create_event(request):
    # only for admin
    if request.user.is_superuser:
        form = EventForm(request.POST or None)
        if request.POST and form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            Event.objects.get_or_create(
                user=request.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
            )
            return HttpResponseRedirect(reverse("calendarapp:calendar"))
        return render(request, "event.html", {"form": form})
    else:
        return redirect("calendarapp:calendar")

def delete_event(request):
    # print csrf_token
    if request.method == "POST":
        print(f'{request.POST.get("title")} title')
        event = Event.objects.get(title=request.POST.get("title"))
        event.delete()
        # event = Event.objects.get(title=request.POST.get("title"))
        # event.delete()
    return redirect("calendarapp:calendar")


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"
    # only for admin
    @login_required
    @user_passes_test(lambda u: u.is_superuser, login_url='accounts:signin')
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Event.objects.all()
        else:
            return Event.objects.none()


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='accounts:signin')
def add_eventmember(request, event_id):
    # only for admin
    if request.user.is_superuser:
        forms = AddMemberForm()
        if request.method == "POST":
            forms = AddMemberForm(request.POST)
            if forms.is_valid():
                member = EventMember.objects.filter(event=event_id)
                event = Event.objects.get(id=event_id)
                if member.count() <= 9:
                    user = forms.cleaned_data["user"]
                    EventMember.objects.create(event=event, user=user)
                    
                    return redirect("calendarapp:calendar")
                else:
                    print("--------------User limit exceed!-----------------")
        context = {"form": forms}
        return render(request, "add_member.html", context)
    else:
        return redirect("calendarapp:calendars")

def qr_generate(event, user):
    import qrcode
    import qrcode.image.svg
    from io import BytesIO
    factory = qrcode.image.svg.SvgPathImage
    # convert to base64
    qr_saved = QRCode.objects.create(event=event, user=user)
    verficaton_code = qr_saved.verfication_code
    print(verficaton_code)
    # data = f'{event} {user} {verficaton_code}'
    # img = qrcode.make(data, image_factory=factory,)
    # img = qrcode.make(data)
    # img.save(f'media/qr_codes/{event}-{user}.png')
    # qr_saved.image = f'qr_codes/{event}-{user}.png'
    # buffer = BytesIO()
    # img.save(buffer)
    # qr_saved.qr_code = buffer.getvalue().decode()
    # qr_saved.save()
    return qr_saved
# from newsletter.sitemessages import MyMessage
from  sitemessage.messages.email import EmailHtmlMessage
def member_join(request, event_id):
    # if already joined
    event = Event.objects.get(id=event_id)
    if EventMember.objects.filter(event=event_id, user=request.user).exists():
        messages.warning(request, "لقد قمت بالتسجيل مسبقاً في هذه الدورة")
        
        # return to event details page
        return redirect(event.get_absolute_url())
    print("--------------User joined!-----------------")
    code = qr_generate(event, request.user)
    v_c = code.verfication_code
    c_l = code.get_absolute_url()
    print(c_l)
    c_qr = code.image.url
    print(c_qr)
    email = request.user.email
    context = {
        "event": event,
        "user": request.user,
        "verfication_code": v_c,
        "code_link": c_l,
        "qr_code": c_qr,
        "name" : request.user.username,
    }
    subject = 'شكرا للأشتراك'
    html_message = render_to_string('sitemessages/messages/my_message.html', context)
    plain_message = strip_tags(html_message)
    from_email = f'{settings.EMAIL_SENDGRID}'
    to = f'{email}'       
    mail.send_mail(subject, plain_message, from_email, [to,], html_message=html_message)
    # schedule_messages(
    #     # EmailHtmlMessage("تم الإشتراك بنجاح" ,f'<html><head></head><body>{event} \n {code.qr_code} \n <b></b></body></html>',),recipients('smtp', email),
        
    #     EmailHtmlMessage("تم الإشتراك بنجاح",{'event':f'{event}','user':f'{request.user}','code':f'{code}','c_l':f'{c_l}','v_c':f'{v_c}','c_qr':f'{c_qr}',}
    #                      , 'sitemessages/messages/my_message.html'),recipients('smtp', email),
    #     # EmailHtmlMessage("تم الإشتراك بنجاح" ,mail),recipients('smtp', email),
    #     sender=User.objects.get(id=1)
    # )
    

    import os
    os.system('python3 manage.py sitemessage_send_scheduled')
    EventMember.objects.create(event=event, user=request.user)
    Newsletter.objects.create(user=request.user, email=request.user.email, name=request.user.username)
    # schedule_email(message=f'تم تسجيلك في دورة {event.title} بنجاح', email=email,sender=User.objects.get(id=1))
    messages.success(request, " تم الإشتراك بنجاح يرجي تفقد البريد الإلكتروني ويمكن أن يكون في البريد الغير مرغوب فيه أو الرسائل الأعلانية")
    return redirect(event.get_absolute_url())
    # generate qr code
    
    return redirect("calendarapp:calendar")
    # schedule_messages(MyMessage(context={"event": f'{event}', "user": f'{request.user}'}), recipients('smtp', email),sender=User.objects.get(id=1))
    # schedule_messages(MyMessage(context={"event": f'{event}', "user": f'{request.user}'}), recipients('smtp', email),sender=User.objects.get(id=1))
    # schedule_email(f'تم تسجيلك في دورة {event} بنجاح', [email], sender=User.objects.get(id=1))
class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")
    # only for admin
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EventMember.objects.all()
        else:
            return EventMember.objects.none()


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm
    # only for admin

    def get(self, request, *args, **kwargs):
        # only for admin
        if request.user.is_superuser:
            forms = self.form_class()
            events = Event.objects.get_all_events(user=request.user)
            events_month = Event.objects.get_running_events(user=request.user)
            event_list = []
            # start: '2020-09-16T16:00:00'
            for event in events:
                event_list.append(
                    {
                        "title": event.title,
                        "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                    }
                )
            context = {"form": forms, "events": event_list,
                    "events_month": events_month}
            return render(request, self.template_name, context)
        else:
            return redirect("calendarapp:calendars")

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
