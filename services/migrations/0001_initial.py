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

        # Adding model 'Service'
        db.create_table('services_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Service'])

        # Adding model 'Hardware'
        db.create_table('services_hardware', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('oType', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Location'], null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Hardware'])

        # Adding M2M table for field port on 'Hardware'
        db.create_table('services_hardware_port', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hardware', models.ForeignKey(orm['services.hardware'], null=False)),
            ('service', models.ForeignKey(orm['services.service'], null=False))
        ))
        db.create_unique('services_hardware_port', ['hardware_id', 'service_id'])

        # Adding model 'Server'
        db.create_table('services_server', (
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Hardware'], unique=True, primary_key=True)),
            ('cpu_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('memory', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('disk', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Server'])

        # Adding model 'Switch'
        db.create_table('services_switch', (
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('services', ['Switch'])


    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('services_location')

        # Deleting model 'Service'
        db.delete_table('services_service')

        # Deleting model 'Hardware'
        db.delete_table('services_hardware')

        # Removing M2M table for field port on 'Hardware'
        db.delete_table('services_hardware_port')

        # Deleting model 'Server'
        db.delete_table('services_server')

        # Deleting model 'Switch'
        db.delete_table('services_switch')


    models = {
        'services.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Location']", 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'oType': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['services.Service']", 'symmetrical': 'False'})
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
            'memory': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'services.service': {
            'Meta': {'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'services.switch': {
            'Meta': {'object_name': 'Switch', '_ormbases': ['services.Hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Hardware']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['services']
