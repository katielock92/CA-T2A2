# API Web Server Application (_Coder Academy Term 2 Assignment 2_)

### _Prepared by Katie Lock_

___
## **Project Summary**
x
___
## Planning and Documentation Requirements
### ***R1: Identification of the problem you are trying to solve by building this particular app***
For my API web server application, I am creating a basic Application Tracking System (known as an ATS for short).  An ATS "streamlines the hiring process by automating and organising each step along the way, making it easier to connect with qualified candidates more efficiently."^[1]^

Companies of varying sizes commonly utilise an ATS in their recruitment and hiring practices to support a standardised workflow for recruitment.  This ensures that all applications are kept in a central location and there is consistency in the data collected and stored for roles, candidates and interviews.  Using an ATS also saves hours of administration and manual work, such as copying applications from a job board, or individually emailing rejected candidates.

My API web server application would be the foundation for a simple, low-cost ATS that could provide the key tasks to supporting in hiring, and provide a centralised database of hiring data for richer reporting.

___
### ***R2: Why is it a problem that needs solving?***
A real-life problem that many small businesses face is that a dedicated ATS is often outside of their budget, and therefore they have to rely on a combination of other cheaper SaaS tools to manage their recruitment processes.  This is something that I personally faced in my current company - at the start of the pandemic we had no ATS, and therefore after applicants applied for roles on our website, different departments followed different processes for the next steps.  The Engineering team utilised a private Trello board per role for short-listed candidates, though this involved needing to have interview notes linked from Google Docs, manually sending calendar invites and communications with candidates, and manually uploading resumes to the Trello board.

Having an ATS, even if a simple one, helps to provide consistency and efficiency in hiring for businesses.  The current economic conditions mean that many businesses are not actively hiring, and often only have open roles if staff leave.  This makes it more difficult, particularly for start-ups, to justify the cost of having an ATS to their management, despite the enormous time saving and rich centralised data that it can provide.

___
### ***R3: Why have you chosen this database system. What are the drawbacks compared to others?***
My API application will utilise a PostgreSQL database system.

___
### ***R4: Identify and discuss the key functionalities and benefits of an ORM***
x

^[3]^

___
### ***R5: Document all endpoints for your API***
The API has a total of **x** endpoints, documented below in detail.

There are 2 primary types of authentication (beyond simply requiring a JWT) that are utilised in routes through a wrapper function, which will be summarised here and then referenced when discussing each route:

***authorise_as_admin:***
- A valid JWT token is required for this request
- The user's identity is checked using the token, and then the Staff table is searched for the user_id value that matches
- If there is no match in the Staff table, an error is returned as the user is not validated
- If there is a match in the Staff table, the admin field is checked for the user's row - the user is only authenticated if this field is True

***authorise_as_staff:***
- A valid JWT token is required for this request
- The user's identity is checked using the token, and then the Staff table is searched for the user_id value that matches
- If there is no match in the Staff table, an error is returned as the user is not validated
- If there is a match in the Staff table, the user is validated

### Endpoint Documentation

***Endpoint #1 - Register:***
- **Route:** */auth/register*
- **Purpose:** Allows new users to register for the app
- **HTTP request method:** POST
- **Required data:**
    - User to supply "email" and "password" in string format
    - Email must be unique and meet regex conditions
    - Password must be at least 8 characters in length
- **Expected response data:**
    - *If successful:* The "email" and "user_id" fields are returned to the user in JSON format
    - If either field is missing, an IntegrityError triggers an error message to be returned to the user
    - If email address is not unique, an IntegrityError triggers an error message to be returned to the user
    - If the email address or password do not meet the validation conditions, a ValidationError triggers an error message to be returned to the user
- **Authentication methods:** None

***Endpoint #2 - Login:***
- **Route:** */auth/login*
- **Purpose:** Allows existing users to login to the app and perform authenticated tasks
- **HTTP request method:** POST
- **Required data:**
    - User to supply "email" and "password" in string format, that match an existing record in the Users table
