import psycopg2
from tabulate import tabulate
from datetime import date


def connect_to_db(DB_NAME, DB_USER, DB_PASS, DB_HOST):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    return conn


def disconnect_to_db(conn):
    conn.close()


def query(conn, query_string):
    lst = []
    with conn.cursor() as cur:
        cur.execute(query_string)
        lst.append(cur.fetchall())
        conn.commit()
    return lst


def insert(conn, query_string):
    check = 1
    try:
        with conn.cursor() as cur:
            cur.execute(query_string)
            conn.commit()
            print("Successfully!")
            return check
    except (Exception, psycopg2.Error) as error:
        if conn:
            check = 0
            print("Failed to insert record", error)
            return check


def check_account(conn, username, userpass):
    customer_info = query(conn, "select email, pass, fname, status from customer_info")
    management_info = query(conn, "select user_id, pass, user_name,designation, status from management")
    check = 0
    name = ''
    designation = ''
    # check custtomer account
    for account in customer_info:
        for user in account:
            if username == user[0] and userpass == user[1]:
                if user[3] == 'Active':
                    check = 1
                    name = user[2]
                    break
                else:
                    check = -1
    # check employee and manager account
    for account in management_info:
        for empl in account:
            if username == empl[0] and userpass == empl[1]:
                if empl[4] != 'Blkd':
                    check = 2
                    name = empl[2]
                    designation = empl[3]
                    if empl[3] == 'Manager':
                        check = 3
                else:
                    check = -2
    # customer login successfull
    if check == 1:
        print(f"Login successfully!\nHello, {name}!")
    # employee login successful
    elif check == 2:
        print(f"Login successfully!\nHello, {name}!")
        print(f"Your designation is: {designation}")
    # manager login successful
    elif check == 3:
        print(f'Login successfully!\nHello, {designation} {name}')
    # customer login block
    elif check == -1:
        print("Your account has been blocked!")
        print("Because you cancel orders too much!")
    # employee login fail
    elif check == -2:
        print("Your account has been blocked!")

    else:
        print("Username or password is incorrect!")

    return check


def sale_by_day():
    pass


def login(conn):
    username = input("Enter your email or username: ")
    userpass = input("Enter your password: ")
    i = check_account(conn, username, userpass)
    select_1 = select_2 = select_3 = 5,
    count = 0
    while i == 0 and count < 3:
        print("Please enter again!")
        username = input("Enter your email: ")
        userpass = input("Enter your password: ")
        i = check_account(conn, username, userpass)
        count += 1
    if i == -1:
        print("Goodbye!")
        return
    if count == 3:
        char = input("Do you want to create a new account! (y/n)")
        while char != 'y' and char != 'n':
            char = input("Do you want to create a new account! (y/n)")
        if char == 'n':
            print("Goodbye!")
            return
        else:
            check = 0
            while check != 1:
                email = input("Enter your email:")
                if '@' not in email:
                    email = input("Your email is wrong! Enter again:")
                fname = input("Enter your firstname:")
                lname = input("Enter your lastname:")
                password = input("Enter your password:")
                phone = input("Enter your phone number:")
                if len(phone) == 11:
                    phone= input("Your phone number is wrong! Please enter again:")
                city = input("Enter your city:")
                town = input("Enter your town:")
                check = insert(conn, f"INSERT INTO customer_info VALUES ('{email}','{fname}','{lname}','{password}','{phone}','{city}','{town}','Active');")
    elif i == 1:
        while select_1 != 5:
            print("-----------CUSTOMER MENU:----------\n")
            print("1. Customer information")
            print("2. Show your previous order")
            print("3. Order")
            print("4. Check your present order")
            print("5. Exit\n")
            select_1 = int(input("Enter your choice: "))
            if select_1 == 1 : show_info_customer(conn, username)
            elif select_1 == 2 : show_old_order(conn, username)
            elif select_1 == 3 : order(conn, username)
            elif select_1 == 4 : check_present_order(conn, username)
            while select_1 < 1 or select_1 > 5:
                print("Invalid selection!")
                select_1 = input("Enter your choice: ")
    elif i == 2:
        while select_2 != 5:
            print("-----------EMPLOYEE MENU----------\n")
            print("1. Employee Information")
            print("2. Check order")
            print('3. Complete order')
            print("4. Show order can be delivery today")
            print("5. Exit\n")
            select_2 = int(input("Enter your choice: "))
            while select_2 < 1 or select_2 > 6:
                print("Invalid selection!")
                select_2 = input("Enter your choice: ")
            if select_2 == 1:
                show_employee_info(conn, username)
            if select_2 == 2:
                show_order(conn)
            if select_2 == 3:
                complete_order(conn)
            if select_2 == 4:
                check_order(conn)
    elif i == 3:
        while select_3 != 5:
            print("-----------MANAGER MENU----------\n")
            print("1. Database Management")
            print("2. Sales Management")
            print("3. Overview of sales areas")
            print("4. Exit\n")
            select_3 = int(input("Enter your choice: "))
            while select_3 < 1 or select_3 > 4:
                print("Invalid selection!")
                select_3 = input("Enter your choice: ")
            if select_3 == 1:
                print("-----------Database Management----------\n")
                print("1. Customer Information Management")
                print("2. Personnel Management")
                print("3. Show Order Information")
                print("4. Edit Menu")
                print("5. Exit\n")
                select_3_ = int(input("Enter your choice: "))
                while select_3_ < 1 or select_3_ > 5:
                    print("Invalid selection!")
                    select_3_ = input("Enter your choice: ")
            if select_3 == 2:
                print("-----------Sales Management----------\n")
                sale_by_day()
            if select_3 == 3:
                print("-----------Overview of sales areas----------\n")
                print("1. Most cancel area")
                print("2. Number of dishes sold in each area")
                print("3. Top 3 towns have the most customers")
                print("4. Exit\n")
                select_3_ = int(input("Enter your choice: "))
                while select_3_ < 1 or select_3_ > 5:
                    print("Invalid selection!")
                    select_3_ = input("Enter your choice: ")


