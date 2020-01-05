from django.contrib import admin
from . import models


# Register your models here.

class ResultInline(admin.TabularInline):
    model = models.Result
    extra = 1
    


@admin.register(models.User)
class AdminUser(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','is_active','is_staff','is_superuser']
    fieldsets = (
        (None, {
            'fields':(('username','password'),'email')
            }),
        ('Personal Data', {
            'classes': ('extrapretty',),
            'fields': (('first_name',), 'last_name')
            }),
        ('Status', {
            'classes': ('extrapretty',),
            'fields':(('is_active','is_staff','is_superuser'), )
            }),
        ('Permissions', {
            'fields':('groups','user_permissions')
            })
    )

@admin.register(models.LocalGovernmentArea)
class AdminLocalGovernmentArea(admin.ModelAdmin):
    list_display = ['lga_name', 'lga_code']
    list_display_links = ['lga_name','lga_code']


@admin.register(models.Candidate)
class AdminCandidate(admin.ModelAdmin):
    list_display = ['name','examination_num','gender','school','year']
    list_display_links = ['name','gender','year']
    radio_fields = {'gender': admin.HORIZONTAL}
    list_filter = ['school','year']
    readonly_fields = ('examination_num',)
    inlines = (ResultInline,)
    ordering = ['candidate_num','year']

    fieldsets = (
        ('Examination Info', {
            'classes': ('extrapretty',),
            'fields':(('school','year',),('candidate_num','examination_num'),)
            }),
        ('Personal Data', {
            'classes': ('extrapretty',),
            'fields': ('first_name','middle_name','last_name','gender','birth_date',)
            }),
        
    )

    class Media:
        css = {
            "all": ("main.css",)
        }
        js = ("my_code.js",)

@admin.register(models.Result)
class AdminResult(admin.ModelAdmin):
    pass


@admin.register(models.School)
class AdminSchool(admin.ModelAdmin):
    list_display = ['school_name','getLocalGovernmentArea']
    list_display_links = ['school_name']
    list_filter = ['lga__lga_name']

    def getLocalGovernmentArea(self, obj):
        return obj.lga.lga_name
    getLocalGovernmentArea.short_description = 'Local Government Area'

@admin.register(models.Subjects)
class AdminSubjects(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_code']
    list_display_links = ['subject_name']

    fieldsets = (
        ('Subjects Offered', {
            'classes': ('extrapretty',),
            'fields':(('subject_name','subject_code',),)
            }),   
    )

'''
@admin.register(models.Result)
class AdminResult(admin.ModelAdmin):
    list_display = ['canditesExaminationNumber','examinationYear']
    list_display_links = ['canditesExaminationNumber']
    list_filter = ['candidate__year','candidate__school']
    

    
    def canditesExaminationNumber(self, obj):
        return obj.candidate.examination_num

    def examinationYear(self, obj):
        return obj.candidate.year

    def subjectsOffered(self, obj):
        return obj.subject_offered
    
    def gradeScored(self, obj):
        return obj.grade


@admin.register(models.Grade)
class AdminGrade(admin.ModelAdmin):
    list_display = ['grade_name','grade_code']
    list_display_links = ['grade_name']
    radio_fields = {'grade_code': admin.VERTICAL}

  '''  
