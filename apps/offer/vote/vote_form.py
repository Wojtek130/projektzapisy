# -*- coding: utf-8 -*-

"""
    Form for vote
"""

from django                   import forms
from django.core.exceptions   import ObjectDoesNotExist
from django.utils.safestring  import SafeUnicode

from apps.offer.vote.models import SystemState
from apps.offer.vote.models import SingleVote


class VoteForm( forms.Form ):
    """
        Voting form
    """
    choices = [(str(i), i) for i in range(SystemState.get_max_points()+1)]
    subject_types = {}
    subject_fan_flag = {}
    
    def __init__ (self, *args, **kwargs):
        winter  = kwargs.pop('winter')
        summer  = kwargs.pop('summer')
        unknown = kwargs.pop('unknown')
        voter   = kwargs.pop('voter')
        
        state   = SystemState.get_state()
        
        super(VoteForm, self).__init__(*args, **kwargs)

        for sub in winter:
            try:
                choosed = SingleVote.objects.get( 
                            student = voter, 
                            subject = sub,
                            state   = state ).value
            except ObjectDoesNotExist:
                choosed = 0
            
            self.fields['winter_%s' % sub.pk] = forms.ChoiceField(
                                            label     = sub.name,
                                            choices   = self.choices,
                                            help_text = u'Semestr Zimowy',
                                            initial   = choosed)
            self.subject_types['winter_%s' % sub.pk] = sub.description().types()
            self.subject_fan_flag['winter_%s' % sub.pk] = sub.is_in_group(voter, 'fans')
                                            
        for sub in summer:
            try:
                choosed = SingleVote.objects.get( 
                            student = voter, 
                            subject = sub,
                            state   = state ).value
            except ObjectDoesNotExist:
                choosed = 0
            
            self.fields['summer_%s' % sub.pk] = forms.ChoiceField(
                                            label     = sub.name,
                                            choices   = self.choices,
                                            help_text = u'Semestr Letni',
                                            initial   = choosed)
            self.subject_types['summer_%s' % sub.pk] = sub.description().types()
            self.subject_fan_flag['summer_%s' % sub.pk] = sub.is_in_group(voter, 'fans')
        
        for sub in unknown:
            try:
                choosed = SingleVote.objects.get( 
                            student = voter, 
                            subject = sub,
                            state   = state ).value
            except ObjectDoesNotExist:
                choosed = 0
            
            self.fields['unknown_%s' % sub.pk] = forms.ChoiceField(
                                            label     = sub.name,
                                            choices   = self.choices,
                                            help_text = u'Semestr Nieokreślony',
                                            initial   = choosed)
            self.subject_types['unknown_%s' % sub.pk] = sub.description().types()
            self.subject_fan_flag['unknown_%s' % sub.pk] = sub.is_in_group(voter, 'fans')
    
    def vote_points( self ):
        """
            Calculates points
        """
        for name, value in self.cleaned_data.items():
            if name.startswith('winter_') or \
               name.startswith('summer_') or \
               name.startswith('unknown_'):
                yield (self.fields[name].label, value)
    
    def as_lists( self ):
        """
            Creates html form
        """
        winter   = u'<div class="od-vote-semester" id="od-vote-semester-winter"><h2>Semestr zimowy</h2><ul>'
        summer   = u'<div class="od-vote-semester" id="od-vote-semester-summer"><h2>Semestr letni</h2><ul>'
        unknown  = u'<div class="od-vote-semester" id="od-vote-semester-unknown"><h2>Semestr nieokreślony</h2><ul>'

        winter_empty = True
        summer_empty = True
        unknown_empty = True
        
        maksimum  = u'<p id="od-vote-maxPoints">Maksymalna liczba punktów do wykorzystania: <span>'
        maksimum += str(SystemState.get_max_vote())
        maksimum += u' </span></p>'
        
        for key in self.fields.iterkeys():
            field = self.fields[key]
            subject_class = u''
            for type in self.subject_types[key]:
                subject_class += u' subject-type-' + str(type.lecture_type.id)
            if self.subject_fan_flag[key]:
                subject_class += " isFan"
            field_str = \
                u'<li class="od-vote-subject ' + subject_class + '">\
                    <label for="id_' + key + '">' + field.label + '</label>\
                    <select name="' + key + '" id="id_' + key + '">'
            for (i, s) in field.choices:
                field_str += '<option value="'
                field_str += str(i)
                field_str += '"' 
                if i == str(field.initial):
                    field_str += ' selected="selected"'
                field_str += '>'
                field_str += str(s)
                field_str += '</option>'
            field_str += ' </select></li>'
                    
            if   key.startswith('winter_'):
                winter_empty = False
                winter += field_str
            elif key.startswith('summer_'):
                summer_empty = False
                summer += field_str
            elif key.startswith('unknown_'):
                unknown_empty = False
                unknown += field_str

        list = SafeUnicode(u'')
        if (not winter_empty):
            list += SafeUnicode(winter) + SafeUnicode(u'</ul></div>')
        if (not summer_empty):
            list += SafeUnicode(summer) + SafeUnicode(u'</ul></div>')
        if (not unknown_empty):
            list += SafeUnicode(unknown) + SafeUnicode(u'</ul></div>')

        return  list + SafeUnicode(maksimum)