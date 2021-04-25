import random


def randstring(length):
    valid_letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join((random.choice(valid_letters) for i in range(length)))


def randnumber(length):
    valid_letters = '0987654321'
    return ''.join((random.choice(valid_letters) for i in range(length)))


def make_data_customer_info(num):
    #INSERT INTO customer_info
    #VALUES ('rksazid@gmail.com','MD.REZAUL','KARIM','rksazid123','01521453995','TELIGATI','Khulna','Active');
    towns = ['Bach Khoa', 'Cau Giay', 'Ba Dinh', 'Hoan Kiem', 'Long Bien', 'Hoang Mai', 'Thanh Tri', 'Ha Dong']
    city = 'Ha Noi'
    last_mail = '@gmail.com'
    userpasswords = ['abcd1234', '12345678', 'asdfqwer', 'qwer1234', '1234asdf', 'sdfqwer12']
    emails = []
    with open('database/customer_info.sql', 'w+') as f:
        for i in range(num):
            email = randstring(random.choice([8, 9, 10])) + last_mail
            emails.append(email)
            first_name = randstring(8)
            last_name = randstring(5)
            userpassword = random.choice(userpasswords)
            number = '0' + randnumber(9)
            town = random.choice(towns)
            f.write(f"INSERT INTO customer_info VALUES ('{email}','{first_name}','{last_name}','{userpassword}','{number}','{city}','{town}','Active');\n")
    return emails


def make_data_order_info(num, emails):
    #INSERT INTO order_info VALUES ('1000','dipto.8081@gmail.com','4-APR-2017','5-APR-2017');
    max = 2000 + num
    with open('database/order_info.sql', 'w+') as f:
        for order_id in range(2000, max):
            email = random.choice(emails)
            year = '2020'
            month = random.choice(range(1, 12))
            day = random.choice(range(1, 29))
            torcv = year + '-' + str(month) + '-' + str(day)
            todef = year + '-' + str(month) + '-' + str(day + random.choice([0, 1]))

            f.write(
                f"INSERT INTO order_info VALUES ('{order_id}','{email}','{torcv}','{todef}');\n")


def make_data_management(num):
    #INSERT INTO management VALUES ('Masud','m12345','Masud Rana','Active','Employee');
    cook_user_ids = []
    with open('database/management.sql', 'w+') as f:
        for i in range(num):
            user_id = randstring(random.choice([6, 7, 8, 9]))
            user_pass = user_id + '123'
            name = random.choice(['Nguyen', 'Luu', 'Le', 'Phung', 'Lai', 'Pham'])+' '+random.choice(['Van', 'Minh', 'Xuan', 'Duy', 'Hoang', 'Phuc', 'Quang', 'Hong'])+' '+random.choice(['Hieu', 'Dat', 'Huyen', 'Dai', 'Long', 'Phuc', 'Quang', 'Truong'])
            role = random.choice(['Cook','Employee'])
            if role == 'Cook': cook_user_ids.append(user_id)
            f.write(
                f"INSERT INTO management VALUES ('{user_id}','{user_pass}','{name}','Actv','{role}');\n")
    return cook_user_ids


def make_data_menu():
    #INSERT INTO menu VALUES ('20001','Shami Kabab','Kabab',60,'Fastfood','Available','HasibIq');
    item_names = ['Ga Ran Gion','Ga Sot Dau','Pizza Ga', 'Burger Ga', 'Coca', 'Pepsi', 'Tra Dao', 'Tra Chanh', 'Tra Quat', 'Kem']
    descriptions = ['Ga', 'Ga', 'Ga', 'Ga', 'Co gas', 'Co gas', 'Khong gas', 'Khong gas', 'Khong gas', 'Kem tuoi']
    prices = [39, 43, 32, 31, 10, 10, 12, 12, 12, 5]
    with open('database/menu.sql', 'w+') as f:
        for i in range(10):
            item_id = i + 30000
            f.write(
                f"INSERT INTO menu VALUES ('{item_id}','{item_names[i]}','{descriptions[i]}','{prices[i]}','fastfood','Available','HasibIq');\n")


def make_data_order_items(num, cook_user_ids):
    max = 2000 + num
    #INSERT INTO order_items VALUES ('1000','20003',5,'Pending','Bahadur');
    with open('database/order_items.sql', 'w+') as f:
        for order_id in range(2000, max):
            item_id = random.choice(range(30000, 30011))
            number = random.choice(range(5, 21))
            status = random.choice(['Ready', 'Pending'])
            user = random.choice(cook_user_ids)
            f.write(
                f"INSERT INTO order_items VALUES ('{order_id}','{item_id}',{number},'{status}','{user}');\n")


def make_data_account_info():
    #INSERT INTO account_info VALUES ('rksazid','sazidcse1234');
    pass


if __name__ == '__main__':
    emails = make_data_customer_info(1000)
    make_data_order_info(1000, emails)
    cook_user_ids = make_data_management(50)
    make_data_menu()
    make_data_order_items(1000,cook_user_ids)
