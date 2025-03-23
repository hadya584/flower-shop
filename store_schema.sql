DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username    varchar(32) not null PRIMARY KEY,
    password    varchar(128) not null,
    fname       varchar(32),
    lname       varchar(32)
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        varchar(50) not null,
    description varchar(128),
    category    varchar(32),
    price       decimal(10,2) not null,
    quantity    int(9) not null,
    image_url   varchar(128)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    varchar(32) not null,
    total       decimal(10,2) not null,
    date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_numb  TEXT UNIQUE,
    FOREIGN KEY (username) REFERENCES users(username)
        ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    order_num   int(9) not null,
    product_id  int(9) not null,
    quantity    int(9) not null,
    subtotal    decimal(10,2) not null,
    FOREIGN KEY (order_num) REFERENCES orders(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO users (username, password, fname, lname) VALUES
('testuser', 'testpass', 'Test', 'User');

INSERT INTO products (name, description, category, price, quantity, image_url) VALUES
('Red Roses', 'Classic bouquet of red roses', 'Roses', 19.99, 20, 'images/red_roses.png'),
('Pink Roses', 'Bouquet of soft pink roses', 'Roses', 19.99, 20, 'images/pink_roses.png'),
('White Roses', 'Elegant bouquet of white roses', 'Roses', 19.99, 20, 'images/white_roses.webp'),
('Yellow Roses', 'Cheerful bouquet of yellow roses', 'Roses', 19.99, 20, 'images/yellow_roses.png'),
('Purple Roses', 'Splendid bouquet of purple roses', 'Roses', 19.99, 20, 'images/purple_roses.png'),
('Blue Roses', 'Mystical bouquet of blue roses', 'Roses', 19.99, 20, 'images/blue_roses.webp'),
('Red Tulips', 'Bold bouquet of red tulips', 'Tulips', 15.99, 15, 'images/red_tulips.png'),
('Pink Tulips', 'Delicate bouquet of pink tulips', 'Tulips', 15.99, 15, 'images/pink_tulips.png'),
('White Tulips', 'Bouquet of simple white tulips', 'Tulips', 15.99, 15, 'images/white_tulips.webp'),
('Yellow Tulips', 'Vibrant bouquet of yellow tulips', 'Tulips', 15.99, 15, 'images/yellow_tulips.png'),
('Purple Tulips', 'Regal bouquet of purple tulips', 'Tulips', 15.99, 15, 'images/purple_tulips.png'),
('Orange Tulips', 'Lively bouquet of orange tulips', 'Tulips', 15.99, 15, 'images/orange_tulips.png'),
('Red Daisies', 'Playful bouquet of red daisies', 'Daisies', 14.99, 15, 'images/red_daisies.png'),
('Pink Daisies', 'Sweet bouquet of pink daisies', 'Daisies', 14.99, 15, 'images/pink_daisies.webp'),
('White Daisies', 'Classic bouquet of white daisies', 'Daisies', 14.99, 15, 'images/white_daisies.png'),
('Yellow Daisies', 'Bouquet of sunny yellow daisies', 'Daisies', 14.99, 15, 'images/yellow_daisies.webp'),
('Orange Daisies', 'Beautiful bouquet of orange daisies', 'Daisies', 14.99, 15, 'images/orange_daisies.png'),
('Purple Daisies', 'Whimsical bouquet of purple daisies', 'Daisies', 14.99, 15, 'images/purple_daisies.png'),
('Red Carnations', 'Fluffy bouquet of red carnations', 'Carnations', 18.99, 15, 'images/red_carnations.png'),
('Pink Carnations', 'Bouquet of soft pink carnations', 'Carnations', 18.99, 15, 'images/pink_carnations.webp'),
('White Carnations', 'Bouquet of pure white canrations', 'Carnations', 18.99, 15, 'images/white_carnations.png'),
('Yellow Carnations', 'Bright bouquet of yellow carnations', 'Carnations', 18.99, 15, 'images/yellow_carnations.png'),
('Purple Carnations', 'Unique bouquet of purple carnations', 'Carnations', 18.99, 15, 'images/purple_carnations.png'),
('Blue Carnations', 'Gorgeous bouquet of blue carnations', 'Carnations', 18.99, 15, 'images/blue_carnations.png');
