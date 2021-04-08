# techdegree_project_6
_________________________________________________________________

Techdegree Project 9-Improve a Django Project
_________________________________________________________________

Introduction




Installation

It is recommended that a virtual environment is used when installing the dependancies for this project.

1. Download the project files.

2. Navigate to the directory containing the requirements.txt file.

3. Run: pip install -r requirements.txt


Running the Server

1. Navigate to the 'mineral_catalog' folder.

2. Run: python manage.py migrate

3. Run: python manage.py runserver


Features

Mineral Catalog-A list of all available minerals are displayed. Any mineral my be selected to view on a detail page.

Mineral Details-A page displaying the name, photograph, and mineral details can be accessed from the mineral catalog.

Random Mineral-The user may go to the random mineral page to view a mineral selected at random. A new mineral may be requested from that page.

Routing Uses Slugs-URLs are readable. Slugs are automatically generated when a mineral is created and the slugs are used for URL routing.

New for Project 8:

You can now search the catalog by: search term, first letter of mineral name, mineral group, or mineral color.


Thanks Kenneth Love, Chris Howell, Zachary Jackson, Jordan Hoover, and the rest of Team Treehouse!
