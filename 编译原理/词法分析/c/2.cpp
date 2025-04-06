#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
#include <iomanip>

using namespace std;
/*
 * +----------------------------------------------------+
 * |  @author: Hearo @Email: hearotop@outlook.com 
 * |  1、check_eight_bit() 检查是否是八进制数  
 * |  2、check_ten_bit() 检查是否是十进制数 
 * |  3、check_hex_bit() 检查是否是十六进制数
 * |  4、main() 主函数，读取用户输入并检查每个数值的类别及其十进制值
 * |  5、_span_hex 十六进制字符集合
 * |  注意事项：
 * |  1、本程序使用标准库的 istream 和 ostream 类，以及一些 STL 算法和容器。
 * |  2、使用g++编译！！！而不是gcc！！！
 *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
 * |                                                                          
 * +----------------------------------------------------+
 */
vector<char> _span_hex = {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

/**
 * @brief 检查字符串是否为八进制数
 * 
 * @param temp 要检查的字符串
 * @return true 如果字符串是八进制数
 * @return false 如果字符串不是八进制数
 */

bool check_eight_bit(const string &temp) // 检查是否是八进制
{
    for (char c : temp)
    {
        if (c < '0' || c > '7')
        {
            return false;
        }
    }
    return true;
}

/**
 * @brief 检查字符串是否为十进制数
 * 
 * @param temp 要检查的字符串
 * @return true 如果字符串是十进制数
 * @return false 如果字符串不是十进制数
 */
bool check_ten_bit(const string &temp) // 检查是否是十进制
{
    for (char c : temp)
    {
        if (!isdigit(c))
        {
            return false;
        }
    }
    return true;
}

/**
 * @brief 检查字符串是否为十六进制数
 * 
 * @param temp 要检查的字符串
 * @return true 如果字符串是十六进制数
 * @return false 如果字符串不是十六进制数
 */
bool check_hex_bit(const string &temp) // 检查是否是十六进制
{
    for (char c : temp)
    {
        if (find(_span_hex.begin(), _span_hex.end(), toupper(c)) == _span_hex.end())
        {
            return false;
        }
    }
    return true;
}

/**
 * @brief 主函数，读取用户输入并检查每个数值的类别及其十进制值
 * 
 * @return int 返回状态码，0 表示成功
 */
int main()
{
    string input;
    cout << "请输入一个字符串：";
    getline(cin, input);

    stringstream ss(input);
    string temp;
    while (ss >> temp)
    {
        if (temp[0] == '0')
        {
            if (temp.length() > 2 && (temp[1] == 'x' || temp[1] == 'X'))
            {
                if (check_hex_bit(temp.substr(2)))
                {
                    try
                    {
                        long decimal_value = stol(temp, nullptr, 16);
                        cout << "(3," << temp << ")" << " 十六进制, 十进制值: " << decimal_value << endl;
                    }
                    catch (const std::invalid_argument &e)
                    {
                        cout << temp << " 无效的十六进制数值" << endl;
                    }
                    catch (const std::out_of_range &e)
                    {
                        cout << temp << " 十六进制数值超出范围" << endl;
                    }
                }
                else
                {
                    cout << temp << " 既不是十六进制也不是八进制还不是十进制" << endl;
                }
            }
            else
            {
                if (check_eight_bit(temp.substr(1)))
                {
                    try
                    {
                        long decimal_value = stol(temp, nullptr, 8);
                        cout << "(2," << temp << ")" << " 八进制, 十进制值: " << decimal_value << endl;
                    }
                    catch (const std::invalid_argument &e)
                    {
                        cout << temp << " 无效的八进制数值" << endl;
                    }
                    catch (const std::out_of_range &e)
                    {
                        cout << temp << " 八进制数值超出范围" << endl;
                    }
                }
                else
                {
                    cout << temp << " 既不是十进制也不是八进制" << endl;
                }
            }
        }
        else
        {
            if (check_ten_bit(temp))
            {
                try
                {
                    long decimal_value = stol(temp);
                    cout << "(1," << temp << ")" << " 十进制, 十进制值: " << decimal_value << endl;
                }
                catch (const std::invalid_argument &e)
                {
                    cout << temp << " 无效的十进制数值" << endl;
                }
                catch (const std::out_of_range &e)
                {
                    cout << temp << " 十进制数值超出范围" << endl;
                }
            }
            else
            {
                cout << temp << " 既不是十进制也不是八进制" << endl;
            }
        }
    }

    return 0;
}