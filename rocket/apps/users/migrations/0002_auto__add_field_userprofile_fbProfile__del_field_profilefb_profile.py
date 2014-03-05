# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.fbProfile'
        db.add_column(u'users_userprofile', 'fbProfile',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['users.ProfileFB'], unique=True),
                      keep_default=False)

        # Deleting field 'ProfileFB.profile'
        db.delete_column(u'users_profilefb', 'profile_id')


    def backwards(self, orm):
        # Deleting field 'UserProfile.fbProfile'
        db.delete_column(u'users_userprofile', 'fbProfile_id')


        # User chose to not deal with backwards NULL issues for 'ProfileFB.profile'
        raise RuntimeError("Cannot reverse this migration. 'ProfileFB.profile' and its values cannot be restored.")

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
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'users.usercomment': {
            'Meta': {'object_name': 'UserComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date_posted': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': "'5'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'TWITTER_OAUTH_TOKEN': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'TWITTER_OAUTH_TOKEN_SECRET': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'default_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.ListingCategory']", 'null': 'True', 'blank': 'True'}),
            'facebook_connected_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fbProfile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.ProfileFB']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing_credits': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'profile_completed_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'propic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'seller_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'total_credits': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'twitter_connected_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
