cmake_minimum_required(VERSION 3.30)
project(untitled)

set(CMAKE_CXX_STANDARD 20)

find_package(CURL REQUIRED)
#include_directories(${CURL_INCLUDE_DIR})

add_executable(Azure main.cpp begin.cpp STT.cpp TTS.cpp)
#target_include_directories(Azure PRIVATE ${CURL_INCLUDE_DIR})
target_link_libraries(Azure PRIVATE CURL::libcurl)

