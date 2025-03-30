#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>    // 引入vector头文件
#include <string>    // 引入string头文件
#include <cctype>  // 引入cctype头文件
#include <iostream>  
using namespace std;
/*
 * +----------------------------------------------------+
 * |  @author: Hearo @Email: hearotop@outlook.com                                                    
 * |  这段代码是一个简单的词法分析器，用于检查输入字符串是否以字母开头，并判断该字符串是否为C语言的关键字。
 * |                                                    
 * |  主要功能包括：                                     
 * |  1. 定义了一个包含C语言关键字的全局向量c_key。     
 * |  2. check_start函数用于检查字符串是否以字母开头。  
 * |  3. check_import_key函数用于检查字符串是否为C语言关键字。
 * |  4. main函数中，程序提示用户输入一个字符串，然后根据上述两个函数的结果输出相应的合法性判断。
 * |                                                    
 * |  注意事项：                                         
 * |  - 如果输入字符串以数字或特殊字符开头，则直接判断为不合法。
 * |  - 如果输入字符串是C语言关键字，则判断为不合法。    
 * |  - 否则，判断为合法。                                                                              
 * +----------------------------------------------------+
 */
//关键字全局变量
vector<string> c_key = {
    "auto", "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "enum", "extern", "float", "for", "goto", "if",
    "int", "long", "register", "return", "short", "signed", "sizeof", "static",
    "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
};
bool check_start(char check)//检查开始是否合乎规范
{
   
return isalpha(check);//

}
bool check_import_key(string check)//检查关键字是否存在
{
    int i=0;
    for (i; i < c_key.size(); i++)
    {
        if (check == c_key[i])
        {
            return true;
        }
    }
    
    return false;
}
int main()
{
    
    string str_input;  // 使用std::string
    cout << "请输入一个字符串: ";  // 提示用户输入
    cin >> str_input;  // 正确的输入方式
    if(check_start(str_input[0]))
       {
        if(check_import_key(str_input))
        {
            cout << "含有关键字" << str_input << "不合法！" << endl; // 输出检查的字符串而不是 c_key[i]
         
            return 0;
        }
        else
        {
            cout<<str_input<<endl;
            cout<<"合法！"<<endl;
            return 0;
        }
       
       } 
        else
        {
            cout<<"c_key"<<endl;
            cout<<"含有数字"<<str_input[0]<<"不合法！"<<endl;
            return 0;

        } 
      return 0;  
}