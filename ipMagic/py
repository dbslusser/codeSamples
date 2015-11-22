import socket, struct

def dec2bin(value, bit_length=8):
    """
    Description:
        Convert a decimal value to a binary with a given length 
    
    Parameters:
        value      - integer value
        bit_length - number of bits in binary representation 
            
    Returns:
        Binary representation of an binary number
    """
    return bin(value)[2:].zfill(bit_length)

def long2ip(x):
    """ 
    Description:
        Convert a long to an IPv4 address
    
    Parameters:
        x - long integer 
    Returns:
        IPv4 address as a string in dotted-decimal format
    """
    return socket.inet_ntoa(struct.pack('!L', x))

def bin2ip(x):
    """
    Description:
        Convert a binary number to an IPv4 address 
    
    Parameters:
        x - binary number as a string
        
    Returns:
        IPv4 address as a string in dotted-decimal format
    """
    return long2ip(int(x, 2))

def ip2bin(ip_addr):
    """
    Description:
        Convert an IPv4 address to a binary number
        
    Parameters:
        ip_addr - IPv4 address provided as a string in dotted-decimal format 
    
    Returns:
        Binary representation of an IPv4 address
    """
    return ''.join([bin(int(x)+256)[3:] for x in ip_addr.split('.')])
    
    
    
class IpMagic():
    """
    Description:
        Represent an IPv4 into meaningful fields of arbitrary lengths
    
    Parameters:
        bit_length_list - list of integers representing field bit lengths
    """
    def __init__(self, bit_length_list):
        """ class entry point """
        self.bit_length_list = bit_length_list
        self.bit_list_count = len(self.bit_length_list)
        self.verifyBitTotal()

    def verifyBitTotal(self):
        """ Verify the total number of bits equals 32 """
        if sum(self.bit_length_list) != 32:
            raise Exception("field bit lengths total %s, expected 32" % sum(self.bit_length_list))

    def verifyValues(self, value_list):
        """ 
        Description:
            Verify number of values match bit format 
        
        Parameters:
            value_list - list of integers 
        """
        value_list_count = len(value_list)
        if value_list_count != self.bit_list_count:
            raise Exception("%s values required; %s provided" % (self.bit_list_count, value_list_count))
    
    def combine(self, value_list):
        """
        Description:
            Construct an IPv4 address from a list of integers
        
        Parameters:
            value_list - list of integers representing the value 
                         of the corresponding index of the field 
                         length taken by the constructor
        
        Returns:
            IPv4 address in dotted-decimal format
        """
        self.verifyValues(value_list)
        bin_number = ""
        for e, v in enumerate(value_list):
            bl = self.bit_length_list[e]
            x = dec2bin(v, bl)
            bin_number += x
        return bin2ip(bin_number)
        
    def uncombine(self, ip_addr):
        """
        Description:
            Break an IPv4 address into a list of integers
        
        Parameters:
            ip_addr - IPv4 address provided as a string in 
                      dotted-decimal format   
        
        Returns:
            A list of integers representing the value of the 
            corresponding index of the field length taken by 
            the constructor 
        """
        resp = []
        b = ip2bin(ip_addr)
        start = 0
        end = 0
        for i in self.bit_length_list:
            end += i
            bit_slice = b[start:end]
            resp.append(int(bit_slice, 2))
            start = end
        return resp
