# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'mailgun.text'
        db.add_column('mail_mailgun', 'text',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'mailgun.signature'
        db.add_column('mail_mailgun', 'signature',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'mailgun.timestamp'
        db.add_column('mail_mailgun', 'timestamp',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'mailgun.token'
        db.add_column('mail_mailgun', 'token',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'mailgun.sig'
        db.add_column('mail_mailgun', 'sig',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'mailgun.text'
        db.delete_column('mail_mailgun', 'text')

        # Deleting field 'mailgun.signature'
        db.delete_column('mail_mailgun', 'signature')

        # Deleting field 'mailgun.timestamp'
        db.delete_column('mail_mailgun', 'timestamp')

        # Deleting field 'mailgun.token'
        db.delete_column('mail_mailgun', 'token')

        # Deleting field 'mailgun.sig'
        db.delete_column('mail_mailgun', 'sig')


    models = {
        'mail.mailgun': {
            'Meta': {'object_name': 'mailgun'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'frm': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sig': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['mail']