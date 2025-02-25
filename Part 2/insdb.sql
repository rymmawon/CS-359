INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate)
VALUES ('Amy Adams', 'aadams123@yahoo.com', '505-123-4567', '123 Fake St NW', 22, '2024-01-01', '2024-02-01'),
 ('Bill Burr', 'bburr321@gmail.com', '505-234-5678', '124 Fake St NW', 17, '2024-01-01', '2024-02-01'),
 ('Cathy Chavez', 'cchavez246@aol.com', '505-345-6789', '125 Fake St NW', 25, '2024-02-01', '2025-01-01'),
 ('Danny Dimes', 'ddimes135@yahoo.com', '505-456-7890', '126 Fake St NW', 34, '2024-03-10', '2024-09-10'),
 ('Evan Ewing', 'eewing1245@enmu.edu', '505-567-8901', '127 Fake St NW', 67, '2024-02-23', '2024-03-02');

INSERT INTO Instructor (name, specialty, phone, email)
VALUES ('Fabian Fever', 'Spinning', '505-678-9012', 'fabFever@yahoo.com'),
 ('Gal Gadot', 'Swimming', '505-789-0123', 'Ggadot@gmail.com'),
 ('Hallie Hobbs', 'Weightlifting', '505-890-1234', 'HHobbs@aol.com'),
 ('Isaac Ingles', 'Powerlifting', '505-901-2345', 'IINgles23@yahoo.com'),
 ('Jeremy Jaramillo', 'Yoga', '505-012-3456', 'JJJ24@enmu.edu');

INSERT INTO GymFacility (location, phone, manager)
VALUES ('Riverside', '505-123-4567', 'Kris Kringle'),
 ('Rio Rancho', '505-234-5678', 'Lex Luthor'),
 ('Santa Fe', '505-345-6789', 'Max Markham'),
 ('Westside', '505-456-7890', 'Nancy Nunez'),
 ('The Heights', '505-567-8901', 'Otto Octavius');

INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId)
VALUES ('Hot Yoga', 'Yoga', 60, 20, 5, 5),
 ('Powerlifting for Beginners', 'Weights', 90, 10, 4, 2),
 ('Advanced Zumba', 'Zumba', 30, 20, 1, 3),
 ('Swim Lessons', 'Swim', 45, 5, 2, 1),
 ('Cross training', 'HIIT', 60, 15, 3, 4);

INSERT INTO Equipment (name, type, quantity, gymId)
VALUES ('Squat Rack', 'Strength', 5, 2),
 ('Life Vest', 'Safety', 10, 1),
 ('Yoga Block', 'Flexibility', 20, 5),
 ('Barbell', 'Strength', 10, 4),
 ('Stationary Bike', 'Cardio', 20, 3);

INSERT INTO MembershipPlan (planType, cost)
VALUES ('Monthly', 40),
 ('Annual', 360),
 ('Punch Card', 50),
 ('Weekly', 18),
 ('Discount', 35);

INSERT INTO Payment (memberId, planId, amountPaid, paymentDate)
VALUES (1, 5, 35, '2024-01-01'),
 (2, 1, 40, '2024-01-01'),
 (3, 2, 360, '2024-02-01'),
 (4, 3, 50, '2024-03-10'),
 (5, 4, 18, '2024-02-23');

INSERT INTO Attends (memberId, classId, attendanceDate)
VALUES (1, 1, '2024-01-01'),
 (2, 2, '2024-01-02'),
 (3, 3, '2024-02-10'),
 (4, 5, '2024-03-20'),
 (5, 4, '2024-02-25');