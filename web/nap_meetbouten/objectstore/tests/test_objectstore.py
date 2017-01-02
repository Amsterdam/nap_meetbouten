import os
import mimetypes
from django.test import TestCase

from unittest import skip

from ..objectstore import ObjectStore


class TestObjectstore(TestCase):

    @skip('integration test only')
    def test_objects(self):
        self.objectstore = ObjectStore('NAP')

        # clean up
        stored_objects = self.objectstore._get_full_container_list([])

        # remove old cruft if any
        for ob in stored_objects:
            if ob['name'].startswith('naptest/'):
                self.objectstore.delete_from_objectstore(ob['name'])

        res = self.objectstore._get_full_container_list([])

        # check if we have a test folder on the object store
        test_folder_found = False

        for ob in res:
            if ob['name'].startswith('naptest'):
                test_folder_found = True
                break

        self.assertTrue(test_folder_found)

        # check local test files
        objects = ['diva/nap/{}'.format(filename) for filename in os.listdir('diva/nap')]

        self.assertEqual(len(objects), 1)

        ob_name = 'file_name_we_put_remote'

        # put local test files in remote folder
        for ob in objects:
            ob_name = ob.split('/')[-1]
            content = open(ob, 'rb').read()
            content_type = mimetypes.MimeTypes().guess_type(ob)[0]
            if not content_type:
                content_type = "application/octet-stream"
            self.objectstore.put_to_objectstore('naptest/{}'.format(ob_name), content, content_type)

        res = self.objectstore._get_full_container_list([])

        # check if we have a test folder on the object store
        test_file_found = False

        for ob in res:
            if ob_name in ob['name']:
                test_file_found = True
                break

        self.assertTrue(test_file_found)
