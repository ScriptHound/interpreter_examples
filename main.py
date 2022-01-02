import operator


class Interpreter:
    
    def tokenize(self, string):
        tokenized = string.split()
        return tokenized


if __name__ == '__main__':
    inter = Interpreter()

    test_string = '2 + 2 - 2'
    print(inter.tokenize(test_string))
