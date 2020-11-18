from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from brandbooster.utils import unique_slug_generator
# Create your models here.
from BrandBoosterUser.models import Account

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return str(self.pk) + " - " + self.name

class Company_Info(models.Model):
    company_id              = models.AutoField(primary_key=True)
    user_id                 = models.ForeignKey(Account,on_delete=models.CASCADE)
    company_name            = models.CharField(max_length=50)
    slug                    = models.SlugField(max_length=250,null=True,blank=True)
    company_category        = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    custom_category         = models.TextField(blank=True)
    company_short_info      = models.TextField()
    company_long_info       = models.TextField()
    company_ceo             = models.CharField(max_length=50)
    company_address         = models.TextField()
    company_state           = models.CharField(max_length=50)
    company_city            = models.CharField(max_length=50)
    company_pincode         = models.IntegerField()
    company_phone           = PhoneNumberField()
    company_phone_code      = models.CharField(max_length=50,default="",null=True,blank=True)
    company_telephone       = models.BigIntegerField(blank=True,null=True)
    company_whatsapp        = PhoneNumberField(blank=True,null=True)
    company_whatsapp_code   = models.CharField(max_length=50,default="",null=True,blank=True)
    company_email           = models.EmailField(max_length=50)
    company_domain          = models.CharField(max_length=50)
    company_status          = models.BooleanField(default=False)
    company_photo           = models.ImageField(_("Company Logo"), upload_to="profile_pics")
    cover_image             = models.ImageField(upload_to="cover images")
    date_time_created       = models.DateTimeField(auto_now_add=True)
    date_time_modified      = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.pk) + ") " + str(self.company_pincode)
    # def __str__(self):
    #     return str(self.company_id) or ""

def slug_generator(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    def getAbsolutePhoneNumber(self):
        return str(self.company_phone)[3:]

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
pre_save.connect(slug_generator,sender=Company_Info)

class Company_Marketing_Photos(models.Model):
    company_Marketing_Photos_id = models.AutoField(primary_key=True)
    company_id          = models.ForeignKey(Company_Info,on_delete=models.CASCADE)
    company_mrk_image   = models.ImageField(upload_to='image', null=False)
    image_name          = models.CharField(max_length=200, default='', null=False)
    date_time_created   = models.DateTimeField(auto_now_add=True)
    date_time_modified  = models.DateTimeField(auto_now=True) 

    # def __str__(self):
    #     return str(self.pk) + ") " + self.company_id.company_name + " - " + self.image_name

    class Meta:
        verbose_name = _("Company Marketing Photo")
        verbose_name_plural = _("Company Marketing Photos")

class Company_videos(models.Model):
    company_videos_id   = models.AutoField(primary_key=True)
    company_id          = models.ForeignKey(Company_Info,on_delete=models.CASCADE)
    video_name          = models.CharField(max_length=200, default='', null=False)
    video_link          = models.CharField(max_length=200, null= False)
    date_time_created   = models.DateTimeField(auto_now_add=True)
    date_time_modified  = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.pk) + ") " + self.company_id.company_name + " - " + self.video_name

    class Meta:
        verbose_name = _("Company Video")
        verbose_name_plural = _("Company Videos")

class Company_Product_Photos(models.Model):
    company_product_photos_id = models.AutoField(primary_key=True)
    company_id          = models.ForeignKey(Company_Info,on_delete=models.CASCADE)
    company_prd_image   = models.ImageField(upload_to='image', null=False)
    image_name          = models.CharField(max_length=200, default='', null=False)
    date_time_created   = models.DateTimeField(auto_now_add=True)
    date_time_modified  = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.pk) + ") " + self.company_id.company_name + " - " + self.image_name

    class Meta:
        verbose_name = _("Company Product Photo")
        verbose_name_plural = _("Company Product Photos")

class Company_Audio(models.Model):
    company = models.ForeignKey(Company_Info, on_delete=models.CASCADE)
    audio_name = models.CharField(max_length=50)
    audio_file = models.FileField(upload_to="audios")

    class Meta:
        verbose_name = _("Company Audio")
        verbose_name_plural = _("Company Audios")

class Main_Slider(models.Model):
    slide_image         = models.ImageField(upload_to='slider', null=False)
    image_name          = models.CharField(max_length=50, default='', null=False)
    image_information   = models.CharField(max_length=500, default='', null=False)
    date_time_created   = models.DateTimeField(auto_now_add=True)
    date_time_modified  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Slider Image")
        verbose_name_plural = _("Slider Images")