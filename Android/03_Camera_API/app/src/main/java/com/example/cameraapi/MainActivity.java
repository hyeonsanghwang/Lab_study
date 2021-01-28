package com.example.cameraapi;

import android.os.Bundle;
import android.view.TextureView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    private TextureView textureView;
    private MyCameraManager cameraManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textureView = (TextureView)findViewById(R.id.texture_view);
        cameraManager = new MyCameraManager(this, textureView);
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