def check_order(conn):
    lst = query(conn, "select order_items.order_id, quantity, status, torcv, todel \
                       from order_info, order_items \
                       where status = 'Ready' and  order_items.order_id = order_info.order_id and todel = current_date")
    for items in lst:
            print(tabulate(items, headers=['Order ID', 'Quantity', 'Status', 'Order Date', 'Delivery Day']))
    r = input("Press any key to continue!")


def complete_order(conn):
    order_in = input("Enter order id: ")
    order_inf = query(conn, f"select order_info.order_id, email, item_id, quantity, status, user_id, torcv, todel\
                            from order_info, order_items \
                            where order_info.order_id = order_items.order_id and order_info.order_id = '{order_in}'")
    for items in order_inf:
        for item in items:
            if item[4] == 'Ready':
                print("The Order is already done, you can not change it anymore")
                return
            else:
                print("------------------------------------")
                print(f"Order ID: {item[0]}")
                print(f"Customer's Email: {item[1]}")
                print(f"Item ID: {item[2]}")
                print(f"Quantity: {item[3]}")
                print(f"Status: {item[4]}")
                print(f"User ID: {item[5]}")
                print(f"Order Day: {item[6]}")
                print(f"Delivery Day: {item[7]}")
                print("------------------------------------")
    print("Confirm change order?(y/n): ")
    cf = input()
    if cf == 'n':
        print("Cancel!")
    if cf == 'y':
        insert(conn, f"UPDATE order_items SET status = 'Ready' WHERE order_id = '{order_in}'")
        print("Complete")
    r = input("Press ENTER to continue!")


def show_order(conn):
    order_inf = query(conn, "select order_info.order_id, email, item_id, quantity, status, user_id, torcv, todel\
                            from order_info, order_items \
                            where order_info.order_id = order_items.order_id")
    print("----------------------------------------------------")
    print("---------------------ORDER INFO---------------------")

    for items in order_inf:
        print(tabulate(items, headers=['Order Id', 'Email', 'Item ID', 'Quantity',
                                       'Status', 'User ID', 'Order Date', 'Deliver Date']))


def show_employee_info(conn, user_id):
    empl_info = query(conn, f"select user_id, user_name, designation, status from management where user_id = '{user_id}'")
    for items in empl_info:
        for item in items:
            print("------------------------------------")
            print(f"Id: {item[0]}")
            print(f"Name: {item[1]}")
            print(f"Designation: {item[2]}")
            print(f"Status: {item[3]}")
            print("------------------------------------")
            r = input("Press any key to continue!")


