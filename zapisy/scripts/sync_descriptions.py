# -*- coding: utf-8 -*-

from apps.enrollment.courses.models import Semester, Course, CourseEntity, CourseDescription

def run():
    s = Semester.get_current_semester()
    cs = s.course_set.all()
    counter = 0
    for c in cs:
        if c.information_id != c.entity.information_id:
            print('updating '+str(c.entity)+': '+str(c.entity.information)+' -> '+str(c.information))
            c.entity.information = c.information
            c.entity.save()
            counter += 1
    print('Updated '+str(counter) + ' descriptions.')