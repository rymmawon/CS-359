PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Member (
memberId INTEGER PRIMARY KEY,
name VARCHAR(50),
email VARCHAR(50) NOT NULL,
phone VARCHAR(15),
address VARCHAR(100),
age INTEGER NOT NULL CHECK (age >= 15),
membershipStartDate DATE NOT NULL,
membershipEndDate DATE NOT NULL CHECK (membershipEndDate >= membershipStartDate)
);
CREATE TABLE Instructor (
instructorId INTEGER PRIMARY KEY,
name VARCHAR(50),
specialty VARCHAR(50),
phone VARCHAR(15),
email VARCHAR(100) NOT NULL
);
CREATE TABLE GymFacility (
gymId INTEGER PRIMARY KEY,
location VARCHAR(100),
phone VARCHAR(50),
manager VARCHAR(50)
);
CREATE TABLE Class (
classId INTEGER PRIMARY KEY,
className VARCHAR(50),
classType VARCHAR(20) NOT NULL CHECK (classType IN ('Yoga', 'Zumba', 'HIIT', 'Weights', 'Swim')),
duration INTEGER NOT NULL,
classCapacity INTEGER NOT NULL,
instructorId INTEGER,
gymId INTEGER,
FOREIGN KEY (instructorId) REFERENCES Instructor(instructorId),
FOREIGN KEY (gymId) REFERENCES GymFacility(gymId)
);
CREATE TABLE Equipment (
equipmentId INTEGER PRIMARY KEY,
name VARCHAR(50) NOT NULL,
type VARCHAR(30) NOT NULL CHECK (type IN ('Cardio', 'Strength', 'Flexibility', 'Recovery', 'Safety')),
quantity INTEGER,
gymId INTEGER,
FOREIGN KEY (gymId) REFERENCES GymFacility(gymId)
);
CREATE TABLE MembershipPlan (
planId INTEGER PRIMARY KEY,
planType VARCHAR(20) NOT NULL CHECK (planType IN ('Monthly', 'Annual', 'Punch Card', 'Weekly', 'Discount')),
cost NUMERIC NOT NULL
);
CREATE TABLE Payment (
paymentId INTEGER PRIMARY KEY,
memberId INTEGER,
planId INTEGER,
amountPaid REAL NOT NULL,
paymentDate DATE NOT NULL,
FOREIGN KEY (memberId) REFERENCES Member(memberId),
FOREIGN KEY (planId) REFERENCES MembershipPlan(planId)
);
CREATE TABLE Attends (
memberId INTEGER NOT NULL,
classId INTEGER NOT NULL,
attendanceDate DATE NOT NULL,
PRIMARY KEY (memberId, classId, attendanceDate),
FOREIGN KEY (memberId) REFERENCES Member(memberId),
FOREIGN KEY (classId) REFERENCES Class(classId)
);
COMMIT;
