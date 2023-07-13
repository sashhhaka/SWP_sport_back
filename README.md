# [SWP] Sport Achievements: functionality for coaches

![Pipeline](https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg)

## Project description
The main idea of Sport Achievements project is to add achievements to Innopolis University Sport website. 
This part of the project is directed to coaches functionality specifically. Coaches should be able to mark achievements as completed, when a student shows them their progress.

## Demo
(TODO: Demo screenshots)

## How to use
You should install the project on your device, following the steps described in the Project Installation section. Otherwise, you can see the [deployed project](http://89.223.121.66/admin/login/?next=/admin/). 
user: t.testovich@innopolis.university
password: pqowieur
Note: this user does not have all the admin functionality

## Features list
1. From admin page:
    * All the functionality from current Sport site admin page
    * Create new achievements
    * Change achievements
    * Select which students can have achievements
    * Select which coaches are responsible for achievements
    * Assign achievements to coaches
    * Assign achievements to students
    * Mark achievements as finished for students
    * Delete achievements
2. From coach page
    * See all achievements available for this coach
    * See achievement cards
    * Mark achievements as finished for particular students

## Project Installation
This part was taken from the original Sport site repository

### Requirements:
* Python3
* Docker

### How to start coding:
1. Clone the repository
2. Go to repo folder
3. `pip3 install -r ./adminpage/requirements.txt`. If not everything works at this stage (for example, some packages do not install), you still can move to the next step.
4. To start server 
    1. Rename file: `example.env` to `.env`. If you do not have .env file, install it direactly from a branch which has it
    2. From repo folder: `docker-compose -f ./compose/docker-compose.yml up`. Docker on your computer should be opened beforehand.
5. To create superuser and make migrations
    1. `docker exec -it sport_adminpanel bash`
    2. `python manage.py makemigrations`
    3. `python manage.py migrate`
    4. `python manage.py createsuperuser`


##  Technologies used
* Python
* Docker
* HTML
* CSS
* JavaScript
* PostgreSQL