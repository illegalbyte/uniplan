# UniPlan Design Documentation
This document is an ongoing record of my design process (mistakes and all) – here I will jot down all my thoughts, considerations, and processes for designing uniplan. Let's start with functionality requirements, shall we?

## Functionality Requirements

- [X] Login / Logout
- [ ] Ability to track units enrolled in 
- [ ] Plan future unit enrollments (coursemap) and have this validated against Deakin University unit guides (eg warn me if a unit is only available in semester 2 etc)
- [ ] Deploy using AWS – include some sort of serverless functionality
- [X] Implement an accounts and login system utilising Django Auth (this tool should be able to benefit others)
- [ ] Track unit grades (High Distinction, etc)
- [ ] Measure and track assignment performance, assessment weightings, throughout the semester 
- [ ] Able to handle complexity: hurdle tasks
- [ ] Have a dashboard which displays your WAM
- [ ] Design using React and Boostrap (limit efforts invested in manually writing CSS)
- [ ] CRUD API functionality
- [ ] Working email backend
- [ ] Upcoming assessments and email notifications
- [ ] [Implement sessions](https://www.youtube.com/watch?v=N-R5mT-nIDk)
- [ ] Batch add units
- [ ] Batch add assignments (a dropdown to select relevant unit -> one blank box for assignment, and a plus undearneath to add another blank form)
- [ ] implement REACT for handsome front-end design - research examples of Django + react 

## UI Design 

- [ ] Dropdown for all accounts tasks (use django if statements to only show relevant links: eg don't show logout if not logged in)

## UX Design

- [ ] Homeoage should have easy access to most often needed utilities: adding assignment, updating data on assignments, 
adding grade for an ongoing assignment, completing an assignment, displaying WAM, a list of upcoming assignments, a calendar view (or something more useful and bespoke?) a list of weeks starting on sunday, through to Saturday, and each line is a uni week with demarkations for the week number, census dates etc etc)

## Database design

<s>Use Draw.io file 'schema.drawio'</s>

I've stumbled upon the dbml markup language which is incredibly useful and has a great tool at [dbdiagrams.io](https://dbdiagrams.io) – essentially this is a way of writing ER diagrams as code, and it's really neat! Definitely something I need, mainly to keep track of all the attribute names. All my database schema design will be done in the schema.dbml file for now. 

# Django Login Functionality

- [https://learndjango.com/tutorials/django-login-and-logout-tutorial](https://learndjango.com/tutorials/django-login-and-logout-tutorial)
- [Youtube Series on Django user forms](https://www.youtube.com/watch?v=Nxgi4qF6i1Q&list=PLCC34OHNcOtr025c1kHSPrnP18YPB-NFi&index=24)
- [How to save profile info alongside Django user object](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)

Login and authentication functionality leverages Django's builtin auth model. Rather than modifying the base user class there is a supplementary model 'profile' which has its own form and is saved alongside the user object at signup. It turned out to be incredibly challenging to get the user profile to be created alongside the user at signup – there were many different approaches to this, most of which involved creating a listener within the Django model, however I could not get this to work (trust me, I tried). [This method of parsing and saving two forms ended up saving me](https://youtu.be/Tja4I_rgspI). We are now saving the profile as a one-to-one relationship with the user, and storing attributes such as University, and Course under this 'student_profile' model. Needless to say – lesson learnt: keep it simple stupid. 

Next I will implement enrolling in units, registering assignments etc – lets start with fixing our models.

# Enrollments, Units, Assignments

So this tool is meant to somewhat be a live 'course-map'. You should be able to make edits to it, and in realtime, the coursemap will validate and tell you if your course is valid or not. 

One issue is that this validation requires a huge dataset which will need to be able to check unit pre-requisites, whether the unit is available in the given semester, etc. I've added the ability to manually add units, however it's probably best we move onto web-scraping the unit guide. Thankfully these are fairly standardised documents which shouldn't be very hard to digest. We need a few key items from them: 

* course map URL
* Deakin course code
* List of major sequences
* list of Minor sequences
* Core units

–– a few hours later ––

Great, the web scraper is now able to take a URL from a webform at /scrape and leverage beautifulsoup4 to scrape the Bachelor of Information Technology Web Page – it will then search for all the units listed, and collect the unit code, links to the unit's handbook, and the unit's title. The scraper also collects information about the degree, but given I'm still working with just Bachelor of IT data, I'll handle this later. ( **TODO**: allow scraper to add the course if it does not yet exist )

There are some limitations so far: 
-  the scraper can't parse a list of core units, a list of major sequences, or a list of minor sequences: this is because I'm fairly unfamiliar with beautiful soup, and how to best go about parsing the document. I'm sure the answer is waiting for me on some ungodly stackoverflow thread, but I'll leave it for another day. 
-  In order to save this data, I'll have to add a few tables to my database too – major_sequences, core_sequences, and minor_sequences tables. Each course has one core_sequence so this is a one-to-one relationship, while the other two will be one-to-many relationships with the units table.


# form.as_table

I'm putting this here as a reminder to try format my forms a bit differently


# add detailed unit data:

web scraping work is largely done for now, I want to pivot to working on the assignments and grade tracking - all this enrollment is doing my head in and I'll benefit from thinking about something else for now. 
-> TODO: 

[ ] Units lack relevant data about how many credit points they are worth. I'll need to implement updating the existing database entries with this data, because currently the only way unit data is changed is at the time of creation OR via the admin panel. Maybe I will implement a CRUD API to make this easier. 

[ ] Assignments, grades, etc


## Feature ideas

[ ] Ability to rate units on different dimensions: teaching quality, difficulty, etc etc - can use a glassdoor mechanism to get users to review a unit in order to view other units



# useful links: 
- [Django Javascript Hybrid Framework pt 1](https://www.saaspegasus.com/guides/modern-javascript-for-django-developers/client-server-architectures/)


## API related Rest Framework stuff

- [Rest API Examples](https://simpleisbetterthancomplex.com/tutorial/2018/02/03/how-to-use-restful-apis-with-django.html)
- [Rest CRUD API outline](https://stackabuse.com/creating-a-rest-api-with-django-rest-framework/)


## Javascript Toolchain notes: 

- [Django Javascript Hybrid Framework pt 1](https://www.saaspegasus.com/guides/modern-javascript-for-django-developers/client-server-architectures/)

- package manager: npm
- bundler: webpack 
- compiler: babel 

![Js Architecture](https://www.saaspegasus.com/static/images/web/modern-javascript/js-pipeline-with-django.png)

- [Setting up the pipeline](https://www.saaspegasus.com/guides/modern-javascript-for-django-developers/integrating-javascript-pipeline/)

```bash 

npm run dev

```