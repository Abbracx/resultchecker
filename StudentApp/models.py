from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save

# Create your models here.
class User(AbstractUser):
    pass

class LocalGovernmentArea(models.Model):
    lga_name = models.CharField(max_length=50)
    lga_code = models.CharField(max_length=2, primary_key=True)

    class Meta:
        ordering = ['lga_name']

    def __str__(self):
        return self.lga_name

class School(models.Model):
    school_name = models.TextField()
    school_code = models.CharField(max_length=4, primary_key=True)
    lga = models.ForeignKey(LocalGovernmentArea, on_delete=models.CASCADE, verbose_name='school lga location')

    def __str__(self):
        return self.school_name

'''
class Grade(models.Model):
    GRADE = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('F','F'),
    )

    grade_name = models.CharField(max_length=20, blank=True, verbose_name='remark')
    grade_code = models.CharField(max_length=1, choices=GRADE, blank=True, verbose_name='remark')

    class Meta:
        ordering = ['grade_code']
        
    def __str__(self):
        return self.grade_name
'''

        
class Subjects(models.Model):

    subject_name = models.CharField(max_length=20)
    subject_code = models.CharField(max_length=5, primary_key=True)
    
    
    def __str__(self):
        return '{}'.format(self.subject_name)



class Candidate(models.Model):

    GENDER = (
        ('m','male'),
        ('f','female'),
    )
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20)
    candidate_num = models.CharField(max_length=4, verbose_name='candidate serial number')
    examination_num = models.CharField(max_length=10, primary_key=True,verbose_name='candidate examination number')
    year = models.DateField(default=timezone.now, verbose_name='year of exmamination')
    gender = models.CharField(max_length=2, choices=GENDER)
    birth_date = models.DateField(default=timezone.now, verbose_name='Date of Birth')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='candidate school')
    subjects = models.ManyToManyField(Subjects, through='Result', related_name='candidates', verbose_name='subjects offered')


    def __str__(self):
        return '{0} {1}  ({2})'.format(self.first_name, self.last_name, self.examination_num)

    def name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)     
    name.short_description = 'Name'



'''
class Result(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, verbose_name='Student')
    year = models.DateField(default=timezone.now)
'''

class Result(models.Model):
    GRADE = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('F','F'),
    )

    candidate = models.ForeignKey(Candidate, related_name='student_results', on_delete=models.SET_NULL, null=True)
    subjects = models.ForeignKey(Subjects, related_name='student_results', on_delete=models.SET_NULL, verbose_name='subjects taken', null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    grade = models.CharField(max_length=1, choices=GRADE, verbose_name='remark', null=True, blank=True)

    def __str__(self):
        return self.candidate.examination_num


def checkLeadingZeroes(value):

    if len(value) == 1:
        return '000' + value
    elif len(value) == 2:
        return '00' + value
    elif len(value) == 3:
        return '0' + value
    else:
        return value

def getExaminationNumber(instance=None):
    lga = instance.school.lga.lga_code
    school = instance.school.school_code
    serial_num = checkLeadingZeroes(instance.candidate_num)

    return lga.strip() + school.strip() + serial_num.strip()
    
    
def createExaminationNumber(sender, instance, **kwargs):
        instance.examination_num = getExaminationNumber(instance)
pre_save.connect(createExaminationNumber, sender=Candidate, dispatch_uid='StudentApp.models.Candidate')

