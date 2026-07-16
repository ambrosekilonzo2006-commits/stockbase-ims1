import sys
class InventoryApp:
    def __init__(self,repository,role="cashier"):
        self.rep=repository
        self.role=role

                 
    def login(self):
        username=input("username: ").strip().lower()
        password=input("password: ").strip()
        self.role=self.rep.verify_user(username,password)
        return self.role is not None
    def cashier_menu(self):
        print("\n ----CASHIER DASHBOARD----")
        
        print("1.VIEW INVENTORY" )
        print("2.ADD SALE" )
        print("3.UPDATE PASSWORD" )
        print("4.LOG OUT")
        return int(input("option: ").strip())
    
        
    

    def manager_menu(self):
        print("Welcome to your Inventory Management System" )
        print("What do you wish to do?" )
        print("1.ADD PRODUCTS" )
        print("2.DELETE PRODUCTS" )
        print("3.UPDATE PRODUCTS" )
        print("4.VIEW PRODUCTS" )
        print("5.ADD SALE" )
        print("6.VIEW PROFIT REPORT" )
        print("7.MANAGE STAFF" )
        print("8.CHANGE PASSWORD" )
        print("9.EXIT")
        return int(input("please choose using the numbers: "))
    def action(self):
        if not self.login(): return

        while True:
        
            if self.role=="manager":
                choice=self.manager_menu()
                self.handle_manager_choice(choice)

            else:  
                choice=self.cashier_menu()
                self.handle_cashier_choice(choice)
            
                    
            
    def handle_manager_choice(self,choice):
                if choice ==1:
                    try:

                        name=input("please input the name of the product : ").strip().lower()
                        stock=int(input("stock quantity in numerical form : ").strip())
                        price=float(input("product price in  decimal form : ").strip())
                        buying_price=float(input("buying price : ").strip())
                        if  self.rep.add_product(name,stock,price,buying_price):
                            print(f"{name} has been added successfully")
                        else:
                            print("ERROR! Failed to add product")
                    except Exception as e:
                        print(f"an error occurred{e}")
                elif choice ==2:
                    try:
                        name1=input("please input the name of the product you wish to delete : ")
                        finding=self.rep.get_product(name1)
                        if finding:
                            approval=input(f"Are you sure you wish to delete {name1}(y/n)").strip().lower()
                            if approval=="y":
                                self.rep.delete_product(name1)
                                print(f"{name1} successfully deleted")
                            else:
                                print("deletion not approved")
                    except Exception as e:
                        print(f"an error occurred{e}")    
                elif choice ==3:
                    try:
                        name2=input("product_name of what to be updated: ").strip().lower()
                        print("do you wish to:" \
                      "1.update product name" \
                      "2.update stock" \
                      "3.update price" \
                      "4.update buying price" \
                      "5.update all values")
                        action_updater=int(input("input your action here : ").strip())
                        if action_updater==1:
                            new_name=input("new product_name : ").strip().lower()
                            finding2=self.rep.get_product(name2)
                            if finding2:
                                print(finding2)
                                approval1=input(f"{name2} are you sure you want to change it to{new_name}(y/n)").strip().lower()
                                if approval1=="y":
                                    self.rep.update_prod_name(name2,new_name)
                                    print("process successfull")
                                else:
                                    print("Update process cancelled")
                        elif action_updater==2:
                            new_stock=int(input("new_stock_price in numerical form: ").strip())
                            finding3=self.rep.get_product(name2)
                            if finding3:
                                print(finding3)
                                approval3=input("are you sure you want update stock (y/n)").strip().lower()
                                if approval3=="y":
                                    self.rep.update_stock(name2,new_stock)
                                    print("process successfull")
                                else :
                                    print("process cancelled")
                        elif action_updater==3:
                            new_price=float(input("new price : ").strip())
                            finding4=self.rep.get_product(name2)
                            if finding4:
                                print(finding4)
                                approval4=input("do you wish to proceed(y/n)").strip().lower()
                                if approval4 =="y":
                                    self.rep.update_price(name2,new_price)
                                    print("process successfull")
                                else:
                                    print("process cancelled")
                        elif action_updater==4:
                            new_buying_price=float(input("new buying price: ").strip())
                            finding6=self.rep.get_product(name2)
                            if finding6:
                                print(finding6)
                                approve=input("Do you wish to proceed ?(y/n)")
                                if approve=="y":
                                    self.rep.update_bp(name2,new_buying_price)
                                    print("process sucessfull")
                                else:
                                    print("Process cancelled")    

                        elif action_updater==5:
                            new_price1=float(input("new price in decimal places :").strip())
                            new_stock1=int(input("new stock : ").strip())
                            new_bp=float(input("new buying price : ").strip())
                            finding5=self.rep.get_product(name2)
                            if finding5:
                                print(finding5)
                                approval5=input("do you wish to proceed?(y/n)").strip()
                                if approval5=="y":
                                    self.rep.update_all(name2,new_price1,new_stock1,new_bp)
                                else:
                                    print("process cancelled")
                    except Exception as e:
                        print(f"{e}")
                elif choice==4:
                    try:
                        print("Do you wish:" \
                            "1.whole table" \
                            "2.certain product")
                        find=int(input(" input you choice here in numerical form : ").strip())
                        if find==1:
                            find2=self.rep.get_whole_table()
                            print(find2)
                        if find==2:
                            product_name=input("product name: ").strip().lower()
                            find3=self.rep.get_product(product_name)
                            print(find3)
                        else:
                            print("process cancelled")
                    except Exception as e:
                        print(f"{e}")
                elif choice ==5:
                    try:
                        question=input("Is the customer willing to give out his name(y/n")
                        if question =="y":
                            names=input("Enter his name : ")
                        
                        elif question=="n":
                            names="anonymous"
                            
                        else:
                            print("process failed")    
                        phone=int(input("input the number in form of 07xx: ").strip())
                        product_bought=input("product name : ").strip().lower()
                        quantity=int(input("quantity").strip())
                        if self.rep.record_sale(names,phone,product_bought,quantity):
                            print("sale recorded successfully")
                        else:
                            print("Error ! sale record failed")
                    except Exception as e:
                        print(f"{e}")        
                elif choice==6:
                    try:
                        report=self.rep.get_profit_report()
                        print("\n----PROFIT REPORT---")
                        print(f"{'Product' : <15} | {'stock': <6} |{'Profit/unit' :<12} | {'Total Profit': <12}")
                        print("-" * 55)
                        for row in report:
                            print(f"{row[0]: <15} |{row[1]:<6} | {row[2] : <12.2f} |{row[3]:<12.2f}")
                    except Exception as e:
                        print(f"error generating report:{e}") 
                elif choice==7:
                    try:
                        manage=int(input("do you wish to " \
                        "1.ALTER ROLE" \
                        "2.ADD USER" \
                        "3.DELETE USER").strip())
                        if manage==1:
                            user_name=input("username: ").strip().lower()
                            finder=self.rep.get_user(user_name)
                            if finder:
                                print(finder)
                                new_role=input("new role(manager/cashier) : ")
                                self.rep.update_user_role(user_name,new_role)
                                print("process successfull")
                            else:
                                print("process cancelled")
                        if manage==2:
                            new_user_name=input("username: ").strip().lower()
                            id=int(input("id no: ").strip())
                            password=input("give the user to put the password :")
                            role=input("manager input role(manager/cashier): ").strip().lower()
                            self.rep.add_user(id,new_user_name,password,role)
                            print("process_complete")
                        elif manage==3:
                            user=input("username : ").strip().lower()
                            finder1=self.rep.get_user(user)
                            if finder1:
                                print(finder1)
                                approved=input("Are you sure you want to delete(y/n)?: ").strip().lower()
                                if approved=="y":
                                    self.rep.del_user(user)
                                else:
                                    print("process cancelled")
                    except Exception as e:
                        print(f" error occured as {e}")   
                elif choice==8:
                    try:

                       new_find=input("username: ") 
                       initial_password=input("initial_password")
                       process=self.rep.verify_user(new_find,initial_password)
                       if process:
                           new_password=input("new_password : ")
                           self.rep.change_password(new_find,new_password)
                           print("process complete")
                       else:
                           print("process cancelled")
                    except Exception as e:
                        print(f"error occured{e}")                                         




                elif choice==9:
                    print("Exiting system .Goodbye")
                    sys.exit()
                else:
                    print("wrong input")  
    def handle_cashier_choice(self,choice):
                if choice==1:
                    try:
                        print("Do you wish:" \
                            "1.whole table" \
                            "2.certain product")
                        find=int(input(" input you choice here in numerical form : ").strip())
                        if find==1:
                            find2=self.rep.get_whole_table()
                            print(find2)
                        if find==2:
                            product_name=input("product name: ").strip().lower()
                            find3=self.rep.get_product(product_name)
                            print(find3)
                        else:
                            print("process cancelled")
                    except Exception as e:
                        print(f"{e}")
                elif choice ==2:
                    try:
                        question=input("Is the customer willing to give out his name(y/n")
                        if question =="y":
                            names=input("Enter his name : ")
                        
                        elif question=="n":
                            names="anonymous"
                            
                        else:
                            print("process failed")    
                        phone=int(input("input the number in form of 07xx: ").strip())
                        product_bought=input("product name : ").strip().lower()
                        quantity=int(input("quantity").strip())
                        if self.rep.record_sale(names,phone,product_bought,quantity):
                            print("sale recorded successfully")
                        else:
                            print("Error ! sale record failed")
                    except Exception as e:
                        print(f"{e}")
                elif choice==3:
                    try:

                       new_find=input("username: ") 
                       initial_password=input("initial_password")
                       process=self.rep.verify_user(new_find,initial_password)
                       if process:
                           new_password=input("new_password : ")
                           self.rep.change_password(new_find,new_password)
                           print("process complete")
                       else:
                           print("process cancelled")
                    except Exception as e:
                        print(f"error occured{e}")                   
                elif choice==4:
                    print("Exiting system .Goodbye")
                    sys.exit() 
                else:
                    print("wrong input!")  
if __name__=="__main__":
        from repository import DatabaseRepository
        
        db_config={
            "host":"localhost",
            "database":"sales_records",
            "user":input("username: ").strip(),
            "password":input("postgres_password: ")
            }
        try:
            rep=DatabaseRepository(db_config)
            app=InventoryApp(rep)
            app.action()
        except Exception as e: 
            print(f"System failed to start: {e}")       

                                       

                        
                          
                



                                            
                












                   




                       













