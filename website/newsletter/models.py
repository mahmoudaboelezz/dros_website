from asyncio import format_helpers
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from calendarapp.models import Event
from accounts.models import User
from django.utils.safestring import mark_safe
import uuid
# Create your models here.
class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100, verbose_name=_('Name'),null=True,blank=True)
    email = models.EmailField(verbose_name=_('Email'))

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.user is not None:
            self.name = self.user.username
            self.email = self.user.email
        super(Newsletter, self).save(*args, **kwargs)
        
        
class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True,blank=True)
    # svg of qr code
    qr_code = models.TextField(null=True, blank=True)
    verfication_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='qrcodes', null=True, blank=True)
    attend = models.BooleanField(default=False)
    # qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    class Meta:
        verbose_name = _('QR Code')
        verbose_name_plural = _('QR Codes')
        unique_together = ('user', 'event')
        
    
    @property
    def show_qr_code(self):
        return self.qr_code
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('newsletter:qr_code', kwargs={'verfication_code': self.verfication_code})
    
    def get_veriy_url(self):
        return redirect('newsletter:verify')
    
    @property
    def show_qr_code(self):
        return mark_safe(f'{self.qr_code}'+' <style>svg{background: white;}</style>')
    
    @property
    def save_qr_code_as_png(self):
        import qrcode
        import qrcode.image.svg
        factory = qrcode.image.svg.SvgPathImage
        img = qrcode.make(self.verfication_code, image_factory=factory)
        img.save(f'media/qrcodes/{self.verfication_code}.svg')
        return f'media/qrcodes/{self.verfication_code}.svg'
    
    def save(self, *args, **kwargs):
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data = f'http://127.0.0.1:8090/newsletter/verfiy/a9b57c21-8c88-40c3-8451-234f66a9533d/'
        qr.add_data(data)
        qr.make(fit=True)
        print('hey')
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f'media/qrcodes/{self.verfication_code}.png')
        self.image = f'qrcodes/{self.verfication_code}.png'
        super(QRCode, self).save(*args, **kwargs)
        