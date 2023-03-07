CREATE TABLE Usertypes (
	User_type_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_type VARCHAR (25) NOT NULL,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL	
);



CREATE TABLE Login (
	Login_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	Email VARCHAR (100) NOT NULL,
	Password VARCHAR (100) NOT NULL,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL	
);

CREATE TABLE Users (
	User_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	First_name VARCHAR (100) NOT NULL,
	Last_name VARCHAR (100) NOT NULL,
	Address VARCHAR (200) NOT NULL,
	Telephone VARCHAR (15) NOT NULL,
	Is_pending INT NOT NULL,
	Is_approved INT NOT NULL,
	Login_id INT NOT NULL,
	User_type_id INT NOT NULL,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL,
	CONSTRAINT fk_login_id
		FOREIGN KEY (Login_id)
			REFERENCES Login(Login_id),
	CONSTRAINT fk_ut_id
		FOREIGN KEY (User_type_id)
			REFERENCES Usertypes(User_type_id)
);

CREATE TABLE Companies(
	Company_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	Company_name VARCHAR (50) UNIQUE NOT NULL,
	Address VARCHAR (100) NOT NULL,
	Telephone VARCHAR (15) NOT NULL,
	Email VARCHAR (50) NOT NULL,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL
);

CREATE TABLE Status (
	Status_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	status_type VARCHAR (20) DEFAULT 'open' ,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL
);

CREATE TABLE Placements (
	Placement_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	Title VARCHAR (100) NOT NULL,
	Description VARCHAR (500) NOT NULL,
	Skills VARCHAR (500) NOT NULL,
	Status_id INT NOT NULL,
	Company_id INT NOT NULL,
	User_id INT NOT NULL,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL,
	CONSTRAINT fk_status_id
		FOREIGN KEY (Status_id)
			REFERENCES Status(Status_id),
	CONSTRAINT fk_company_id
		FOREIGN KEY (Company_id)
			REFERENCES Companies(Company_id),
	CONSTRAINT fk_user_id
		FOREIGN KEY (User_id)
			REFERENCES Users(User_id)
);

CREATE TABLE Priorities (
	Priority_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	Priority_name VARCHAR(10) NOT NULL,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL
);

CREATE TABLE StudentsPreferences(
	StudentsPreferences_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	Priority_id INT NOT NULL,
	User_id INT NOT NULL,
	Placement_id INT NOT NULL,
	Is_pending INT NOT NULL,
	Is_approved INT NOT NULL,
	Created TIMESTAMP NOT NULL,
	Updated TIMESTAMP NOT NULL,
	CONSTRAINT fk_priority_id
		FOREIGN KEY (Priority_id)
			REFERENCES Priorities(Priority_id),
	CONSTRAINT fk_user_id_sp
		FOREIGN KEY (User_id)
			REFERENCES Users(User_id),
	CONSTRAINT fk_placement_id
		FOREIGN KEY (Placement_id)
			REFERENCES Placements(Placement_id)
);