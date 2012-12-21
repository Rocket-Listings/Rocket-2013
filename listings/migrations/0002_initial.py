# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ListingCategory'
        db.create_table('listings_listingcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('listings', ['ListingCategory'])

        # Adding model 'ListingType'
        db.create_table('listings_listingtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('listings', ['ListingType'])

        # Adding model 'ListingSpec'
        db.create_table('listings_listingspec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('listings', ['ListingSpec'])

        # Adding model 'ListingHighlight'
        db.create_table('listings_listinghighlight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('listings', ['ListingHighlight'])

        # Adding model 'Listing'
        db.create_table('listings_listing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingCategory'])),
            ('listing_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listings.ListingType'])),
            ('specs', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['listings.ListingSpec'], null=True, blank=True)),
            ('highlights', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['listings.ListingHighlight'], null=True, blank=True)),
        ))
        db.send_create_signal('listings', ['Listing'])


    def backwards(self, orm):
        # Deleting model 'ListingCategory'
        db.delete_table('listings_listingcategory')

        # Deleting model 'ListingType'
        db.delete_table('listings_listingtype')

        # Deleting model 'ListingSpec'
        db.delete_table('listings_listingspec')

        # Deleting model 'ListingHighlight'
        db.delete_table('listings_listinghighlight')

        # Deleting model 'Listing'
        db.delete_table('listings_listing')


    models = {
        'listings.listing': {
            'Meta': {'object_name': 'Listing'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['listings.ListingCategory']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'highlights': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['listings.ListingHighlight']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['listings.ListingType']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'specs': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['listings.ListingSpec']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'value': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'listings.listingspec': {
            'Meta': {'object_name': 'ListingSpec'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
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