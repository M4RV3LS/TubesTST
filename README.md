# 🎵Collaborative Jamming Scheduler (CJS) API Service
## Table of Contents
- [Introduction](#introduction)
- [Using the API](#using-the-api)
  - [FastAPI Docs](#fastapi-docs)
  - [Terminal Commands](#terminal-commands)
  - [Using Postman](#using-postman)
- [CRUD Operations](#crud-operations)
- [Author](#author)

## 😀Introduction

Welcome to the Collaborative Jamming Scheduler (CJS) API service! Crafted with precision by Marvel Subekti (NIM: 18221058), this service is designed to orchestrate musical jamming sessions seamlessly. Part of the esteemed Sistem dan Teknologi Informasi - Institut Teknologi Bandung, this API lets you create, manage, and participate in jamming sessions with ease.



## ❓How to Use the API Service

### Using FastAPI Docs
[click the API Service Docs here](http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/docs)

## Documentation

[Documentation](https://docs.google.com/document/d/14eSss1uJOFtZJBpz1CMrtTIpAJ-EjZTIdrVaOsAyWEM/edit?usp=sharing)

#### Read Operations
- Navigate to the CJS API Documentation.
- Click on the GET operation you want to test (e.g., `/participants/` to list all participants).
- Hit the "Try it out" button, input any required parameters, and then execute the request.

#### Create, Update, and Delete Operations
- For POST (create), PUT (update), or DELETE operations, follow the same steps as above, but input the necessary JSON body or path parameters.
- Ensure you fill out all the required fields in the request body for POST and PUT requests.
- Execute the request and observe the response.

### 👩‍💻Using Terminal

#### Read (GET)
```bash
curl -X 'GET' \
  'http://<your-api-url>/sessions/' \
  -H 'accept: application/json'
```

#### Create (POST)
```bash
curl -X 'POST' \
  'http://<your-api-url>/sessions/' \
  -H 'Content-Type: application/json' \
  -d '{
    "host_name": "John Doe",
    "studio_name": "Best Studio",
    ...
  }'
```
#### Update (PUT)
```bash
curl -X 'PUT' \
  'http://<your-api-url>/sessions/{session_id}' \
  -H 'Content-Type: application/json' \
  -d '{
    ...
  }'
```

#### Delete (DELETE)
```bash
curl -X 'DELETE' \
  'http://<your-api-url>/sessions/{session_id}' \
  -H 'accept: application/json'
```

## 📮Using Postman

### Read (GET)
- Initiate a new request in Postman.
- Set the HTTP method to `GET`.
- Enter the endpoint URL you wish to query.
- Click 'Send' to execute the request and view the response.

### Create (POST)
- Create a new request in Postman.
- Change the HTTP method to `POST`.
- In the 'Body' tab, choose 'raw' and select 'JSON' from the dropdown.
- Enter the JSON payload for creating a new session.
- Click 'Send' to submit the request.

### Update (PUT)
- Change the method to `PUT` for updating an existing resource.
- Input the endpoint URL for the resource you want to update.
- In the 'Body' tab, choose 'raw' and select 'JSON' from the dropdown.
- Enter the updated JSON data.
- Click 'Send' to apply the update.

### Delete (DELETE)
- For deletion, set the method to `DELETE`.
- Enter the endpoint URL of the resource you wish to delete.
- Click 'Send' to execute the deletion.

## CRUD Operations

- **Create:** Utilize `POST` requests to add new sessions or participants.
- **Read:** Employ `GET` requests to obtain details about existing sessions or participants.
- **Update:** Use `PUT` requests to revise information of sessions or participants.
- **Delete:** Implement `DELETE` requests to expunge sessions or participants.


## 🔥API Reference

The API is structured around two main classes, `Session` and `Participant`, and provides endpoints to interact with them. Below are the endpoints and utility functions available.

```python
class Session(BaseModel):
    ...

class Participant(BaseModel):
    ...

app = FastAPI()

@app.get("/")
...

@app.post("/sessions/")
...

@app.get("/sessions/{session_id}")
...

@app.put("/sessions/{session_id}")
...

@app.delete("/sessions/{session_id}")
...

@app.get("/participants/{participant_id}")
...

@app.post("/participants/")
...

@app.put("/participants/{participant_id}")
...

@app.delete("/participants/{participant_id}")
...

@app.get("/participants/")
...

@app.get("/participants/{participant_id}/sessions")

## API Reference

#### Get all items

```http
  GET /api/items
```
## FAQ 🤔

**Q: How do I add a new participant to a session?**

A: Use the PUT endpoint `/sessions/{session_id}/participants/{participant_id}`.

**Q: How do I remove a participant from a session?**

A: Use the DELETE endpoint `/sessions/{session_id}/participants/{participant_id}`.

**Q: What if I encounter a 404 error?**

A: This means the resource you're trying to access doesn't exist. Double-check your IDs and try again.

**Q: How do I report an issue or suggest a feature?**

A: You can reach out to the author directly via email or raise an issue in the project's repository.

<br>

# 🚀 FastAPI Registration, Login, and Authentication - User Guide

This guide will walk you through the steps to test the login, registration, and authentication features of our FastAPI application, which is containerized and deployed on Microsoft Azure. You can interact with the API using FastAPI's interactive documentation, Postman, or via PowerShell.

## Prerequisites

- Access to [FastAPI Docs](http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/docs)
- [Postman](https://www.postman.com/downloads/) (for API testing)
- PowerShell (for command-line interactions)

## 📝 Using FastAPI Docs

FastAPI automatically generates interactive documentation for your API. You can use this to test the API endpoints directly from your browser.

### 1. Open FastAPI Documentation

Navigate to [FastAPI Docs](http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/docs).

### 2. Register a New User

- Click on the `/register/` endpoint.
- Click `Try it out`, enter the required user details, and then click `Execute`.
- You should receive a response indicating successful registration.

### 3. Login

- Find the `/token/` endpoint.
- Again, click `Try it out`. Use the same credentials you registered with and click `Execute`.
- You will receive a JWT token in the response.

### 4. Access Protected Endpoints

- Copy the JWT token from the login response.
- For any protected endpoint, click the `Authorize` button at the top of the docs and paste your token.
- Now you can `Try out` protected endpoints with your authenticated user.

## 📫 Using Postman

Postman is a popular tool for API testing. You can use it to send requests to your API and view the responses.

### 1. Set Up

Open Postman and create a new request.

### 2. Register a New User

- Set the request type to `POST` and the URL to `http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/register/`.
- In the `Body` tab, select `raw` and `JSON`, then input the user details in JSON format.
- Send the request and check the response.

### 3. Login

- Change the URL to `http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/token/`.
- Send the login credentials. Save the JWT token from the response.

### 4. Test Authenticated Requests

- For any protected endpoint, add an `Authorization` header with the value `Bearer <your_token>`.
- Send your request to the protected endpoint.

## 💻 Using PowerShell

For those who prefer using the command line, PowerShell can be used to make HTTP requests to the API.

### 1. Register a New User

```powershell
$body = @{
    email = 'your_email@example.com'
    password = 'your_password'
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/register/' -Method Post -Body $body -ContentType 'application/json'
```

### 2. Login
```powershell
$loginBody = @{
    username = 'your_email@example.com'
    password = 'your_password'
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri 'http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/token/' -Method Post -Body $loginBody -ContentType 'application/x-www-form-urlencoded'
$token = $response.access_token
```

### 3. Access Protected Endpoints
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri 'http://tubestst2.c4d6hxc3gvdqexg2.southeastasia.azurecontainer.io/protected-endpoint/' -Method Get -Headers $headers
```

## Skills Required 🛠️

- **FastAPI**: Knowledge of FastAPI framework for building APIs.
- **Python**: Proficiency in Python for scripting and backend logic.
- **JSON**: Understanding of JSON format for request and response data.
- **HTTP**: Familiarity with HTTP methods and status codes.
- **Client-Server Model**: Understanding of client-server architecture.
- **Microsoft Azure**: Experience with Microsoft Azure for server management.

## Tech Stack

**Client:** FastApi <br>
**Server:** Microsoft Azure



## Authors

- [@marvelsubekti](https://github.com/M4RV3LS)
- **Name:** Marvel Subekti
- **Contact:** marvelsubekti@gmail.com

