# DevOpsData
DevOps - Software Evolution and Software Maintenance - BSc (Spring 2021)

# Workflow
## Repository

We’ll be using a single repository (/mono repository/ model) for the entire project. Multiple reasons for this choice: 

* It fits better with the hand-in structure of the course. A single repo with one release containing everything. 

* Our technology stack (Django - Python) encourages using a single project for multiple “apps” such as a front-end website and a backend API. 

* Small team working on the same thing throughout the projects lifetime.


## Branching
We incorporate a bit of everything in our “branching strategy”. We’ll move all working code to a new /develop/ branch, such that /main/ is only used for full releases/stable versions. Topic branches are used for single, specific features, usually only handled by a single developer at a time. 

From /GitHub flow/, we further incorporate the use of pull-requests when merging topic branches into /develop/. This ensures the quality of the code and that every team member is /up-to-date/ on the state of the code-base. 


## Virtualization
We are using docker docker containers for eg. Api, Web, Database

## CI-CD
The docker images are stored on docker hub (anderstandevad) and the aplication is hosted via digitalocean (gergokoncz). We utilize github actions to orcastrate automatic deployment. It is a two step sprocess: 1. pushing to the development branch results in testing, linting and deploying to a test server (http://134.209.248.68/) 2. pushing to main is the same, except that images are deployed to the  production server (http://157.230.77.141/). This allows us to test changes in a production like workflow/environment.

## Static code analysis
We use 
* black for styling, 
* and xenon for code complexity analysis

## Monitoring
We monitor our oprations using prometheus and visualize metrics using grafana. Each has its own container that is hosted on the same servers (test and production). You can see the dashboards on port 3000 using the 
* username devops
* password -lEtMeIn-

## Logging
