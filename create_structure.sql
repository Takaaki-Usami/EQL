CREATE TABLE Construction_info (
    ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    main_structure NVARCHAR(32) NOT NULL,
    pile_type NVARCHAR(32) NOT NULL,
    purchased_soil NUMERIC(10,2) NOT NULL DEFAULT 0,
    sand NUMERIC(10,2) NOT NULL DEFAULT 0,
    gravel NUMERIC(10,2) NOT NULL DEFAULT 0,
    crushed_stone NUMERIC(10,2) NOT NULL DEFAULT 0,
    solidifying NUMERIC(10,2) NOT NULL DEFAULT 0,
    rebar NUMERIC(10,2) NOT NULL DEFAULT 0,
    formwork NUMERIC(10,2) NOT NULL DEFAULT 0,
    steel_frame NUMERIC(10,2) NOT NULL DEFAULT 0,
    deck_plate NUMERIC(10,2) NOT NULL DEFAULT 0,
    affiliation NVARCHAR(32) NOT NULL DEFAULT '未入力',
    lastname NVARCHAR(32) NOT NULL DEFAULT '未入力',
    firstname NVARCHAR(32) NOT NULL DEFAULT '未入力',
    department NVARCHAR(32) NOT NULL DEFAULT '未入力',
    phonenumber NVARCHAR(32) NOT NULL DEFAULT '未入力',
    email_address NVARCHAR(128) NOT NULL DEFAULT '未入力',
    creation_date DATETIME NOT NULL DEFAULT GETDATE(),
    update_date DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TABLE Use_options (
    ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Construction_ID INT NOT NULL,
    use_option NVARCHAR(64) NOT NULL,
    area NUMERIC(10,2) NOT NULL DEFAULT 0,
    creation_date DATETIME NOT NULL DEFAULT GETDATE(),
    update_date DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Use_options_Construction_info FOREIGN KEY (Construction_ID)
    REFERENCES Construction_info(ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Cast_pile (
    ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Construction_ID INT NOT NULL,
    cement_type NVARCHAR(32) NOT NULL,
    strength INT NOT NULL DEFAULT 0,
    cast_pile_quantity NUMERIC(10,2) NOT NULL DEFAULT 0,
    creation_date DATETIME NOT NULL DEFAULT GETDATE(),
    update_date DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Cast_pile_Construction_info FOREIGN KEY (Construction_ID)
    REFERENCES Construction_info(ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Precast_pile (
    ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Construction_ID INT NOT NULL,
    sign NVARCHAR(32) NOT NULL,
    pile_type NVARCHAR(32) NOT NULL,
    phi NUMERIC(10,2) NOT NULL DEFAULT 0,
    pile_length NUMERIC(10,2) NOT NULL DEFAULT 0,
    thickness NUMERIC(10,2) NOT NULL DEFAULT 0,
    precast_pile_quantity INT NOT NULL DEFAULT 0,
    creation_date DATETIME NOT NULL DEFAULT GETDATE(),
    update_date DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Precast_pile_Construction_info FOREIGN KEY (Construction_ID)
    REFERENCES Construction_info(ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Cast_concrete (
    ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Construction_ID INT NOT NULL,
    cement_type NVARCHAR(32) NOT NULL,
    strength INT NOT NULL DEFAULT 0,
    cast_concrete_quantity NUMERIC(10,2) NOT NULL DEFAULT 0,
    creation_date DATETIME NOT NULL DEFAULT GETDATE(),
    update_date DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Cast_concrete_Construction_info FOREIGN KEY (Construction_ID)
    REFERENCES Construction_info(ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Precast_concrete (
    ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Construction_ID INT NOT NULL,
    strength INT NOT NULL DEFAULT 0,
    precast_concrete_quantity NUMERIC(10,2) NOT NULL DEFAULT 0,
    creation_date DATETIME NOT NULL DEFAULT GETDATE(),
    update_date DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Precast_concrete_Construction_info FOREIGN KEY (Construction_ID)
    REFERENCES Construction_info(ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);