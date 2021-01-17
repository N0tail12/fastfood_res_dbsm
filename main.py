import datetime
import psycopg2
from tabulate import tabulate
from datetime import date


def connect_to_db(DB_NAME, DB_USER, DB_PASS, DB_HOST):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    return conn


# def connect_to_db(url):
#     conn = psycopg2.connect(url)
#     return conn


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
                if empl[4] != 'Blockd':
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


def search_by_field(conn):
    lst = query(conn, f"select email, fname, lname, pass, phone, area, town, status\
                        from customer_info\
                        order by email\
                        limit 1;")
    for items in lst:
        print(tabulate(items, headers=['email', 'fname', 'lname', 'pass', 'phone', 'area', 'town', 'status']))
    head = ['email', 'fname', 'lname', 'pass', 'phone', 'area', 'town', 'status']
    select = ''
    while select not in head:
        select = input("Choose a field to search: ")
        if select in head:
            keyword = input("Input keyword: ")
            _lst = query(conn, f"   select email, fname, lname, pass, phone, area, town, status\
                                    from customer_info\
                                    where {select} = '{keyword}'\
                                    order by {select}")
            for lst_item in _lst:
                if not lst_item:
                    print("No record macth your search!")
                else:
                    print("Your search: ")
                    print(tabulate(lst_item, headers=['email', 'fname', 'lname', 'pass', 'phone', 'area', 'town', 'status']))
                r = input("\nDo you want to search another? Press ENTER to continue or type EXIT to exit: ")
                if r != 'EXIT':
                    select = ''
                    continue
        else:
            print("Your field is invalid!")
            print("Choose another field to search: ")


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
    menu = query(conn, "select item_id, item_name, description, price, category\
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
                        where status != 'Blockd' and user_id in (\
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


def is_day(string):
    format = "%Y-%m-%d"
    i = 1
    try:
        datetime.datetime.strptime(string, format)
    except ValueError:
        i = 0
        print("This is the incorrect date string format. It should be YYYY-MM-DD")
    return i


def sale_by_day(conn):
    day_start = day_end = ''
    i = 0
    while i == 0:
        day_start = input("Choose day start: (YYYY-MM-DD) ")
        i = is_day(day_start)
    i = 0
    while i == 0:
        day_end = input("Choose day end: (YYYY-MM-DD) ")
        i = is_day(day_end)

    sale = query(conn, f"select oi.todel, sum(me.price * ot.quantity) as total\
                        from menu as me, order_items  as ot, order_info as oi\
                        where me.item_id = ot.item_id and ot.order_id = oi.order_id\
                            and todel between '{day_start}' and '{day_end}' and ot.status != 'Cancel'\
                        group by(todel)\
                        order by(total) desc")
    for items in sale:
        print(tabulate(items, headers=['Date', 'Sale']))
    averge = query(conn, f"with bill_month as (\
                            select oi.todel, sum(me.price * ot.quantity)as total\
                            from menu as me, order_items  as ot, order_info as oi\
                            where me.item_id = ot.item_id and ot.order_id = oi.order_id\
                                and todel between '{day_start}' and '{day_end}' and ot.status != 'Cancel'\
                            group by(todel)\
                            )\
                        select sum(total)/count(*) AS averge\
                        from bill_month;")
    for items in averge:
        for item in items:
            print("------------------")
            print(f"Total: {item[0]}")
    r = input("Press ENTER to continue!")


def most_cancel_area(conn):
    lst = query(conn, f"select town, count(*) as num_cancel\
                        from order_info oi, order_items ot, customer_info c\
                        where oi.order_id = ot.order_id and ot.status = 'Cancel' and oi.email = c.email\
                        group by(town)\
                        order by(num_cancel) desc\
                        limit 3")
    for items in lst:
        print(tabulate(items, headers=['Town', 'Number cancel times']))
    r = input("Press ENTER to continue!")


def num_dish_sold(conn):
    lst = query(conn, f"select town, item_name, sum(quantity) as total_num\
                        from menu m, customer_info c, order_items ot, order_info oi\
                        where c.email = oi.email and ot.order_id = oi.order_id \
                            and ot.item_id = m.item_id and ot.status != 'Cancel'\
                        group by(town, item_name)\
                        order by(town, item_name)")
    for items in lst:
        print(tabulate(items, headers=['Town', 'Name', 'Total']))
    r = input("Press ENTER to continue!")


def town_have_most_cus(conn):
    lst = query(conn, f"select town, count(email)\
                        from customer_info \
                        group by town\
                        order by count(email) desc\
                        limit 3")
    for items in lst:
        print(tabulate(items, headers=['Town', 'Total customer']))
    r = input("Press ENTER to continue!")


def the_most_order_dish(conn):
    lst = query(conn, f"select menu.item_id,menu.item_name , sum(quantity) as total_quantity\
                        from order_items, menu\
                        where order_items.item_id = menu.item_id\
                        group by(menu.item_id)\
                        order by(total_quantity) desc")
    for items in lst:
        print(tabulate(items, headers=['ID', 'Name', 'Total']))
    r = input("Press ENTER to continue!")


def show_order_by_field(conn):
    lst = query(conn, f"select ot.order_id, item_name, quantity, email, ot.status, ot.user_id\
                        from order_items ot, order_info oi, menu m\
                        where ot.order_id = oi.order_id and ot.item_id = m.item_id\
                        limit 1")
    for items in lst:
        print(tabulate(items, headers=['ot.order_id', 'item_name', 'quantity', 'email', 'ot.status', 'ot.user_id']))
    head = ['ot.order_id', 'item_name', 'quantity', 'email', 'ot.status', 'ot.user_id']
    select = ''
    while select not in head:
        select = input("Choose a field to search: ")
        if select in head:
            keyword = input("Input keyword: ")
            _lst = query(conn, f"   select ot.order_id, item_name, quantity, email, ot.status, ot.user_id\
                                    from order_items ot, order_info oi, menu m\
                                    where ot.order_id = oi.order_id and ot.item_id = m.item_id\
                                        and {select} = '{keyword}'")
            for lst_item in _lst:
                if not lst_item:
                    print("No record macth your search!")
                else:
                    print("Your search: ")
                    print(tabulate(lst_item,
                                   headers=['ot.order_id', 'item_name', 'quantity', 'email', 'ot.status', 'ot.user_id']))
                r = input("\nDo you want to search another? Enter EXIT to exit\n")
                if r != 'EXIT':
                    select = ''
                    continue
        else:
            print("Your field is invalid!")
            print("Choose another field to search: ")


def show_manager_menu():
    print("-----------MANAGER MENU----------\n")
    print("1. Database Management")
    print("2. Sales Management")
    print("3. Overview of sales areas")
    print("4. Exit\n")


def show_database_manager_menu():
    print("-----------Database Management----------\n")
    print("1. Customer Information Management")
    print("2. Personnel Management")
    print("3. Show Order Information")
    print("4. Edit Menu")
    print("5. Exit\n")


def top_10_cus(conn):
    lst = query(conn, "select email, sum(quantity) as total_num from order_info as oi, order_items as ot\
                            where oi.order_id = ot.order_id and ot.status != 'Cancel'\
                            group by(email)\
                            order by(total_num) desc\
                            limit 10")
    for items in lst:
        print(tabulate(items, headers=['Email', 'Quantity']))
    r = input("Press Enter to continue")


def did_not_order(conn):
    lst = query(conn, "select c.email, c.fname||' '||c.lname as Full_Name\
                        from customer_info as c\
                        where c.email not in (\
                            select email\
                            from menu as me, order_items  as ot, order_info as oi\
                            where me.item_id = ot.item_id and ot.order_id = oi.order_id\
                                and extract(year from torcv) = extract(year from current_date) and \
                                extract(month from torcv) = extract(month from current_date)  and ot.status != 'Cancel'\
                        )")
    for items in lst:
        print(tabulate(items, headers=['Email', 'Name']))
    r = input("Press Enter to continue")


def more_than_700(conn):
    lst = query(conn, "select customer_info.fname||' '||customer_info.lname, customer_info.email, town, area, phone, a.total\
                        from order_info,customer_info,\
                        (select order_items.item_id,order_id, quantity*price as total\
                        from order_items,menu where order_items.item_id = menu.item_id) as a\
                        where a.order_id = order_info.order_id and\
                         order_info.email = customer_info.email and a.total > '700000'")
    for items in lst:
        print(tabulate(items, headers=['Name', 'Email', 'Town', 'Area', 'Phone', 'Total']))
    r = input("Press Enter to continue")


def familiar_cus(conn):
    lst = query(conn, "select count(o.email), cus.email,cus.fname||' '||cus.lname\
                        from order_info o, customer_info cus\
                        where o.email = cus.email \
                        group by o.email,cus.email\
                        having count(o.email)>10 and max(torcv) > '2020-12-31'")
    for items in lst:
        print(tabulate(items, headers=['Number Order', 'Email', 'Name']))
    r = input("Press Enter to continue")


def order_today(conn):
    lst = query(conn, "select cus.fname||' '||cus.lname, cus.email, menu.item_name, order_info.order_id\
                        from customer_info cus, order_info, order_items, menu\
                        where torcv = current_date and cus.email = order_info.email\
                         and order_info.order_id = order_items.order_id and order_items.item_id = menu.item_id")
    for items in lst:
        print(tabulate(items, headers=['Name', 'Email', 'Items', 'Order ID']))
    r = input("Press Enter to continue")


def show_cus_info(conn):
    choice = 99
    while choice != 7:
        print("--------Customer Information Management-------\n")
        print("1.Search customers by field")
        print("2.Top 10 customers with the most order")
        print("3.Customers did not order anything this month ")
        print("4.Customers with total amount more than 700 ")
        print("5.Customers that order in today")
        print("6.List of familiar customers")
        print("7.Exit")
        choice = int(input("Enter your choice: "))
        while choice < 1 or choice > 7:
            print("Invalid selection!")
            choice = input("Enter your choice: ")
        if choice == 1:
            search_by_field(conn)
            r = input("Press Enter to continue")
        elif choice == 2:
            top_10_cus(conn)
        elif choice == 3:
            did_not_order(conn)
        elif choice == 4:
            more_than_700(conn)
        elif choice == 5:
            order_today(conn)
        elif choice == 6:
            familiar_cus(conn)


def show_orderview_area_menu():
    print("-----------Overview of sales areas----------\n")
    print("1. Most cancel area")
    print("2. Number of dishes sold in each area")
    print("3. Top 3 towns have the most customers")
    print("4. Exit\n")


def list_emp(conn):
    lst = query(conn, "select user_id, user_name, designation from management")
    for items in lst:
        print(tabulate(items, headers=['ID', 'Name', 'Designation']))
    r = input("Press Enter to continue")


def add_emp(conn):
    lst = query(conn, "select user_id, user_name, status, designation from management")
    print("Please enter the information")
    user_id = input("Enter user_id: ")
    count = 0
    while count == 0:
        for items in lst:
            for item in items:
                if user_id == item[0]:
                    print("The user_id is already exit, please try another user_id")
                    user_id = input("Enter user_id: ")
        if count == 0:
            count += 1
            continue
    pass_word = input("Enter the password: ")
    user_name = input("Enter Name: ")
    # user_id = input("Enter the user id for login: ")
    designation = input("Designation: ")
    while designation != 'Employee' and designation != "Cook" and designation != 'Manager' :
        print("Designation is not suitable, please Enter correctly")
        designation = input("Designation: ")
    insert(conn, f"insert into management values ('{user_id}','{pass_word}','{user_name}','Active','{designation}')")
    r = input("Press Enter to continue")


def change_info(conn):
    lst = query(conn,  "select user_id, user_name, status, designation from management")
    user_id = input("Enter user_id: ")
    count = 0
    while count == 0:
        for items in lst:
            for item in items:
                if user_id == item[0]:
                    print("Found!")
                    count += 1
        if count == 0:
            print("Can't find!")
            user_id = input("Enter user_id: ")
    print("You can only change two fields: status and designation")
    print("Type correctly the field that you want to change")
    field_change = input("Enter the field that you want to change: ")
    values = ''
    while field_change != 'status' and field_change != 'designation':
        print("Your field you just entered is wrong.Please try again")
        field_change = input("Enter the field that you want to change: ")
    if field_change == 'status':
        values = input("Enter the value that you want to change(Active/Block): ")
        while values != 'Active' and values != 'Block':
            print("Incorrect value, please try again")
            values = input("Enter the value that you want to change(Active/Block): ")
    else:
        values = input("Enter the value that you want to change(Employee/Cook/Manager): ")
        while values != 'Employee' and values != 'Cook' and values != 'Manager':
            print("Incorrect value, please try again")
            values = input("Enter the value that you want to change(Employee/Cook/Manager): ")
    insert(conn, f"update management set {field_change} = '{values}' where user_id = '{user_id}'")


def delete_employ(conn):
    lst = query(conn, "select user_id, user_name, status, designation from management")
    user_id = input("Enter user_id: ")
    count = 0
    while count == 0:
        for items in lst:
            for item in items:
                if user_id == item[0]:
                    print("Found!")
                    count += 1
        if count == 0:
            print("Can't find!")
            user_id = input("Enter user_id: ")
    choice = input("Are you sure you want to delete this employee(y/n)?: ")
    while choice != 'y' and choice != 'n':
        print("Please enter your choice again1")
        choice = input("Are you sure you want to delete this employee(y/n)?: ")
    if choice == 'y':
        insert(conn, f"delete from management where user_id = '{user_id}'")
    else:
        print("Cancel!")


def num_order(conn):
    day_start = day_end = ''
    i = 0
    while i == 0:
        day_start = input("Choose day start: (YYYY-MM-DD) ")
        i = is_day(day_start)
    i = 0
    while i == 0:
        day_end = input("Choose day end: (YYYY-MM-DD) ")
        i = is_day(day_end)
    lst = query(conn, f"select ot.user_id, user_name, sum(quantity)\
                        from order_items as ot, management as m, order_info as oi\
                        where ot.status != 'Cancel' and m.user_id = ot.user_id\
                            and ot.order_id = oi.order_id and torcv between '{day_start}' and '{day_end}'\
                        group by (ot.user_id, user_name)")
    for items in lst:
        print(tabulate(items, headers=['User ID', 'Name', 'Sum']))
    r = input("Press ENTER to continue")


def show_emp_management(conn):
    choice = 99
    while choice != 6:
        print("--------Employees Management-------\n")
        print("1.List of employees are now working for restaurant")
        print("2.Add an employees")
        print("3.Change employee's information ")
        print("4.Delete employee")
        print("5.Number of order that each person had done")
        print("6.Exit")
        choice = int(input("Enter your choice: "))
        while choice < 1 or choice > 6:
            print("Invalid selection!")
            choice = input("Enter your choice: ")
        if choice == 1:
            list_emp(conn)
        elif choice == 2:
            add_emp(conn)
        elif choice == 3:
            change_info(conn)
        elif choice == 4:
            delete_employ(conn)
        elif choice == 5:
            num_order(conn)


def menu_funct():
    print("-----------MENU FUNCTION----------\n")
    print("1. Add a dish in to menu")
    print("2. Change a dish in menu")
    print("3. Delete")
    print("4. Exit\n")


def add_dish(conn):
    lst = query(conn, "select item_id from menu")
    print("Please enter the information")
    item_id = input("Enter item_id: ")
    count = 0
    while count == 0:
        for items in lst:
            for item in items:
                if item_id == item[0]:
                    print("The item_id is already exit, please try another item_id")
                    item_id = input("Enter item_id: ")
        if count == 0:
            count += 1
            continue
    item_name = input("Enter name of new food: ")
    description = input("Enter description of new food: ")
    price = float(input("Enter the price: "))
    category = input("Enter category: ")
    status = input("Enter status(Available/UnAvailable): ")
    while status != 'Available' and status != 'UnAvailable':
        print("Please enter again!")
        status = input("Enter status(Available/UnAvailable): ")
    insert(conn,
           f"insert into menu values('{item_id}','{item_name}','{description}','{price}','{category}','{status}', 'datlt132')")
    
    
def change_dish(conn):
    lst = query(conn, "select item_id,item_name, description, price, category, status, user_id from menu")
    item_id = input("Enter item_id: ")
    count = 0
    while count == 0:
        for items in lst:
            for item in items:
                if item_id == item[0]:
                    print("Found!")
                    count += 1
        if count == 0:
            print("Can't find!. Please enter again")
            item_id = input("Enter item_id: ")
    head = ['item_name', 'description', 'price', 'category', 'status']
    select = input("Enter the field you want to change: ")
    while select not in head:
        print("Unavailable field. Please enter again or try another field")
        select = input("Enter the field you want to change: ")
    if select in head:
        values = input("Enter the values: ")
        if select == 'status' and values != 'Available' and values != 'UnAvailable':
            print("Values is not suitable. Only 'Available' or 'UnAvailable' is except!")
            values = input("Enter the values: ")
        insert(conn, f"update menu set {select} = '{values}' where item_id = '{item_id}'")


def delete_dish(conn):
    lst = query(conn, "Select item_id from menu")
    item_id = input("Enter item_id: ")
    count = 0
    while count == 0:
        for items in lst:
            for item in items:
                if item_id == item[0]:
                    print("Found!")
                    count += 1
                    insert(conn, f"delete from menu where item_id = '{item_id}'")
        if count == 0:
            print("Can't find!. Please Enter again")
            item_id = input("Enter item_id: ")


def login(conn):
    username = input("Enter your email or username: ")
    userpass = input("Enter your password: ")
    i = check_account(conn, username, userpass)
    select_1 = select_2 = select_3 = luachon = select_3_ = select_4 = 9,
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
        while select_3 != 4:
            show_manager_menu()
            select_3 = int(input("Enter your choice: "))
            while select_3 < 1 or select_3 > 4:
                print("Invalid selection!")
                select_3 = int(input("Enter your choice: "))
            if select_3 == 1:
                select_3_ = 0
                while select_3_ != 5:
                    show_database_manager_menu()
                    select_3_ = int(input("Enter your choice: "))
                    while select_3_ < 1 or select_3_ > 5:
                        print("Invalid selection!")
                        select_3_ = int(input("Enter your choice: "))
                    if select_3_ == 1:
                        show_cus_info(conn)
                    elif select_3_ == 2:
                        show_emp_management(conn)
                    elif select_3_ == 3:
                        while luachon != 3:
                            print("-----------Order Management----------\n")
                            print("1. Show all order")
                            print("2. The most order dish")
                            print("3. Exit")
                            luachon = int(input("Enter your choice: "))
                            while luachon < 1 or luachon > 5:
                                print("Invalid selection!")
                                luachon = input("Enter your choice: ")
                            if luachon == 1:
                                show_order_by_field(conn)
                            elif luachon == 2:
                                the_most_order_dish(conn)
                    elif select_3_ == 4:
                        while select_4 != 4:
                            menu_funct()
                            select_4 = int(input("Enter your choice: "))
                            while select_4 < 1 or select_4 > 5:
                                print("Invalid selection!")
                                select_4 = int(input("Enter your choice: "))
                            if select_4 == 1:
                                add_dish(conn)
                            elif select_4 == 2:
                                change_dish(conn)
                            elif select_4 == 3:
                                delete_dish(conn)
            elif select_3 == 2:
                print("-----------Sales Management----------\n")
                sale_by_day(conn)
            elif select_3 == 3:
                while select_3_ != 4:
                    show_orderview_area_menu()
                    select_3_ = int(input("Enter your choice: "))
                    while select_3_ < 1 or select_3_ > 5:
                        print("Invalid selection!")
                        select_3_ = input("Enter your choice: ")
                    if select_3_ == 1:
                        most_cancel_area(conn)
                    elif select_3_ == 2:
                        num_dish_sold(conn)
                    elif select_3_ == 3:
                        town_have_most_cus(conn)


def main():
    # conn = connect_to_db("postgres://gecksmtj:8xTHFHDY7Nqu80PT8yv_0OLZi7sA1Uz9@suleiman.db.elephantsql.com:5432/gecksmtj")
    conn = connect_to_db('fastfood_restaurant', 'postgres', 'admin', 'localhost')
    login(conn)
    disconnect_to_db(conn)


if __name__ == '__main__':
    main()