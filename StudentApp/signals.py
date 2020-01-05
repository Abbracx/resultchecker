from .models import Candidate, Result
from django.db.models.signals import post_save, pre_save
from django.dispatch import reciever

@receiver(post_save, sender=Candidate)
def create_ExaminationNumber(sender, instance, created, **kwargs):
    
    candidate = Candidate.objects.select_related('school','school__lga').filter(candidate_num=instance.candidate_num).first()
    
    lga_code = candidate.school.lga.lga_code
    school_code = candidate.school.school_code
    serial_num = candidate.candidate_num
    candidate.examination_num = lga_code 
    candidate.save()

        
@receiver(post_save, sender=Candidate)
def save_ExaminationNumber(sender, instance, **kwargs):
    instance.save()