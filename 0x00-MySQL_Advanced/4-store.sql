-- Create trigger to decrease item quantity after adding a new order
DELIMITER //

CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    --  a variable to hold the current quantity of the item.
    DECLARE item_quantity INT;

    -- Retrieve current quantity of the item
    SELECT quantity INTO item_quantity
    FROM items
    WHERE name = NEW.item_name;

    -- Update item quantity by subtracting the number of items in the new order
    UPDATE items
    SET quantity = item_quantity - NEW.number
    WHERE name = NEW.item_name;
END //

DELIMITER ;
