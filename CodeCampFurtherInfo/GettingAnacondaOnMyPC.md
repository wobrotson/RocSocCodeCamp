I recommend downloading and installing the Anaconda distribution:
https://www.anaconda.com/products/individual

This manages the configuration of different Python libraries, sorting out dependencies etc for you in your coding environment. It's what most data scientists use.

Run the installer by double-clicking on the downloaded file and follow the steps below.

1. Click “Run”.
2. Click on “Next”.
3. Click on “I agree”.
4. Leave the selection on “Just me” and click on “Next”.
5. Click on “Next”.
6. Select the first option for “Add Anaconda to my PATH environment variable” and also leave the selection on “Register Anaconda as my default Python 3.x”. Click on “Install”.
    *You will also see a message in red text that selecting “Add Anaconda to my PATH environment variable” is not recommended; ignore this, it makes everything much easier later on.
7. When the install is complete, Click on “Next”.
8. Click on “Finish”.

Once you've installed Anaconda, then you want to open the 'Anaconda prompt' aka the software's own terminal shell (find it under Start menu - Anaconda). Open this, then type the following 3 commands:

>> conda init
>> conda activate
>> jupyter notebook

You should do the first two whenever you get going with Anaconda.

What you should have now is a local browser window with your file structure laid out (Anaconda will set the 'home' directory as C:\user\your_username or something like that).

Navigate to the folder you want to do the coding in (probably wherever your data is). Go to 'New - Python 3' and you now have a Jupyter notebook ready to do Python in!