class Parser:
    def __init__(self, input_str):
        """
        初始化解析器。

        参数：
        input_str (str): 要解析的输入字符串。
        """
        self.input_str = input_str  # 输入字符串
        self.pos = 0  # 当前字符位置
        self.current_token = None  # 当前词法单元
        self.next_token()  # 获取第一个词法单元

    def next_token(self):
        """
        获取下一个词法单元。

        跳过空白字符，并识别数字和运算符。
        """
        while self.pos < len(self.input_str) and self.input_str[self.pos].isspace():
            self.pos += 1  # 跳过空白字符
        if self.pos >= len(self.input_str):
            self.current_token = ('$', '$')  # 到达输入字符串末尾
        else:
            char = self.input_str[self.pos]
            if char.isdigit():
                self.current_token = ('num', char)  # 数字
            else:
                self.current_token = (char, char)  # 运算符或括号
            self.pos += 1  # 移动到下一个字符

    def match(self, expected_token):
        """
        匹配当前词法单元是否为期望的词法单元。

        参数：
        expected_token (str): 期望的词法单元类型。

        抛出异常：
        Exception: 如果当前词法单元与期望的词法单元不匹配。
        """
        if self.current_token[0] == expected_token:
            self.next_token()  # 获取下一个词法单元
        else:
            raise Exception(f"错误位置 {self.pos - 1}: 期望 '{expected_token}', 但得到 '{self.current_token[1]}'")

    def E(self):
        """
        解析表达式 E。

        E → TE'
        """
        self.T()
        self.E_prime()

    def E_prime(self):
        """
        解析表达式 E'。

        E' → +TE' | -TE' | ε
        """
        if self.current_token[0] == '+':
            self.match('+')
            self.T()
            self.E_prime()
        elif self.current_token[0] == '-':
            self.match('-')
            self.T()
            self.E_prime()
        else:
            pass  # ε (空串)

    def T(self):
        """
        解析项 T。

        T → FT'
        """
        self.F()
        self.T_prime()

    def T_prime(self):
        """
        解析项 T'。

        T' → *FT' | /FT' | ε
        """
        if self.current_token[0] == '*':
            self.match('*')
            self.F()
            self.T_prime()
        elif self.current_token[0] == '/':
            self.match('/')
            self.F()
            self.T_prime()
        else:
            pass  # ε (空串)

    def F(self):
        """
        解析因子 F。

        F → num | (E)
        """
        if self.current_token[0] == 'num':
            self.match('num')
        elif self.current_token[0] == '(':
            self.match('(')
            self.E()
            self.match(')')
        else:
            raise Exception(f"错误位置 {self.pos - 1}: 期望 'num' 或 '(', 但得到 '{self.current_token[1]}'")

    def parse(self):
        """
        开始解析输入字符串。
        """
        self.E()
        if self.current_token[0] != '$':
            raise Exception(f"错误: 意外的词法单元 '{self.current_token[1]}'")
        print("解析成功!")

# 测试用例
valid_expressions = ["(2)", "(2+3)", "(8-2)*3", "(8-2)/3", "(2-8+2+3/2-2)/3"]
invalid_expressions = ["(3+4*5))", "2+3+"]

for expr in valid_expressions:
    print(f"解析: {expr}")
    parser = Parser(expr)
    try:
        parser.parse()
    except Exception as e:
        print(e)

for expr in invalid_expressions:
    print(f"解析: {expr}")
    parser = Parser(expr)
    try:
        parser.parse()
    except Exception as e:
        print(e)