package com.example.cameraapiopencv;

public class ImageProcessing {
    static{
        System.loadLibrary("opencv_java4");
        System.loadLibrary("native-lib");
    }

    public static native void convert_YUV420_to_ARGB8888(byte[] y,
                                                         byte[] u,
                                                         byte[] v,
                                                         int[] output,
                                                         int width,
                                                         int height,
                                                         int yRowStride,
                                                         int uvRowStride,
                                                         int uvPixelStride);

    public static native void processing(long input_addr, long output_addr);
}

