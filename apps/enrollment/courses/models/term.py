# -*- coding: utf8 -*-

from django.db import models
from datetime import time

DAYS_OF_WEEK = [( '1', 'poniedziałek' ), ( '2', 'wtorek' ), ( '3', 'środa' ), ( '4', 'czwartek'), ( '5', 'piątek'), ( '6', 'sobota'), ( '7', 'niedziela')]

HOURS = [(str(hour), "%s.00" % hour) for hour in range(8, 23)] 
  
class Term( models.Model ):
    """terms of groups"""
    dayOfWeek = models.CharField( max_length = 1, choices = DAYS_OF_WEEK, verbose_name = 'dzień tygodnia') 
    start_time = models.TimeField(verbose_name = 'rozpoczęcie')
    end_time = models.TimeField(verbose_name = 'zakończenie')
    classroom = models.ForeignKey('Classroom', verbose_name='sala')
    group = models.ForeignKey('Group', verbose_name='grupa', related_name='term')

    class Meta:
        #TO DO /pkacprzak/ add advanced constraint - example: start_time < end_time, any pair of terms can't overlap
        verbose_name = 'termin'
        verbose_name_plural = 'terminy'
        app_label = 'courses'
    
    @staticmethod
    def get_all_in_semester(semester, student=None):
        filtered = Term.objects.filter(group__course__semester=semester)
        
        if student:
            from apps.enrollment.records.models import Record
            filtered = filtered.filter(group__id__in=\
                Record.get_student_enrolled_ids(student, semester))
            
        return filtered.select_related('classroom', 'group', 'group__course', \
            'group__course__semester', 'group__course__entity',
            'group__course__type', \
            'group__teacher', 'group__teacher__user').\
            order_by('dayOfWeek', 'start_time').all()

    def day_in_zero_base(self):
        return int(self.dayOfWeek)-1
    
    def length_in_minutes(self):
        return (self.end_time.hour - self.start_time.hour)*60 + (self.end_time.minute - self.start_time.minute)
    
    def time_from_in_minutes(self):
        "Returns number of minutes from start of day (midnight) to term beggining"""
        return (self.start_time.hour)* 60 + (self.start_time.minute) 

    def time_from(self):
        "Returns hourFrom in time format"""
        return self.start_time
  
    def time_to(self):
        "Returns hourTo in time format"""
        return self.end_time

    def _convert_string_to_time(self, str):
        hour, minute = map(lambda x: int(x), str.split('.'))
        return time(hour=hour, minute=minute)
    
    def period_string(self):
        return "%s – %s" % (self.start_time.strftime("%H"), self.end_time.strftime("%H"))
        
    def __unicode__(self):
        return "%s (%s-%s) s.%s" % (self.get_dayOfWeek_display(), self.start_time.strftime("%H:%M"), self.end_time.strftime("%H:%M"), self.classroom.number)