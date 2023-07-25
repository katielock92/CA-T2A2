# API Web Server Application (_Coder Academy Term 2 Assignment 2_)

### _Prepared by Katie Lock_

---

## **Project Summary and Table of Contents**
xx
### Contents

1. [Identification of problem](#r1-identification-of-the-problem-you-are-trying-to-solve-by-building-this-particular-app)
2. [Why this problem needs solving](#r2-why-is-it-a-problem-that-needs-solving)
3. [Choice of database system](#r3-why-have-you-chosen-this-database-system-what-are-the-drawbacks-compared-to-others)
4. [Key functionalities and benefits of an ORM](#r4-identify-and-discuss-the-key-functionalities-and-benefits-of-an-orm)
5. [Endpoint Documentation](#r5-document-all-endpoints-for-your-api)
6. [Entity Relational Diagram (ERD)](#r6-an-erd-for-your-app)
7. [Third party services](#r7-detail-any-third-party-services-that-your-app-will-use)
8. [Models and relations](#r8-describe-your-projects-models-in-terms-of-the-relationships-they-have-with-each-other)
9. [Database relations](#r9-discuss-the-database-relations-to-be-implemented-in-your-application)
10. [Project management](#r10-describe-the-way-tasks-are-allocated-and-tracked-in-your-project)

---

## Planning and Documentation Requirements

### **_R1: Identification of the problem you are trying to solve by building this particular app_**

For my API web server application, I am creating a basic Application Tracking System (known as an ATS for short). An ATS "streamlines the hiring process by automating and organising each step along the way, making it easier to connect with qualified candidates more efficiently."^[1]^

Companies of varying sizes commonly utilise an ATS in their recruitment and hiring practices to support a standardised workflow for recruitment. This ensures that all applications are kept in a central location and there is consistency in the data collected and stored for roles, candidates and interviews. Using an ATS also saves hours of administration and manual work, such as copying applications from a job board, or individually emailing rejected candidates.

My API web server application would be the foundation for a simple, low-cost ATS that could provide the key tasks to supporting in hiring, and provide a centralised database of hiring data for richer reporting.

---

### **_R2: Why is it a problem that needs solving?_**

A real-life problem that many small businesses face is that a dedicated ATS is often outside of their budget, and therefore they have to rely on a combination of other cheaper SaaS tools to manage their recruitment processes. This is something that I personally faced in my current company - at the start of the pandemic we had no ATS, and therefore after applicants applied for roles on our website, different departments followed different processes for the next steps. The Engineering team utilised a private Trello board per role for short-listed candidates, though this involved needing to have interview notes linked from Google Docs, manually sending calendar invites and communications with candidates, and manually uploading resumes to the Trello board.

Having an ATS, even if a simple one, helps to provide consistency and efficiency in hiring for businesses. The current economic conditions mean that many businesses are not actively hiring, and often only have open roles if staff leave. This makes it more difficult, particularly for start-ups, to justify the cost of having an ATS to their management, despite the enormous time saving and rich centralised data that it can provide.

---

### **_R3: Why have you chosen this database system. What are the drawbacks compared to others?_**

My API application will utilise a PostgreSQL database system.

---

### **_R4: Identify and discuss the key functionalities and benefits of an ORM_**

x

^[3]^

---

### **_R5: Document all endpoints for your API_**

The API has a total of **35** endpoints, documented below in detail. Each database table/model has at least one route for each component of CRUD - Create, Read, Update, Delete.

There are 2 primary types of authentication (beyond simply requiring a JWT) that are utilised in routes through a wrapper function, which will be summarised here and then referenced when discussing each route:

**_authorise_as_admin:_**

- A valid JWT token is required for this request
- The user's identity is checked using the token, and then the Staff table is searched for the user_id value that matches
- If there is no match in the Staff table, an error is returned as the user is not validated
- If there is a match in the Staff table, the admin field is checked for the user's row - the user is only authenticated if this field is True

**_authorise_as_staff:_**

- A valid JWT token is required for this request
- The user's identity is checked using the token, and then the Staff table is searched for the user_id value that matches
- If there is no match in the Staff table, an error is returned as the user is not validated
- If there is a match in the Staff table, the user is validated

### Endpoint Documentation

**_Endpoint #1 - Register:_**

- **Route:** _/auth/register_
- **Purpose:** Allows new users to register for the app
- **HTTP request method:** POST
- **Required data:**
  - User to supply "email" and "password" in string format
  - Email must be unique and meet regex conditions
  - Password must be at least 8 characters in length
- **Expected response data:**
  - _If successful:_ The "email" and "user_id" fields are returned to the user in JSON format
  - If either field is missing, an IntegrityError triggers an error message to be returned to the user
  - If email address is not unique, an IntegrityError triggers an error message to be returned to the user
  - If the email address or password do not meet the validation conditions, a ValidationError triggers an error message to be returned to the user
- **Authentication methods:** None

**_Endpoint #2 - Login:_**

- **Route:** _/auth/login_
- **Purpose:** Allows existing users to login to the app and perform authenticated tasks
- **HTTP request method:** POST
- **Required data:**
  - User to supply "email" and "password" in string format, that match an existing record in the Users table
- **Expected response data:**
  - _If successful:_ the "email" field and a JWT access token are returned to the user in JSON format
  - If the email address does not exist in the users table, or an incorrect password for this email was supplied, an error message is returned to the user
- **Authentication methods:** None

**_Endpoint #3 - View Users:_**

- **Route:** _/users_
- **Purpose:** Allows admin users to view the list of all users
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ a list is returned in JSON format of all records in the Users table, excluding the password field
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #4 - Update User:_**

- **Route:** _/users_
- **Purpose:** Allows a user to update their own email and password that is used to login
- **HTTP request method:** PUT, PATCH
- **Required data:** "email" and/or "password" (in string format)
- **Expected response data:**
  - _If successful:_ The "email" and "user_id" for the updated user record will be returned in JSON format, password is not displayed even if this is updated
  - An error is returned if no JWT is supplied
- **Authentication methods:**:
  - get_jwt_identity is used to the confirm the user_id of the logged in user

**_Endpoint #5 - Delete User:_**

- **Route:** _/users/<user_id>_
- **Purpose:** Allows an admin to delete a user
- **HTTP request method:** DELETE
- **Required data:** user_id to be entered into the route
- **Expected response data:**
  - _If successful:_ A message is returned confirming that the user has been deleted
  - If the user_id supplied does not match an entry in the Users table, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #6 - View Candidates:_**

- **Route:** _/candidates_
- **Purpose:** Allows admin users to view the list of all candidates
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ a list is returned in JSON format of all records in the Candidates table
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #7 - Create Candidate:_**

- **Route:** _/candidates_
- **Purpose:** Allows a user to create a link record for themselves in the Candidates table
- **HTTP request method:** POST
- **Required data:** "name" and "phone_number" in string format
- **Expected response data:**
  - _If successful:_ The "name", "phone_number" and "candidate_id" fields for the new record are returned to the user in JSON format
  - An IntegrityError is triggered and an error message is returned if there is already a candidate record for that user, or if a field is missing
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if no JWT is supplied
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user

**_Endpoint #8 - Update Candidate:_**

- **Route:** _/candidates_
- **Purpose:** Allows an existing candidate user to update their name and/or phone number
- **HTTP request method:** PUT, PATCH
- **Required data:** "name" and/or "phone_number" in string format
- **Expected response data:**
  - _If successful:_ The "name", "phone_number" and "candidate_id" fields for the updated record are returned to the user in JSON format
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if there is no existing candidate record for the logged in user
  - An error is returned if no JWT is supplied
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user

**_Endpoint #9 - Delete Candidate:_**

- **Route:** _/candidates/<candidate_id>_
- **Purpose:** Allows an admin to delete a candidate from the Candidates table
- **HTTP request method:** DELETE
- **Required data:** candidate_id to be entered into the route
- **Expected response data:**
  - _If successful:_ A message is returned confirming that the candidate has been deleted
  - If the candidate_id supplied does not match an entry in the Candidates table, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #10 - View Staff:_**

- **Route:** _/staff_
- **Purpose:** Allows admin users to view the list of all staff
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ a list is returned in JSON format of all records in the Staff table
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #11 - Create Staff:_**

- **Route:** _/staff_
- **Purpose:** Allows an admin to add a registered user to the Staff table, enabling them to access staff-only and admin-only routes (if applicable)
- **HTTP request method:** POST
- **Required data:** "name" and "title" in string format, "user_id" in integer format
- **Expected response data:**
  - _If successful:_ The schema fields for the new staff record are returned to the user in JSON format
  - An IntegrityError is triggered and an error message returned if there is already a staff record for the supplied user_id, or if a required field has not been provided
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if the user_id provided does not match any records in the Users table
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #12 - Update Staff (Own Record):_**

- **Route:** _/staff_
- **Purpose:** Allows a staff user to update the "name" and "title" fields on their own record
- **HTTP request method:** PUT, PATCH
- **Required data:** "name" and/or "title" in string format
- **Expected response data:**
  - _If successful:_ The schema fields for the updated staff record are returned to the user in JSON format
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if there is no existing staff record for the logged in user
  - An error is returned if no JWT is supplied
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user

**_Endpoint #13 - Update Staff (Admin Access):_**

- **Route:** _/staff/<staff_id>_
- **Purpose:** Allows an admin user to update the admin field on an existing staff record
- **HTTP request method:** PUT, PATCH
- **Required data:** staff_id to be entered into the route
- **Expected response data:**
  - _If successful:_ The schema fields for the updated staff record are returned to the user in JSON format
  - If the staff_id supplied does not match an entry in the Staff table, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #14 - Delete Staff:_**

- **Route:** _/staff/<staff_id>_
- **Purpose:** Allows an admin to delete a staff record from the Staff table
- **HTTP request method:** DELETE
- **Required data:** staff_id to be entered into the route
- **Expected response data:**
  - _If successful:_ A message is returned confirming that the staff record has been deleted
  - If the staff_id supplied does not match an entry in the Staff table, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #15 - View Open Jobs:_**

- **Route:** _/jobs_
- **Purpose:** Returns a list of all jobs with a status of open, with some fields not displayed unless a user is authenticated
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ a list is returned in JSON format of all records in the Jobs table with a status of "Open"
  - Non-staff users will not see "hiring manager" and "salary_budget" fields
  - Non-admin users will not see "salary_budget" field
- **Authentication methods:**
  - Optional: get_jwt_identity() is used to get the user_id of the logged in user to check if a more detailed schema can be returned, but a JWT is not required for the route to work

**_Endpoint #16 - View All Jobs:_**

- **Route:** _/jobs/all_
- **Purpose:** Returns a list of all jobs (regardless of status), with some fields not displayed unless a user is authenticated
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ a list is returned in JSON format of all records in the Jobs table
  - Non-staff users will not see "hiring manager" and "salary_budget" fields
  - Non-admin users will not see "salary_budget" field
- **Authentication methods:**
  - Optional: get_jwt_identity() is used to get the user_id of the logged in user to check if a more detailed schema can be returned, but a JWT is not required for the route to work

**_Endpoint #17 - View One Job:_**

- **Route:** _/jobs/<job_id>_
- **Purpose:** Returns the job record with the matching job_id, with some fields not displayed unless a user is authenticated
- **HTTP request method:** GET
- **Required data:** job_id to be entered into the route
- **Expected response data:**
  - _If successful:_ the matching record from the Jobs table is returned in JSON format
  - Non-staff users will not see "hiring manager" and "salary_budget" fields
  - Non-admin users will not see "salary_budget" field
  - If the job_id supplied does not match an entry in the Jobs table, an error message is returned
- **Authentication methods:**
  - Optional: get_jwt_identity() is used to get the user_id of the logged in user to check if a more detailed schema can be returned, but a JWT is not required for the route to work

**_Endpoint #18 - View Applications for a Job:_**

- **Route:** _/jobs/<job_id>/applications_
- **Purpose:** Allows a staff user to see the applications for a particular job
- **HTTP request method:** GET
- **Required data:** job_id to be entered into the route
- **Expected response data:**
  - _If successful:_ the matching records from the Applications table are returned in JSON format
  - If the job_id supplied does not match an entry in the Jobs table, an error message is returned
  - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
  - authorise_as_staff

**_Endpoint #19 - Create Job:_**

- **Route:** _/jobs_
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
  - _If successful:_ The schema fields for the new job record are returned to the user in JSON format
  - An IntegrityError is triggered and an error message returned if a required field has not been provided
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if the "hiring_manager_id" provided does not match any records in the Staff table
  - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
  - authorise_as_staff

**_Endpoint #20 - Update Job:_**

- **Route:** _/jobs/<job_id>_
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
  - _If successful:_ The schema fields for the updated job record are returned to the user in JSON format
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if the new "hiring_manager_id" provided does not match any records in the Staff table
  - An error is returned if the job_id in the route does not match any records in the Jobs table
  - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
  - authorise_as_staff

**_Endpoint #21 - Delete Job:_**

- **Route:** _/jobs/<job_id>_
- **Purpose:** Allows an admin to delete a job record from the Jobs table
- **HTTP request method:** DELETE
- **Required data:** job_id to be entered into the route
- **Expected response data:**
  - _If successful:_ A message is returned confirming that the job record has been deleted
  - If the job_id supplied does not match an entry in the Jobs table, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #22 - View All Applications:_**

- **Route:** _/applications_
- **Purpose:** Allows an admin to see all applications across all jobs
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ all records from the Applications table are returned in JSON format
  - An error is returned any user who is not authenticated as an admin user
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #23 - View One Application:_**

- **Route:** _/applications/<application_id>_
- **Purpose:** Returns the application record with the matching application_id to a staff user
- **HTTP request method:** GET
- **Required data:** application_id to be entered into the route
- **Expected response data:**
  - _If successful:_ the matching record from the Applications table is returned in JSON format
  - If the application_id supplied does not match an entry in the Applications table, an error message is returned
  - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
  - authorise_as_staff

**_Endpoint #24 - Create Application:_**

- **Route:** _/applications_
- **Purpose:** Allows a candidate user to create an application for a particular job
- **HTTP request method:** POST
- **Required data:**
  - "job_id" in integer format
  - "location" in string format
  - "notice_period" in string format
  - "working_rights" in string format
  - "resume" in string format
  - "salary_expectations" in integer format
- **Expected response data:**
  - _If successful:_ The schema fields for the new application record are returned to the user in JSON format
  - An IntegrityError is triggered and an error message returned if a required field has not been provided
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if the "job_id" provided does not match any records in the Jobs table
  - An error is returned if the user's user_id is not in the Candidates table
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user

**_Endpoint #25 - Update Application:_**

- **Route:** _/applications/<application_id>_
- **Purpose:** Allows an admin user to update the status field on an application
- **HTTP request method:** PUT, PATCH
- **Required data:**
  - application_id to be entered into the route
  - "status" in string format
- **Expected response data:**
  - _If successful:_ The schema fields for the updated application record are returned to the user in JSON format
  - A ValidationError is triggered and an error message returned to the user if the status does not match one of the accepted values
  - An error is returned if the "application_id" provided does not match any records in the Applications table
  - An error is returned any user who is not authenticated as an admin user
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #x26 - Delete Application:_**

- **Route:** _/applications/<application_id>_
- **Purpose:** Allows an admin to delete an application record from the Applications table
- **HTTP request method:** DELETE
- **Required data:** application_id to be entered into the route
- **Expected response data:**
  - _If successful:_ A message is returned confirming that the application record has been deleted
  - If the application_id supplied does not match an entry in the Applications table, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #27 - View All Interviews:_**

- **Route:** _/interviews/all_
- **Purpose:** Allows an admin to view all interviews across all jobs/interviewers
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ all records from the Interviews table are returned in JSON format
  - An error is returned any user who is not authenticated as an admin user
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #28 - View My Interviews:_**

- **Route:** _/interviews_
- **Purpose:** Allows a user to view all interviews that include them, either as a candidate or as an interviewer
- **HTTP request method:** GET
- **Required data:** None
- **Expected response data:**
  - _If successful:_ the matching records from the Interviews table are returned in JSON format, or a message is displayed if there are no matching records
  - An error is returned if no JWT is supplied
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user

**_Endpoint #29 - Create Interview:_**

- **Route:** _/interviews_
- **Purpose:** Allows a staff user to create an interview for an application
- **HTTP request method:** POST
- **Required data:**
    - "application_id" in integer format
    - "interviewer_id" in integer format
    - "interview_datetime" in datetime format
    - "format" in string format
    - "length_mins" in integer format
- **Expected response data:**
  - _If successful:_ The schema fields for the new interview record are returned to the user in JSON format
  - An IntegrityError is triggered and an error message returned if a required field has not been provided
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if the "application_id" provided does not match any records in the Applications table, or if the "interviewer_id" provided does not match any records in the Staff table
  - An error is returned any user who is not authenticated as a staff user
- **Authentication methods:**
  - authorise_as_staff

**_Endpoint #30 - Update Interview:_**

- **Route:** _/interviews/<interview_id>_
- **Purpose:** Allows an admin user to update the details of an existing interview record
- **HTTP request method:** PUT, PATCH
- **Required data:**
    - interview_id to be entered into the route
    - Plus at least one of the following:
        - "interviewer_id" in integer format
        - "interview_datetime" in datetime format
        - "format" in string format
        - "length_mins" in integer format
- **Expected response data:**
  - _If successful:_ The schema fields for the updated interview record are returned to the user in JSON format
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - An error is returned if the new "interviewer_id" provided does not match any records in the Staff table
  - An error is returned if the interview_id in the route does not match any records in the Interviews table
  - An error is returned any user who is not authenticated as an admin user
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #31 - Delete Interview:_**

- **Route:** _/interviews/<interview_id>_
- **Purpose:** Allows an admin to delete an interview record from the Interviews table
- **HTTP request method:** DELETE
- **Required data:** interview_id to be entered into the route
- **Expected response data:**
  - _If successful:_ A message is returned confirming that the interview record has been deleted
  - If the interview_id supplied does not match an entry in the Interviews table, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

**_Endpoint #32 - View Scorecard:_**

- **Route:** _/interviews/<interview_id>/scorecard_
- **Purpose:** Allows an admin or the interview to view an existing scorecard record from an interview
- **HTTP request method:** GET
- **Required data:** interview_id to be entered into the route
- **Expected response data:**
  - _If successful:_ the matching record from the Scorecards table is returned in JSON format
  - If the interview_id supplied does not match an entry in the Interviews table, an error message is returned
  - An error is returned if there is no scorecard that matches the interview_id supplied
  - An error is returned if the user is not authorised to view the scorecard - they will need to be in the Staff table, and either have the admin permission, or their staff_id match the interviewer_id
  - An error is returned if no JWT is supplied
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user and validate their access

**_Endpoint #33 - Create Interview:_**

- **Route:** _/interviews/<interview_id>/scorecards_
- **Purpose:** Allows the interviewer to create a scorecard for an interview
- **HTTP request method:** POST
- **Required data:**
    - interview_id to be entered into the route
    - "notes" to be entered in text format
    - "rating" to be entered in string format
- **Expected response data:**
  - _If successful:_ The schema fields for the new scorecard record are returned to the user in JSON format
  - An IntegrityError is triggered and an error message returned if a required field has not been provided, or if there is already a scorecard record for this interview_id
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - If the interview_id supplied does not match an entry in the Interviews table, an error message is returned
  - An error is returned if the user is not authorised to create the scorecard - the user will need to exist in the Staff table and their staff_id will need to match the interviewer_id on the interview record referenced
  - An error is returned if no JWT is supplied
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user and validate their access

**_Endpoint #34 - Update Scorecard:_**

- **Route:** _/interviews/<interview_id>/scorecards_
- **Purpose:** Allows an interviewer to update an existing scorecard record
- **HTTP request method:** PUT, PATCH
- **Required data:**
    - interview_id to be entered into the route
    - One (or both) of:
        - "notes" to be entered in text format
        - "rating" to be entered in string format
- **Expected response data:**
  - _If successful:_ The schema fields for the updated scorecard record are returned to the user in JSON format
  - A ValidationError is triggered and an error message returned if a field does not meet the validation requirements (such as regex or length)
  - If the interview_id supplied does not match an entry in the Interviews table, an error message is returned
  - An error is returned if the user is not authorised to update the scorecard - the user will need to exist in the Staff table and their staff_id will need to match the interviewer_id on the interview record referenced
  - An error is returned if no JWT is supplied
- **Authentication methods:**
  - get_jwt_identity is used to the confirm the user_id of the logged in user and validate their access

**_Endpoint #35 - Delete Scorecard:_**

- **Route:** _/interviews/<interview_id>/scorecards_
- **Purpose:** Allows an admin to delete a scorecard record from the Scorecards table
- **HTTP request method:** DELETE
- **Required data:** interview_id to be entered into the route
- **Expected response data:**
  - _If successful:_ A message is returned confirming that the scorecard record has been deleted
  - If the interview_id supplied does not match an entry in the Interviews table, an error message is returned
  - If there is no scorecard record for the interview_id provided, an error message is returned
  - An error is returned any user who is not authenticated as an admin
- **Authentication methods:**
  - authorise_as_admin

---

### **_R6: An ERD for your app_**

x

---

### **_R7: Detail any third party services that your app will use_**

x

---

### **_R8: Describe your project's models in terms of the relationships they have with each other_**

x

---

### **_R9: Discuss the database relations to be implemented in your application_**

x

---

### **_R10: Describe the way tasks are allocated and tracked in your project_**

For this project, I am utilising a Trello board for the project management and task tracking.

The Trello board can be viewed here: [T2A2 - API Webserver](https://trello.com/b/EcnQEn4x/t2a2-api-webserver)

---

## **Sources**

^[1]^ McCann, A., 13 ATS benefits and what they mean for your business, viewed 11/07/2023, https://resources.workable.com/tutorial/ats-benefits

^[2]^ x

^[3]^ Hoyos, M., What is an ORM and Why You Should Use It, viewed 11/07/2023, https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a
