//
// Created by Administrator on 24-12-17.
//


#ifndef BEGIN_H
#define BEGIN_H


class Begin {
public:
    Begin();
    int begin_exchange();
    std::string send_post_request(const std::string& url, const std::string& data);
    void sendPostRequest(const std::string& prompt);
};

class STT {
public:
    STT();
    std::string speech_to_text();
};

class TTS {
    public:
    TTS();
    void text_to_speech(std::string text);
};


#endif //BEGIN_H
