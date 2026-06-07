from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import random
from time import strptime
from datetime import datetime
import mysql.connector
from tkinter import messagebox

class Details_Staff:
    def __init__(self, root):
        self.root=root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")

        #=======================variables================
        self.employee_id=StringVar()
        x=random.randint(1000,9999)
        self.employee_id.set(str(x))

        self.var_employee_name=StringVar()
        self.var_job=StringVar()
        self.var_department=StringVar()
        self.var_date_of_join=StringVar()
        self.var_mobile=StringVar()
        self.var_email=StringVar()
        self.var_shift=StringVar()
        self.var_address=StringVar()
        self.var_salary=StringVar()


        # ======================title=====================
        lbl_title=Label(self.root,text="SAFF DETAILS",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=0,width=1295,height=50)

        # ======================logo=====================
        img2=Image.open(r"D:\hotel management system\hotel images\hotel logo.webp")
        img2=img2.resize((100,40),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg2=Label(self.root,image=self.photoimg2,bd=0,relief=RIDGE)
        lblimg2.place(x=5,y=2,width=100,height=40)

        # ======================label_frame=====================
        label_frame_left=LabelFrame(self.root,bd=2,relief=RIDGE,text="Staff Details",padx=2,font=("times new roman",12,"bold"))
        label_frame_left.place(x=5,y=50,width=425,height=490)

        # ======================labels and entries=====================
        #employee id
        lbl_employee_id=Label(label_frame_left,text="Employee Id:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_employee_id.grid(row=0,column=0,sticky=W)

        entry_employee_id=ttk.Entry(label_frame_left,width=22,textvariable=self.employee_id,font=("arial",13,"bold"),state="readonly")
        entry_employee_id.grid(row=0,column=1)

        #employee name
        cname=Label(label_frame_left,text="Employee Name:",font=("arial",12,"bold"),padx=2,pady=6)
        cname.grid(row=1,column=0,sticky=W)

        txt_cname=ttk.Entry(label_frame_left,width=22,textvariable=self.var_employee_name,font=("arial",13,"bold"))
        txt_cname.grid(row=1,column=1)

        #job
        lbl_mname=Label(label_frame_left,text="Job:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_mname.grid(row=2,column=0,sticky=W)

        txt_mname=ttk.Entry(label_frame_left,width=22,textvariable=self.var_job,font=("arial",13,"bold"))
        txt_mname.grid(row=2,column=1)

        #department
        lbl_department=Label(label_frame_left,text="Department:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_department.grid(row=3,column=0,sticky=W)

        combo_department=ttk.Combobox(label_frame_left,textvariable=self.var_department,font=("arial",12,"bold"),width=20,state="readonly")
        combo_department["value"]=("Kitchen","Maintenance","Security","Front Office","Sales and Marketing")
        combo_department.current(0)
        combo_department.grid(row=3,column=1)

        #Date of join
        lbl_date_0f_join=Label(label_frame_left,text="Date Of Join:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_date_0f_join.grid(row=4,column=0,sticky=W)

        txt_date_0f_join=ttk.Entry(label_frame_left,width=22,textvariable=self.var_date_of_join,font=("arial",13,"bold"))
        txt_date_0f_join.grid(row=4,column=1)

        #mobile
        lbl_mobile=Label(label_frame_left,text="Mobile No.:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_mobile.grid(row=5,column=0,sticky=W)

        txt_mobile=ttk.Entry(label_frame_left,width=22,textvariable=self.var_mobile,font=("arial",13,"bold"))
        txt_mobile.grid(row=5,column=1)

        #email
        lbl_email=Label(label_frame_left,text="Email:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_email.grid(row=6,column=0,sticky=W)

        txt_email=ttk.Entry(label_frame_left,width=22,textvariable=self.var_email,font=("arial",13,"bold"))
        txt_email.grid(row=6,column=1)

        #shift
        lbl_shift=Label(label_frame_left,text="Shift:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_shift.grid(row=7,column=0,sticky=W)

        combo_shift=ttk.Combobox(label_frame_left,textvariable=self.var_shift,font=("arial",12,"bold"),width=20,state="readonly")
        combo_shift["value"]=("Morning","Day","Night")
        combo_shift.current(0)
        combo_shift.grid(row=7,column=1)

        #address
        lbl_address=Label(label_frame_left,text="Address:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_address.grid(row=8,column=0,sticky=W)

        txt_address=ttk.Entry(label_frame_left,width=22,textvariable=self.var_address,font=("arial",13,"bold"))
        txt_address.grid(row=8,column=1)

        #salary
        lbl_address=Label(label_frame_left,text="Salary:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_address.grid(row=9,column=0,sticky=W)

        txt_address=ttk.Entry(label_frame_left,width=22,textvariable=self.var_salary,font=("arial",13,"bold"))
        txt_address.grid(row=9,column=1)

        #===============Buttons==================
        btn_frame=Frame(label_frame_left,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=400,width=412,height=40)

        btn_add=Button(btn_frame,text="Add",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.add_button)
        btn_add.grid(row=0,column=0,padx=1)

        btn_update=Button(btn_frame,text="Update",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.update)
        btn_update.grid(row=0,column=1,padx=1)

        btn_delete=Button(btn_frame,text="Delete",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.deleted)
        btn_delete.grid(row=0,column=2,padx=1)

        btn_reset=Button(btn_frame,text="Reset",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.reset)
        btn_reset.grid(row=0,column=3,padx=1)

        #===============table frame search system==================

        table_frame1=LabelFrame(self.root,bd=2,relief=RIDGE,text="View Details And Search System",padx=2,font=("times new roman",12,"bold"))
        table_frame1.place(x=435,y=50,width=860,height=490)

        lbl_searchby=Label(table_frame1,text="Search By:",font=("arial",12,"bold"),bg="pink",fg="green")
        lbl_searchby.grid(row=0,column=0,sticky=W,padx=2)

        self.search_var=StringVar() 

        combo_search=ttk.Combobox(table_frame1,textvariable=self.search_var,font=("arial",12,"bold"),width=20,state="readonly")
        combo_search["value"]=("Employee Id","Mobile No.")
        combo_search.current(0)
        combo_search.grid(row=0,column=1,padx=2)

        self.txt_search=StringVar() 

        txt_search=ttk.Entry(table_frame1,width=22,text=self.txt_search,font=("arial",13,"bold"))
        txt_search.grid(row=0,column=2,padx=2)

        btn_search=Button(table_frame1,text="Search",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.search)
        btn_search.grid(row=0,column=3,padx=1)

        btn_show_all=Button(table_frame1,text="Show All",command=self.fetch_data,font=("arial",12,"bold"),bg="black",fg="gold",width=9)
        btn_show_all.grid(row=0,column=4,padx=1)


        #===============Show data table==================
        details_table=Frame(table_frame1,bd=2,relief=RIDGE)   
        details_table.place(x=0,y=50,width=860,height=350)

        scrollbar_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        scrollbar_y=ttk.Scrollbar(details_table,orient=VERTICAL) 

        self.employee_details_table=ttk.Treeview(details_table,column=("Employee Id","Employee Name","Job","Department","Date Of Join","Mobile No.","Email","Shift","Address","Salary"),xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)

        scrollbar_x.pack(side=BOTTOM,fill=X)
        scrollbar_y.pack(side=RIGHT,fill=Y)
        scrollbar_x.config(command=self.employee_details_table.xview)
        scrollbar_y.config(command=self.employee_details_table.yview)

        self.employee_details_table.heading("Employee Id",text="Employee Id")
        self.employee_details_table.heading("Employee Name",text="Employee Name")
        self.employee_details_table.heading("Job",text="Job")
        self.employee_details_table.heading("Department",text="Department")
        self.employee_details_table.heading("Date Of Join",text="Date Of Join")
        self.employee_details_table.heading("Mobile No.",text="Mobile No.")
        self.employee_details_table.heading("Email",text="Email")
        self.employee_details_table.heading("Shift",text="Shift")
        self.employee_details_table.heading("Address",text="Address")
        self.employee_details_table.heading("Salary",text="Salary")


        self.employee_details_table["show"]="headings"

        self.employee_details_table.column("Employee Id",width=100)
        self.employee_details_table.column("Employee Name",width=100)
        self.employee_details_table.column("Job",width=100)
        self.employee_details_table.column("Department",width=100)
        self.employee_details_table.column("Date Of Join",width=100)
        self.employee_details_table.column("Mobile No.",width=100)
        self.employee_details_table.column("Email",width=100)
        self.employee_details_table.column("Shift",width=100)
        self.employee_details_table.column("Address",width=100)
        self.employee_details_table.column("Salary",width=100)


        self.employee_details_table.pack(fill=BOTH,expand=1)
        self.employee_details_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()


    def search(self):
        connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
        my_cursor=connection.cursor() 

        query = "SELECT * FROM staff WHERE `" + str(self.search_var.get()) + "` LIKE %s"
        value = ('%' + self.txt_search.get() + '%',)
        my_cursor.execute(query, value)
        rows = my_cursor.fetchall()
        if len(rows)!=0:
            self.employee_details_table.delete(*self.employee_details_table.get_children())
            for i in rows:
                self.employee_details_table.insert("",END,values=i) 
            connection.commit()
        connection.close()

    def fetch_data(self):
                connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
                my_cursor=connection.cursor()
                my_cursor.execute("select * from staff")
                rows=my_cursor.fetchall()
                if len(rows)!=0:
                    self.employee_details_table.delete(*self.employee_details_table.get_children())
                    for i in rows:
                        self.employee_details_table.insert("",END,values=i)
                    connection.commit()
                connection.close()

    def get_cursor(self,event=""):
        cursor_row=self.employee_details_table.focus()
        content=self.employee_details_table.item(cursor_row)
        row=content["values"]

        self.employee_id.set(row[0]),
        self.var_employee_name.set(row[1]),
        self.var_job.set(row[2]),
        self.var_department.set(row[3]),
        self.var_date_of_join.set(row[4]),
        self.var_mobile.set(row[5]),
        self.var_email.set(row[6]),
        self.var_shift.set(row[7]),
        self.var_address.set(row[8]),
        self.var_salary.set(row[9])

    def add_button(self):
        if self.var_mobile.get()=="" or self.var_employee_name.get()=="" or self.var_date_of_join.get()=="":
            messagebox.showerror("Error","Employee Name,Mobile and date of join must be filled.",parent=self.root)
        else:
            try:
                connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
                my_cursor=connection.cursor()
                my_cursor.execute("insert into staff values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                self.employee_id.get(),
                                                                                self.var_employee_name.get(),
                                                                                self.var_job.get(),
                                                                                self.var_department.get(),
                                                                                self.var_date_of_join.get(),
                                                                                self.var_mobile.get(),
                                                                                self.var_email.get(),
                                                                                self.var_shift.get(),
                                                                                self.var_address.get(),
                                                                                self.var_salary.get()
                                                                                                ))
                connection.commit()
                self.fetch_data()
                connection.close()
                messagebox.showinfo("Success","Staff has been added",parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning",f"Something went wrong:{str(es)}",parent=self.root)

    def update(self):
        if self.var_mobile.get()=="":
            messagebox.error("Error","Please enter mobile number.",parent=self.root)
        else:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor()
            my_cursor.execute("update staff set `Employee Name`=%s,`Job`=%s,Department=%s,`Date Of Join`=%s,`Mobile No.`=%s,Email=%s,Shift=%s,Address=%s,Salary=%s where `Employee Id`=%s",(
                                                                            self.var_employee_name.get(),
                                                                            self.var_job.get(),
                                                                            self.var_department.get(),
                                                                            self.var_date_of_join.get(),
                                                                            self.var_mobile.get(),
                                                                            self.var_email.get(),
                                                                            self.var_shift.get(),
                                                                            self.var_address.get(),
                                                                            self.var_salary.get(),
                                                                            self.employee_id.get()
                                                                        ))
            connection.commit()
            self.fetch_data()
            connection.close()
            messagebox.showinfo("Update","Employee details has been successfully updated..",parent=self.root)

    def deleted(self):
        deleted=messagebox.askyesno("Hotel Management System","Do you want to delete this customer?",parent=self.root)
        if deleted>0:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor() 
            query="delete from staff where `Employee Id`=%s"
            value=(self.employee_id.get(),)  # pass value as a tupule
            my_cursor.execute(query,value)           
        else:
            if not deleted:
                return
        connection.commit()
        self.fetch_data()
        connection.close()

    def reset(self):
        self.var_employee_name.set("")
        self.var_job.set("")
        self.var_date_of_join.set("")
        self.var_mobile.set("")
        self.var_email.set("")
        self.var_address.set("")
        self.var_salary.set("")

        x=random.randint(1000,9999)
        self.employee_id.set(str(x))






if __name__=="__main__":
    root=Tk()
    obj=Details_Staff(root)
    root.mainloop()