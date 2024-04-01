# How to run the project

- To run the api server execute: make run
- To execute the tests: make test

Both commands are only suitd for linux based operating systems not for windows

# Project considerations

- I decided to use Flask framework as i consider it's a good fit for this application, however in order for it to scale properly there are a couple of things we need to take care of which are not introduced here for timing reasons:
  1. In order to handle concurrecy we might need to integrate it with Gunicorn or use a library like asyncio.
  2. Caching is crucial, we have a cache in our main endpoint that also considers query params, but we might need further configuration as needed. For this project we have used FlaskCaching which is a good caching library to integrate with Flask.
  3. Horizontal Scaling: Horizontal scaling by deploying multiple instances of our Flask application behind a load balancer would be a common approach to handle increased traffic, specially for our high peeks. Containerization with Docker or orchestration with Kubernetes would simplify the deployment and management of multiple instances of our app.
  4. As an Alternative we might also consider using FastApi instead of Flask, so we get all the async behaviour out of the gate.
  5. In production we would need to run this application behind a web server like Nginx or Apache to handle static and caching on the server more efficiently.
  6. For a production setup we would need to set up monitoring tools such as datadog, sentry. What is most important to keep an eye is our server runtime status and also our endpoint response time as well, to check how it behaves with high traffic and with huge responses from the external api
