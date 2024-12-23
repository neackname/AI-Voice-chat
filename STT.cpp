#include <iostream>
#include <fstream>
#include <string>
#include <future>
#include <thread>
#include <map>
#include <sstream>
#include <cstdlib>
#include "begin.h"

using namespace std;

STT :: STT(){}

string STT::speech_to_text()
{
    stringstream ss;
    auto py_prog = async(launch::async, [&ss]()
    {
        string cmd = "python D:\\studycode\\untitled\\py\\STT.py";

#ifdef _WINDOWS
        FILE* in = _popen(cmd.c_str(), "r");
        if (in == nullptr)
        {
            ss << "Failed to open Python script (popen failed)." << endl;
            return;
        }
#else
        FILE* in = popen(cmd.c_str(), "r");
        if (in == nullptr)
        {
            ss << "Failed to open Python script (popen failed)." << endl;
            return;
        }
#endif

        char buf[2048];
        while (fgets(buf, sizeof(buf), in) != NULL)
        {
            ss << buf;
        }

        int exit_code = pclose(in); // Check the exit code of the process
        if (exit_code != 0)
        {
            ss << "Python script exited with a non-zero status: " << exit_code << endl;
        }
    });

    py_prog.wait(); // Wait for the async task to finish
    string strRet = ss.str();
    return strRet;
}


