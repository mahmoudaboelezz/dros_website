from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from sitemessage.shortcuts import schedule_email
from .models import Newsletter,QRCode
from .forms import NewsletterForm
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib import messages
from accounts.models import User
# def send_mail_view(request):
#     ...

#     # Suppose `user_model` is a recipient Django User model instance.
#     user1_model = ...

#     # We pass `request.user` into `sender` to keep track of senders.
#     schedule_email('Message from sitemessage.', [user1_model, 'user2@host.com'], sender=request.user)

#     ...
    
def send_mail_view(request):
    form = NewsletterForm(request.POST or None)
    if form.is_valid():
        form.save()
        if request.user.is_authenticated:
            form.instance.user = request.user
            form.save()
        schedule_email('Hello to you!', [form.cleaned_data['email']], sender=request.user)
    context = {
        'form': form
    }
    return render(request, 'newsletter.html', context)

@require_POST
def send_mail(request):
    print(request.POST)
    
    # email = request.POST.get('news_email')
    # interstes = request.POST.getlist('states[]')
    # print(interstes)
    
    # if request.user.is_authenticated:
    #     name = request.user.username
    # else:
    #     name = request.POST.get('news_name')
        
    # categories = []
    # for i in interstes:
    #     category = CourseCategory.objects.get(ar_category=i)
    #     if category:
    #         categories.append(category)
            
    
    # if Newsletter.objects.filter(email=email).exists():
    #     msg = 'You are already subscribed to our newsletter'
    # else:
    #     subs = Newsletter.objects.create(name=name, email=email)
    #     if request.user.is_authenticated:
    #         subs.user = request.user
    #         subs.save()
    #     for i in categories:
    #         subs.intersts.add(i)
    #     subs.save()
    #     if request.affiliate.exists():
    #         subs.affiliate = request.affiliate
    #         print(request.affiliate)
    #         subs.save()
    #     msg = f'Wonderful {name}, You have been subscribed successfully!'
    #     schedule_email('Hello to you!', [email], sender=User.objects.get(username='admin'))
        
    # return JsonResponse({'status': 'ok', 'msg': msg})


# class NewsletterListView(ListView):
#     model = Newsletter
#     template_name = 'newsletter.html'
#     ordering = ['-id']
#     paginate_by = 10
#     def get_queryset(self):
#         all = Newsletter.objects.all()
#         return all
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['all'] = self.get_queryset()
#         return context

def qr_code(request,verfication_code):
    if QRCode.objects.filter(verfication_code=verfication_code).exists():
        qr = QRCode.objects.get(verfication_code=verfication_code)
        # if user is staff or superuser 
        context = {}
        if request.user.is_staff or request.user.is_superuser:
            print('staff')
            print(qr.attend)
            if qr.attend == False:   
                qr.attend = True
                qr.save()
                messages.success(request, 'تم تسجيل الحضور بنجاح')
            else:
                messages.error(request, 'هذا الحضور مسجل مسبقا')
        context = {
            'qr':qr
        }
        return render(request,'qr_code.html',context)
    
def verify_url(request):
    if request.method == 'POST':
        verfication_code = request.POST.get('verfication_code')
        if QRCode.objects.filter(verfication_code=verfication_code).exists():
            qr = QRCode.objects.get(verfication_code=verfication_code)
            return render(request,'qr_code.html',{'qr':qr})