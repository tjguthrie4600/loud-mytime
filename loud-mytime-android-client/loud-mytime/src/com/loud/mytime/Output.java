package com.loud.mytime;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import android.content.Intent;
import android.widget.Button;
import android.view.View;
import android.widget.ScrollView;
import android.widget.ImageView;

// Activity To View Results
public class Output extends Activity 
{
    // Called when the activity is first created
    @Override
	public void onCreate(Bundle savedInstanceState) 
    {
	// Save The State, Set The Layout
        super.onCreate(savedInstanceState);
        setContentView(R.layout.output);

	// Get The Result From The Main Activity
	Intent intent = getIntent();
	String result = intent.getStringExtra("result");
	
	// Get The Reference For Output Elements
	TextView nameValue = (TextView) this.findViewById(R.id.nameValue);
	TextView statusValue = (TextView) this.findViewById(R.id.statusValue);
	TextView totalHoursValue = (TextView) this.findViewById(R.id.totalHoursValue);
	TextView datesValue = (TextView) this.findViewById(R.id.datesValue);
	Button closeButton = (Button) findViewById(R.id.closeButton);

	// If The Server Did Not Respond With Authentication Failure
	if (result.length() > 22)
	    {
		// Define The Delimeters
		String dateDelimiter = "[&]";
		String statusDelimiter = "[*]";
		String hoursDelimiter = "[%]";
		String nameDelimiter = "[-]";
		
		String[] temp = new String[2];
		
		String status;
		String totalHours;
		String name;
		
		// Parse For The Dates
		String [] dates = result.split(dateDelimiter);
		temp = dates[dates.length - 1].split(statusDelimiter);
		dates[dates.length - 1] = temp[0];
		
		// Parse For The Status
		temp = temp[1].split(hoursDelimiter);
		status = temp[0];
		
		// Parse For The Cumulative Hours
		temp = temp[1].split(nameDelimiter);
		totalHours = temp[0];
		
		// Parse For The Name
		name = temp[1];
		
                // Format The Data
		String nameData =  new StringBuilder("").append(name).toString();
		String totalHoursData = new StringBuilder("").append(totalHours).toString();
		String statusData = new StringBuilder("").append(status).toString();
		String dateString;
		
		// Format The Dates
		int isStart = 1;
		StringBuilder datesData = new StringBuilder();
		for (int i = 0; i < dates.length; i++)
		    {
			// If Its A Date
			if (dates[i].length() == 14)
			    {
				datesData.append("\n").append(dates[i]).append("\n");
				dateString = datesData.toString();
			    }
			// If Its A Time
			else
			    {
				if (isStart == 1)
				    {
					isStart = isStart - 1;
					datesData.append(dates[i]).append("\n");
					dateString = datesData.toString();
				    }
				else 
				    {
					isStart = isStart + 1;
					datesData.append(dates[i]).append("................................................");
					dateString = datesData.toString();
				    }
			    }
		    }
		
		// Display The Data
		nameValue.setText(nameData);
		statusValue.setText(statusData);
		totalHoursValue.setText(totalHoursData);
		datesValue.setText(datesData);
	    }
	else
	    {
		// If The Server Responds With Authentication Failure
		if (result.length() == 22)
		    {
			// Display The Data
			datesValue.setText("Authentication Failure");
		    }
		// The Server Is Sending Empty Packets (Needs Restarted)
		else
		    {
			// Display The Data
                        datesValue.setText("An Error Has Occured, Please Contact The System Administrator");
		    }
	    }	

	// Listen For Clicks
	closeButton.setOnClickListener(new View.OnClickListener() 
	    {
		
	    // When The Close Button Is Pressed Switch To Main Activity
		public void onClick(View arg0) 
		{
		    //Closing SecondScreen Activity                                                           
		    finish();
		}
	    });
	
    }
}