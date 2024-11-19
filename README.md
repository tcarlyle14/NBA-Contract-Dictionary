Communication Contract:


1.) For which teammate did you implement “Microservice A”?

Trevor Carlyle


2.) What is the current status of the microservice? Hopefully, it’s done!

Completed.


3.) If the microservice isn’t done, which parts aren’t done and when will they be done?

N/A.


4.) How is your teammate going to access your microservice? Should they get your code from GitHub (if so, provide a link to your public or private repo)? Should they run your code locally? Is your microservice hosted somewhere? Etc.

- Forked repo link: https://github.com/brentwooley95/NBAtradesimulator_micros
- Microservice located in NBAtradesimulator_micros/nbatradesimulator/csv_microservice/csvmicros.py
- Code should be run locally within virtual enviroment. Main program 'manage.py' and microservice 'csvmicros.py' will run concurrently, one local address for main and another for microservice. 


5.) If your teammate cannot access/call YOUR microservice, what should they do? Can you be available to help them? What’s your availability?

Please contact me at any point during the week. I will respond within 24 hours and we can schedule to troubleshoot if need be. I am avaialble most days during the week 12PM - 10PM CST.


6.) If your teammate cannot access/call your microservice, by when do they need to tell you?

Please contact me by 11:59 PM on Saturday 11/23/2024.


7.) Is there anything else your teammate needs to know? Anything you’re worried about? Any assumptions you’re making? Any other mitigations / backup plans you want to mention or want to discuss with your teammate?

The microservice itself is a small flask app. It's purpose is to validate the uploaded CSV through http requests to ensure it's data is compatible.
Refer to the 'requirements.txt' found at NBAtradesimulator_micros/nbatradesimulator/ & NBAtradesimulator_micros/nbatradesimulator/csv_microservice/ for dependencies needed to run the program. THe only new libraries outside existing added are 'requests' for the main program and 'flask' for the microservice.
To ensure correct installation:
1.) Set up and activate venv
2.) Run 'pip install -r requirements.txt' for both main program and microservice.






A.) How to programmatically REQUEST data from the microservice:

To request data, a test csv file and it's path are needed. A post request containing the form data(file) is then sent to the microservice endpoint.
Example:

 ```
file_path = "path/to/file/test.csv"
 url = "http://127.0.0.1:8001/validate_csv/" OR wherever microservice endpoint is.
 with open(file_path, 'rb') as file:
            response = requests.post(url, files={'file': file})
```

  
B.) How to programmatically RECEIVE data from the microservice:

The response object contains the message returned by the microservice. If the response status code is anything but 200 then an error has occured.
Example:

```
if response.status_code == 200:
    # Success
    data = response.json()  
else:
    # Validation failed or an error occurred
    error_data = response.json()
```

UML Sequence Diagram:



![Screenshot 2024-11-18 at 11 40 06 PM](https://github.com/user-attachments/assets/5c87b117-1923-4182-a16c-3df405d7f1b8)


