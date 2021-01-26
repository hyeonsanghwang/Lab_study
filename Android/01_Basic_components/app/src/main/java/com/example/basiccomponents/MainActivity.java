package com.example.basiccomponents;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.media.Image;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

public class MainActivity extends AppCompatActivity {

    private TextView textView;
    private EditText editText;
    private Button button;
    private ToggleButton toggleButton;
    private CheckBox checkBox;
    private RadioGroup radioGroup;
    private RadioButton radioButton1, radioButton2, radioButton3;
    private Switch switchButton;
    private ImageView imageView;
    private ImageButton imageButton;
    private Button button_linear, button_frame, button_constraint;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setId();
        setEventListener();
    }

    private void setId() {
        textView = (TextView)findViewById(R.id.textView);
        editText = (EditText) findViewById(R.id.editText);
        button = (Button) findViewById(R.id.button);
        toggleButton = (ToggleButton) findViewById(R.id.toggleButton);
        checkBox = (CheckBox) findViewById(R.id.checkBox);
        radioGroup = (RadioGroup) findViewById(R.id.radioGroup);
        radioButton1 = (RadioButton) findViewById(R.id.radioButton1);
        radioButton2 = (RadioButton) findViewById(R.id.radioButton2);
        radioButton3 = (RadioButton) findViewById(R.id.radioButton3);
        switchButton = (Switch)findViewById(R.id.switch1);
        imageView = (ImageView)findViewById(R.id.imageView);
        imageButton = (ImageButton)findViewById(R.id.imageButton);
        button_linear = (Button) findViewById(R.id.button_linear);
        button_frame = (Button) findViewById(R.id.button_frame);
        button_constraint = (Button) findViewById(R.id.button_constraint);
    }

    private void setEventListener() {
        textView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String str = textView.getText().toString();
                str += "!!!";
                textView.setText(str);
            }
        });

        editText.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String str = editText.getText().toString();
                str += "!!!";
                editText.setText(str);
            }
        });

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Logcat
                Log.d("MainActivity", "Button clicked");

                // Toast message
                Toast.makeText(MainActivity.this, editText.getText().toString(), Toast.LENGTH_SHORT).show();
                editText.setText("");


            }
        });

        toggleButton.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener(){
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                Toast.makeText(MainActivity.this, ""+isChecked, Toast.LENGTH_SHORT).show();
            }
        });

        checkBox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                Toast.makeText(MainActivity.this, ""+isChecked, Toast.LENGTH_SHORT).show();
            }
        });

        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                if (checkedId == R.id.radioButton1)
                    Toast.makeText(MainActivity.this, "1", Toast.LENGTH_SHORT).show();
                else if(checkedId == R.id.radioButton2)
                    Toast.makeText(MainActivity.this, "2", Toast.LENGTH_SHORT).show();
                else
                    Toast.makeText(MainActivity.this, "3", Toast.LENGTH_SHORT).show();

                // or
                int id = radioGroup.getCheckedRadioButtonId();
                if (id == R.id.radioButton1)
                    Toast.makeText(MainActivity.this, "1", Toast.LENGTH_SHORT).show();
                else if(id == R.id.radioButton2)
                    Toast.makeText(MainActivity.this, "2", Toast.LENGTH_SHORT).show();
                else
                    Toast.makeText(MainActivity.this, "3", Toast.LENGTH_SHORT).show();

                // or
                if (radioButton1.isChecked())
                    Toast.makeText(MainActivity.this, "1", Toast.LENGTH_SHORT).show();
                else if(radioButton2.isChecked())
                    Toast.makeText(MainActivity.this, "2", Toast.LENGTH_SHORT).show();
                else
                    Toast.makeText(MainActivity.this, "3", Toast.LENGTH_SHORT).show();
            }
        });

        switchButton.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked)
                    imageView.setImageResource(R.drawable.image);
                else
                    imageView.setImageResource(0);
            }
        });

        imageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                imageButton.setImageResource(R.drawable.icon);
                imageButton.setScaleType(ImageView.ScaleType.FIT_XY);
                imageButton.setLayoutParams(new LinearLayout.LayoutParams(200,200));
            }
        });


        View.OnClickListener buttons_listener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = null;
                if (v.getId() == R.id.button_linear)
                    intent = new Intent(MainActivity.this, LinearLayoutActivity.class);
                else if (v.getId() == R.id.button_frame)
                    intent = new Intent(MainActivity.this, FrameLayoutActivity.class);
                else if (v.getId() == R.id.button_constraint)
                    intent = new Intent(MainActivity.this, ConstraintLayoutActivity.class);

                if (intent != null)
                    startActivity(intent);
            }
        };
        button_linear.setOnClickListener(buttons_listener);
        button_frame.setOnClickListener(buttons_listener);
        button_constraint.setOnClickListener(buttons_listener);
    }
}
