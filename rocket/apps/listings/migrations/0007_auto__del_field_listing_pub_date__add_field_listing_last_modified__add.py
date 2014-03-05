# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Listing.pub_date'
        db.delete_column(u'listings_listing', 'pub_date')

        # Adding field 'Listing.last_modified'
        db.add_column(u'listings_listing', 'last_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Listing.create_date'
        db.add_column(u'listings_listing', 'create_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Listing.status'
        db.alter_column(u'listings_listing', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingStatus']))

        # Changing field 'Listing.category'
        db.alter_column(u'listings_listing', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingCategory'], null=True))

        # Changing field 'Listing.description'
        db.alter_column(u'listings_listing', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Listing.title'
        db.alter_column(u'listings_listing', 'title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Listing.price'
        db.alter_column(u'listings_listing', 'price', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Listing.market'
        db.alter_column(u'listings_listing', 'market', self.gf('django.db.models.fields.CharField')(max_length=3, null=True))

        # Changing field 'Listing.location'
        db.alter_column(u'listings_listing', 'location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):
        # Adding field 'Listing.pub_date'
        db.add_column(u'listings_listing', 'pub_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True),
                      keep_default=False)

        # Deleting field 'Listing.last_modified'
        db.delete_column(u'listings_listing', 'last_modified')

        # Deleting field 'Listing.create_date'
        db.delete_column(u'listings_listing', 'create_date')


        # Changing field 'Listing.status'
        db.alter_column(u'listings_listing', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingStatus'], null=True))

        # Changing field 'Listing.category'
        db.alter_column(u'listings_listing', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['listings.ListingCategory']))

        # User chose to not deal with backwards NULL issues for 'Listing.description'
        raise RuntimeError("Cannot reverse this migration. 'Listing.description' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Listing.title'
        raise RuntimeError("Cannot reverse this migration. 'Listing.title' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Listing.price'
        raise RuntimeError("Cannot reverse this migration. 'Listing.price' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Listing.market'
        raise RuntimeError("Cannot reverse this migration. 'Listing.market' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Listing.location'
        raise RuntimeError("Cannot reverse this migration. 'Listing.location' and its values cannot be restored.")

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
        u'listings.buyer': {
            'Meta': {'object_name': 'Buyer'},
            'curMaxOffer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rocket_address': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'listings.listing': {
            'CL_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'CL_view': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Meta': {'unique_together': "(('title', 'user'),)", 'object_name': 'Listing'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.ListingCategory']", 'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'listing_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'market': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['listings.ListingStatus']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        u'listings.listingphoto': {
            'Meta': {'ordering': "['order']", 'object_name': 'ListingPhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'listings.listingstatus': {
            'Meta': {'object_name': 'ListingStatus'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'listings.message': {
            'Meta': {'object_name': 'Message'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Buyer']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isSeller': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']"}),
            'seen': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'listings.offer': {
            'Meta': {'object_name': 'Offer'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Buyer']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'listings.spec': {
            'Meta': {'object_name': 'Spec'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listings.Listing']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['listings']
