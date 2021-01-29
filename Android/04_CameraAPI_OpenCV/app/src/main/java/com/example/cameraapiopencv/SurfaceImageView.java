package com.example.cameraapiopencv;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.util.AttributeSet;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class SurfaceImageView extends SurfaceView {
    private Context context;
    private SurfaceHolder holder;

    private int width;
    private int height;


    public SurfaceImageView(Context context) {
        super(context);
        this.context = context;
        holder = getHolder();
    }

    public SurfaceImageView(Context context, AttributeSet attrs) {
        super(context, attrs);
        this.context = context;
        holder = getHolder();
    }

    void setAspectRatio(int width, int height) {
        int widget_width = getWidth();
        int widget_height = getHeight();

        float ratio = (float)width / (float)height;
        float widget_ratio = (float)widget_width / (float)widget_height;
        if (ratio > widget_ratio) {
            this.width = widget_width;
            this.height = (int) (widget_width / ratio);
        }
        else {
            this.width = (int) (widget_height * ratio);
            this.height = widget_height;
        }
        holder.setFixedSize(this.width, this.height);
    }

    protected void draw(Bitmap bitmap) {
        Canvas c = holder.lockCanvas();
        synchronized (holder){
            Bitmap scaled = Bitmap.createScaledBitmap(bitmap, width, height, true);
            c.scale(-1.0f, 1.0f, width/2.0f, height/2.0f);
            c.drawBitmap(scaled, 0, 0, null);
        }
        holder.unlockCanvasAndPost(c);
    }
}




