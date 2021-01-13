package com.example.camera;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.WindowManager;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    private static final int REQUEST_PERMISSION_CODE = 200;

    private Camera camera_manager;
    private AutoFitTextureView view;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON, WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setContentView(R.layout.activity_main);

        checkPermission();
        view = (AutoFitTextureView)findViewById(R.id.texture_view);
        camera_manager = new Camera(this, view);
    }

    @Override
    protected void onResume() {
        camera_manager.startThreads();
        super.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        camera_manager.closeCamera();
        camera_manager.stopThreads();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        camera_manager.closeCamera();
        camera_manager.stopThreads();
    }

    /*  Permission methods  */
    private void checkPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED)
                Log.d(TAG, "checkPermission: START!!!!!!!!!!!!");
            else
                requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_PERMISSION_CODE);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch(requestCode){
            case REQUEST_PERMISSION_CODE:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                    Log.d(TAG, "checkPermission: START!!!!!!!!!!!!");
                else
                    finish();
                break;
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
}