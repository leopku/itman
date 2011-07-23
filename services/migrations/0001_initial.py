# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('services_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=29, null=True, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=29, null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Location'])

        # Adding model 'Machine'
        db.create_table('services_machine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('mType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('disk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('memory', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Location'], null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Machine'])

        # Adding model 'Service'
        db.create_table('services_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Machine'], null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Service'])


    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('services_location')

        # Deleting model 'Machine'
        db.delete_table('services_machine')

        # Deleting model 'Service'
        db.delete_table('services_service')


    models = {
        'services.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '29', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '29', 'null': 'True', 'blank': 'True'})
        },
        'services.machine': {
            'Meta': {'object_name': 'Machine'},
            'disk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Location']", 'null': 'True', 'blank': 'True'}),
            'mType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'memory': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'services.service': {
            'Meta': {'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Machine']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['services']
