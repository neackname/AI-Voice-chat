#include <future>
#include <iostream>
#include "begin.h"
#include <windows.h>
#include <thread>
#include <nlohmann/json.hpp>

using namespace std;
void speech_to_text_async(STT* stt, promise<std::string>&& p) {
    // 语音转文本操作
    std::string result = stt->speech_to_text(); // 模拟语音转文本
    // 设置返回值
    p.set_value(result);
}



int main() {
    SetConsoleOutputCP(CP_UTF8);

    // 创建 promise 和 future 用于获取语音转文本的结果
    std::promise<std::string> textPromise;
    std::future<std::string> textFuture = textPromise.get_future();

    STT stt;

    // 启动语音转文本线程
    std::thread speechThread(speech_to_text_async, &stt, std::move(textPromise));
    std::cout << "Speech-to-text thread started." << std::endl;  // 打印线程启动信息

    // 启动大模型加载线程



    // 线程阻塞直到获取文本
    std::string speechText = textFuture.get();
    std::cout << "Received speech text: " << speechText << std::endl;  // 打印获取到的文本
    std::cout.flush();  // 强制刷新输出

    // 等待语音转文本线程完成
    speechThread.join();



    // 传递url和文本进行 POST 请求


    const string url = "http://127.0.0.1:8080/v1/chat/completions";
    nlohmann::json requestData;
    requestData["model"] = "gpt-3.5-turbo";
    requestData["max_tokens"] = 500;
    requestData["messages"] = {
        {{"role", "system"}, {"content", "You are a helpful assistant."}},
        {{"role", "user"}, {"content", speechText}}
    };

    // 将 JSON 对象转换为字符串
    string postData = requestData.dump();  // dump() 自动处理转义

    Begin begin;
    string mxm = "什么是语音助手？";
    std::cout<<"生成回答：\n"<<begin.send_post_request(url, postData);;
    string response =begin.send_post_request(url, postData);
    TTS tts;
    tts.text_to_speech(response);
    return 0;
}