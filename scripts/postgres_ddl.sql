-- SQLINES DEMO *** le SQL Developer Data Modeler 23.1.0.087.0806
-- SQLINES DEMO *** -03-28 17:42:49 EDT
-- SQLINES DEMO *** le Database 21c
-- SQLINES DEMO *** le Database 21c



-- SQLINES DEMO *** no DDL - MDSYS.SDO_GEOMETRY

-- SQLINES DEMO *** no DDL - XMLTYPE

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_account (
    account_no   BIGINT NOT NULL,
    account_name VARCHAR(30) NOT NULL,
    date_opened  TIMESTAMP(0) NOT NULL,
    account_type VARCHAR(2) NOT NULL,
    customer_id  BIGINT NOT NULL,
    address_id   BIGINT NOT NULL
);

ALTER TABLE aty_account
    ADD CONSTRAINT ch_inh_aty_account CHECK ( account_type IN ( 'C', 'HL', 'L', 'S', 'SL' ) );

COMMENT ON COLUMN aty_account.account_no IS
    'Account Number';

COMMENT ON COLUMN aty_account.date_opened IS
    'Date of account opening.';

COMMENT ON COLUMN aty_account.account_type IS
    'Type of Account';


ALTER TABLE aty_account ADD CONSTRAINT aty_account_pk PRIMARY KEY ( account_no );

ALTER TABLE aty_account ADD CONSTRAINT customer_id_account_type_un UNIQUE ( customer_id,
                                                                            account_type );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_address (
    address_id     BIGINT NOT NULL,
    address_line_1 VARCHAR(50) NOT NULL,
    address_line_2 VARCHAR(50),
    city           VARCHAR(30) NOT NULL,
    state          VARCHAR(2) NOT NULL,
    zipcode        VARCHAR(5) NOT NULL
);

COMMENT ON COLUMN aty_address.address_id IS
    'Unique identifier for address';

COMMENT ON COLUMN aty_address.address_line_1 IS
    'First line or stree of the address';

COMMENT ON COLUMN aty_address.address_line_2 IS
    'Additional address information';

COMMENT ON COLUMN aty_address.state IS
    'Abbrevation for each state';

ALTER TABLE aty_address ADD CONSTRAINT aty_address_pk PRIMARY KEY ( address_id );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_checking_account (
    account_no     BIGINT NOT NULL,
    service_charge DECIMAL(6, 2) NOT NULL
);

COMMENT ON COLUMN aty_checking_account.account_no IS
    'Account Number';

COMMENT ON COLUMN aty_checking_account.service_charge IS
    'Monthly service charge';

ALTER TABLE aty_checking_account ADD CONSTRAINT aty_checking_account_pk PRIMARY KEY ( account_no );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_customer (
    customer_id BIGINT NOT NULL,
    fname       VARCHAR(30) NOT NULL,
    lname       VARCHAR(50) NOT NULL,
    address_id  BIGINT NOT NULL
);

COMMENT ON COLUMN aty_customer.customer_id IS
    'Unique Identifier for customer';

COMMENT ON COLUMN aty_customer.fname IS
    'First Name of Customer';

COMMENT ON COLUMN aty_customer.lname IS
    'Last Name of Customer';

ALTER TABLE aty_customer ADD CONSTRAINT aty_customer_pk PRIMARY KEY ( customer_id );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_loan_account (
    account_no   BIGINT NOT NULL,
    rate         DECIMAL(4, 2) NOT NULL,
    amount       DECIMAL(11, 2) NOT NULL,
    loan_months  SMALLINT NOT NULL,
    loan_payment DECIMAL(11, 2) NOT NULL,
    loan_type    VARCHAR(2) NOT NULL
);

ALTER TABLE aty_loan_account
    ADD CONSTRAINT ch_inh_aty_loan_account CHECK ( loan_type IN ( 'HL', 'L', 'SL' ) );

COMMENT ON COLUMN aty_loan_account.account_no IS
    'Account Number';

COMMENT ON COLUMN aty_loan_account.rate IS
    'Rate of Interest';

COMMENT ON COLUMN aty_loan_account.loan_months IS
    'Number of months';

COMMENT ON COLUMN aty_loan_account.loan_payment IS
    'Amount of money paid (monthly)';

COMMENT ON COLUMN aty_loan_account.loan_type IS
    'Type of Loan: Student/House/Personal';

ALTER TABLE aty_loan_account ADD CONSTRAINT aty_loan_account_pk PRIMARY KEY ( account_no );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_savings_account (
    account_no    BIGINT NOT NULL,
    interest_rate DECIMAL(4, 2) NOT NULL
);

