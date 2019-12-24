from django.db import models

# Create your models here.

class Awards(models.Model):
    award_name = models.CharField(max_length=30)


class Person(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(max_length=20)
    depart_name = models.CharField(max_length=200)
    origin_pic = models.CharField(max_length=200)
    snap_pic = models.ImageField(upload_to='uploads/')
    flag = models.IntegerField(default=0)
    award = models.ForeignKey(Awards,on_delete=models.SET_NULL,null=True)



    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


