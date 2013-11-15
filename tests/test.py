#!/usr/bin/env python

import os
import shlex
import sys
import unittest

import MySQLdb

class PdbCheckMaxValueTest(unittest.TestCase):

    def setUp(self):
        self.mysql_user = os.getenv('PDB_TEST_MYSQL_USER', 'root')
        self.mysql_pass = os.getenv('PDB_TEST_MYSQL_PASS', '')

        # Append module directory to path so we can import the plugin and create db connection
        ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.append(ROOT_DIR)
        from int_overflow_check.pdb_check_maxvalue import main
        self.main = main

        conn_opts = {}
        if self.mysql_user:
            conn_opts['user'] = self.mysql_user
        if self.mysql_pass:
            conn_opts['passwd'] = self.mysql_pass
        # Connect to MySQL, Make sure that MySQL user has CREATE grant
        self.db = MySQLdb.connect(**conn_opts)
        cursor = self.db.cursor()

        # Create Test Database
        cursor.execute('CREATE SCHEMA pdbmaxcheck_test;')
        cursor.execute('USE pdbmaxcheck_test;')
        cursor.execute('''
            CREATE TABLE `tbl_test` (
              `intcol` int(11) NOT NULL,
              `tinyintcol` tinyint(4) DEFAULT NULL,
              `smallintcol` smallint(6) DEFAULT NULL,
              `bigintcol` bigint(20) DEFAULT NULL,
              `integercol` int(10) unsigned DEFAULT NULL,
              `intcol1` int(10) unsigned DEFAULT NULL,
              PRIMARY KEY (`intcol`)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
        ''')
        cursor.execute('LOCK TABLES `tbl_test` WRITE;')
        cursor.execute(
            'INSERT INTO `tbl_test` '
            'VALUES '
            '    (1147483647,60,8442,31314242424242442,3535353,4294967295);')
        cursor.execute('UNLOCK TABLES;')

    def test_check_max_value_ok(self):
        params = (
            '-d pdbmaxcheck_test '
            '--row-count-max-ratio 0 '
            '--display-row-count-max-ratio-columns '
            )
        if self.mysql_user:
            params += '-u %s ' % self.mysql_user
        if self.mysql_pass:
            params += '-p %s ' % self.mysql_pass
        exit_code = self.main(shlex.split(params))
        self.assertEqual(exit_code, 0)

    def test_check_max_value_warning(self):
        params = (
            '-d pdbmaxcheck_test --warning 25 --critical 100 '
            '--row-count-max-ratio 0 '
            '--display-row-count-max-ratio-columns '
            )
        if self.mysql_user:
            params += '-u %s ' % self.mysql_user
        if self.mysql_pass:
            params += '-p %s ' % self.mysql_pass
        exit_code = self.main(shlex.split(params))
        self.assertEqual(exit_code, 1)

    def test_check_max_value_critical(self):
        params = (
            '-d pdbmaxcheck_test --warning 20 --critical 25 '
            '--row-count-max-ratio 0 '
            '--display-row-count-max-ratio-columns '
            )
        if self.mysql_user:
            params += '-u %s ' % self.mysql_user
        if self.mysql_pass:
            params += '-p %s ' % self.mysql_pass
        exit_code = self.main(shlex.split(params))
        self.assertEqual(exit_code, 2)

    def tearDown(self):
        # Drop Test DATABASE
        cursor = self.db.cursor()
        cursor.execute('DROP SCHEMA pdbmaxcheck_test')
        # Close DB connection
        self.db.close()

if __name__ == '__main__':
    unittest.main()
