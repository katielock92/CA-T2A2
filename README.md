# API Web Server Application (_Coder Academy Term 2 Assignment 2_)

### _Prepared by Katie Lock_

---

## **Project Summary and Table of Contents**
For this project, we were given the following introduction/brief:
> *Web servers can come in many shapes and contain different levels of complexity. At their core, they always involve server concepts such as routing, and handling the communication of data between users and a data storage medium. To solidify your knowledge of core web server concepts and show your ability to work with web servers at a fundamental level, you should be able to write code to create a functioning web API server.*

This required selecting an idea for a web application that utilises relational databases, so that we could create the backend of the application and API routes using Python and Flask.
### README Contents
- [Planning and Documentation Requirements:](#planning-and-documentation-requirements)
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
- [Appendix](#appendix)
    - [How to Operate](#how-to-operate)
    - [Sources](#sources)

---

## Planning and Documentation Requirements

### **_R1: Identification of the problem you are trying to solve by building this particular app_**

For my API web server application, I am creating a basic Application Tracking System (known as an ATS for short). An ATS *"streamlines the hiring process by automating and organising each step along the way, making it easier to connect with qualified candidates more efficiently."*^[1]^

Companies of varying sizes commonly utilise an ATS in their recruitment and hiring practices to support a standardised workflow for recruitment. This ensures that all applications are kept in a central location and there is consistency in the data collected and stored for roles, candidates and interviews. Using an ATS also saves hours of administration and manual work, such as copying applications from a job board, or individually emailing rejected candidates.

My API web server application would be the foundation for a simple, low-cost ATS that could provide the key tasks to supporting in hiring, and provide a centralised database of hiring data for richer reporting.

*Question sources:* ^[1]^

---

### **_R2: Why is it a problem that needs solving?_**

A real-life problem that many small businesses face is that a dedicated ATS is often outside of their budget, and therefore they have to rely on a combination of other cheaper SaaS tools to manage their recruitment processes. This is something that I personally faced in my current company - at the start of the pandemic we had no ATS, and therefore after applicants applied for roles on our website, different departments followed different processes for the next steps. The Engineering team utilised a private Trello board per role for short-listed candidates, though this involved needing to have interview notes linked from Google Docs, manually sending calendar invites and communications with candidates, and manually uploading resumes to the Trello board.

Having an ATS, even if a simple one, helps to provide consistency and efficiency in hiring for businesses. The current economic conditions mean that many businesses are not actively hiring, and often only have open roles if staff leave. This makes it more difficult, particularly for start-ups, to justify the cost of having an ATS to their management, despite the enormous time saving and rich centralised data that it can provide.

---

### **_R3: Why have you chosen this database system. What are the drawbacks compared to others?_**

My API application will utilise a PostgreSQL database management system (DBMS), which I have chosen for the benefits and versatility that it provides.  PostgreSQL is known for its *"reliability, flexibility and support of open technical standards"*^[3]^, as well as having support for both relational and non-relational databases.  As this project does not currently have any financial backing, being free and open-source is a significant benefit as an early-career developer.  PostgreSQL is not just suitable because of its free cost though - the flexibility of the system provides me with significant freedom as my project may grow and change in the future.

PostgreSQL has deep language support, so while this project is currently only written in Python, it would allow me to operate in other languages in future if they were better suited to the project.  It also allows the use of non-relational databases, if I were to expand the use of databases for other types of data on my project.

In regards to drawbacks, an easy way to demonstrate these is to compare PostgreSQL to MySQL, as this is the other most common DBMS used in market today. PostgreSQL is more technical when compared to MySQL, and therefore has a stepper learning curve for non-technical or new users.  This could be an issue if my project were to involve more users in future who are non-technical or not experienced with PostgreSQL.

Another key difference between PostgreSQL and MySQL is the performance of read and write operations. MySQL is far more efficient with read operations, whilst PostgreSQL is more efficient with write operations.  Whether this is a drawback for PostgreSQL is situational depending on use case and the frequency of each of these operations.  For my API, there is a similar number of read and write operations, and therefore the other benefits of PostgreSQL outweigh any performance delays with read operations.  However if you had an application that primarily performed read operations, this would be a significant drawback of using PostgreSQL.

*Question sources:* ^[2]^, ^[3]^

---

### **_R4: Identify and discuss the key functionalities and benefits of an ORM_**

Object-Relational-Mapping (ORM) is *"a technique used in creating a "bridge" between object-oriented programs and ...databases."*^[5]^ This allows a programmer to interact with a (usually relational) database by writing queries in the object-oriented programming language of choice, rather than in SQL.

ORM is designed to simplify the process of interacting with databases in an application by utilising a consistent language throughout the application code. ORM tools are how programmers apply ORM in an application, with their ORM tool of choice being imported as a library.  There are a wide variety of ORM tools available for different popular languages, and they tend to have slightly different syntax to create the same result when translated into SQL.

Some of the key functionalities of ORMs are:
- **Abstraction** - ORMs allow the developer to access and manipulate objects in a database without having to know or consider all of the relations in the database. Naturally it does help if the developer also knows the database relations and structure, but it is not a requirement when writing queries, in contrast to raw SQL.
- **No SQL required** - ORMs allow you to perform CRUD (create, read, update, delete) operations in a relational database without needing to know SQL, or the need to write SQL queries.
- **Translation** - ORMs work by translating the code written in the object-oriented language into a SQL query so that the database can understand and perform the query.

Using an ORM when writing an application that interacts with databases can have many benefits. As a programmer, you are likely more component and familiar with a programming language such as JavaScript, Python or Java, rather than SQL. By being able to write your database queries in your primary programming language, you are more efficient and can likely write more complex queries than if you were needing to write these in SQL.

Not only do you save time by writing in your primary language, but using an ORM results in shorter, cleaner code.  ORM queries are typically much shorter to achieve the same result than the equivalent SQL query.

ORMs are abstract in how they translate to SQL, and therefore you can easily switch between using different database systems whilst still having similar query syntax.  This makes it easier for a developer to switch between projects or companies who use different database systems without needing to learn a completely new skillset for database queries.

Another major benefit of using ORMs for businesses is that they provide security benefits, due to the tools preventing malicious attacks via direct SQL.

*Question sources:* ^[4]^, ^[5]^, ^[6]^

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

**_Endpoint #26 - Delete Application:_**

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

My draft ERD, which was used to get my application idea approved, was as follows:
![A draft version of the ERD for this application](./docs/Draft%20ERD.png)

When planning the routes and considering the architecture of the application, I ran into one key issue - I couldn't reference the *id* field in the Users table twice within a different table. This meant that a job couldn't reference both the recruiter and hiring manager, and an interview couldn't reference both the candidate and interviewer.

Ultimately I decided to then split the Users entity into three separate entities:
- Users (simply contains a user_id, email and password, for authenticating a user)
- Staff (for internal users who have higher permission levels)
- Candidates (for external users who are applying for jobs and interviewing with the company)

I also tidied up the ERD to remove some of the Flask-specific conditions from this diagram, solely focusing on keeping it based around the entities, their relations and the basic data type.

The final ERD for my application, and what this documentation is based on, is as follows:
![Final ERD for ATS application](./docs/API%20Project%20ERD.png)

---

### **_R7: Detail any third party services that your app will use_**

My application is written in Python, which allows you to implement many third party services through the use of libraries. These imported libraries provide significant functionality to my Python application, from defining the framework to allowing database interaction and authentication.

The primary third party Python libraries used in my application, and their functionality, are as follows:
- **Flask** - Flask is the Python framework that is implemented in this application, and is used for building web applications. Flask manages the low-level details of an application for the user to make it simple to start building a web application - which is perfect for a new developer such as myself.
- **SQLAlchemy** - SQLAlchemy is the ORM tool used to translate the Python Flask queries in my application into SQL for interacting with the PostgreSQL database, and performing CRUD operations.
- **Marshmallow** - Marshmallow is a tool that converts complex data types from an ORM into a format that be rendered in Python. In my application, it is used to create a schema for each model, so that queries can be serialised and returned to the user in a JSON format.
- **JWT Extended** - This allows users to be authenticated through the use of a Javascript Web Token (JWT). In my application this is used in conjunction with the Users table in the database and a set of register/login features, so that a token is returned when a user logs in and this token is associated with that particular user's session.
- **Bcrypt** - Bcrypt is an encryption tool that uses a hashing algorithm when storing sensitive fields in the database. In my application this is used to encrypt user passwords, so that these are stored in a hashed format, and can not be accessed at ease.
- **pythondotenv** - This library allows us to set the environment variables within system files called *.env* and *.flaskenv* so that these do not need to be entered into the terminal query every time we are running our Flask application. There are key-value pairs for specific variables, such as the port, application name, database URI and secret key.
- **Psycopg** - This is a PostgreSQL database adaptor for Python, which enables us to access our PostgreSQL database from our Python application. The difference between this and an ORM such as SQLAlchemy is that Psycopg is used to *connect* to the database, whilst an ORM is used to perform operations within the database once we are connected.

---

### **_R8: Describe your project's models in terms of the relationships they have with each other_**

All of the models in my project's database have at least one relationship with another model, some even having multiple relationships. The next section discusses these database relations from an ERD perspective, however when implementing these relations in Flask code, we need to do this within models.

The models within my application have the following relationships with each other:

**Users model:**
- The Users model has no parent relations, and is the first model a user should interact with unless using existing database records.
- There is a *child* relationship with the Staff model with the following parameters:
    - *user_id* is a foreign key in the Staff model, linked with the *id* field in the Users model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is a "cascade delete" condition on the Users side of the relationship, which means that if a user record is deleted, any related entries in the Staff table are also deleted.
- There is a *child* relationship with the Candidates model with the following parameters:
    - *user_id* is a foreign key in the Candidates model, linked with the *id* field in the Users model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is a "cascade delete" condition on the Users side of the relationship, which means that if a user record is deleted, any related entries in the Candidates table are also deleted.

**Staff model:**
- There is a *parent* relationship with the Users model with the following parameters:
    - *user_id* is a foreign key in the Staff model, linked with the *id* field in the Users model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *user_id* field is set as "nullable=False" in the Staff model, which means that a staff record must contain a user_id.
    - The *user_id* field is set as "unique=True" in the Staff model, which means that this field must contain a unique entry for each record in the Staff table.
- There is a *child* relationship with the Job model with the following parameters:
    - *hiring_manager_id* is a foreign key in the Jobs model, linked with the *id* field in the Staff model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is no "cascade delete" condition on this relationship, meaning that either side can be deleted without the other. This is because a job does not cease to exist if a hiring manager leaves, you would update it prior to deleting the Staff record.
- There is a *child* relationship with the Interview model with the following parameters:
    - *interviewer_id* is a foreign key in the Interviews model, linked with the *id* field in the Staff model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is no "cascade delete" condition on this relationship, meaning that either side can be deleted without the other. This is because an interview does not cease to exist if an interviewer leaves, you would update it prior to deleting the Staff record.

**Candidates model:**
- There is a *parent* relationship with the Users model with the following parameters:
    - *user_id* is a foreign key in the Candidates model, linked with the *id* field in the Users model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *user_id* field is set as "nullable=False" in the Candidates model, which means that a staff record must contain a user_id.
    - The *user_id* field is set as "unique=True" in the Candidates model, which means that this field must contain a unique entry for each record in the Candidates table.
- There is a *child* relationship with the Applications model with the following parameters:
    - *candidate_id* is a foreign key in the Applications model, linked with the *id* field in the Candidates model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is a "cascade delete" condition on the Candidates side of the relationship, which means that if a candidate record is deleted, any related entries in the Applications table are also deleted.
- There is a *child* relationship with the Interviews model with the following parameters:
    - *candidate_id* is a foreign key in the Interviews model, linked with the *id* field in the Candidates model, and sourced via the application_id foreign key field to prevent invalid entries.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is a "cascade delete" condition on the Candidates side of the relationship, which means that if a candidate record is deleted, any related entries in the Interviews table are also deleted.

**Jobs model:**
- There is a *parent* relationship with the Staff model with the following parameters:
    - *hiring_manager_id* is a foreign key in the Jobs model, linked with the *id* field in the Staff model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *user_id* field is set as "nullable=False" in the Jobs model, which means that a job record must contain a hiring_manager_id.
- There is a *child* relationship with the Applications model with the following parameters:
    - *job_id* is a foreign key in the Applications model, linked with the *id* field in the Jobs model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is a "cascade delete" condition on the Jobs side of the relationship, which means that if a job record is deleted, any related entries in the Applications table are also deleted.

**Applications model:**
- There is a *parent* relationship with the Jobs model with the following parameters:
    - *job_id* is a foreign key in the Applications model, linked with the *id* field in the Job model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *job_id* field is set as "nullable=False" in the Applications model, which means that an application record must contain a job_id.
- There is a *parent* relationship with the Candidates model with the following parameters:
    - *candidate_id* is a foreign key in the Applications model, linked with the *id* field in the Candidates model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *candidate_id* field is set as "nullable=False" in the Applications model, which means that an application record must contain a candidate_id.
- There is a *child* relationship with the Interview model with the following parameters:
    - *application_id* is a foreign key in the Interviews model, linked with the *id* field in the Applications model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is a "cascade delete" condition on the Applications side of the relationship, which means that if an application record is deleted, any related entries in the Interviews table are also deleted.

**Interviews model:**
- There is a *parent* relationship with the Staff model with the following parameters:
    - *interviewer_id* is a foreign key in the Interviews model, linked with the *id* field in the Staff model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *interviewer_id* field is set as "nullable=False" in the Interviews model, which means that an interview record must contain an interviewer_id.
- There is a *parent* relationship with the Applications model with the following parameters:
    - *application_id* is a foreign key in the Interviews model, linked with the *id* field in the Applications model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *application_id* field is set as "nullable=False" in the Interviews model, which means that an interview record must contain an application_id.
- There is a *parent* relationship with the Candidates model with the following parameters:
    - *candidate_id* is a foreign key in the Interviews model, linked with the *id* field in the Candidates model, and sourced through the application_id.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *candidate_id* field is set as "nullable=False" in the Interviews model, which means that an application record must contain a candidate_id.
- There is a *child* relationship with the Scorecards model with the following parameters:
    - *interview_id* is a foreign key in the Scorecards model, linked with the *id* field in the Interviews model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - There is a "cascade delete" condition on the Interviews side of the relationship, which means that if an interview record is deleted, any related entries in the Scorecards table are also deleted.

**Scorecards model:**
- There is a *parent* relationship with the Interviews model with the following parameters:
    - *interview_id* is a foreign key in the Scorecards model, linked with the *id* field in the Interviews model.
    - This relationship uses the "back_populates" condition, which means that a change in data one side of the relationship will updated the other.
    - The *interview_id* field is set as "nullable=False" in the Scorecards model, which means that a scorecard record must contain an interview_id.
- The Scorecards model has no child relationships.

---

### **_R9: Discuss the database relations to be implemented in your application_**

From our ERD, you can see there are planned relations between each of the entities within our database that will need to be implemented when developing the application.  These relations are documented through the arrows connecting the row from one table to another, with the symbols on each arrow indicating the nature of the relationship.  FK is used to indicate when a field in a table is a foreign key from another database table, sourced through the relation.

The **Users** table has 2 relations:
- **Staff:** One-to-one relationship between the *id* field in the Users table and *user_id* field in the Staff table. One user can only be referenced once in the Staff table and a staff member must be a user, but a user doesn't need to be a staff member.
- **Candidates:** One-to-one relationship between the *id* field in the Users table and *user_id* field in the Candidates table. One user can only be referenced once in the Candidates table and a candidate must be a user, but a user doesn't need to be a candidate.

The **Staff** table has 3 relations:
- **Users:** One-to-one relationship between the *id* field in the Users table and *user_id* field in the Staff table. user_id is a foreign key. One user can only be referenced once in the Staff table and a staff member must be a user, but a user doesn't need to be a staff member.
- **Jobs:** One-to-many relationship between the *id* field in the Staff table and *hiring_manager_id* field in the Jobs table. A job requires a staff member as the hiring manager, but a staff member can be the hiring manager on zero, one or multiple jobs.
- **Interviews:** One-to-many relationship between the *id* field in the Staff table and *interviewer_id* field in the Interviews table. An interview requires a staff member as an interviewer, but a staff member can be the interviewer on zero, one or multiple jobs.

The **Candidates** table has 3 relations:
- **Users:** One-to-one relationship between the *id* field in the Users table and *user_id* field in the Candidates table. user_id is a foreign key. One user can only be referenced once in the Candidates table and a candidate must be a user, but a user doesn't need to be a candidate.
- **Applications:** One-to-many relationship between the *id* field in the Candidates table and *candidate_id* field in the Applications table. A candidate can apply for zero, one or multiple jobs, but all applications require a candidate.
- **Interviews:** One-to-many relationship between the *id* field in the Candidates table and *candidate_id* field in the Interviews table, which is sourced via the *application_id*. A candidate can have zero, one or multiple interviews, but all interviews require a candidate.

The **Jobs** table has 2 relations:
- **Staff**: One-to-many relationship between the *id* field in the Staff table and *hiring_manager_id* field in the Jobs table. hiring_manager_id is a foreign key. A job requires a staff member as the hiring manager, but a staff member can be the hiring manager on zero, one or multiple jobs.
- **Applications:** One-to-many relationship with the *id* field in the Jobs table and *job_id* in the Applications table. A job can have zero, one or multiple applications, but all applications require a job.

The **Applications** table has 3 relations:
- **Candidates:** One-to-many relationship between the *id* field in the Candidates table and *candidate_id* field in the Applications table. candidate_id is a foreign key. A candidate can apply for zero, one or multiple jobs, but all applications require a candidate.
- **Job:** One-to-many relationship with the *id* field in the Jobs table and *job_id* in the Applications table. job_id is a foreign key. A job can have zero, one or multiple applications, but all applications require a job.
- **Interviews:** One-to-many relationships between the *id* field in the Applications table and the *application_id* field in the Interviews table. An application can have zero, one or multiple interviews, but all interviews require an application.

The **Interviews** table has 4 relations:
- **Staff:** One-to-many relationship between the *id* field in the Staff table and *interviewer_id* field in the Interviews table. interviewer_id is a foreign key. An interview requires a staff member as an interviewer, but a staff member can be the interviewer on zero, one or multiple jobs.
- **Candidates:** One-to-many relationship between the *id* field in the Candidates table and *candidate_id* field in the Interviews table, which is sourced via the *application_id*. candidate_id is a foreign key. A candidate can have zero, one or multiple interviews, but all interviews require a candidate.
- **Applications:** One-to-many relationships between the *id* field in the Applications table and the *application_id* field in the Interviews table. application_id is a foreign key. An application can have zero, one or multiple interviews, but all interviews require an application.
- **Scorecards:** One-to-one relationships between the *id* field in the Interviews table and the *interview_id* field in the Scorecards table. One interview can only be referenced once in the Scorecards table and a scorecard must be linked to an interview, but an interview isn't require to have a scorecard.

The **Scorecards** table has 1 relation:
- **Interviews:** One-to-one relationships between the *id* field in the Interviews table and the *interview_id* field in the Scorecards table. interview_id is a foreign key. One interview can only be referenced once in the Scorecards table and a scorecard must be linked to an interview, but an interview isn't require to have a scorecard.


---

### **_R10: Describe the way tasks are allocated and tracked in your project_**

For this project, I am utilising a Trello board for the project management and task tracking.

The Trello board can be viewed here: [T2A2 - API Webserver](https://trello.com/b/EcnQEn4x/t2a2-api-webserver)

I created 5 Lists within this board, for different statuses:
- To-Do: Planning
- To-Do: Development
- In Progress
- Blocked
- Done

I then created a card for a high-level task, and a checklist within to go into more detail. Examples of the cards are:
- A card for each stage in the project conception, approval and setup
- A card for each question in the Documentation requirements
- A card for creating each key configuration/setup files for the Flask application
- A card for each of:
    - Models
    - Schemas
    - Controllers
    - CLI commands

Once the task described in the card was commenced, it was moved from the To-Do list to the In Progress list. The coding features of the application had far more activity, which included regularly adding items to the checklist, ticking and unticking these as I created functions or refactors were required, and using the Comments section to summarise my progress.

As I am the only person working on this application, I did not assign any of the cards or checklist items to myself. In addition I did not set due dates on tasks, as I knew the process would be quite fluid and often resulted in working on multiple different cards at once.

In a real world scenario, this would look different due to having multiple people working on a project, and projects being broken into tickets within a sprint. Even if due dates or user assignments were not utilised on my Trello board, it was still beneficial to track and document my progress on my application - particularly if I was coming back to code on a new day and needed to refresh my mind on my progress.

---
## Appendix

### **How to Operate**
In order to operate this webserver application, you will require the following:
- A modern computer (no specific OS requirements) with an internet connection
- An API Platform tool (such as Postman or Insomnia)
- A IDE software of your choice (such as VSCode)

The steps to operate are as follows:
1. All files in the *.src* folder should be downloaded to your local machine.
2. If you have downloaded this application from GitHub:
    - Open the Terminal application on your local machine.
    - Install PostgreSQL, if this is not already installed.
    - Run PostgreSQL, and create a new database user (name and password of your choice), along with a new database called *ats_db*.
    - Copy the *.envsample* file to a new file named *.env*.
    - In this new file, set your own secret key, and set the database URL using the psycopg2 format, with the ats_db database and the new database username and password on your machine's psql.
3. Check that the ports specified in .env and .flaskenv are available on your local machine, and change if required.
4. Open the .src folder in the Terminal (either on your IDE or the Terminal application).
5. Enter the following commands into your terminal:
    - To launch the virtual environment for the application: ``python3 -m venv .venv && source .venv/bin/activate``
    - To install all required libraries into this virtual environment: ``pip3 install -r requirements.txt``
    - To create the database tables on your machine: ``flask db create``
    - To seed the CLI commands into your local psql: ``flask db seed``
    - To run the application: ``flask run``
6. If the above steps are successful, the Flask application will now be running on the port specified in the *.flaskenv* file.
7. Open your API Platform and create a GET request for the following route: *http://127.0.0.1:8080/jobs* (modify if the port changed, or if your local machine uses localhost instead of an IP address)
8. If this route successfully returns the list of jobs for non-Staff users, the app is working for you! You can now begin navigating through the remaining routes once you register as a user, or if you use one of the existing logins in the CLI commands.

If any help is required when operating the application, please contact the application author for further assistance.
___
### **Sources**

^[1]^ McCann, A., 13 ATS benefits and what they mean for your business, viewed 11/07/2023, https://resources.workable.com/tutorial/ats-benefits

^[2]^ Amazon Web Services, What's The Difference Between MySQL And PostgreSQL?
, viewed 26/07/2023, https://aws.amazon.com/compare/the-difference-between-mysql-vs-postgresql/

^[3]^ IBM, PostgreSQL vs. MySQL: What’s the Difference?, viewed 26/07/2023, https://www.ibm.com/cloud/blog/postgresql-vs-mysql-whats-the-difference

^[4]^ Hoyos, M., What is an ORM and Why You Should Use It, viewed 11/07/2023 and 26/07/2023, https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a

^[5]^ Ihechikara, V.A., What is an ORM – The Meaning of Object Relational Mapping Database Tools, viewed 26/07/2023, https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/

^[6]^ Awati, R., object-relational mapping (ORM), viewed 26/07/2023, https://www.theserverside.com/definition/object-relational-mapping-ORM