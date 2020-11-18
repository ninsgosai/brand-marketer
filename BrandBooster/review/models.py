from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
from BrandBoosterUser.models import Account
from Company.models import Company_Info

class Review(models.Model):
    class Meta:
        unique_together = (('user_id','company_id'),)
    STAR_CHOICES = (
        (0, 'Defult'),
        (1, '1star'),
        (2, '2star'),
        (3, '3star'),
        (4, '4star'),
        (5, '5star')
    )
    review_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company_Info,on_delete=models.CASCADE)
    review = models.TextField()
    star = models.PositiveSmallIntegerField(choices=STAR_CHOICES, default=0)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

like_choices = [[0 ,'0'],[1 ,'1'],[2 ,'2']]

class Likes(models.Model):
    class Meta:
        unique_together = (('user_id','company_id'),)
    company_id = models.ForeignKey(Company_Info,on_delete=models.CASCADE)
    like_id = models.AutoField(primary_key=True)
    like = models.IntegerField(default=0,choices=like_choices)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