def show_info_customer(conn, email):
    lst = query(conn, f"select email, fname, lname, phone, area, town from customer_info where email = '{email}';")
    for items in lst:
        for item in items:
            print("------------------------------------")
            print(f"Email: {item[0]}")
            print(f"First Name: {item[1]}")
            print(f"Last Name: {item[2]}")
            print(f"Phone number: {item[3]}")
            print(f"Area: {item[4]}")
            print(f"Town: {item[5]}")
            print("------------------------------------")
            r = input("Press ENTER to continue!")


def show_old_order(conn, email):
    lst = query(conn, f"select email, item_name, quantity, torcv as order_date\
                        from order_info oi, order_items ot, menu n\
                        where oi.order_id = ot.order_id and ot.item_id = n.item_id\
                            and email = '{email}'")
    # print(lst)
    if lst == [[]]:
        print("You haven't order yet!\n")
    else:
        for items in lst:
            print(tabulate(items, headers=['Email', 'Item Name', 'Quantity', 'Order date']))
            print('\n')
        r = input("Press ENTER to continue!")


def order(conn, username):
    menu = query(conn, "select item_id, item_name, description, price, catagory\
                        from menu\
                        where status = 'Available'")
    item_ids = []
    item_names = []
    prices = []
    for items in menu:
        print(tabulate(items, headers=['ID','Name', 'Description', 'Price', 'Category']))
        print('\n')
        for item in items:
            item_ids.append(item[0])
            item_names.append(item[1])
            prices.append(item[3])
    first_order_id = int((((query(conn, "select max(order_id) from order_info"))[0])[0])[0])
    while 1:
        item_id = input("Select your choice: ")
        while item_id not in item_ids:
            item_id = input("Wrong! Select your choice again: ")

        quantity = input("Quantity: ")
        while quantity.isdigit() is False:
            quantity = input("Wrong! Quantity: ")

        todel = input("Choose day you want to receive! (MM-DD)")
        todel = '2021-' + todel
        order_id_max = int((((query(conn, "select max(order_id) from order_info"))[0])[0])[0])

        order_id_next = order_id_max + 1
        try:
            a = insert(conn, f"insert into order_info values('{order_id_next}','{username}','{date.today()}','{todel}')")
        except Exception as e:
            print(e)
        try:
            user_id = query(conn, "select user_id\
                        from management\
                        where status != 'Blkd' and user_id in (\
                            select user_id\
                            from order_items\
                            where status = 'Pending'\
                            group by(user_id)\
                            order by(count(*))\
                            limit 1)")[0][0][0]
            # print(user_id)
            a = insert(conn, f" insert into order_items \
                                values('{order_id_next}','{item_id}',{quantity}, 'Pending','{user_id}')")
        except Exception as e:
            print(e)

        select = input("Do want to continue order? (y/n): ")
        if select == 'n':
            break
        else:
            continue
    export_bill(conn, username, first_order_id)
    r = input("Press ENTER to continue!")


def export_bill(conn, username, first_order_id):
    lst = query(conn, f"	select ot.order_id, email, item_name , quantity, quantity * price as price, ot.status\
                            from order_items as ot, order_info as oi, menu as m\
                            where ot.order_id = oi.order_id and email = '{username}'\
                                    and torcv <= '{date.today()}' and '{date.today()}' <= todel\
                                    and ot.item_id = m.item_id and ot.order_id > '{first_order_id}'\
                                    and ot.status != 'Cancel'")
    all_amount = 0
    for items in lst:
        print(tabulate(items, headers=['Order_id', 'Email', 'Name', 'Quantity', 'Price', 'Status']))
        for item in items:
            aaaa = item[4].replace('₫', '')
            all_amount = all_amount + float(aaaa)
    print(f"Total: {all_amount}")


def check_present_order(conn, username):
    export_bill(conn, username, 0)

    if input("Do you want to change?(y/n) :") == 'y':
        print("You only cancel order which status is Pending")
        cancel_id = input("Enter your cancel id: ")
        insert(conn, f" update order_items \
                        set status = 'Cancel'\
                        where order_id = '{cancel_id}'")

        check_present_order(conn, username)
    else:
        return


def main():
    conn = connect_to_db('res', 'postgres', 'admin', 'localhost')
    login(conn)
    disconnect_to_db(conn)


if __name__ == '__main__':
    main()