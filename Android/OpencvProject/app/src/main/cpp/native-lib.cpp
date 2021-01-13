#include <jni.h>
#include <string>

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_opencvproject_MainActivity_stringFromJNI(
        JNIEnv* env,
        jobject /* this */) {
    std::string hello = "Hello from C++";
    return env->NewStringUTF(hello.c_str());
}


#include <opencv2/opencv.hpp>
using namespace cv;

extern "C"
JNIEXPORT void JNICALL
Java_com_example_opencvproject_MainActivity_process(JNIEnv *env, jobject thiz, jlong mat_input_addr,
                                                    jlong mat_result_addr) {
    Mat &input = *(Mat *)mat_input_addr;
    Mat &result = *(Mat *)mat_result_addr;

    cvtColor(input, result, COLOR_BGR2GRAY);
}

