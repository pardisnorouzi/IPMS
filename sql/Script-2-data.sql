GRANT UNLIMITED TABLESPACE TO IPMS;
GRANT UNLIMITED TABLESPACE TO SYSTEM;


INSERT INTO IPMS.USERTYPES (user_type, Created, Updated)
VALUES ('coordinator', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Usertypes (user_type, Created, Updated)
VALUES ('company', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Usertypes (user_type, Created, Updated)
VALUES ('student', SYSTIMESTAMP, SYSTIMESTAMP);


--Insert data into Login:



INSERT INTO IPMS.Login (Email, Password, Created, Updated)
VALUES ('Tiziana@gmail.com', '827ccb0eea8a706c4c34a16891f84e7b', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Login (Email, Password, Created, Updated)
VALUES ('Pardis@gmail.com', '827ccb0eea8a706c4c34a16891f84e7b', SYSTIMESTAMP, SYSTIMESTAMP);



--Insert data into Users:

INSERT INTO IPMS.Users (First_name, Last_name, Address, Telephone, Is_pending, Is_approved, Login_id, User_type_id, Created, Updated)
VALUES ('Tiziana', 'Margaria', 'O’connel Street, Limerick', '833399124',0,1, 1,1, SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Users (First_name, Last_name, Address, Telephone, Is_pending, Is_approved, Login_id, User_type_id, Created, Updated)
VALUES ('Pardis', 'Norouzi', 'Henry Street, Limerick', '833366124',0,1, 2,3, SYSTIMESTAMP, SYSTIMESTAMP);


--Insert into Companies:

INSERT INTO IPMS.Companies (Company_name, Address, Telephone, Email, Created, Updated)
VALUES ('CompanyA', 'William Street', '555555555', 'acompany@gmail.com', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Companies (Company_name, Address, Telephone, Email, Created, Updated)
VALUES ('CompanyB', 'William Street', '555555444', 'bcompany@gmail.com', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Companies (Company_name, Address, Telephone, Email, Created, Updated)
VALUES ('CompanyC', 'William Street', '555553333', 'ccompany@gmail.com', SYSTIMESTAMP, SYSTIMESTAMP);

--Insert into Status:

INSERT INTO IPMS.Status (Status_type, Created, Updated)
VALUES ('open', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Status (Status_type, Created, Updated)
VALUES ('in-process', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Status (Status_type, Created, Updated)
VALUES ('closed', SYSTIMESTAMP, SYSTIMESTAMP);

--Insert into placement as coordinator:

INSERT INTO IPMS.Placements (Title, Description, Skills, Status_id, Company_id, User_id, Created, Updated)
VALUES ('Software Engineer Intern', 'Assist with software development tasks', 'Java, Python, SQL', 1,1,1, SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Placements (Title, Description, Skills, Status_id, Company_id, User_id, Created, Updated)
VALUES ('Programming Intern', 'Assist with software development tasks', 'Java, Python, SQL', 1,1, 1, SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Placements (Title, Description, Skills, Status_id, Company_id, User_id, Created, Updated)
VALUES ('Analytics Intern', 'Assist with statistics', 'Java, Python, C++', 1,1, 1, SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Placements (Title, Description, Skills, Status_id, Company_id, User_id, Created, Updated)
VALUES ('Data Programming', 'Assist with Data', 'Java, Python, C++', 1,1, 1, SYSTIMESTAMP, SYSTIMESTAMP);

--Insert data into Priorities table:

INSERT INTO IPMS.Priorities (Priority_name, Created, Updated)
VALUES ('First', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Priorities (Priority_name, Created, Updated)
VALUES ('Second', SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.Priorities (Priority_name, Created, Updated)
VALUES ('Third', SYSTIMESTAMP, SYSTIMESTAMP);

--Insert data into StudentsPreferences table:

INSERT INTO IPMS.StudentsPreferences (Priority_id, User_id, Placement_id, Is_pending, Is_approved, Created, Updated)
VALUES (1, 2, 1, 1, 0, SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.StudentsPreferences (Priority_id, User_id, Placement_id, Is_pending, Is_approved, Created, Updated)
VALUES (2, 2, 3, 1, 0, SYSTIMESTAMP, SYSTIMESTAMP);

INSERT INTO IPMS.StudentsPreferences (Priority_id, User_id, Placement_id, Is_pending, Is_approved, Created, Updated)
VALUES (3, 2, 2, 1, 0, SYSTIMESTAMP, SYSTIMESTAMP);