COMMENT ON COLUMN aty_savings_account.account_no IS
    'Account Number';

ALTER TABLE aty_savings_account ADD CONSTRAINT aty_savings_account_pk PRIMARY KEY ( account_no );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_student_loan (
    account_no      BIGINT NOT NULL,
    student_id      BIGINT NOT NULL,
    university_name VARCHAR(50) NOT NULL,
    degree          VARCHAR(30) NOT NULL,
    graduation_date TIMESTAMP(0) NOT NULL
);

COMMENT ON COLUMN aty_student_loan.account_no IS
    'Account Number';

COMMENT ON COLUMN aty_student_loan.student_id IS
    'Student Id for each student';

COMMENT ON COLUMN aty_student_loan.university_name IS
    'University Name';

COMMENT ON COLUMN aty_student_loan.degree IS
    'Degree - Graduate or Undergraduate';

COMMENT ON COLUMN aty_student_loan.graduation_date IS
    'Date of Graduation';

ALTER TABLE aty_student_loan ADD CONSTRAINT aty_student_loan_pk PRIMARY KEY ( account_no );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE aty_home_loan (
    account_no               BIGINT NOT NULL,
    house_built_year         SMALLINT NOT NULL,
    insurance_account_no     BIGINT NOT NULL,
    insurance_company        VARCHAR(50) NOT NULL,
    yearly_insurance_premium DECIMAL(6, 2) NOT NULL,
    address_id               BIGINT NOT NULL
);

COMMENT ON COLUMN aty_home_loan.account_no IS
    'Account Number';

COMMENT ON COLUMN aty_home_loan.house_built_year IS
    'Year the house was built';

COMMENT ON COLUMN aty_home_loan.insurance_account_no IS
    'Home Insurance account number';

COMMENT ON COLUMN aty_home_loan.insurance_company IS
    'Insurance Company';

COMMENT ON COLUMN aty_home_loan.yearly_insurance_premium IS
    'Yearly Premium Rate ';

ALTER TABLE aty_home_loan ADD CONSTRAINT home_loan_pk PRIMARY KEY ( account_no );

ALTER TABLE aty_customer
    ADD CONSTRAINT customer_address_fk FOREIGN KEY ( address_id )
        REFERENCES aty_address ( address_id );

ALTER TABLE aty_account
    ADD CONSTRAINT fk_account_address FOREIGN KEY ( address_id )
        REFERENCES aty_address ( address_id );

ALTER TABLE aty_account
    ADD CONSTRAINT fk_account_customer FOREIGN KEY ( customer_id )
        REFERENCES aty_customer ( customer_id );

ALTER TABLE aty_checking_account
    ADD CONSTRAINT fk_checking_account_account FOREIGN KEY ( account_no )
        REFERENCES aty_account ( account_no );

ALTER TABLE aty_home_loan
    ADD CONSTRAINT fk_home_loan_address FOREIGN KEY ( address_id )
        REFERENCES aty_address ( address_id );

ALTER TABLE aty_home_loan
    ADD CONSTRAINT fk_home_loan_loan_account FOREIGN KEY ( account_no )
        REFERENCES aty_loan_account ( account_no );

ALTER TABLE aty_loan_account
    ADD CONSTRAINT fk_loan_account_account FOREIGN KEY ( account_no )
        REFERENCES aty_account ( account_no );

ALTER TABLE aty_savings_account
    ADD CONSTRAINT fk_savings_account_account FOREIGN KEY ( account_no )
        REFERENCES aty_account ( account_no );

ALTER TABLE aty_student_loan
    ADD CONSTRAINT fk_student_loan_loan_account FOREIGN KEY ( account_no )
        REFERENCES aty_loan_account ( account_no );

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE OR REPLACE FUNCTION arc_fkarc_13_home_loan_func() RETURNS TRIGGER AS $$
DECLARE
    d VARCHAR(2);
BEGIN
    SELECT
        a.loan_type
    INTO d
    FROM
        aty_loan_account a
    WHERE
        a.account_no = new.account_no;

    IF ( d IS NULL OR d <> 'HL' ) THEN
        raise exception '%s',  'FK FK_HOME_LOAN_LOAN_ACCOUNT in Table HOME_LOAN violates Arc constraint on Table ATY_LOAN_ACCOUNT - discriminator column LOAN_TYPE doesn''t have value ''HL'''
         using errcode = -20223;
    END IF;

    -- Return statement for AFTER triggers
    RETURN NEW;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER arc_fkarc_13_home_loan BEFORE
    INSERT OR UPDATE OF account_no ON aty_home_loan
    FOR EACH ROW
