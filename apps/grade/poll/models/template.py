# -*- coding: utf8 -*-
from django.db                         import models
from django.utils.safestring           import SafeUnicode

from apps.users.models               import Employee, \
                                              Student, \
                                              Program
from apps.enrollment.subjects.models import Group, \
                                              Subject, \
                                              Semester, \
                                              GROUP_TYPE_CHOICES
from apps.enrollment.records.models  import Record, \
                                              STATUS_ENROLLED
from apps.grade.ticket_create.models import PublicKey                                              
from section                         import SectionOrdering, Section

class Template( models.Model ):
    title             = models.CharField( max_length = 40, verbose_name = 'tytuł' )
    description       = models.TextField( blank = True, verbose_name = 'opis' )
    studies_type      = models.ForeignKey( Program, verbose_name = 'typ studiów', blank = True, null = True )
    subject           = models.ForeignKey( Subject, verbose_name = 'przedmiot', blank = True, null = True)
    no_subject        = models.BooleanField( blank = False, null = False, default = False, verbose_name = 'nie przypisany' )
    deleted           = models.BooleanField( blank = False, null = False, default = False, verbose_name = 'usunięty' )
    group_type        = models.CharField( max_length=1, choices=GROUP_TYPE_CHOICES, verbose_name='typ zajęć')
    sections          = models.ManyToManyField( Section, verbose_name = 'sekcje',
                                                through = 'TemplateSections')

    class Meta:
        verbose_name        = 'szablon' 
        verbose_name_plural = 'szablony'
        app_label           = 'poll'
        ordering            =['title']
        
    def __unicode__( self ):
        res = unicode( self.title )
        if self.studies_type: res += u', typ studiów: ' + unicode( self.studies_type )
        if self.subject:      res += u', przedmiot: ' + unicode( self.subject )
        if self.group_type:   res += u', typ grupy: ' + unicode( self.group_type )
        return res
        

class TemplateSections( models.Model ):
    id = models.AutoField(primary_key=True)
    template     = models.ForeignKey( Template,      verbose_name = 'ankieta' )
    section  = models.ForeignKey( Section, verbose_name = 'sekcja' )

    class Meta:
        verbose_name_plural = 'pozycje sekcji'
        verbose_name        = 'pozycja sekcji'
        app_label           = 'poll'
        ordering = ['id']


