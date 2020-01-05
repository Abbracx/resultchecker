from django.shortcuts import render, redirect
from .models import Result, Candidate
from .forms import  CandidateForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.

def homepage_view(request):
    form = CandidateForm()
    return render(request, 'StudentApp/homepage.html', {'form': form})

def detail_view(request):

    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        data = request.POST.copy()
        
        exam_num = data.get('exam_number')
        candidate = Candidate.objects.select_related('school','school__lga').filter(examination_num=exam_num).first()
        if candidate is not None:
            results = Result.objects.filter(candidate=candidate.examination_num).values('subjects','score','grade')
            messages.success(request,f'one result found')      
        else:
            messages.info(request,f'No result for these candidate for the specified year/examinaton number')
            return redirect('StudentApp:homepage')
        return render(request,'StudentApp/detail.html', {'candidate': candidate, 'results': results,})

    results = {} 
    candidate = None
    return render(request,'StudentApp/detail.html', {'candidate': candidate, 'results': results,})
    