#include <jni.h>
#include <string>

#include "opencv2/opencv.hpp"
using namespace cv;

extern "C"
JNIEXPORT void JNICALL
Java_com_example_opencvcamera_MainActivity_process(JNIEnv *env, jobject thiz, jlong mat_input_addr, jlong mat_result_addr) {
    Mat &input = *(Mat *)mat_input_addr;
    Mat &result = *(Mat *)mat_result_addr;

    cvtColor(input, result, COLOR_BGR2GRAY);
}



