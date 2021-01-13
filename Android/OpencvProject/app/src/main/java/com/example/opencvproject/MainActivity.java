package com.example.opencvproject;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.view.WindowManager;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Mat;


public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {
    private static final String TAG = "MainActivity";
    private static final int REQUEST_PERMISSION_CODE = 200;

    private CameraBridgeViewBase camera_view;

    static {
        System.loadLibrary("opencv_java4");
        System.loadLibrary("native-lib");
    }

    private BaseLoaderCallback loaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch(status) {
                case LoaderCallbackInterface.SUCCESS:
                    camera_view.enableView();
                    break;
                default:
                    super.onManagerConnected(status);
            }
        }
    };

    // Native method
    public native void process(long mat_input_addr, long mat_result_addr);


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON, WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setContentView(R.layout.activity_main);

        camera_view = (CameraBridgeViewBase)findViewById(R.id.camera_view);
        camera_view.setCameraIndex(0);
        camera_view.setCvCameraViewListener(this);

        checkPermission();
    }

    @Override
    public void onResume() {
        super.onResume();
        if (OpenCVLoader.initDebug())
            loaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        else
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_2_0, this, loaderCallback);
    }

    @Override
    public void onPause() {
        super.onPause();
        if (camera_view != null)
            camera_view.disableView();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (camera_view != null)
            camera_view.disableView();
    }


    /*  Camera callbacks  */
    @Override
    public void onCameraViewStarted(int width, int height) {

    }

    @Override
    public void onCameraViewStopped() {

    }

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
        Mat input_mat = inputFrame.rgba();
        Mat result_mat = new Mat();

        process(input_mat.getNativeObjAddr(), result_mat.getNativeObjAddr());
        return result_mat;
    }


    /*  Permission methods  */
    private void checkPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED)
                camera_view.setCameraPermissionGranted();
            else
                requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_PERMISSION_CODE);
        }
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

