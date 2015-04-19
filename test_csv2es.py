## Copyright 2015 Ray Holder
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import csv2es
import unittest


class TestDelimiter(unittest.TestCase):

    def test_sanitize(self):
        self.assertEqual(None, csv2es.sanitize_delimiter(None, False))
        self.assertEqual(str('\t'), csv2es.sanitize_delimiter(None, True))
        self.assertEqual(str('|'), csv2es.sanitize_delimiter('|', False))
        self.assertEqual(str('|'), csv2es.sanitize_delimiter(u'|', False))
        self.assertEqual(str('\t'), csv2es.sanitize_delimiter('|', True))
        self.assertEqual(str('\t'), csv2es.sanitize_delimiter('||', True))
        self.assertRaises(Exception, csv2es.sanitize_delimiter, '||', False)


class TestLoading(unittest.TestCase):

    def test_csv(self):
        # TODO fill this in
        self.assertTrue(True)

    def test_tsv(self):
        # TODO fill this in
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
