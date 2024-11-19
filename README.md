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


Is there anything else your teammate needs to know? Anything you’re worried about? Any assumptions you’re making? Any other mitigations / backup plans you want to mention or want to discuss with your teammate?




A.) How to programmatically REQUEST data from the microservice:

- To request data from the microservice, you would write the input team name as a string to the txt file team_input.txt. The microservice then reads the team name, checks if the team name is in the cfbd API, and returns True or False.
- Example call:
with open("team_input.txt", "w") as file:
    file.write(team_name)
How to programmatically RECEIVE data from the microservice:

- To receive data from the microservice, you would read the True or False string returned from the microservice to the txt file team_input.txt to know if a orginal input team name is valid.
- Example call:
with open("team_input.txt", "r") as file:
    result = file.read().strip().lower()
UML Sequence Diagram:
