# 关键字全局变量
c_key = [
    "auto", "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "enum", "extern", "float", "for", "goto", "if",
    "int", "long", "register", "return", "short", "signed", "sizeof", "static",
    "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
]

def check_start(check):  # 检查开始是否合乎规范
    return check.isalpha()

def check_import_key(check):  # 检查关键字是否存在
    return check in c_key

def main():
    str_input = input("请输入一个字符串: ")  # 提示用户输入
    if check_start(str_input[0]):
        if check_import_key(str_input):
            print(f"含有关键字 {str_input} 不合法！")
        else:
            print(str_input)
            print("合法！")
    else:
        print(f"含有数字 {str_input[0]} 不合法！")

if __name__ == "__main__":
    main()