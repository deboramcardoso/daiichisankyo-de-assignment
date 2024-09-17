-- Step 3: Rename columns with descriptive names for readability
ALTER TABLE interactions RENAME COLUMN customers TO customer_id;
ALTER TABLE products RENAME COLUMN product TO product_name;

-- Step 4: Add a foreign key constraint to link 'interactions' to 'customers'
ALTER TABLE interactions ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);