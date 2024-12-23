#include<iostream>
#include<direct.h>
#include "begin.h"
#include <chrono>
#include <thread>
#include <cstdio> // 用于 popen
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>



using namespace std;
using json = nlohmann::json;
Begin::Begin() {

}

/*int Begin::begin_exchange(){
  char buffer[128];

  const char* path = "D:\\work\\VirtualDigitalPerson\\llama.cpp\\"
                     "llama.cpp\\build\\bin\\Release"; //指向llama-cli的路径

  if(_chdir(path) == 0){
    cout << "win to change the path" << endl;
  } else {
    cout << "error to change" << endl;
    return 1;
  }

  // 使用完整路径并指定命令
  string command = "llama-server -m D:\\work\\VirtualDigitalPerson\\vicuna\\chinese_q4_0.gguf -c 2048 > nul 2>&1";

  // 打开管道与 llama-cli 进程进行交互
  system(command.c_str());
  return 0;
} */

// 回调函数：将返回的数据存入字符串
size_t WriteCallback(void *ptr, size_t size, size_t nmemb, std::string *data) {
  size_t totalSize = size * nmemb;
  data->append((char*)ptr, totalSize);
  return totalSize;
}

string Begin::send_post_request(const std::string& url, const std::string& postData) {
    CURL* curl;
    CURLcode res;
    string responseData;

    // 初始化 libcurl
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl) {
        // 设置目标URL
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        // 设置POST请求
        curl_easy_setopt(curl, CURLOPT_POST, 1L);

        // 设置POST数据
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData.c_str());

        // 设置请求头，指定发送内容为JSON格式
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // 设置回调函数，用于处理返回数据
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseData);

        // 执行请求
        res = curl_easy_perform(curl);

        // 检查请求是否成功
        if (res != CURLE_OK) {
            std::cerr << "请求失败: " << curl_easy_strerror(res) << std::endl;
            curl_easy_cleanup(curl);
            curl_global_cleanup();
            return "";  // 请求失败，返回空字符串
        }



        // 解析JSON响应
        try {
            // 解析返回的JSON字符串
            json responseJson = json::parse(responseData);

            // 从JSON中提取content字段
            if (responseJson.contains("choices") && responseJson["choices"].is_array() && !responseJson["choices"].empty()) {
                // 获取message中的content
                string content = responseJson["choices"][0]["message"]["content"].get<string>();
                return content;  // 返回提取到的content字段
            } else {
                std::cerr << "JSON解析失败，未找到有效的'content'字段" << std::endl;
                return "";  // 返回空字符串
            }
        } catch (const json::exception& e) {
            std::cerr << "JSON解析错误: " << e.what() << std::endl;
            return "";  // 解析错误，返回空字符串
        }

        // 清理
        curl_easy_cleanup(curl);
    }

    // 清理 libcurl
    curl_global_cleanup();

    return "";  // 如果没有进入if块，返回空字符串
}



