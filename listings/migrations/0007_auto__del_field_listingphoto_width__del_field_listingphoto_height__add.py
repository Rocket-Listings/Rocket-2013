# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ListingPhoto.width'
        db.delete_column('listings_listingphoto', 'width')

        # Deleting field 'ListingPhoto.height'
        db.delete_column('listings_listingphoto', 'height')

        # Adding field 'ListingPhoto.url'
        db.add_column('listings_listingphoto', 'url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


        # Changing field 'ListingPhoto.listing'
        db.alter_column('listings_listingphoto', 'listing_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.Listing'], null=True))

        # Changing field 'ListingPhoto.order'
        db.alter_column('listings_listingphoto', 'order', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ListingPhoto.width'
        raise RuntimeError("Cannot reverse this migration. 'ListingPhoto.width' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ListingPhoto.height'
        raise RuntimeError("Cannot reverse this migration. 'ListingPhoto.height' and its values cannot be restored.")
        # Deleting field 'ListingPhoto.url'
        db.delete_column('listings_listingphoto', 'url')


        # User chose to not deal with backwards NULL issues for 'ListingPhoto.listing'
        raise RuntimeError("Cannot reverse this migration. 'ListingPhoto.listing' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ListingPhoto.order'
        raise RuntimeError("Cannot reverse this migration. 'ListingPhoto.order' and its values cannot be restored.")

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'listings.listing': {
            'Meta': {'object_name': 'Listing'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['listings.ListingCategory']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['listings.ListingType']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'listings.listingcategory': {
            'Meta': {'object_name': 'ListingCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'listings.listinghighlight': {
            'Meta': {'object_name': 'ListingHighlight'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['listings.Listing']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'listings.listingphoto': {
            'Meta': {'object_name': 'ListingPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['listings.Listing']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.FilePathField', [], {'path': "'/Users/teddyknox/Workspace/Python/rocketlistings/media/uploads'", 'max_length': '100'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'listings.listingspec': {
            'Meta': {'object_name': 'ListingSpec'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['listings.Listing']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'listings.listingtype': {
            'Meta': {'object_name': 'ListingType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['listings']