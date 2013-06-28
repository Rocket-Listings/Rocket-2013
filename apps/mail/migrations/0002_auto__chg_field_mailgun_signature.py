# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'mailgun.signature'
        db.alter_column(u'mail_mailgun', 'signature', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'mailgun.signature'
        db.alter_column(u'mail_mailgun', 'signature', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

    models = {
        u'mail.mailgun': {
            'Meta': {'object_name': 'mailgun'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'frm': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sig': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['mail']