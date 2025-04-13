// AutoPIN.cpp
#include <Windows.h>
#include <string>
#include <iostream>

void SendUnicodeChar(wchar_t ch) {
    INPUT input[2] = {};

    input[0].type = INPUT_KEYBOARD;
    input[0].ki.wScan = ch;
    input[0].ki.dwFlags = KEYEVENTF_UNICODE;

    input[1].type = INPUT_KEYBOARD;
    input[1].ki.wScan = ch;
    input[1].ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;

    SendInput(2, input, sizeof(INPUT));
}

void SendText(const std::wstring& text) {
    for (wchar_t ch : text) {
        SendUnicodeChar(ch);
        Sleep(50); // 每个字符间隔
    }
}

int wmain(int argc, wchar_t* argv[]) {
    if (argc < 2) {
        std::wcerr << L"[错误] 未提供 PIN 参数" << std::endl;
        return 1;
    }

    std::wstring pin = argv[1];
    Sleep(3000); // 等待用户切换到锁屏界面
    SendText(pin);

    // 模拟回车键
    INPUT enter = {};
    enter.type = INPUT_KEYBOARD;
    enter.ki.wVk = VK_RETURN;
    SendInput(1, &enter, sizeof(INPUT));
    enter.ki.dwFlags = KEYEVENTF_KEYUP;
    SendInput(1, &enter, sizeof(INPUT));

    return 0;
}
