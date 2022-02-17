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
		- State: a char field that stores the current status of the epic. This attribute is automaticaly computed. 
		- Linked epic: a Foreign Key, stores the parent epic
	- Bug:
		- Title: a unique char field
		- Epic: a Foreign Key, stores the parent epic
	- Task:
		- Title: a unique char field
		- Epic: a Foreign Key, stores the parent epic
 - Relations between tables are Many to One since we used only Foreign Keys:
	- An Epic can have many children Bugs, but a Bug can have only one parent Epic
	- An Epic can have many children Tasks, but a Task can have only one parent Epic
	- An Epic can have many children Epics, but an Epic can have only one parent Epic

 ---

## Features

#### Home page
 - Top Navigation Bar:
	- "Epics": link to epics list
	- "Search": search engine over Bugs table
 - Import backlog: upload a text file and parse a backlog formatted as a dictionary. If a backlog is already stored in database, the app wil merge them accoring to these rules:
	- If an Epic already exists in database (based on title), then it updates it. If not, it creates it.
	- If a Bug already exists (based on title), it updates its parent Epic. If not, it creates it.
	- If a Task already exists (based on title), it updates its parent Epic. If not, it creates it.
 - Export backlog: export the current backlog stored in database into a text file, format as a dictionary.
 - Reset database: flush database. This function is mainly for testing purpose.

#### Epics page
 - Provides a list of all Epics and their status. Each Epic is a link to its detailed view.

#### Epic detailed view page
 - Provides different informations:
	- List of children Bugs
	- List of children Tasks
	- List of children Epics
	- List of all children Bugs linked to all children Epics
 - For Bugs and Tasks lists, users can add objects to the current Epic. A Django automaticaly generated form performs all safe checks (empty title, Bug or Task title already exists). Then Epic status is refreshed.
 - For Bugs and Tasks lists, user can delete objects from the current Epic. Then Epic status is refreshed.

#### Search page
 - User can make a research on Bug title. It returns all matching bugs and list their blocked Epics (all parents Epics). The highest Epic in this tree is shown first on the list.

---

## UX Design
 - For the web interface, I kept things simple. I used Bootstrap 4.1.3 default components and colors.
 - My main goal was to create as few pages as possible to improve readability and to have an easy to navigate website.

---

## Testing

#### Automatic written tests
 - I must admit that I found this part the biggest challenge of this project, mainly because I did it at the end of it. For the future, it would definitely be better to write tests as I write the code.
 - I used Django built in TestCase and test the views, forms and models associated with Epics app and Search app. The tests generally follow these patterns:
	- Create a new object instance, save it, and check if the model works well
	- Test the routes response status codes
	- Test whether an object list is in the global context and its values
	- Test if a form is delivering the correct data
	- Test if a model instance saves correctly
	- Test routes that receive get or post requests by simulating with self.client.post and check if the object has been created / updated / deleted

#### Browser testing
 - I used Google Chrome to test app frontend, such as responsiveness, the grid and fonts.
 - For import and export features, I mainly test them on browser. I wish I had time to write some stronger tests for this part.

---

## Deployment

#### Run project
 - Full project is available on Git.
 - Install requirements.txt dependancies.
 - Run app by executing command: `python manage.py runserver`
 - The web app is hosted on 127.0.0.1:8000 by default.

#### Docker
 - Dockerfile is provided
 - Run commands from FreeJira folder:
	- `docker build -t freejira .`
	- `docker run -p 8000:8000 -i -t freejira`
 - The web app is hosted on 127.0.0.1:8000 by default.

#### Testing
 - App is shipped with a full test database. This test dataset is available in `/serialize/test_backlog_import.txt`

---

## To Do
 - Improve User Interface
 - Add more tests, especially on import/export features
 - Do not save data if the import fails
 - Improve errors management by raising exceptions




