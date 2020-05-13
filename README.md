# rolesGenerator
Python application which is able to interact with a mysql database in order to add data about students and roles.
Then it generates month after month a table where for each role a student master and a vice are assigned.
The sake of this program is to balance the roles for each student, trying to assign a certain master role to 
each student not more than once. The db is used to store results of previous months in order to keep track
of the assignments. The GUI contains a the possibility to add students and roles with a form when th db
is empty and so we are in the situation of generating the first month (september). After the first generation,
and so after one month, we will open the application again and we will have only the possibility to generate
the results for the next month and the reset all, and so on for the other months until june.
In total we have 10 months (from september to june) are taken in conideration, 
so the constraints for a fair balancing are: 
- Nr = number of roles >= 5
- Ns = number of students >= 10
- Nr < Ns <= 2*Nr

Requirements:
- mysql 8.0 installed locally
- mysql-connector-python version 8.0.19
- texttable version 1.6.2