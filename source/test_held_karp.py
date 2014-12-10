#!/usr/bin/env python2.7
"""Testing module for several example TSPs."""

import unittest

import held_karp
import q1

class TestHeldKarp(unittest.TestCase):
    """unittest module for testing the held-karp algo on example
    TSPs."""

    @staticmethod
    def read_process_tsp(file_name):
        """Reads in a TSP problem from file and runs Held-Karp"""
        file_ = open(file_name, 'rb')
        count, cities = q1.parse_cities(file_)
        return held_karp.held_karp_dicts(cities, count, False)

    @staticmethod
    def read_process_tsp2(file_name):
        """Reads in a TSP problem from file and runs Held-Karp"""
        file_ = open(file_name, 'rb')
        count, cities = q1.parse_cities(file_)
        return held_karp.held_karp_scipy(cities, count, False)

    def test_tsp_examples(self):
        """Test several TSP examples."""
        actual1 = TestHeldKarp.read_process_tsp('../data/tsp2.txt')
        self.assertEqual(actual1, 4.0)

        actual2 = round(TestHeldKarp.read_process_tsp('../data/tsp3.txt'), 4)
        self.assertEqual(actual2, 10.4721)

        actual3 = round(TestHeldKarp.read_process_tsp('../data/tsp4.txt'), 5)
        self.assertEqual(actual3, 6.17986)

        actual4 = round(TestHeldKarp.read_process_tsp('../data/tsp5.txt'), 5)
        self.assertEqual(actual4, 6.26533)

        actual5 = round(TestHeldKarp.read_process_tsp('../data/tsp6.txt'), 3)
        self.assertEqual(actual5, 124.966)

        actual6 = round(TestHeldKarp.read_process_tsp('../data/tsp8.txt'), 1)
        self.assertEqual(actual6, 16898.1)

        actual7 = round(TestHeldKarp.read_process_tsp('../data/tsp9.txt'), 1)
        self.assertEqual(actual7, 26714.9)

    def test_tsp_examples2(self):
        """Test several TSP examples."""
        actual1 = TestHeldKarp.read_process_tsp2('../data/tsp2.txt')
        self.assertEqual(actual1, 4.0)

        actual2 = round(TestHeldKarp.read_process_tsp('../data/tsp3.txt'), 4)
        self.assertEqual(actual2, 10.4721)

        actual3 = round(TestHeldKarp.read_process_tsp('../data/tsp4.txt'), 5)
        self.assertEqual(actual3, 6.17986)

        actual4 = round(TestHeldKarp.read_process_tsp('../data/tsp5.txt'), 5)
        self.assertEqual(actual4, 6.26533)

        actual5 = round(TestHeldKarp.read_process_tsp('../data/tsp6.txt'), 3)
        self.assertEqual(actual5, 124.966)

        actual6 = round(TestHeldKarp.read_process_tsp('../data/tsp8.txt'), 1)
        self.assertEqual(actual6, 16898.1)

        actual7 = round(TestHeldKarp.read_process_tsp('../data/tsp9.txt'), 1)
        self.assertEqual(actual7, 26714.9)

if __name__ == '__main__':
    unittest.main(exit=False)