EXECUTE FUNCTION arc_fkarc_13_home_loan_func();

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE OR REPLACE FUNCTION arc_fkarc_13_aty_student_loan_func() RETURNS TRIGGER AS $$
DECLARE
    d VARCHAR(2);
BEGIN
    SELECT
        a.loan_type
    INTO d
    FROM
        aty_loan_account a
    WHERE
        a.account_no = new.account_no;

    IF ( d IS NULL OR d <> 'SL' ) THEN
        raise exception '%s',  'FK FK_STUDENT_LOAN_LOAN_ACCOUNT in Table ATY_STUDENT_LOAN violates Arc constraint on Table ATY_LOAN_ACCOUNT - discriminator column LOAN_TYPE doesn''t have value ''SL'''
         using errcode = -20223;
    END IF;

    -- Return statement for AFTER triggers
    RETURN NEW;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER arc_fkarc_13_aty_student_loan BEFORE
    INSERT OR UPDATE OF account_no ON aty_student_loan
    FOR EACH ROW
EXECUTE FUNCTION arc_fkarc_13_aty_student_loan_func();

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE OR REPLACE FUNCTION arc_fkarc_14_aty_loan_account_func() RETURNS TRIGGER AS $$
DECLARE
    d VARCHAR(2);
BEGIN
    SELECT
        a.account_type
    INTO d
    FROM
        aty_account a
    WHERE
        a.account_no = new.account_no;

    IF ( d IS NULL OR d <> 'L' ) THEN
        raise exception '%s',  'FK FK_LOAN_ACCOUNT_ACCOUNT in Table ATY_LOAN_ACCOUNT violates Arc constraint on Table ATY_ACCOUNT - discriminator column ACCOUNT_TYPE doesn''t have value ''L'''
         using errcode = -20223;
    END IF;

    -- Return statement for AFTER triggers
    RETURN NEW;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER arc_fkarc_14_aty_loan_account BEFORE
    INSERT OR UPDATE OF account_no ON aty_loan_account
    FOR EACH ROW
EXECUTE FUNCTION arc_fkarc_14_aty_loan_account_func();

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE OR REPLACE FUNCTION arc_fkarc__aty_savings_account_func() RETURNS TRIGGER AS $$
DECLARE
    d VARCHAR(2);
BEGIN
    SELECT
        a.account_type
    INTO d
    FROM
        aty_account a
    WHERE
        a.account_no = new.account_no;

    IF ( d IS NULL OR d <> 'S' ) THEN
        raise exception '%s',  'FK FK_SAVINGS_ACCOUNT_ACCOUNT in Table ATY_SAVINGS_ACCOUNT violates Arc constraint on Table ATY_ACCOUNT - discriminator column ACCOUNT_TYPE doesn''t have value ''S'''
         using errcode = -20223;
    END IF;

    -- Return statement for AFTER triggers
    RETURN NEW;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER arc_fkarc__aty_savings_account BEFORE
    INSERT OR UPDATE OF account_no ON aty_savings_account
    FOR EACH ROW
EXECUTE FUNCTION arc_fkarc__aty_savings_account_func();

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE OR REPLACE FUNCTION arc_fkarc_aty_checking_account_func() RETURNS TRIGGER AS $$
DECLARE
    d VARCHAR(2);
BEGIN
    SELECT
        a.account_type
    INTO d
    FROM
        aty_account a
    WHERE
        a.account_no = new.account_no;

    IF ( d IS NULL OR d <> 'C' ) THEN
        raise exception '%s',  'FK FK_CHECKING_ACCOUNT_ACCOUNT in Table ATY_CHECKING_ACCOUNT violates Arc constraint on Table ATY_ACCOUNT - discriminator column ACCOUNT_TYPE doesn''t have value ''C'''
         using errcode = -20223;
    END IF;

    -- Return statement for AFTER triggers
    RETURN NEW;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER arc_fkarc_aty_checking_account BEFORE
    INSERT OR UPDATE OF account_no ON aty_checking_account
    FOR EACH ROW
EXECUTE FUNCTION arc_fkarc_aty_checking_account_func();

-- Additional Constraints
ALTER TABLE aty_checking_account ADD CONSTRAINT chk_service_charge CHECK (service_charge BETWEEN 0 AND 100);
ALTER TABLE aty_home_loan ADD CONSTRAINT chk_house_built_year CHECK (house_built_year BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE));
ALTER TABLE aty_loan_account ADD CONSTRAINT chk_loan_rate CHECK (rate BETWEEN 0 AND 20);
ALTER TABLE aty_savings_account ADD CONSTRAINT chk_interest_rate CHECK (interest_rate BETWEEN 0 AND 10);

