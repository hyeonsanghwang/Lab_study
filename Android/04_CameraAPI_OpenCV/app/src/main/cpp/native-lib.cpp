#include <jni.h>
#include <string>
#include "opencv2/opencv.hpp"
using namespace cv;

extern "C"{
    static const int kMaxChannelValue = 262143;
    static inline jlong YUV2RGB(int nY, int nU, int nV) {
        nY -= 16;
        nU -= 128;
        nV -= 128;
        if (nY < 0)
            nY = 0;

        // This is the floating point equivalent. We do the conversion in integer
        // because some Android devices do not have floating point in hardware.
        // nR = (int)(1.164 * nY + 2.018 * nU);
        // nG = (int)(1.164 * nY - 0.813 * nV - 0.391 * nU);
        // nB = (int)(1.164 * nY + 1.596 * nV);

        int nR = (int)(1192 * nY + 1634 * nV);
        int nG = (int)(1192 * nY - 833 * nV - 400 * nU);
        int nB = (int)(1192 * nY + 2066 * nU);

        nR = MIN(kMaxChannelValue, MAX(0, nR));
        nG = MIN(kMaxChannelValue, MAX(0, nG));
        nB = MIN(kMaxChannelValue, MAX(0, nB));

        nR = (nR >> 10) & 0xff;
        nG = (nG >> 10) & 0xff;
        nB = (nB >> 10) & 0xff;

        return 0xff000000 | (nR << 16) | (nG << 8) | nB;
    }

    JNIEXPORT void JNICALL
    Java_com_example_cameraapiopencv_ImageProcessing_convert_1YUV420_1to_1ARGB8888(JNIEnv *env, jclass instance, jbyteArray yDataArr,
            jbyteArray uDataArr, jbyteArray vDataArr, jintArray outputArr, jint width, jint height,
            jint y_row_stride, jint uv_row_stride, jint uv_pixel_stride){

        jbyte *yData = (*env).GetByteArrayElements(yDataArr, 0);
        jbyte *uData = (*env).GetByteArrayElements(uDataArr, 0);
        jbyte *vData = (*env).GetByteArrayElements(vDataArr, 0);
        jint *output = (*env).GetIntArrayElements(outputArr, 0);
        jint *out = output;


        for (int y = 0; y < height; y++) {
            const jbyte* pY = yData + y_row_stride * y;

            const int uv_row_start = uv_row_stride * (y >> 1);
            const jbyte* pU = uData + uv_row_start;
            const jbyte* pV = vData + uv_row_start;

            for (int x = 0; x < width; x++) {
                const int uv_offset = (x >> 1) * uv_pixel_stride;
                *out++ = (unsigned int)YUV2RGB((unsigned char)pY[x], (unsigned char)pU[uv_offset], (unsigned char)pV[uv_offset]);
            }
        }
    }
}

extern "C"
JNIEXPORT void JNICALL
Java_com_example_cameraapiopencv_ImageProcessing_processing(JNIEnv *env, jclass clazz,
                                                            jlong input_addr, jlong output_addr) {
    Mat &matInput = *(Mat *) input_addr;
    Mat &matResult = *(Mat *) output_addr;
    Mat mat;
    cvtColor(matInput, mat, COLOR_RGBA2BGR);



    cvtColor(mat, matResult, COLOR_BGR2RGBA);
}


