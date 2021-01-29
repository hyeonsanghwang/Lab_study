package com.example.cameraapiopencv;

import android.os.Bundle;
import android.view.SurfaceView;
import android.view.TextureView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    private SurfaceImageView surfaceImageView;
    private MyCameraManager cameraManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        surfaceImageView = (SurfaceImageView) findViewById(R.id.image_view);
        cameraManager = new MyCameraManager(this, surfaceImageView);
    }


    @Override
    protected void onPause() {
        super.onPause();
        cameraManager.closeCamera();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        cameraManager.closeCamera();
    }
}