- **Expected response data:**
    - *If successful:* the "email" field and a JWT access token are returned to the user in JSON format
    - If the email address does not exist in the users table, or an incorrect password for this email was supplied, an error message is returned to the user
- **Authentication methods:** None

***Endpoint #3 - View Users:***
- **Route:** */users*
- **Purpose:** Allows admin users to view the list of all users
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
    - *If successful:* a list is returned in JSON format of all records in the Users table, excluding the password field
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #4 - Update User:***
- **Route:** */users*
- **Purpose:** Allows a user to update their own email and password that is used to login
- **HTTP request method:** PUT, PATCH
- **Required data:** "email" and/or "password" (in string format)
- **Expected response data:**
    - *If successful:* The "email" and "user_id" for the updated user record will be returned in JSON format, password is not displayed even if this is updated
    - An error is returned if no JWT is supplied
- **Authentication methods:**:
    - get_jwt_identity is used to the confirm the user_id of the logged in user

***Endpoint #5 - Delete User:***
- **Route:** */users/<user_id>*
- **Purpose:** Allows an admin to delete a user
- **HTTP request method:** DELETE
- **Required data:** user_id to be entered into the route
- **Expected response data:**
    - *If successful:* A message is returned confirming that the user has been deleted
    - If the user_id supplied does not match an entry in the Users table, an error message is returned
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #6 - View Candidates:***
- **Route:** */candidates*
- **Purpose:** Allows admin users to view the list of all candidates
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
    - *If successful:* a list is returned in JSON format of all records in the Candidates table
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #7 - Create Candidate:***
- **Route:** */candidates*
- **Purpose:** Allows a user to create a link record for themselves in the Candidates table
- **HTTP request method:** POST
- **Required data:** "name" and "phone_number" in string format
- **Expected response data:**
    - *If successful:* The "name", "phone_number" and "candidate_id" fields for the new record are returned to the user in JSON format
    - An IntegrityError is triggered and an error message is returned if there is already a candidate record for that user, or if a field is missing
    - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
    - An error is returned if no JWT is supplied
- **Authentication methods:**
    - get_jwt_identity is used to the confirm the user_id of the logged in user

***Endpoint #8 - Update Candidate:***
- **Route:** */candidates*
- **Purpose:** Allows an existing candidate user to update their name and/or phone number
- **HTTP request method:** PUT, PATCH
- **Required data:** "name" and/or "phone_number" in string format
- **Expected response data:**
    - *If successful:* The "name", "phone_number" and "candidate_id" fields for the updated record are returned to the user in JSON format
    - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
    - An error is returned if there is no existing candidate record for the logged in user
    - An error is returned if no JWT is supplied
- **Authentication methods:**
    - get_jwt_identity is used to the confirm the user_id of the logged in user

***Endpoint #9 - Delete Candidate:***
- **Route:** */candidates/<candidate_id>*
- **Purpose:** Allows an admin to delete a candidate from the Candidates table
- **HTTP request method:** DELETE
- **Required data:** candidate_id to be entered into the route
- **Expected response data:**
    - *If successful:* A message is returned confirming that the candidate has been deleted
    - If the candidate_id supplied does not match an entry in the Candidates table, an error message is returned
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #10 - View Staff:***
- **Route:** */staff*
- **Purpose:** Allows admin users to view the list of all staff
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
    - *If successful:* a list is returned in JSON format of all records in the Staff table
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #11 - Create Staff:***
- **Route:** */staff*
- **Purpose:** Allows an admin to add a registered user to the Staff table, enabling them to access staff-only and admin-only routes (if applicable)
- **HTTP request method:** POST
- **Required data:** "name" and "title" in string format, "user_id" in integer format
- **Expected response data:**
    - *If successful:* The schema fields for the new staff record are returned to the user in JSON format
    - An IntegrityError is triggered and an error message returned if there is already a staff record for the supplied user_id, or if a required field has not been provided
    - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
    - An error is returned if the user_id provided does not match any records in the Users table
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #12 - Update Staff (Own Record):***
- **Route:** */staff*
- **Purpose:** Allows a staff user to update the "name" and "title" fields on their own record
- **HTTP request method:** PUT, PATCH
- **Required data:** "name" and/or "title" in string format
- **Expected response data:**
    - *If successful:* The schema fields for the updated staff record are returned to the user in JSON format
    - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
    - An error is returned if there is no existing staff record for the logged in user
    - An error is returned if no JWT is supplied
