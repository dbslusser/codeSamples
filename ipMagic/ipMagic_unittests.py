
import unittest
from ipMagic import *


class TestIpMagic(unittest.TestCase):
    
    def testBitsOver32(self):
        field_bit_lengths = [8,8,8,9]
        self.failUnlessRaises(Exception, IpMagic, field_bit_lengths)

    def testBitsUnder32(self):
        field_bit_lengths = [8,8,8,7]
        self.failUnlessRaises(Exception, IpMagic, field_bit_lengths)

    def testBitListMismatch(self):
        field_bit_lengths = [8,8,8,8]
        field_bit_values  = [10, 4, 0, 1, 4, 30]
        magic = IpMagic(field_bit_lengths)
        self.failUnlessRaises(Exception, magic.combine, field_bit_values)        

    def testCombineEqualOne(self):
        field_bit_lengths = [8,8,8,8]
        field_bit_values  = [10,20,30,40]
        expected_response = "10.20.30.40"
        magic = IpMagic(field_bit_lengths)
        self.assertEqual(magic.combine(field_bit_values), expected_response)
        
    def testCombineEqualTwo(self):
        field_bit_lengths = [8, 5, 4, 5, 4, 6]
        field_bit_values  = [10, 4, 0, 1, 4, 30]
        expected_response = "10.32.5.30"
        magic = IpMagic(field_bit_lengths)
        self.assertEqual(magic.combine(field_bit_values), expected_response)       

    def testCombineUnequal(self):
        field_bit_lengths = [8, 5, 4, 5, 4, 6]
        field_bit_values  = [10, 4, 0, 1, 4, 30]
        expected_response = "10.32.5.31"
        magic = IpMagic(field_bit_lengths)
        self.assertNotEqual(magic.combine(field_bit_values), expected_response) 

    def testUncombineEqualOne(self):
        field_bit_lengths = [8,8,8,8]
        ip_addr = "10.20.30.40"
        expected_response = [10,20,30,40]
        magic = IpMagic(field_bit_lengths)
        self.assertEqual(magic.uncombine(ip_addr), expected_response) 

    def testUncombineEqualTwo(self):
        field_bit_lengths = [8, 5, 4, 5, 4, 6]
        ip_addr = "10.32.5.30"
        expected_response = [10, 4, 0, 1, 4, 30]
        magic = IpMagic(field_bit_lengths)
        self.assertEqual(magic.uncombine(ip_addr), expected_response) 

    def testUncombineUnequal(self):
        field_bit_lengths = [8, 5, 4, 5, 4, 6]
        ip_addr = "10.32.5.31"
        expected_response = [10, 4, 0, 1, 4, 30]
        magic = IpMagic(field_bit_lengths)
        self.assertNotEqual(magic.uncombine(ip_addr), expected_response) 


if __name__ == '__main__':
    unittest.main()
