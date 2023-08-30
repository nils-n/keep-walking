# *Keep on Walking* - improve your health and happiness by daily walks

Have you walked 7000 steps today? According to science, a daily step count of 7000 steps is associated with increased happiness, mental health and improvement of various body parameters ( [Paluch, et. al., 2021](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2783711?utm_source=For_The_Media&utm_medium=referral&utm_campaign=ftm_links&utm_term=090321), [Choi, et. al., 2019](https://jamanetwork.com/journals/jamapsychiatry/article-abstract/2720689)). The aim of this website is to take up on this idea and promote health, fitness and happiness.

 Users are encouraged to sign up and log their daily step count using their  Garmin&copy; watch. The website will keep them on track with their step goal, and inform them if they are progessing in their goal of either reaching or maintaining a healthy BMI (body-mass-index). In addition, a simple statistic will be applied across all signed up users as to wheter meeting the targeted step count  improves their health parameters, such as increased sleep times, reduced heart variability and reduced stress levels. 

**References:**

[1] *Paluch, Amanda E., et al. "Steps per day and all-cause mortality in middle-aged adults in the coronary artery risk development in young adults study." JAMA Network Open 4.9 (2021): e2124516-e2124516.*

[2] *Choi, Karmel W., et al. "Assessment of bidirectional relationships between physical activity and depression among adults: a 2-sample mendelian randomization study." JAMA psychiatry 76.4 (2019): 399-408.*

--- 

- [*Keep on Walking* - improve your health and happiness by daily walks](#keep-on-walking---improve-your-health-and-happiness-by-daily-walks)
  - [User Experience (UX)](#user-experience-ux)
    - [User Stories](#user-stories)
    - [Website Aims](#website-aims)
    - [How these needs are addressed](#how-these-needs-are-addressed)
    - [Opportunities](#opportunities)
    - [Feature selection](#feature-selection)
  - [Design](#design)
    - [Color Scheme](#color-scheme)
    - [Typography](#typography)
    - [Imagery](#imagery)
  - [Wireframes](#wireframes)
  - [Features](#features)
    - [General Features](#general-features)
    - [Main Page](#main-page)
    - [Future Implementations](#future-implementations)
    - [Accessibility](#accessibility)
  - [Models](#models)
  - [](#)
  - [Technologies Used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks](#frameworks)
  - [Deployment](#deployment)
      - [How to Fork](#how-to-fork)
      - [How to Clone](#how-to-clone)
    - [Deployment on Heroku](#deployment-on-heroku)
    - [2. Heroku Setup](#2-heroku-setup)
  - [Testing](#testing)
    - [Testing Procedure](#testing-procedure)
    - [Solved Bugs](#solved-bugs)
    - [Open Bugs](#open-bugs)
  - [Credits](#credits)
    - [Code Used](#code-used)
    - [Content](#content)
  - [Acknowledgements](#acknowledgements)


----

## User Experience (UX)

### User Stories 

--- 

### Website Aims

### How these needs are addressed

### Opportunities 

### Feature selection

----- 

## Design

### Color Scheme

### Typography

### Imagery

-----

## Wireframes

---- 

## Features

### General Features 


The website consits of several pages, and a 404 page and are responsive, designed using a mobile-first approach.

### Main Page 


### Future Implementations


### Accessibility

--- 

## Models 

User data are stored in a relational database. The main model has been carefully designed to allow for emotional ratings and API calls from the Garmin Connect App:

- **User**: each row is a user that has signed up on the website
- **GarminData**:  each row is an entry as read from the Garmin API (Many-to-Many Field)
- **EmotionRating**:  each row is a rating that a User for a specific date (Many-to-Many Field)

<table style='width:90%; content-align:center'>
    <tr>
       <td> <img src="./assets/images/drawSQL-pp4-activity-tracker.png"; alt="ER diagram of the model" >  </td>
    </tr>
</table>
--- 

## Technologies Used 

- [DrawSQL](https://drawsql.app/) 

### Languages 

- HTML
- CSS
- Python

### Frameworks 

- jQuery
- Bootstrap (V. 4.2)
- Pytest 

----- 

## Deployment

#### How to Fork

#### How to Clone

---- 

### Deployment on Heroku 

###  2. Heroku Setup

---


## Testing 

### Testing Procedure 


---

### Solved Bugs 

- In a first iteration of this project, I made a mistake in the Model design where I kept the emotional rating linked to the readout from the Garmin device. This has made my life *very* difficult creating `POST` requests and handling the CRUD functionality. 
  - Solution : The best way seemed to me to go back to the Models and simplify from the start by improving the data structure design. The solution was to separate the *GarminData* table(readouts from the Garmin API) and the *EmotionRating* table. In this way, the user can do CRUD operations for each table *independently* - and also, the data structure seems more natural.   

### Open Bugs 

---- 

## Credits 

### Code Used


### Content 

- All of the content was written by myself.
- Externally used code (such as code snippets from stackoverflow) in this project are referenced in this Readme and inside the HTML / CSS / JS / Python source code. 


## Acknowledgements

- Teaching and Support from Code Insitute [Code Insitute](https://codeinstitute.net/)
- How to approach designing Django Models  :
  - DjangoGirls online tutorial : [Django models](https://tutorial.djangogirls.org/en/django_models/) 
  - LearnDjango Blog from W. Vincent  [Django Best Practices: Models](https://learndjango.com/tutorials/django-best-practices-models)
  - I've spent a fair amount of time researching how Models work. Here a selection of blog Articles and Youtube videos that contributed to my understanding :
    -  Klement Omeri : [Best practices and tips to build better Django models (Medium)](https://medium.com/@daspiyush0_44431/best-practices-and-tips-to-build-better-django-models-c0f78cd4e52e)
    -  Sagar Chopade:  [Django Model Best Practices: Tips and Tricks for Clean and Efficient Code (Medium)](https://medium.com/@schopade333/django-model-best-practices-c5c8a142dfc)
    -   Sagar Chopade:  [Custom Model Managers In Django (Medium)](https://medium.com/scalereal/custom-model-managers-in-django-2dac30acdf55)
    -  Ben Lopatin/ Cobey Potter, 'This Old Pony', Wellfire Interactive : [The problem with fat models, or, an OOPs mistake](https://wellfire.co/this-old-pony/the-problem-with-fat-models--or--an-oops-mistake--this-old-pony-69/)
    - Jair Verçosa [Django model Guideline (Medium)](https://jairvercosa.medium.com/django-model-guideline-d48a96c9b38c)
    - Aravind Srinivas [Essential Tips for Optimizing Your Django Models for Better Code Readability  (Medium)](https://awstip.com/essential-tips-for-optimizing-your-django-models-for-better-code-readability-f1a22665fe25)
    - Michał Macura (Soft Kraft) : [Django Best Practices — Refactoring Django Fat Models](https://www.softkraft.co/django-best-practises/)
    - Matt Freire, [Learn the basics of Django's Model Managers and Querysets - YouTube](https://www.youtube.com/watch?v=rjUmA_pkGtw)
    - Tarun Garg [Design Django models such that your future self will thank you - YouTube](https://www.youtube.com/watch?v=dXCh8m4P5Tc)
- Thanks to my mentor Ronan (Code Institute) for his advices and clear feedback 