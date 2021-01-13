package com.example.camera;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.ImageFormat;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.media.ImageReader;
import android.os.Handler;
import android.os.HandlerThread;

import android.util.Log;
import android.util.Size;
import android.view.Surface;
import android.view.TextureView;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;

import java.util.Arrays;
import java.util.concurrent.Semaphore;


public class Camera {
    private static final String TAG = "Camera";

    // Widgets
    private Context context;
    private AutoFitTextureView view;

    // Permission
    private static final int REQUEST_CAMERA_PERMISSION = 200;

    // Camera
    private static final int CAMERA_INDEX = 1;
    private static final int MAXIMUM_CAMERA_WIDTH = 640;
    private static final int MAXIMUM_CAMERA_HEIGHT = 480;
    private String cameraID;
    private Semaphore cameraLock = new Semaphore(1);
    private CameraDevice cameraDevice;
    private CameraCaptureSession cameraCaptureSessions;
    private CaptureRequest.Builder previewRequestBuilder;
    private CaptureRequest.Builder processRequestBuilder;

    // Threads
    private Handler backgroundHandler;
    private HandlerThread backgroundThread;
    private Handler inferenceHandler;
    private HandlerThread inferenceThread;

    // Preview
    private boolean preview_mode = true;
    private Size previewSize;
    private ImageReader previewReader;
    private Surface preview_surface;

    // Listeners
    TextureView.SurfaceTextureListener previewTextureViewListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(@NonNull SurfaceTexture surface, int width, int height) {
            openCamera();
        }

        @Override
        public void onSurfaceTextureSizeChanged(@NonNull SurfaceTexture surface, int width, int height) {

        }

        @Override
        public boolean onSurfaceTextureDestroyed(@NonNull SurfaceTexture surface) {
            return false;
        }

        @Override
        public void onSurfaceTextureUpdated(@NonNull SurfaceTexture surface) {

        }
    };
    CameraDevice.StateCallback cameraStateCallback = new CameraDevice.StateCallback() {
        @Override
        public void onOpened(@NonNull CameraDevice camera) {
            cameraDevice = camera;
            createCameraPreveiw();
        }

        @Override
        public void onDisconnected(@NonNull CameraDevice camera) {
            cameraDevice.close();
        }

        @Override
        public void onError(@NonNull CameraDevice camera, int error) {
            cameraDevice.close();
            cameraDevice = null;
        }
    };


    public Camera(Context context, AutoFitTextureView view) {
        this.context = context;
        this.view = view;

        startThreads();
        this.view.setSurfaceTextureListener(previewTextureViewListener);
    }


    /**********************************************************************************************/
    /*************************************** Camera control ***************************************/
    /**********************************************************************************************/
    private void openCamera() {
        try {
            // Get camera ID
            cameraLock.acquire();
            CameraManager manager = (CameraManager)context.getSystemService(Context.CAMERA_SERVICE);
            cameraID = manager.getCameraIdList()[CAMERA_INDEX];

            // Set preview size
            previewSize = getPreviewSize(manager);
            view.setAspectRatio(previewSize.getHeight(), previewSize.getWidth());


            // Check permission
            if (ActivityCompat.checkSelfPermission(context, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED){
                ActivityCompat.requestPermissions((Activity) context, new String[] {
                        Manifest.permission.CAMERA,
                        Manifest.permission.WRITE_EXTERNAL_STORAGE
                }, REQUEST_CAMERA_PERMISSION);
                return;
            }

            // Open camera
            manager.openCamera(cameraID, cameraStateCallback, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private Size getPreviewSize(CameraManager manager) throws CameraAccessException {
        CameraCharacteristics characteristics = manager.getCameraCharacteristics(cameraID);
        StreamConfigurationMap map = characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
        Size[] sizes = map.getOutputSizes(SurfaceTexture.class);
        Size target_size = new Size(MAXIMUM_CAMERA_WIDTH, MAXIMUM_CAMERA_HEIGHT);

        for (final Size size: sizes) {
            int width = size.getWidth();
            int height = size.getHeight();
            if (MAXIMUM_CAMERA_WIDTH >= width && MAXIMUM_CAMERA_HEIGHT >= height) {
                target_size = size;
                break;
            }
        }
        return target_size;
    }

    private void createCameraPreveiw() {
        try{
            // Preview setting
            previewRequestBuilder = cameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);

            SurfaceTexture texture = view.getSurfaceTexture();
            texture.setDefaultBufferSize(previewSize.getWidth(), previewSize.getHeight());
            preview_surface = new Surface(texture);

            previewRequestBuilder.addTarget(preview_surface);

            // Preview start
            startPreview();

        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void startPreview() throws CameraAccessException {
        cameraDevice.createCaptureSession(Arrays.asList(preview_surface), new CameraCaptureSession.StateCallback() {
            @Override
            public void onConfigured(@NonNull CameraCaptureSession session) {
                try {
                    cameraCaptureSessions = session;
                    previewRequestBuilder.set(CaptureRequest.CONTROL_MODE, CaptureRequest.CONTROL_MODE_AUTO);
                    cameraCaptureSessions.setRepeatingRequest(previewRequestBuilder.build(), null, backgroundHandler);
                } catch (CameraAccessException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onConfigureFailed(@NonNull CameraCaptureSession session) { }
        }, null);
    }

    void closeCamera() {
        try {
            cameraLock.acquire();

            if (cameraCaptureSessions != null) {
                cameraCaptureSessions.close();
                cameraCaptureSessions = null;
            }
            if (cameraDevice != null) {
                cameraDevice.close();
                cameraDevice = null;
            }
            if (previewReader != null) {
                previewReader.close();
                previewReader = null;
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            cameraLock.release();
        }
    }


    /**********************************************************************************************/
    /************************************** Thread management *************************************/
    /**********************************************************************************************/
    void startThreads() {
        if (backgroundThread == null){
            backgroundThread = new HandlerThread("ImageListener");
            backgroundThread.start();
            backgroundHandler = new Handler(backgroundThread.getLooper());
        }
        if (inferenceHandler == null) {
            inferenceThread = new HandlerThread("InferenceThread");
            inferenceThread.start();
            inferenceHandler = new Handler(inferenceThread.getLooper());
        }
    }

    void stopThreads() {
        try {
            if (backgroundThread != null){
                backgroundThread.quitSafely();
                backgroundThread.join();
                backgroundThread = null;
                backgroundHandler = null;
            }
            if (inferenceThread != null){
                inferenceThread.quitSafely();
                inferenceThread.join();
                inferenceThread = null;
                inferenceHandler = null;
            }
        } catch (InterruptedException e) {
            Log.e(TAG, "stopThreads: ", e);
        }
    }
}
