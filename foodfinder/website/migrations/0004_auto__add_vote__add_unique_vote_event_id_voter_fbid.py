# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table(u'website_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Event'])),
            ('voter_fbid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('was_food', self.gf('django.db.models.fields.BooleanField')()),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['event_id', 'voter_fbid']
        db.create_unique(u'website_vote', ['event_id_id', 'voter_fbid'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['event_id', 'voter_fbid']
        db.delete_unique(u'website_vote', ['event_id_id', 'voter_fbid'])

        # Deleting model 'Vote'
        db.delete_table(u'website_vote')


    models = {
        u'website.event': {
            'Meta': {'object_name': 'Event'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator_fbid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'food': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'website.vote': {
            'Meta': {'unique_together': "(('event_id', 'voter_fbid'),)", 'object_name': 'Vote'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voter_fbid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'was_food': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['website']