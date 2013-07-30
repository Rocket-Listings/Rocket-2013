# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'users_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('default_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingCategory'], null=True, blank=True)),
            ('default_listing_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('default_seller_type', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('propic', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('OAUTH_TOKEN', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('OAUTH_TOKEN_SECRET', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'users', ['UserProfile'])

        # Adding model 'UserComment'
        db.create_table(u'users_usercomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_posted', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'users', ['UserComment'])

        # Adding model 'ProfileFB'
        db.create_table(u'users_profilefb', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.UserProfile'], unique=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'users', ['ProfileFB'])

        # Adding model 'FirstVisit'
        db.create_table(u'users_firstvisit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template_path', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'users', ['FirstVisit'])

        # Adding model 'ViewCount'
        db.create_table(u'users_viewcount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'users', ['ViewCount'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'users_userprofile')

        # Deleting model 'UserComment'
        db.delete_table(u'users_usercomment')

        # Deleting model 'ProfileFB'
        db.delete_table(u'users_profilefb')

        # Deleting model 'FirstVisit'
        db.delete_table(u'users_firstvisit')

        # Deleting model 'ViewCount'
        db.delete_table(u'users_viewcount')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'listings.listingcategory': {
            'Meta': {'object_name': 'ListingCategory'},
            'cl_dealer_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'cl_owner_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'users.firstvisit': {
            'Meta': {'object_name': 'FirstVisit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template_path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'users.profilefb': {
            'Meta': {'object_name': 'ProfileFB'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.UserProfile']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'users.usercomment': {
            'Meta': {'object_name': 'UserComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date_posted': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'OAUTH_TOKEN': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'OAUTH_TOKEN_SECRET': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'default_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.ListingCategory']", 'null': 'True', 'blank': 'True'}),
            'default_listing_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'default_seller_type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'propic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'users.viewcount': {
            'Meta': {'object_name': 'ViewCount'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['users']