- **Authentication methods:**
    - get_jwt_identity is used to the confirm the user_id of the logged in user

***Endpoint #13 - Update Staff (Admin Access):***
- **Route:** */staff/<staff_id>*
- **Purpose:** Allows an admin user to update the admin field on an existing staff record
- **HTTP request method:** PUT, PATCH
- **Required data:** staff_id to be entered into the route
- **Expected response data:**
    - *If successful:* The schema fields for the updated staff record are returned to the user in JSON format
    - If the staff_id supplied does not match an entry in the Staff table, an error message is returned
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #14 - Delete Staff:***
- **Route:** */staff/<staff_id>*
- **Purpose:** Allows an admin to delete a staff record from the Staff table
- **HTTP request method:** DELETE
- **Required data:** staff_id to be entered into the route
- **Expected response data:**
    - *If successful:* A message is returned confirming that the staff record has been deleted
    - If the staff_id supplied does not match an entry in the Staff table, an error message is returned
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #15 - View Open Jobs:***
- **Route:** */jobs*
- **Purpose:** Returns a list of all jobs with a status of open, with some fields not displayed unless a user is authenticated
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
    - *If successful:* a list is returned in JSON format of all records in the Jobs table with a status of "Open"
    - Non-staff users will not see "hiring manager" and "salary_budget" fields
    - Non-admin users will not see "salary_budget" field
- **Authentication methods:**
    - Optional: get_jwt_identity() is used to get the user_id of the logged in user to check if a more detailed schema can be returned, but a JWT is not required for the route to work

***Endpoint #16 - View All Jobs:***
- **Route:** */jobs/all*
- **Purpose:** Returns a list of all jobs (regardless of status), with some fields not displayed unless a user is authenticated
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
    - *If successful:* a list is returned in JSON format of all records in the Jobs table
    - Non-staff users will not see "hiring manager" and "salary_budget" fields
    - Non-admin users will not see "salary_budget" field
- **Authentication methods:**
    - Optional: get_jwt_identity() is used to get the user_id of the logged in user to check if a more detailed schema can be returned, but a JWT is not required for the route to work

***Endpoint #17 - View One Job:***
- **Route:** */jobs/<job_id>*
- **Purpose:** Returns the job record with the matching job_id, with some fields not displayed unless a user is authenticated
- **HTTP request method:** GET
- **Required data:** job_id to be entered into the route
- **Expected response data:**
    - *If successful:* the matching record from the Jobs table is returned in JSON format
    - Non-staff users will not see "hiring manager" and "salary_budget" fields
    - Non-admin users will not see "salary_budget" field
    - If the job_id supplied does not match an entry in the Jobs table, an error message is returned
- **Authentication methods:**
    - Optional: get_jwt_identity() is used to get the user_id of the logged in user to check if a more detailed schema can be returned, but a JWT is not required for the route to work

***Endpoint #18 - View Applications for a Job:***
- **Route:** */jobs/<job_id>/applications*
- **Purpose:** Allows a staff user to see the applications for a particular job
- **HTTP request method:** GET
- **Required data:** job_id to be entered into the route
- **Expected response data:**
    - *If successful:* the matching records from the Applications table are returned in JSON format
    - If the job_id supplied does not match an entry in the Jobs table, an error message is returned
    - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
    - authorise_as_staff

