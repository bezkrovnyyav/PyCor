'''
Write an algorithm that will identify valid IPv4 addresses in dot-decimal format. 
IPs should be considered valid if they consist of four octets, with values between 0 and 255, inclusive.

Note: Create the main class for that task and the descriptor for getting and setting ip values.
'''


ip_1 = "1.2.3.4" 
ip_2 = "123.045.067.089"
ip_3 = "123.456.78.90"


class IPAddressException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class IPValidater():
    
    def __init__(self, ip_num):
        self.ip_num = ip_num
        
    def __get__(self, ip_num):
        return self.ip_num

    def __set__(self):
        if self.ip_num:
            exception_message = f"{self.ip_num} is incorrect ip"
            list_num_ip = self.ip_num.split(".")
            if len(list_num_ip) != 4:
                raise IPAddressError(exception_message)
            for i in list_num_ip:
                if i.isdigit():
                    if int(i) > 255 or i[0] == "0" or int(i) < 0:
                        raise IPAddressException(exception_message)
                else:
                    raise IPAddressException(exception_message)
        return f'{self.ip_num} is correct ip'


if __name__ == "__main__":
    ip_validater = IPValidater(ip_2)
    print(ip_validater.__set__())
