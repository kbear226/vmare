#!/usr/bin/env python3.9

import unittest
import donothing
import filecmp


class TestDoNothing(unittest.TestCase):

    def setUp(self):
        self.dn = donothing.DoNothings()
        self.arg_c = donothing.args.c
        self.arg_b = donothing.args.b

    def testFileArgsCheckResponse(self):
        donothing.args.c = "test"
        self.assertIsNone(donothing.DoNothings().run())
        donothing.args.c = self.arg_c

    def testCopyBinaryFileArgResponse(self):
        donothing.args.b = "test"
        self.assertIsNone(donothing.DoNothings().run())
        donothing.args.b = self.arg_b

    def testCopyBinaryFile(self):
        self.dn.CopyBinaryFile("vmare_image.bin", "output.bin")
        self.assertTrue(filecmp.cmp("vmare_image.bin", "output.bin", shallow=True))

    def testExtractUniqueNumberCount(self):
        lst = [1,2,2,3,4,5,4]
        self.assertEqual(3, self.dn.ExtractUniqueNumberCount(lst))

    def testExtractCarbonBlackSiteLocations(self):
        self.dn.ExtractCarbonBlackSiteLocations("location_test")
        self.assertTrue(filecmp.cmp("output", "location_test", shallow=True))

    def testExtractPhoneNumbers(self):
        self.dn.ExtractPhoneNumbers("name_numbers.txt", "numbers_test_output")
        self.assertTrue(filecmp.cmp("name_numbers_test", "numbers_test_output", shallow=True))


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
