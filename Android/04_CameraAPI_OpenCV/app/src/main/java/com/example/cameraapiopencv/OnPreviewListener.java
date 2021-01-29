package com.example.cameraapiopencv;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.graphics.Point;
import android.media.Image;
import android.media.ImageReader;
import android.view.Display;
import android.view.WindowManager;


import org.opencv.android.Utils;
import org.opencv.core.Mat;


public class OnPreviewListener implements ImageReader.OnImageAvailableListener {
    private static final String TAG = "OnPreviewListener";

    private Context context;
    private SurfaceImageView sv_imageview;
    private boolean isProcessing = false;
    private ImageProcessing proc;

    private int image_width = 0;
    private int image_height = 0;
    private int screenRotation = 90;

    private Image.Plane[] planes;
    private byte[][] buffer_YUV;
    private int[] buffer_RGB;

    private Bitmap bitmap_temp;
    private Bitmap bitmap_RGB;



    public OnPreviewListener(Context context, SurfaceImageView view) {
        this.context = context;
        this.sv_imageview = view;
        proc = new ImageProcessing();
    }


    @Override
    public void onImageAvailable(ImageReader reader) {
        Image image = reader.acquireLatestImage();

        if (image == null)
            return;

        if (isProcessing) {
            image.close();
            return;
        }

        isProcessing = true;
        imageToRGBBitmap(image);
        drawImage();
    }

    private void imageToRGBBitmap(Image image) {
        // Get image plane
        planes = image.getPlanes();

        // Initialize buffers
        if (image_width != image.getWidth() || image_height != image.getHeight()) {
            image_width = image.getWidth();
            image_height = image.getHeight();

            bitmap_RGB = null;
            bitmap_temp = Bitmap.createBitmap(image_width, image_height, Bitmap.Config.ARGB_8888);
            buffer_RGB = new int[image_width * image_height];
            buffer_YUV = new byte[planes.length][];
            for (int i = 0; i < planes.length; ++i) {
                buffer_YUV[i] = new byte[planes[i].getBuffer().capacity()];
            }
        }

        // Set YUV buffer
        for (int i = 0; i < planes.length; ++i)
            planes[i].getBuffer().get(buffer_YUV[i]);

        // Convert YUV to ARGB
        final int yRowStride = planes[0].getRowStride();
        final int uvRowStride = planes[1].getRowStride();
        final int uvPixelStride = planes[1].getPixelStride();
        proc.convert_YUV420_to_ARGB8888(
                buffer_YUV[0],
                buffer_YUV[1],
                buffer_YUV[2],
                buffer_RGB,
                image_width,
                image_height,
                yRowStride,
                uvRowStride,
                uvPixelStride);

        // RGB buffer to RGB bitmap and rotate
        bitmap_temp.setPixels(buffer_RGB, 0, image_width, 0, 0, image_width, image_height);
        bitmap_RGB = rotateBitmap(bitmap_temp);
        image.close();
    }

    private Bitmap rotateBitmap(final Bitmap src) {
        Display getOrient = ((WindowManager) context.getSystemService(Context.WINDOW_SERVICE)).getDefaultDisplay();
        Point point = new Point();
        getOrient.getSize(point);
        int screen_width = point.x;
        int screen_height = point.y;

        screenRotation = (screen_width < screen_height) ? 270 : 0;
        if (screenRotation != 0) {
            final Matrix matrix = new Matrix();
            matrix.postRotate(screenRotation);
            return Bitmap.createBitmap(src, 0, 0, src.getWidth(), src.getHeight(), matrix,true);
        }
        return src;
    }


    private void drawImage() {
        Mat src = new Mat();
        Utils.bitmapToMat(bitmap_RGB, src);
        Mat dst = new Mat(src.rows(), src.cols(), src.type());

        proc.processing(src.getNativeObjAddr(), dst.getNativeObjAddr());

        Bitmap bitmap = Bitmap.createBitmap(bitmap_RGB.getWidth(), bitmap_RGB.getHeight(), bitmap_RGB.getConfig());
        Utils.matToBitmap(src, bitmap);

        sv_imageview.draw(bitmap);
        isProcessing = false;
    }
}

