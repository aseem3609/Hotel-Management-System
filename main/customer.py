from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import random
import mysql.connector
from tkinter import messagebox


class Cust_win:
    def __init__(self, root):
        self.root=root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")

        #=======================variables================
        self.var_ref=StringVar()
        x=random.randint(1000,9999)
        self.var_ref.set(str(x))

        self.var_cust_name=StringVar()
        self.var_father=StringVar()
        self.var_gender=StringVar()
        self.var_post=StringVar()
        self.var_mobile=StringVar()
        self.var_email=StringVar()
        self.var_nationality=StringVar()
        self.var_address=StringVar()
        self.var_id_proof=StringVar()
        self.var_id_number=StringVar()


        # ======================title=====================
        lbl_title=Label(self.root,text="ADD CUSTOMER DETAILS",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=0,width=1295,height=50)

        # ======================logo=====================
        img2=Image.open(r"D:\hotel management system\hotel images\hotel logo.webp")
        img2=img2.resize((100,40),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg2=Label(self.root,image=self.photoimg2,bd=0,relief=RIDGE)
        lblimg2.place(x=5,y=2,width=100,height=40)

        # ======================label_frame=====================
        label_frame_left=LabelFrame(self.root,bd=2,relief=RIDGE,text="Customer Details",padx=2,font=("times new roman",12,"bold"))
        label_frame_left.place(x=5,y=50,width=425,height=490)

        # ======================labels and entries=====================
        #customer reference
        lbl_cust_ref=Label(label_frame_left,text="Customer Reference",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_cust_ref.grid(row=0,column=0,sticky=W)

        entry_ref=ttk.Entry(label_frame_left,width=22,textvariable=self.var_ref,font=("arial",13,"bold"),state="readonly")
        entry_ref.grid(row=0,column=1)

        #customer name
        cname=Label(label_frame_left,text="Customer Name:",font=("arial",12,"bold"),padx=2,pady=6)
        cname.grid(row=1,column=0,sticky=W)

        txt_cname=ttk.Entry(label_frame_left,width=22,textvariable=self.var_cust_name,font=("arial",13,"bold"))
        txt_cname.grid(row=1,column=1)

        #father name
        lbl_mname=Label(label_frame_left,text="Father's name:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_mname.grid(row=2,column=0,sticky=W)

        txt_mname=ttk.Entry(label_frame_left,width=22,textvariable=self.var_father,font=("arial",13,"bold"))
        txt_mname.grid(row=2,column=1)

        #gender combo_box
        label_gender=Label(label_frame_left,text="Gender: ",font=("arial",12,"bold"),padx=2,pady=6)
        label_gender.grid(row=3,column=0,sticky=W)

        combo_gender=ttk.Combobox(label_frame_left,textvariable=self.var_gender,font=("arial",12,"bold"),width=20,state="readonly")
        combo_gender["value"]=("Male","Female","Other")
        combo_gender.current(0)
        combo_gender.grid(row=3,column=1)


        #post_code
        lbl_postcode=Label(label_frame_left,text="PostCode:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_postcode.grid(row=4,column=0,sticky=W)

        txt_postcode=ttk.Entry(label_frame_left,width=22,textvariable=self.var_post,font=("arial",13,"bold"))
        txt_postcode.grid(row=4,column=1)

        #mobile number
        lbl_mobile=Label(label_frame_left,text="Mobile:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_mobile.grid(row=5,column=0,sticky=W)

        txt_mobile=ttk.Entry(label_frame_left,width=22,textvariable=self.var_mobile,font=("arial",13,"bold"))
        txt_mobile.grid(row=5,column=1)

        #email
        lbl_email=Label(label_frame_left,text="Email:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_email.grid(row=6,column=0,sticky=W)

        txt_email=ttk.Entry(label_frame_left,width=22,textvariable=self.var_email,font=("arial",13,"bold"))
        txt_email.grid(row=6,column=1)

        #nationality
        lbl_nationality=Label(label_frame_left,text="Nationality:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_nationality.grid(row=7,column=0,sticky=W)

        combo_nationality=ttk.Combobox(label_frame_left,textvariable=self.var_nationality,font=("arial",12,"bold"),width=20,state="readonly")
        combo_nationality["value"]=("Nepali","Indian","American","British","Other")
        combo_nationality.current(0)
        combo_nationality.grid(row=7,column=1)


        #idproof type combobox
        lbl_id_proof=Label(label_frame_left,text="Id Proof Type:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_id_proof.grid(row=8,column=0,sticky=W)

        combo_id=ttk.Combobox(label_frame_left,font=("arial",12,"bold"),textvariable=self.var_id_proof,width=20,state="readonly")
        combo_id["value"]=("Nationality card","Driving License","Passport")
        combo_id.current(0)
        combo_id.grid(row=8,column=1)

        #id number
        lbl_id_number=Label(label_frame_left,text="Id Number:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_id_number.grid(row=9,column=0,sticky=W)

        txt_id_number=ttk.Entry(label_frame_left,width=22,textvariable=self.var_id_number,font=("arial",13,"bold"))
        txt_id_number.grid(row=9,column=1)

        #address
        lbl_address=Label(label_frame_left,text="Address:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_address.grid(row=10,column=0,sticky=W)

        txt_address=ttk.Entry(label_frame_left,width=22,textvariable=self.var_address,font=("arial",13,"bold"))
        txt_address.grid(row=10,column=1)

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

        table_frame=LabelFrame(self.root,bd=2,relief=RIDGE,text="View Details And Search System",padx=2,font=("times new roman",12,"bold"))
        table_frame.place(x=435,y=50,width=860,height=490)

        lbl_searchby=Label(table_frame,text="Search By:",font=("arial",12,"bold"),bg="pink",fg="green")
        lbl_searchby.grid(row=0,column=0,sticky=W,padx=2)

        self.search_var=StringVar() # combo_search input is stored in the variable

        combo_search=ttk.Combobox(table_frame,textvariable=self.search_var,font=("arial",12,"bold"),width=20,state="readonly")
        combo_search["value"]=("Mobile","Ref no.")
        combo_search.current(0)
        combo_search.grid(row=0,column=1,padx=2)

        self.txt_search=StringVar() # text search input

        txt_search=ttk.Entry(table_frame,width=22,text=self.txt_search,font=("arial",13,"bold"))
        txt_search.grid(row=0,column=2,padx=2)

        btn_search=Button(table_frame,text="Search",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.search)
        btn_search.grid(row=0,column=3,padx=1)

        btn_show_all=Button(table_frame,text="Show All",command=self.fetch_data,font=("arial",12,"bold"),bg="black",fg="gold",width=9)
        btn_show_all.grid(row=0,column=4,padx=1)

        #===============Show data table==================
        details_table=Frame(table_frame,bd=2,relief=RIDGE)
        details_table.place(x=0,y=50,width=860,height=350)

        scrollbar_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        scrollbar_y=ttk.Scrollbar(details_table,orient=VERTICAL)

        self.cust_details_table=ttk.Treeview(details_table,column=("Ref no.","Name","Father's name","Gender","Post","Mobile","Email","Nationality","Idproof","Idnumber","Address"),xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)

        scrollbar_x.pack(side=BOTTOM,fill=X)
        scrollbar_y.pack(side=RIGHT,fill=Y)
        scrollbar_x.config(command=self.cust_details_table.xview)
        scrollbar_y.config(command=self.cust_details_table.yview)

        self.cust_details_table.heading("Ref no.",text="Ref no.")
        self.cust_details_table.heading("Name",text="Name")
        self.cust_details_table.heading("Father's name",text="Father's name")
        self.cust_details_table.heading("Gender",text="Gender")
        self.cust_details_table.heading("Post",text="Post")
        self.cust_details_table.heading("Mobile",text="Mobile")
        self.cust_details_table.heading("Email",text="Email")
        self.cust_details_table.heading("Nationality",text="Nationality")
        self.cust_details_table.heading("Idproof",text="Idproof")
        self.cust_details_table.heading("Idnumber",text="Idnumber")
        self.cust_details_table.heading("Address",text="Address")

        self.cust_details_table["show"]="headings"

        self.cust_details_table.column("Ref no.",width=100)
        self.cust_details_table.column("Name",width=100)
        self.cust_details_table.column("Father's name",width=100)
        self.cust_details_table.column("Gender",width=100)
        self.cust_details_table.column("Post",width=100)
        self.cust_details_table.column("Mobile",width=100)
        self.cust_details_table.column("Email",width=100)
        self.cust_details_table.column("Nationality",width=100)
        self.cust_details_table.column("Idproof",width=100)
        self.cust_details_table.column("Idnumber",width=100)
        self.cust_details_table.column("Address",width=100)

        self.cust_details_table.pack(fill=BOTH,expand=1)
        self.cust_details_table.bind("<ButtonRelease-1>",self.get_cursor)# right click on table activates get_cursor
        self.fetch_data()


    def add_button(self):
        if self.var_mobile.get()=="" or self.var_cust_name.get()=="" or self.var_id_proof.get()=="":
            messagebox.showerror("Error","Name,Mobile and id proof must be filled.",parent=self.root)
        else:
            try:
                connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
                my_cursor=connection.cursor()
                my_cursor.execute("insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                self.var_ref.get(),
                                                                                self.var_cust_name.get(),
                                                                                self.var_father.get(),
                                                                                self.var_gender.get(),
                                                                                self.var_post.get(),
                                                                                self.var_mobile.get(),
                                                                                self.var_email.get(),
                                                                                self.var_nationality.get(),
                                                                                self.var_id_proof.get(),
                                                                                self.var_id_number.get(),
                                                                                self.var_address.get(),
                                                                                                ))
                connection.commit()
                self.fetch_data()
                connection.close()
                messagebox.showinfo("Success","Customer has been added",parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning",f"Something went wrong:{str(es)}",parent=self.root)

    def fetch_data(self):
                connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
                my_cursor=connection.cursor()
                my_cursor.execute("select * from customer")
                rows=my_cursor.fetchall()
                if len(rows)!=0:
                    # Clear any existing rows in the treeview widget
                    self.cust_details_table.delete(*self.cust_details_table.get_children())
                    for i in rows:
                        self.cust_details_table.insert("",END,values=i)
                    connection.commit()
                connection.close()

    # getting data on clicking at the table
    def get_cursor(self,event=""):
        cursor_row=self.cust_details_table.focus()
        content=self.cust_details_table.item(cursor_row)
        row=content["values"]

        self.var_ref.set(row[0]),
        self.var_cust_name.set(row[1]),
        self.var_father.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_post.set(row[4]),
        self.var_mobile.set(row[5]),
        self.var_email.set(row[6]),
        self.var_nationality.set(row[7]),
        self.var_id_proof.set(row[8]),
        self.var_id_number.set(row[9]),
        self.var_address.set(row[10])
    
    def update(self):
        if self.var_mobile.get()=="":
            messagebox.error("Error","Please enter mobile number.",parent=self.root)
        else:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor()
            my_cursor.execute("update customer set Name=%s,`Father's name`=%s,Gender=%s,Post=%s,Mobile=%s,Email=%s,Nationality=%s,Idproof=%s,Idnumber=%s,Address=%s where `Ref no.`=%s",(
                                                                            self.var_cust_name.get(),
                                                                            self.var_father.get(),
                                                                            self.var_gender.get(),
                                                                            self.var_post.get(),
                                                                            self.var_mobile.get(),
                                                                            self.var_email.get(),
                                                                            self.var_nationality.get(),
                                                                            self.var_id_proof.get(),
                                                                            self.var_id_number.get(),
                                                                            self.var_address.get(),
                                                                            self.var_ref.get()
                                                                        ))
            connection.commit()
            self.fetch_data()
            connection.close()
            messagebox.showinfo("Update","Customer details has been successfully updated..",parent=self.root)

    def deleted(self):
        deleted=messagebox.askyesno("Hotel Management System","Do you want to delete this customer?",parent=self.root)
        if deleted>0:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor() 
            query="delete from customer where `Ref no.`=%s"
            value=(self.var_ref.get(),)  # pass value as a tupule
            my_cursor.execute(query,value)           
        else:
            if not deleted:
                return
        connection.commit()
        self.fetch_data()
        connection.close()
    
    def reset(self):
        #self.var_ref.set(""),
        self.var_cust_name.set(""),
        self.var_father.set(""),
        #self.var_gender.set(""),
        self.var_post.set(""),
        self.var_mobile.set(""),
        self.var_email.set(""),
        #self.var_nationality.set(""),
        #self.var_id_proof.set(""),
        self.var_id_number.set(""),
        self.var_address.set("") 

        x=random.randint(1000,9999)
        self.var_ref.set(str(x))

    def search(self):
        connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
        my_cursor=connection.cursor() 

        query = "SELECT * FROM customer WHERE `" + str(self.search_var.get()) + "` LIKE %s"
        value = ('%' + self.txt_search.get() + '%',)  # Wrap in a tuple for parameterized query
        my_cursor.execute(query, value)
        rows = my_cursor.fetchall()
        if len(rows)!=0:
            self.cust_details_table.delete(*self.cust_details_table.get_children())
            for i in rows:
                self.cust_details_table.insert("",END,values=i) 
            connection.commit()
        connection.close()

        
if __name__=="__main__":
    root=Tk()
    obj=Cust_win(root)
    root.mainloop()