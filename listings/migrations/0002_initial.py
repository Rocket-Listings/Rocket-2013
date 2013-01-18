# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ListingCategory'
        db.create_table(u'listings_listingcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'listings', ['ListingCategory'])

        # Adding model 'ListingType'
        db.create_table(u'listings_listingtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'listings', ['ListingType'])

        # Adding model 'Listing'
        db.create_table(u'listings_listing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingCategory'])),
            ('listing_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'listings', ['Listing'])

        # Adding model 'ListingSpec'
        db.create_table(u'listings_listingspec', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('listing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.Listing'])),
        ))
        db.send_create_signal(u'listings', ['ListingSpec'])

        # Adding model 'ListingHighlight'
        db.create_table(u'listings_listinghighlight', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('listing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.Listing'])),
        ))
        db.send_create_signal(u'listings', ['ListingHighlight'])

        # Adding model 'ListingPhoto'
        db.create_table(u'listings_listingphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.FilePathField')(path='/Users/teddyknox/Workspace/Python/rocketlistings/media/uploads', max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('upload_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('listing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.Listing'], null=True, blank=True)),
        ))
        db.send_create_signal(u'listings', ['ListingPhoto'])


    def backwards(self, orm):
        # Deleting model 'ListingCategory'
        db.delete_table(u'listings_listingcategory')

        # Deleting model 'ListingType'
        db.delete_table(u'listings_listingtype')

        # Deleting model 'Listing'
        db.delete_table(u'listings_listing')

        # Deleting model 'ListingSpec'
        db.delete_table(u'listings_listingspec')

        # Deleting model 'ListingHighlight'
        db.delete_table(u'listings_listinghighlight')

        # Deleting model 'ListingPhoto'
        db.delete_table(u'listings_listingphoto')


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
        u'listings.listing': {
            'Meta': {'object_name': 'Listing'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.ListingCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.ListingType']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'listings.listingcategory': {
            'Meta': {'object_name': 'ListingCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'listings.listinghighlight': {
            'Meta': {'object_name': 'ListingHighlight'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'listings.listingphoto': {
            'Meta': {'object_name': 'ListingPhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.FilePathField', [], {'path': "'/Users/teddyknox/Workspace/Python/rocketlistings/media/uploads'", 'max_length': '255'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'listings.listingspec': {
            'Meta': {'object_name': 'ListingSpec'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'listings.listingtype': {
            'Meta': {'object_name': 'ListingType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['listings']