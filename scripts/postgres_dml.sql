-- Records for aty_address table
INSERT INTO aty_address (address_id, address_line_1, address_line_2, city, state, zipcode)
VALUES
(10011, '123 Main St', 'Apt 101', 'Anytown', 'NY', '12345'),
(10012, '456 Elm St', NULL, 'Smallville', 'CA', '54321'),
(10013, '789 Oak St', 'Suite 201', 'Metropolis', 'IL', '67890'),
(10014, '101 Pine St', 'Unit 301', 'Springfield', 'IL', '54321'),
(10015, '555 Maple Ave', NULL, 'Gotham City', 'NY', '98765'),
(10016, '777 Cedar Rd', 'Apt 102', 'Riverdale', 'CA', '34567'),
(10017, '888 Birch Ln', 'Suite 501', 'Central City', 'MO', '45678'),
(10018, '999 Elm Blvd', NULL, 'Star City', 'WA', '87654'),
(10019, '111 Oak Dr', 'Unit 202', 'Emerald City', 'KS', '23456'),
(10020, '222 Walnut St', 'Apt 401', 'Atlantis', 'FL', '76543'),
(10021, '333 Cherry Ave', NULL, 'Olympus', 'GA', '65432'),
(10022, '444 Pineapple Blvd', 'Suite 301', 'Aspen Falls', 'CO', '43210'),
(10023, '555 Banana Rd', NULL, 'Neverland', 'CA', '87654'),
(10024, '666 Mango Dr', 'Unit 101', 'Paradise City', 'NV', '54321'),
(10025, '777 Coconut Ln', NULL, 'Rivendell', 'VA', '98765'),
(10026, '888 Papaya Ave', 'Apt 201', 'Elysium', 'TX', '34567'),
(10027, '999 Grapefruit Blvd', NULL, 'Avalon', 'AZ', '45678'),
(10028, '111 Lemon Dr', 'Suite 401', 'Shangri-La', 'HI', '23456');

-- Records for aty_customer table
INSERT INTO aty_customer (customer_id, fname, lname, address_id)
VALUES
(1000001, 'John', 'Doe', 10011),
(1000002, 'Jane', 'Smith', 10012),
(1000003, 'Michael', 'Johnson', 10013),
(1000004, 'Emily', 'Brown', 10014),
(1000005, 'David', 'Martinez', 10015),
(1000006, 'Sophia', 'Garcia', 10016),
(1000007, 'James', 'Miller', 10017),
(1000008, 'Olivia', 'Jackson', 10018),
(1000009, 'William', 'Davis', 10019),
(1000010, 'Isabella', 'Lopez', 10020),
(1000011, 'Michael', 'Hernandez', 10021),
(1000012, 'Amelia', 'Moore', 10022),
(1000013, 'Benjamin', 'Wilson', 10023),
(1000014, 'Mia', 'Anderson', 10024),
(1000015, 'Ethan', 'Thomas', 10025),
(1000016, 'Charlotte', 'Taylor', 10026),
(1000017, 'Alexander', 'White', 10027),
(1000018, 'Emma', 'Clark', 10028);

