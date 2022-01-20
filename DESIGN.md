# UniPlan Design Documentation
This document is an ongoing record of my design process (mistakes and all) – here I will jot down all my thoughts, considerations, and processes for designing uniplan. Let's start with functionality requirements, shall we?

## Functionality Requirements

- [ ] Login / Logout
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
- [ ] Implement sessions
- [ ] Batch add units
- [ ] Batch add assignments (a dropdown to select relevant unit -> one blank box for assignment, and a plus undearneath to add another blank form)


## Database design

Use Draw.io file 'schema.drawio'

# Django Login Functionality

- [https://learndjango.com/tutorials/django-login-and-logout-tutorial](https://learndjango.com/tutorials/django-login-and-logout-tutorial)
- [Youtube Series on Django user forms](https://www.youtube.com/watch?v=Nxgi4qF6i1Q&list=PLCC34OHNcOtr025c1kHSPrnP18YPB-NFi&index=24)
- [How to save profile info alongside Django user object](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)

Login and authentication functionality leverages Django's builtin auth model. Rather than modifying the base user class there is a supplementary model 'profile' which has its own form and is saved alongside the user object at signup. It turned out to be incredibly challenging to get the user profile to be created alongside the user at signup – there were many different approaches to this, most of which involved creating a listener within the Django model, however I could not get this to work (trust me, I tried). [This method of parsing and saving two forms ended up saving me](https://youtu.be/Tja4I_rgspI). We are now saving the profile as a one-to-one relationship with the user, and storing attributes such as University, and Course under this 'student_profile' model. Needless to say – lesson learnt: keep it simple stupid. 

