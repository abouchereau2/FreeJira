# Free Jira - Backlog tracking tool

---

## Overview
 - Free Jira is backlog management site where users can track and visualize Epics.
 - An Epic can contains Bugs, Tasks and other Epics. It can be in differet states: "confirmed", "work in progress" or "pending validation".
 - Users can import a backlog (as a dictionnary) to populate database. The app is deployed with a test database.
 - The app is built with Django and bootstrap. I choose Django because it is one of the top web development framework and has a big and supportive community. It is also fast, simple and reliable.
 - The UX design is very simple since I attached more importance on backend development than frontend for this exercise.
 
 ---

## Database
 - I use the default database shipped with Django (sqlite3) in order to manage data in a more efficient way. Django provides librairies to create models, to do efficient queries and to do testing that improves the reliability of the code.
 - The database is working with three Models:
	- Epic
		- Title: a unique char field
		- State: a char field that stores the current status of the epic
		- Linked epic: a Foreign Key, stores the parent epic
	- Bug:
		- Title: a unique char field
		- Epic: a Foreign Key, stores the parent epic
	- Task:
		- Title: a unique char field
		- Epic: a Foreign Key, stores the parent epic
 - Relations between tables are One to Many since we used only Foreign Keys:
	- An Epic can have many children Bugs, but a Bug can have only one parent Epic
	- An Epic can have many children Tasks, but a Task can have only one parent Epic
	- An Epic can have many children Epics, but an Epic can have only one parent Epic

 ---

## Features
 - 

---

## UX Design
 - 

---

## Testing
 - 

---

## Deployment
 - 
docker build -t FreeJira .
docker run -p 8000:8000 -i -t FreeJira


## To Do
 - 




