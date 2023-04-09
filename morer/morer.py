from util.logger import log

#定义2个列表用来存储待分析的关键字，特殊符号
KeyWord = ['begin', 'integer', 'char', 'program', 'array', 'of', 'record', 'end',
            'var', 'procedure', 'if', 'then', 'else', 'fi', 'while', 'do', 'endwh',
            'read', 'write', 'return', 'type']
SpecialSymbol= ['+' , '-' , '*' , '/' , '(' , ')' , '[' , ']' , ';' , '<' , '=', ':=' , '..' , ',']

#为了保存行数，用类封存
class Token(list):
    # type = ""
    # value = ""
    # line = 1

    def __init__(self, type, value, line):
        self.append(type)
        self.append(value)
        self.append(line)
        # self.type = type
        # self.value = value
        # self.line = line

    def __str__(self):
        return ("<{}|{}|{}>".format(self[0], self[1], self[2]))
    
    def __repr__(self):
        return ("<{}|{}|{}>".format(self[0], self[1], self[2]))

#为了保存和输出error
class Error():
    value = ""
    line = 1

    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __str__(self):
        return ("Error: < line: {}, value: {} >".format(self.line, self.value))

#用来判断一个字符是否是字符
def isLetter(Char):
    if ((Char >= 'a' and Char <= 'z') or (Char >= 'A' and Char <= 'Z')):
        return True
    else:
        return False

#用来判断一个字符是否是大写字符
def isCapitalLetter(Char):
    if(Char >= 'A' and Char <= 'Z'):
        return True
    else:
        return False

#用来判断一个字符是否是数字
def isDigit(Char):
   if (Char <= '9' and Char >= '0'):
      return True
   else:
      return False

#用来判断一个字符是否是空格
def isSpace(Char):
   if (Char == ' '):
      return True
   else:
      return False

#将读入的代码文件中的关键字，标识符，运算符等进行分离
def fenli(List):
    Flag = False #用于标识是否跳过一次循环
    Flag2 = False
    ResultList = list()
    line = 0
    for String in List:
        line += 1
        Letter = ''
        index = 0
        for Char in String:
            if(Flag):
                Flag = False
                index += 1
                continue
            if(Flag2):
                if(Char == '}'):
                    Flag2 = False
                index += 1
                continue

            if (index < len(String) - 1):
                index += 1
                if (isLetter(Char) or isDigit(Char)):
                    if (isLetter(String[index]) or isDigit(String[index])):
                        Letter += Char
                    else:
                        Letter += Char
                        ResultList.append((Letter,line))
                        Letter = ''
                elif Char in SpecialSymbol:
                    ResultList.append((Char,line))
                elif (Char == ':'):
                    if (String[index] == '='):
                        Flag = True
                        Letter += Char
                        Letter += String[index]
                        ResultList.append((Letter,line))
                        Letter = ''
                    else:
                        ResultList.append((Char,line))
                elif(Char == '.'):
                    if (String[index] == '.'):
                        Flag = True
                        Letter += Char
                        Letter += String[index]
                        ResultList.append((Letter,line))
                        Letter = ''
                    else:
                        ResultList.append((Char,line))
                elif(Char == '{'):
                    Flag2 = True
                elif isSpace(Char):
                    pass
                else:
                    Letter += Char
                    ResultList.append((Letter,line))
                    Letter = ''

            elif (index == len(String) - 1):
                if(Letter == ''):
                    ResultList.append((Char,line))
                else:
                    Letter += Char
                    ResultList.append((Letter,line))
                    Letter = '' 
         
    return ResultList

#判断分离出来字符所属的类别并输出
def panduan(Tlist):
    f = open('out.txt','w')
    TokenList = []
    for i in Tlist:
        if i[0] in KeyWord:
            message = Token(i[0].upper(), i[0], i[1])
            TokenList.append(message)
        elif i[0] in SpecialSymbol:
            message = Token(i[0], i[0], i[1])
            TokenList.append(message)
        elif i[0].isdigit():
            message = Token('INTC', i[0], i[1])
            TokenList.append(message)
        elif (i[0].isalnum() and isLetter(i[0][0])):
            message = Token('ID', i[0], i[1])
            TokenList.append(message)
        elif (i[0] == '.'):
            message = Token(i[0], i[0], i[1])
            TokenList.append(message)
        else:
            message = Error(i[0],i[1])
            raise Exception('morer--' + message.__str__())
            
    tokensText = '\n'.join(map(lambda x: x.__str__(), TokenList))
    print(tokensText, file = f)
    f.close() 

    return TokenList

#主函数
def run(snlText: str):
    p = []
    w = []
    tokensText = ''
    tokenList = []
    #m = f.readlines()
    #log(m)
    m = snlText.split('\n')
    for i in m:
        n = i.strip()
        p.append(n)
    #w.append('v1')
    y = fenli(p)
    #log(y)
    tokenList = panduan(y)
    return tokenList 

if __name__ == '__main__':
    with open("test.txt", 'r') as f:
        text = f.readlines()
        log(run(text))
