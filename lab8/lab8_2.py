'''
ISBN-10 or IP modifications¶
Update the decorator used for task from lab4 (choose ISBN-10 or IP) to be the class with overrided method __call__().
'''


from re import search
from functools import wraps


class ISBNDecoder:

    def __call__(self, func):  
        @wraps(isbn)
        def wrapped(isbn):
            checker = search("[0-9]{9}[X0-9]{1}", isbn)
            sum_numbers = 0

            if checker and len(isbn) == 10:
                res = isbn.split()
            for i in range(len(res)):
                if res[i] == "X":
                    res[i] = 10
                sum_numbers += int(isbn[i]) * (i + 1)
            if sum_numbers % 11 == 0:
                print(f"{isbn} is correct ISBN")
      
            else:
                print(f"{isbn} is incorrect ISBN")
   
        return wrapped


if __name__ == '__main__':
    isbn = "048665088X"
    
    
    @ISBNDecoder()
    def isbn_checker(isbn):
        return isbn
        
        
    isbn_checker(isbn)
