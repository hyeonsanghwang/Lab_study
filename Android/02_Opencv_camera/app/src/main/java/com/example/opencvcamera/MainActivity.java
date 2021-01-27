package com.example.opencvcamera;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.view.WindowManager;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewListener2;
import org.opencv.core.Mat;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    // Load native libraries
    static {
        System.loadLibrary("opencv_java4");
        System.loadLibrary("native-lib");
    }

    // Native method
    public native void process(long mat_input_addr, long mat_result_addr);

    private CameraBridgeViewBase camera_view;

    private final CvCameraViewListener2 cameraViewListener = new CvCameraViewListener2() {
        @Override
        public void onCameraViewStarted(int width, int height) {}

        @Override
        public void onCameraViewStopped() {}

        @Override
        public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
            Mat input_mat = inputFrame.rgba();
            Mat result_mat = new Mat();

            process(input_mat.getNativeObjAddr(), result_mat.getNativeObjAddr());
            return result_mat;
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_main);

        camera_view = (CameraBridgeViewBase)findViewById(R.id.camera_view);
        camera_view.setCameraIndex(0);
        camera_view.setCvCameraViewListener(cameraViewListener);
        camera_view.setCameraPermissionGranted();
        camera_view.enableView();
    }


    /*  Permission methods  */
    private static final int REQUEST_PERMISSION_CODE = 200;
    private void checkPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED)
                camera_view.setCameraPermissionGranted();
            else
                requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_PERMISSION_CODE);
        }
        else
            camera_view.setCameraPermissionGranted();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch(requestCode){
            case REQUEST_PERMISSION_CODE:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                    camera_view.setCameraPermissionGranted();
                else
                    finish();
                break;
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
}
