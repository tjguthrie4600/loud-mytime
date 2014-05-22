package com.loud.mytime;

import android.os.Handler;
import android.os.Message;
import android.os.Bundle;
import android.content.Intent;
import android.content.Context;
import android.view.View;
import android.util.Log;
import android.app.Activity;
import android.app.ProgressDialog;
import android.widget.EditText;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import java.net.URI;
import org.xmlrpc.android.XMLRPCClient;
import org.xmlrpc.android.XMLRPCException;

// This Is The Main Activity And Login Page
public class LOUDMyTime extends Activity implements Runnable
{
    // Username Password Login Button Progress Feilds
    EditText usernameValue;
    EditText passwordValue;
    Button loginButton;
    private ProgressDialog progress;
    
    // Storage For The Result
    String serverResult = "";
    
    // Called When The Activity Is First Created
    @Override
	public void onCreate(Bundle savedInstanceState)
    {
	// Save The State, Set The Layout
	super.onCreate(savedInstanceState);
	setContentView(R.layout.main);
	
	// Set Reference For Feilds
	usernameValue = (EditText) findViewById(R.id.usernameValue);
	passwordValue = (EditText) findViewById(R.id.passwordValue);
	loginButton = (Button) findViewById(R.id.loginButton);
	
	listen();
    }
    
    // Listen For Clicks
    public void listen()
    {
	loginButton.setOnClickListener(new View.OnClickListener()
	    {
		// When The Submit Button Is Pressed
		public void onClick(View v)
		{
		    // Check For Network Connection
		    ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
		    NetworkInfo networkInfo = connectivityManager.getActiveNetworkInfo();
		    
		    // The User Is Not Connected To A Network
		    if (networkInfo == null) 
			{
			    // Tell The User They Are Not Connected
			    Context context = getApplicationContext();
			    CharSequence text = "An Active Network Connection Is Required";
			    int duration = Toast.LENGTH_LONG;
			    Toast toast = Toast.makeText(context, text, duration);
			    toast.show();
			}
		    // The User Is Connected To The Internet
		    else
			{
			    // Display Messege
			    progress = ProgressDialog.show(LOUDMyTime.this, "Please Wait", "Retrieving Data", true, false);
			    
			    // Create New Thread
			    Thread thread = new Thread(LOUDMyTime.this);
			    thread.start();
			}
		}
	    });
    }
    
    // When New Thread Is Run
    public void run()
    {
	// Store The Username And Password On Submit
	String usernameString = usernameValue.getText().toString();
	String passwordString = passwordValue.getText().toString();
	
	// Create The XMLRPC Client
	URI uri = URI.create("https://www.lcsee.wvu.edu/lamp/lcsee-mytime/XML-RPC-Server.py");
	XMLRPCClient client = new XMLRPCClient(uri);
	
	try
	    {
		// Make The Call To The Server
		serverResult = (String) client.call("MyTimeMobile", usernameString, passwordString);
	    }
	catch (XMLRPCException e)
	    {
		// Log Errors
		Log.w("XMLRPC Test", "Error", e);
	    }
	
	// Create And Send Message To User Interface Thread
	handler.sendEmptyMessage(0);
    }
    
    // Create The Handler To Communicate Back To The User Interface Thread
    private Handler handler = new Handler() 
	{
	    @Override
		public void handleMessage(Message msg) 
	    {
		// Get Rid Of The Loading Message
		progress.dismiss();
		
		// Start The New Activity, Send It The Result
		Intent nextScreen = new Intent(getApplicationContext(), Output.class);
		nextScreen.putExtra("result", serverResult);
		startActivity(nextScreen);
	    }
        };
}