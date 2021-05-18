# Running iPython Jupyter Notebooks Locally on your PC
These instructions apply primarily to a Windows PC. 

### Downloading this repository
To download the entire repository, go to the [repository homepage](https://github.com/wobrotson/RocSocCodeCamp), click the green 'Code' button, and select 'Download zip'. Unzip in a suitable directory - you will navigate to this location later. 

### Installing the Anaconda Python distribution on your PC
I recommend installing the Anaconda Python distribution to load and run the notebooks. The installer can be downloaded here:
https://www.anaconda.com/products/individual

Anaconda manages the configuration of different Python libraries, sorting out dependencies etc for you in your coding environment. It's what most data scientists use. Anaconda contains over 1000 Python modules and is an 'out of the box' package ready for you to start writing your own notebooks in. However, the number of packages mean that it requires around 3GB of harddrive space to install. If you don't have the required space, then a better strategy might be to use Miniconda (see below).

Run the Anaconda installer by double-clicking on the downloaded .exe file and follow the steps below.

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

```shell
>> conda init
>> conda activate
>> jupyter notebook
```

You should do the first two whenever you get going with Anaconda.

What you should have now is a local browser window with your file structure laid out (Anaconda will set the 'home' directory as *C:\user\your_username* or something like that).

Navigate to the location where you saved the CodeCamp repository. Click on one of the notebook *.ipynb* files to open it in the browser window. You are now ready to code away locally on your PC.

### Using Miniconda instead of Anaconda
If you are low on space on your PC but want to code locally, a good solution is to use Miniconda to manually install only the Python modules you need, rather than 1500 of them. However, this is a substantially more complicated way of doing things, so if you're new to command lines, conda, python and all the rest it may seem a bit confusing. If you run into issues, as usual, a search engine and stackoverflow are probably going to be very useful!

Download the latest Python version of Miniconda installer here:
https://docs.conda.io/en/latest/miniconda.html

If you don't know if your machine is 32 bit or 64 bit, have a look in *"Settings > System > About"* on Windows 10.

Follow the install instructions as for Anaconda above and open 'Anaconda prompt', which should land you in your 'Home' directory (*C:\user\your_username* or something similar). Now it starts to get a tad more complicated. You need to navigate to the location of the repository on your PC using the terminal. Do this using the 'cd' command to 'change directory'. For example:

```shell
>> cd "My Documents"/RocSocCodeCamp
```

Issues will probably arise if you have spaces or weird characters in your folder names. Once you have arrived there, type the following commands into the terminal:

```shell
>> conda init
>> conda env create -f environment.yml
```

It will now take a few minutes to download all the packages, although it can sometimes take a lot longer.
Once that's all done, run the following commands in Anaconda Prompt:

```shell
>> conda activate codecamp2021
>> jupyter notebook
```

If all has worked correctly, then you should now have the same browser window as described above. If you get an error message, copy what it says and search for what it means. You will almost certainly find someone who has had the same issue and someone else giving a helpful answer that fixes the problem.