-- Records for aty_account table
INSERT INTO aty_account (account_no, account_name, date_opened, account_type, customer_id, address_id)
VALUES
(100201, 'Checking Account', TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'C', 1000001, 10011),
(100202, 'Savings Account', TO_DATE('2024-02-01', 'YYYY-MM-DD'), 'S', 1000002, 10012),
(100203, 'Loan Account', TO_DATE('2023-12-01', 'YYYY-MM-DD'), 'L', 1000003, 10013),
(100204, 'Checking Account', TO_DATE('2023-11-15', 'YYYY-MM-DD'), 'C', 1000004, 10014),
(100205, 'Savings Account', TO_DATE('2024-03-10', 'YYYY-MM-DD'), 'S', 1000005, 10015),
(100206, 'Loan Account', TO_DATE('2022-08-20', 'YYYY-MM-DD'), 'L', 1000006, 10016),
(100207, 'Checking Account', TO_DATE('2024-02-28', 'YYYY-MM-DD'), 'C', 1000007, 10017),
(100208, 'Savings Account', TO_DATE('2023-12-05', 'YYYY-MM-DD'), 'S', 1000008, 10018),
(100209, 'Loan Account', TO_DATE('2023-09-18', 'YYYY-MM-DD'), 'L', 1000009, 10019),
(100210, 'Checking Account', TO_DATE('2022-10-30', 'YYYY-MM-DD'), 'C', 1000010, 10020),
(100211, 'Savings Account', TO_DATE('2023-04-15', 'YYYY-MM-DD'), 'S', 1000011, 10021),
(100212, 'Loan Account', TO_DATE('2022-12-25', 'YYYY-MM-DD'), 'L', 1000012, 10022),
(100213, 'Checking Account', TO_DATE('2023-05-20', 'YYYY-MM-DD'), 'C', 1000013, 10023),
(100214, 'Savings Account', TO_DATE('2024-01-08', 'YYYY-MM-DD'), 'S', 1000014, 10024),
(100215, 'Loan Account', TO_DATE('2024-02-14', 'YYYY-MM-DD'), 'L', 1000015, 10025),
(100216, 'Checking Account', TO_DATE('2023-07-01', 'YYYY-MM-DD'), 'C', 1000016, 10026),
(100217, 'Savings Account', TO_DATE('2023-09-30', 'YYYY-MM-DD'), 'S', 1000017, 10027),
(100218, 'Loan Account', TO_DATE('2024-01-30', 'YYYY-MM-DD'), 'L', 1000018, 10028),
(100219, 'Checking Account', TO_DATE('2024-03-15', 'YYYY-MM-DD'), 'C', 1000011, 10021),
(100220, 'Loan Account', TO_DATE('2023-10-20', 'YYYY-MM-DD'), 'L', 1000001, 10011),
(100221, 'Savings Account', TO_DATE('2024-02-25', 'YYYY-MM-DD'), 'S', 1000001, 10011),
(100222, 'Loan Account', TO_DATE('2023-11-30', 'YYYY-MM-DD'), 'L', 1000002, 10012),
(100223, 'Checking Account', TO_DATE('2023-09-10', 'YYYY-MM-DD'), 'C', 1000003, 10013),
(100224, 'Savings Account', TO_DATE('2024-01-05', 'YYYY-MM-DD'), 'S', 1000003, 10013),
(100225, 'Checking Account', TO_DATE('2023-12-20', 'YYYY-MM-DD'), 'C', 1000012, 10022),
(100226, 'Loan Account', TO_DATE('2024-02-05', 'YYYY-MM-DD'), 'L', 1000004, 10014),
(100227, 'Savings Account', TO_DATE('2023-11-10', 'YYYY-MM-DD'), 'S', 1000015, 10025),
(100228, 'Checking Account', TO_DATE('2024-01-20', 'YYYY-MM-DD'), 'C', 1000005, 10015);



-- Records for aty_checking_account table
INSERT INTO aty_checking_account (account_no, service_charge)
VALUES
(100201, 10.00),
(100204, 12.50),
(100207, 15.00),
(100210, 8.50),
(100213, 10.00),
(100216, 9.75),
(100219, 11.25),
(100223, 9.25),
(100225, 13.50),
(100228, 10.75);

-- Records for aty_loan_account table
INSERT INTO aty_loan_account (account_no, rate, amount, loan_months, loan_payment, loan_type)
VALUES
(100203, 4.5, 200000, 240, 1200, 'HL'),
(100206, 3.8, 150000, 180, 1000, 'L'),
(100209, 4.0, 180000, 240, 1100, 'SL'),
(100212, 3.6, 160000, 180, 950, 'L'),
(100215, 4.2, 220000, 240, 1250, 'HL'),
(100218, 3.9, 175000, 180, 1050, 'SL'),
(100220, 4.1, 195000, 240, 1150, 'HL'),
(100222, 3.7, 165000, 180, 975, 'L'),
(100226, 3.6, 160000, 180, 950, 'SL');

-- Records for aty_savings_account table
INSERT INTO aty_savings_account (account_no, interest_rate)
VALUES
(100202, 2.5),
(100205, 3.0),
(100208, 2.75),
(100211, 3.25),
(100214, 2.9),
(100217, 3.15),
(100221, 2.6),
(100224, 3.1),
(100227, 4.3);


-- Populate aty_home_loan table
INSERT INTO aty_home_loan (account_no, house_built_year, insurance_account_no, insurance_company, yearly_insurance_premium, address_id)
VALUES
(100203, 2000, 500001, 'InsuranceCo A', 1000.00, 10013),
(100215, 1988, 500003, 'InsuranceCo C', 1100.00, 10024),
(100220, 2005, 500004, 'InsuranceCo D', 1050.00, 10011);

-- Populate aty_student_loan table
INSERT INTO aty_student_loan (account_no, student_id, university_name, degree, graduation_date)
VALUES
(100209, 20002, 'XYZ College', 'Graduate', TO_DATE('2024-06-30', 'YYYY-MM-DD')),
(100218, 20003, '123 University', 'Undergraduate', TO_DATE('2022-12-20', 'YYYY-MM-DD')),
(100226, 20004, '456 School', 'Graduate', TO_DATE('2023-08-10', 'YYYY-MM-DD'));