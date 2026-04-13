-- Бұл функция аты немесе нөмірі бойынша контактілерді тауып береді
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(contact_name VARCHAR, contact_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    WHERE name ILIKE '%' || p_pattern || '%' 
       OR phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;