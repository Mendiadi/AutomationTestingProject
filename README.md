# Automation Testing Project

simple automation testing build with python and pytest
to verify and test end-to-end a small bookstore web app.
you can read the STD STP also
## Getting Started
make sure you have all the dependencies
clone or download zip this project
and run the tests
## Project Structure


tree of dirs
![script](https://github.com/Mendiadi/AutomationTestingProject/blob/master/assets/tree.PNG?raw=true)

driver.py interface of the driver manage selenium and playwright im wrote it to easily make driver operation in one place and easily write one code for to frameworks
rest.py file http requests im wrote it to learn more about decorators and its make a requests from one place so its cool im wrote in this file a lot of comments you can read if you want :)
im use page object pattern and implementing all the pages and the action in them
im use models and api objects to manage the api requests
all the models are dataclasses
im also have commons dir for all the other stuffs and utils
all the tests are in the tests folder sperate by classes and type of testing
fixture folder 
## Dependencies

- **chromedriver.exe**
- **geckodriver.exe**

run with remote driver
* you need to download java 
* download and run the selenium-server-standalone
* add nodes (chrome, firefox) by attach driver to path 
```commandline
        java -jar "selenium-server-yourversion.jar" standalone
```
* run the tests

you can find basic tutorial  [Here](https://www.selenium.dev/documentation/grid/getting_started/).

selenium grid at running sessions
![script](https://github.com/Mendiadi/AutomationTestingProject/blob/master/assets/grid_png.PNG?raw=true)

you can create image from this project with the dockerfile
just type in the workdir
```commandline
        docker build -t "name" .
```

* **docker** to run the dockerfile 

### Build with
- **pycharm ide**
#### Requirements:
project is depend on the following:
- **python 3.9**
- **build with pytest**
- **allure**
- **java** for grid
- **selenium framework for ui testing**
- **playwright framework for ui testing**


## Run Commands
**Arguments**:
- --url for the url 
- --lib for lib (selenium , playwright)
- --grid for selenium grid
- --browser for browser (chrome,firefox)
- --alluredir=<name> for allure reports

**run methods**

run with marks
- smoke
- regression
```commandline
        pytest tests -m smoke
```
run with arguments
```commandline
        pytest tests --lib playwright --url localhost --browser chrome  
```
run with grid
```commandline
        pytest tests --grid 1 
```
run with allure

```commandline
        pytest tests --alluredir=reports --lib selenium --grid true
```
default arguments values 
config file if not specify argument it will take from here
```json
{
  "url": "http://localhost/",
  "email": "adii@sela.co.il",
  "password": "string11",
  "browser": "chrome",
  "lib": "selenium",
  "selenium_grid":false,
  "driver_path" : "C:\\dri\\chromedriver.exe"
}


```
to run all tests use tests folder but notice you can 
run different tests files if you specify the name  




## Reports
reports with allure are generate automatically to the allure dir
as you set up, reports have some behaviors and structures.
if you click on behavior you can see the epics and features.
inside each of them you can find all the test cases.
im also added a steps and input provider (actual/excepted) are visible
in the allure reports as you can see in the example image down below

Example of reports behaviors (all tests run mode):

![script](https://github.com/Mendiadi/AutomationTestingProject/blob/master/assets/allure_behavior.PNG?raw=true)

also if test failed in the UI tests (selenium and also playwright)
you can find the screenshot in the reports as down below.
example taken from playwright but also same in selenium

Example of picture of test failed in reports (few tests run mode):

![script](https://github.com/Mendiadi/AutomationTestingProject/blob/master/assets/allure_image.PNG?raw=true)

more examples:

![script](https://github.com/Mendiadi/AutomationTestingProject/blob/master/assets/allure_step.PNG?raw=true)

![script](https://github.com/Mendiadi/AutomationTestingProject/blob/master/assets/allure_param.PNG?raw=true)
## Author
adi mendel