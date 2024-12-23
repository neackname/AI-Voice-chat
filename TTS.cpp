#include <iostream>
#include <cstdlib>
#include <string>
#include "begin.h"
using namespace std;

TTS::TTS(){}

void TTS::text_to_speech(string text) {
    string command = "python D:\\studycode\\untitled\\py\\TTS.py \"" + text + "\"";
    int result = system(command.c_str());

    if (result != 0) {
        cout << "TTS::text_to_speech() failed: " << endl;
    }
}

