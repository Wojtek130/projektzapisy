# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    depends_on = (
        ('users',    '0001_initial'),
        ('proposal', '0001_initial'),
    )
    
    def forwards(self, orm):
        
        # Adding model 'SystemState'
        db.create_table('vote_systemstate', (
            ('max_vote', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('vote_end', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 12, 31))),
            ('vote_beg', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 1, 1))),
            ('max_points', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2010, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('vote', ['SystemState'])

        # Adding model 'SingleVote'
        db.create_table('vote_singlevote', (
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.SystemState'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Student'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['proposal.Proposal'])),
        ))
        db.send_create_signal('vote', ['SingleVote'])

        # Adding unique constraint on 'SingleVote', fields ['course', 'state', 'student']
        db.create_unique('vote_singlevote', ['course_id', 'state_id', 'student_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'SystemState'
        db.delete_table('vote_systemstate')

        # Deleting model 'SingleVote'
        db.delete_table('vote_singlevote')

        # Removing unique constraint on 'SingleVote', fields ['course', 'state', 'student']
        db.delete_unique('vote_singlevote', ['course_id', 'state_id', 'student_id'])
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposal.proposal': {
            'Meta': {'object_name': 'Proposal'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'fans': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.Student']", 'symmetrical': 'False', 'blank': 'True'}),
            'helpers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'proposal_helpers_related'", 'blank': 'True', 'to': "orm['users.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wlasciciel'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['proposal.ProposalTag']", 'symmetrical': 'False', 'blank': 'True'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'proposal_teachers_related'", 'blank': 'True', 'to': "orm['users.Employee']"})
        },
        'proposal.proposaltag': {
            'Meta': {'object_name': 'ProposalTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'users.employee': {
            'Meta': {'object_name': 'Employee'},
            'consultations': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receive_mass_mail_offer': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'users.student': {
            'Meta': {'object_name': 'Student'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '20'}),
            'receive_mass_mail_offer': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'records_opening_delay_hours': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'vote.singlevote': {
            'Meta': {'unique_together': "(('course', 'state', 'student'),)", 'object_name': 'SingleVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.SystemState']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Student']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposal.Proposal']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'vote.systemstate': {
            'Meta': {'object_name': 'SystemState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'max_vote': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'vote_beg': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2010, 1, 1)'}),
            'vote_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2010, 12, 31)'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2010', 'unique': 'True'})
        }
    }
    
    complete_apps = ['vote']