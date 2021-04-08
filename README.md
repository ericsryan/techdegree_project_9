# techdegree_project_6
_________________________________________________________________

Techdegree Project 9-Improve a Django Project
_________________________________________________________________

Introduction

The purpose of this project is to take a previously built app, identify ways that it can be improved, and address the issues. The app started with code that didn't follow convention and was buggy. While the app isn't particularly practical, it now adheres to more conventional practices and standards.


Installation

It is recommended that a virtual environment is used when installing the dependancies for this project.

1. Download the project files.

2. Navigate to the directory containing the requirements.txt file.

3. Run: pip install -r requirements.txt


Running the Server

1. Navigate to the 'my_site' folder

2. Run: python manage.py runserver


Issues Identified and Addressed:

1. Provided more efficient queries in the view to reduce the number of queries called by the templates

2. Properly implemented template inheritance

3. Adjusted model field types to more appropriate types and created migrations to convert the data

4. Implemented the proper use of ModelForms and wrote custom validators.

5. Wrote tests for the Menu app with more than 90% coverage

In addition to the project requirements I also refactored the views, updated the project to the current version of Django, changed the URLs from url() to path(), namespaced the URLs, added comments to views, created a navbar, created a registration and authorization system to allow only the creator of a menu to edit their own creations, added notification messages, refactored imports for better readability and more clear namespacing, and improved form styling and function.
