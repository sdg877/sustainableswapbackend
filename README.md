Excalidraw plan:

![ss1](https://github.com/sdg877/sustainableswapfe/assets/149600602/9d9b0c6f-3be7-4883-bb4b-423a435dfa4f)

ERD:

![ss2](https://github.com/sdg877/sustainableswapfe/assets/149600602/728b52cc-205a-4707-9e92-6d8f5f2d7f35)

Login Page:

![ss3](https://github.com/sdg877/sustainableswapfe/assets/149600602/c9774953-a515-460d-90ed-07ce5f3469d1)

Signup Page:

![ss4](https://github.com/sdg877/sustainableswapfe/assets/149600602/5372d25b-8d5a-4172-9cb8-c0634de3bd43)

Homepage before logging in:

![ss5](https://github.com/sdg877/sustainableswapfe/assets/149600602/437c7aac-e5c5-4776-b6f7-afca32afd68f)

Homepage after logging in:

![ss6](https://github.com/sdg877/sustainableswapfe/assets/149600602/8da54752-51db-41dd-9bf9-2005d1bdcaa7)

Add item form:

![ss7](https://github.com/sdg877/sustainableswapfe/assets/149600602/d095b0a3-7c98-47c4-9e13-b49a6374147a)

Profile Page (when User has items listed):

![ss8](https://github.com/sdg877/sustainableswapfe/assets/149600602/bfce005f-5470-414c-b353-4afa2a83afec)

Profile Page (no items listed):

![ss9](https://github.com/sdg877/sustainableswapfe/assets/149600602/5b3b82ca-427e-4f68-a9a0-cb5a6244ab7a)

Item view (no swaps):

![ss10](https://github.com/sdg877/sustainableswapfe/assets/149600602/9990e279-9044-4eb5-984b-bb0cc743a21b)

Itemview (with swap offered):

![ss11](https://github.com/sdg877/sustainableswapfe/assets/149600602/4b38b8ca-5aa7-46a0-adc8-eaac9540b40d)


Description
For my Unit 4 project, we were required to build a full-stack web application using the Python-based Django Web Framework. I am interested in the Environment and fast fashion so I decided to build a clothes swap site. 

Deployment Links 
GitHub Frontend: https://github.com/sdg877/sustainableswapfe
GitHub Backend: https://github.com/sdg877/sustainableswapbackend
Deployed Frontend: http://sustainableswapfe-production.up.railway.app
Deployed Backend: http://sustainableswapbackend-production.up.railway.app

Timeframe
This was a solo project and we were given seven working days to complete this, this included planning. 

Technologies used:
Django
React
PostgreSQL
Bootstrap

Brief
We were asked to build a fully CRUD website with Django and React. We needed to have two data entities besides the built-in User model, ideally with one one-to-many relationship and one many-to-many relationship. Users must be able to Authenticate using Django’s built-in system and CRUD must be restricted to authenticated users. The site must be deployed online using Railway. Additionally, we could allow Users to upload images AWS S3 or consume an API, I chose to allow users to add images of their clothes as this was more relevant to my site. In addition to this, we should focus on UI, ensuring that the app looked professional and was easy to navigate.

Code Process
Created Git Repos for the backend and front end and set up Django and React environments, installing the relevant dependencies.
Integrated Django backend with React frontend.
Established database schemas, models, and serializers using the ERD for reference. Migrating once these had been done. 
Configured URLs to map endpoints to views.
Implemented login, signup forms, and logout. I was having issues allowing only the owner to CRUD their entries, a classmate assisted me with adding a file called currentUser.js in a folder called lib, this added a function that stored the jwt token in local storage which fixed the issue. After deployment, I found that this function did not work on mobile devices which meant that users received an error when trying to access items. I altered the function to manually decode the jwt token which resolved the issue. 
Created the following pages and forms:
Item List - shows all listed items for all users
Item View Page - shows a more detailed view of a single item, any swaps offered and a form for users to add their item to swap.
Profile page - only available if a user is logged in. It shows the current users items, if none, a button linking to the add an item form. Users can also edit or delete their items from this page.
About me page
ItemCreate - allowed users to add their items for swap if logged in.
ItemEdit - allows the item owner to edit the form.
I then created a navbar so users could easily navigate between the different pages.
Image Uploads: Utilized AWS S3 bucket for image uploading. This was quite a complicated process as there were many steps and I had only done this once before so I required some assistance from my instructor to ensure that the images were saved to the database. This was done by modifying the Item model, serializer, and views.
Created a dotenv file to securely store the sensitive information relating to my app. 
Enabled users to upload items and bid on items for swap using a swap form.
Designed pages, components, and item cards using Bootstrap and following the style plan that I created on day one of the project in Excalidraw. 

Models.py (showing Item and Swap schemas):

![ss12](https://github.com/sdg877/sustainableswapfe/assets/149600602/b4b8ce6d-ddde-4f73-b1ac-35220b241dc8)

Urls.py:

![ss13](https://github.com/sdg877/sustainableswapfe/assets/149600602/be468dec-c8ef-4966-9af5-35537662359f)


Snippet from LoginForm.jsx:

![ss14](https://github.com/sdg877/sustainableswapfe/assets/149600602/bba9bad1-7d58-4333-9bf6-f01fab95b306)



Challenges
I needed assistance with Authorization for this project and with allowing Users to upload images with their items. I also ran out of time due to the time taken to set up Authorization so had to cut back on some of my functionality, however, the project still met all of the requirements.

Wins
Getting the project completed was a major win as the setbacks were pretty huge.

Key Learnings
I became much more familiar with and confident using Django during this project.

Bugs
I had issues with my edit function, I resolved this with the help of the instructor. 

Future Improvements
There are several improvements I would like to make to this site:
The User can change the image of a listing when editing 
Owner can approve or delete the swaps offered
An image can be added when offering a swap
Only a different user to the owner can add an item to swap
Filter by items

