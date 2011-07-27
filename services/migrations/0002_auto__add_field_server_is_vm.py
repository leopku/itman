# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Server.is_vm'
        db.add_column('services_server', 'is_vm', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Server.is_vm'
        db.delete_column('services_server', 'is_vm')


    models = {
        'services.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Location']", 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'oType': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'services.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '29', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '29', 'null': 'True', 'blank': 'True'})
        },
        'services.server': {
            'Meta': {'object_name': 'Server', '_ormbases': ['services.Hardware']},
            'cpu_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'disk': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'is_vm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'memory': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'services.service': {
            'Meta': {'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'server'", 'null': 'True', 'to': "orm['services.Server']"}),
            'switch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'switch'", 'null': 'True', 'to': "orm['services.Switch']"})
        },
        'services.switch': {
            'Meta': {'object_name': 'Switch', '_ormbases': ['services.Hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Hardware']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['services']
