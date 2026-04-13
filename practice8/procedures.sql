CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    -- Егер осындай есімді адам базада болса
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        -- Егер жоқ болса, жаңадан қосамыз
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;