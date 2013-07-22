# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.group'
        db.delete_column(u'uploader_project', 'group_id')


    def backwards(self, orm):
        # Adding field 'Project.group'
        db.add_column(u'uploader_project', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], unique=True, null=True, blank=True),
                      keep_default=False)


    models = {
        u'uploader.filesystem': {
            'Meta': {'object_name': 'FileSystem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mount_point': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2000'})
        },
        u'uploader.package': {
            'Meta': {'object_name': 'Package'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uploader.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'uploader.project': {
            'Meta': {'unique_together': "(('file_system', 'directory'),)", 'object_name': 'Project'},
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'file_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uploader.FileSystem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['uploader']