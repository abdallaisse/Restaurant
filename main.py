# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:03:12 2020

@author: abdillahi Isse #101149847
"""

'''
This is an online restuarant project (online store), first it will display menu and ask user how many
orders he want to make in 1 order, if he want just 1 item from menu it will give him 1 input for the
order number and 1 input for the quantity, and if he want 50 different orders it will give him 50 
inputs. Then it will generate receipt for him and finally it will store that receipt in a csv and
database files.

'''


# importing modules


from contextlib import closing
from object import Display
import time, csv, sqlite3, sys
print("------Welcome to DOMA Burgers----- \n")


# menu function that display each item on the menu using the display_items method in the Display class
def display_menu():
    print("MAIN MENU\n")
    print("Here are the dishes available now\n")
    i = 1
    for item in dishes:
        print(str(i)+". " + item.item_name, item.item_price, sep=' : $')
        i += 1

# this function stores the receipt into the sqlite database


def receipt_db():
    global db_file, conn, c, sql
    db_file = "receipts.db"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

#    c.execute("""CREATE TABLE receipts(
#                    order_date interger NOT NULL,
#                    num_of_items interger NOT NULL,
#                    subtotal real NOT NULL,
#                    discounts real NOT NULL,
#                    total real NOT NULL
#                    )""")
#    conn.commit()
    with closing(conn.cursor()) as c:
        sql = '''INSERT INTO receipts (order_date, num_of_orders, num_of_items, subtotal, discounts, total) 
            VALUES (?, ?, ?, ?, ?,?)'''
        c.execute(sql, (time.ctime(), num_of_orders,
                  num_of_items, subtotal, discounts, total))
        conn.commit()

# this function stores the receipt into the csv file


def receipt_csv():
    with open('receipts.csv', 'a')as csv_file:
        #        csv_writer = csv.writer(csv_file)
        #        field_names = ["Order Date","Quantity","Discount","Total"]
        #        writer = csv.DictWriter(csv_file, fieldnames = field_names)
        #        writer.writeheader()
        lines = [[time.ctime(), num_of_orders, num_of_items,
                  subtotal, discounts, total]]
        for row in lines:
            max_len = len(row)
            count = 0
            for colmn in row:
                count += 1
                comma = ","
                if count == max_len:
                    comma = ""
                csv_file.write(str(colmn) + comma)
            csv_file.write("\n")

# this function displays the order details before the final receipt
# this function is helpful if user ordered different items in a one order


def prereceipt():
    global order_name, order_quantity, order_price
    order_name = print("\nItem Name:\t", item_name)
    order_quantity = print("Quantity: \t", int(quantity))
    order_price = print("Price =\t", "$", price, " * ",
                        int(quantity), " = $", price * int(quantity))

# this function generates the final receipt


def receipt():
    print("---------------------------------------")
    print("\n\tReciept\n",
          time.ctime(), "\n"
          "Orders: ", *order_dishes.keys(),
          "\nSubTotal = $", subtotal,
          "\nTotal Quantity = ", num_of_items,
          "\nNumber of Orders = ", num_of_orders,
          "\nTotal Discount = $", round(discounts, 2),
          "\nTotal = $", round(total, 2),
          "\nThank You & See You Again\n",
          "---------------------------------------\n")


'''
I used the main function to do most of the work from menu to calculating orders 
generating receipts

'''


def main():
    global dishes

# I used the Display Class that I created in the object module to add items into the menu

    dishes = []
    dishes.append(Display("HAWAIIAN BURGER", 7))
    dishes.append(Display("CHICKEN BURGER", 9))
    dishes.append(Display("FISH BURGER",  6))
    dishes.append(Display("MEXICAN BURGER", 6.5))
    dishes.append(Display("DOUBLE BURGER", 8))
    dishes.append(Display("DOUBLE CHEESE", 5.5))
    display_menu()
    '''
    this while loop is the most important element in this project, it ask users
    to make their orders and calculate for them, and give them the receipt
    '''

    while True:
        global item_name, num_of_items, discount, price, total, order_num, num_of_orders
        global quantity, pretotal, subtotal, discounts, order_dishes
        order_dishes = {}
        order_num = 0
        quantity_num = 0
        quantity = 0
        num_of_items = 0
        order_no = 0
        discounts = 0
        subtotal = 0
        total = 0

        try:

            # num_of_orders is designed for the users who want to order different items in 1 order

            num_of_orders = int(
                input("How many Orders You Want to Make Today: \t "))
        except ValueError:
            print("You didn't enter a number!!!. Please try again.\n")
            time.sleep(3)
            display_menu()
        except Exception as e:
            print("Error: %s" % e)
            time.sleep(2)
            display_menu()

        '''
        this for loop checks how many orders user want to order, so if he want to order 5 different
        items in 1 order it will give him 5 inputs, then generate pre receipt for every items he 
        order and finally generates the final receipt which has the 5 items total
        '''
        for n in range(num_of_orders):
            try:
                order_no += 1
                order = int(input("Order No "+str(order_no)+": please Enter the number of the "
                                  + "Dish from the Menu: \t"))
                if order == 1:
                    item_name = "HAWAIIAN BURGER"
                    price = 7
                elif order == 2:
                    item_name = "CHICKEN BURGER"
                    price = 9
                elif order == 3:
                    item_name = "FISH BURGER"
                    price = 6
                elif order == 4:
                    item_name = "MEXICAN BURGER"
                    price = 6.5
                elif order == 5:
                    item_name = "DOUBLE BURGER"
                    price = 8
                elif order == 6:
                    item_name = "DOUBLE CHEESE"
                    price = 5.5
                elif order < 1 or order > 6:
                    price = 0
                    print("invalid choice!!")
                    break
            except ValueError:
                print("You didn't enter a number!!!. Please try again.\n")
                break
            except Exception as e:
                print("Error: %s" % e)
                break

            try:
                quantity = int(input("Please Enter the quantity: \t"))
                if quantity < 1:
                    print("The Quantity must be 1 and higher!!!!!!")
                    break
            except ValueError:
                print("You didn't enter a number!!!. Please try again.\n")
                break
            except Exception as e:
                print("Error: %s" % e)
                break
            order_dishes[item_name] = quantity
            order_num += int(order)
            quantity_num += int(quantity)

            num_of_items = quantity_num

            # pretotal is the total price for 1 item even if user order 5 of that item
            pretotal = (price * int(quantity))
            # subtotal is the total for multiple items in 1 order before the discount
            subtotal += pretotal

            # this following if else statement gives the user discount
            if num_of_items <= 3:
                discount = 0
            elif subtotal >= 40 and subtotal <= 60 or num_of_items > 3 and num_of_items <= 7:
                discount = subtotal * 0.05
            elif subtotal > 60 and subtotal <= 90 or num_of_items > 7 and num_of_items <= 15:
                discount = subtotal * 0.1
            elif subtotal > 90 and subtotal <= 120 or num_of_items > 15 and num_of_items <= 30:
                discount = subtotal * 0.15
            elif subtotal > 120 and subtotal <= 150 or num_of_items > 30 and num_of_items <= 50:
                discount = subtotal * 0.20
            elif subtotal > 150 or num_of_items > 50:
                discount = subtotal * 0.25

            # after user order his item, he will get the pre receipt
            if num_of_orders > 1:
                prereceipt()

            # discounts is the total of discounts for example if there is more than 1 item in 1 order
            discounts += discount
            # total is the final price after discounts
            total = subtotal - discounts
        '''
        after user finishs his order the receipt will be generated
        then the menu will display agian
        '''
        if num_of_items >= 1:
            receipt()
        else:
            display_menu()

        # the next two statements will store the receipt in csv and database file
        try:
            receipt_csv()
        except IOError:
            print("Cannot open input files.")
        except Exception as e:
            print("Error: %s" % e)

        try:
            receipt_db()
        except IOError:
            print("Cannot open input files.")
        except Exception as e:
            print("Error: %s" % e)


if __name__ == "__main__":
    main()

conn.close()