***Endpoint #19 - Create Job:***
- **Route:** */jobs*
- **Purpose:** Allows a staff user to create a new job record
- **HTTP request method:** POST
- **Required data:**
    - "title" in string format
    - "description" in text format
    - "department" in string format
    - "location" in string format
    - "salary_budget" in integer format
    - "hiring_manager_id" in integer format
- **Expected response data:**
    - *If successful:* The schema fields for the new job record are returned to the user in JSON format
    - An IntegrityError is triggered and an error message returned if a required field has not been provided
    - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
    - An error is returned if the "hiring_manager_id" provided does not match any records in the Staff table
    - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
    - authorise_as_staff

***Endpoint #20 - Update Job:***
- **Route:** */jobs/<job_id>*
- **Purpose:** Allows a staff user to update any field on an existing job record (other than job_id)
- **HTTP request method:** PUT, PATCH
- **Required data:**
    - job_id to be entered into the route
    - Plus at least one of the following:
        - "title" in string format
        - "description" in text format
        - "department" in string format
        - "location" in string format
        - "salary_budget" in integer format
        - "hiring_manager_id" in integer format
- **Expected response data:**
    - *If successful:* The schema fields for the updated job record are returned to the user in JSON format
    - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
    - An error is returned if the new "hiring_manager_id" provided does not match any records in the Staff table
    - An error is returned if the job_id in the route does not match any records in the Jobs table
    - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
    - authorise_as_staff

***Endpoint #21 - Delete Job:***
- **Route:** */jobs/<job_id>*
- **Purpose:** Allows an admin to delete a job record from the Jobs table
- **HTTP request method:** DELETE
- **Required data:** job_id to be entered into the route
- **Expected response data:**
    - *If successful:* A message is returned confirming that the job record has been deleted
    - If the job_id supplied does not match an entry in the Jobs table, an error message is returned
    - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
    - authorise_as_admin

***Endpoint #x - x:***
- **Route:** */x*
- **Purpose:** x
- **HTTP request method:** x
- **Required data:** x
- **Expected response data:**
    - x
    - x
- **Authentication methods:**
    - x

***Endpoint #x - x:***
- **Route:** */x*
- **Purpose:** x
- **HTTP request method:** x
- **Required data:** x
- **Expected response data:**
    - x
    - x
- **Authentication methods:**
    - x

***Endpoint #x - x:***
- **Route:** */x*
- **Purpose:** x
- **HTTP request method:** x
- **Required data:** x
- **Expected response data:**
    - x
    - x
- **Authentication methods:**
    - x

***Endpoint #x - x:***
- **Route:** */x*
- **Purpose:** x
- **HTTP request method:** x
- **Required data:** x
- **Expected response data:**
    - x
    - x
- **Authentication methods:**
    - x

***Endpoint #x - x:***
- **Route:** */x*
- **Purpose:** x
- **HTTP request method:** x
- **Required data:** x
- **Expected response data:**
    - x
    - x
- **Authentication methods:**
    - x

*Endpoint documentation should include:*
- *HTTP request verb*
- *Required data where applicable*
- *Expected response data*
- *Authentication methods where applicable*

___
### ***R6: An ERD for your app***
x

___
### ***R7: Detail any third party services that your app will use***
x

___
### ***R8: Describe your project's models in terms of the relationships they have with each other***
x

___
### ***R9: Discuss the database relations to be implemented in your application***
x

___
### ***R10: Describe the way tasks are allocated and tracked in your project***
For this project, I am utilising a Trello board for the project management and task tracking.

The Trello board can be viewed here: [T2A2 - API Webserver](https://trello.com/b/EcnQEn4x/t2a2-api-webserver)

___
## **Sources**

^[1]^ McCann, A., 13 ATS benefits and what they mean for your business, viewed 11/07/2023, https://resources.workable.com/tutorial/ats-benefits

^[2]^ x

^[3]^ Hoyos, M., What is an ORM and Why You Should Use It, viewed 11/07/2023, https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a
