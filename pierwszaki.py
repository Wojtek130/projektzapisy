# -*- coding: utf-8 -*-


__author__ = 'maciek'

FEREOL_PATH = '../'

import sys
import os
from django.core.management import setup_environ
from datetime import time



if __name__ == '__main__':
    sys.path.append(FEREOL_PATH)
    sys.path.append(FEREOL_PATH + 'fereol/')
    from fereol import settings
    setup_environ(settings)



from apps.users.models import Student
from django.core.exceptions import ObjectDoesNotExist
from apps.enrollment.courses.models.course import Course
from apps.offer.vote.models import SingleVote
from apps.enrollment.courses.models.semester import Semester

#students = Student.objects.filter(status=0, ects=0)
#
#for s in students:
#    s.records_opening_bonus_minutes = 1440
#    s.save()


f = open("pierwszaki.txt", "r")


lista = []

semester = Semester.get_current_semester()

lista.append(Course.objects.get(name=u"Algebra", semester=semester))
lista.append(Course.objects.get(name=u"Programowanie (L)", semester=semester))
lista.append(Course.objects.get(name=u"Programowanie (M)", semester=semester))
lista.append(Course.objects.get(name=u"Programowanie obiektowe", semester=semester))
lista.append(Course.objects.get(name=u"Kurs języka C++", semester=semester))
lista.append(Course.objects.get(name=u"Kurs języka Pascal", semester=semester))
lista.append(Course.objects.get(name=u"Kurs: tworzenie aplikacji interaktywnych w Pythonie", semester=semester))



for s in Student.objects.filter(status=0, ects=0):


    #s.records_opening_bonus_minutes += int(pola[-1])

    if SingleVote.objects.filter(student=s).count() > 0:
        continue

    print "Przetwarzanie: " + s.matricula

    for p in lista:
        v = SingleVote()
        v.student = s
        v.course = p
        v.entity = p.entity
        v.value = 3
        v.state_id = 4
        v.correction = 3
        v.save()

    #s.save()