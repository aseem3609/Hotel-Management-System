from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import os
from datetime import datetime
from tkinter import messagebox
from tkcalendar import DateEntry
from fpdf import FPDF
from db import get_connection, ensure_schema, INVOICE_DIR

class Room_Booking:
    def __init__(self, root):
        self.root=root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")

        # Make sure the Status column exists for older databases.
        ensure_schema()

        #=======================variables=================\
        self.var_contact=StringVar()
        self.var_roomtype=StringVar()
        self.var_roomavailable=StringVar()
        self.var_meal=StringVar()
        self.var_no_of_day=StringVar()
        self.var_paidtax=StringVar()
        self.var_actualtotal=StringVar()
        self.var_total=StringVar()
        self.var_status=StringVar()
        # ======================title=====================
        lbl_title=Label(self.root,text="ROOM BOOKING DETAILS",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=0,width=1295,height=50)

        # ======================logo=====================
        img2=Image.open(r"D:\hotel management system\hotel images\hotel logo.webp")
        img2=img2.resize((100,40),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg2=Label(self.root,image=self.photoimg2,bd=0,relief=RIDGE)
        lblimg2.place(x=5,y=2,width=100,height=40)

        # ======================label_frame=====================
        label_frame_left=LabelFrame(self.root,bd=2,relief=RIDGE,text="Room Booking Details",padx=2,font=("times new roman",12,"bold"))
        label_frame_left.place(x=5,y=50,width=425,height=490)

        # ======================labels and entries=====================
        #customer contact
        lbl_cust_contact=Label(label_frame_left,text="Customer Contact",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_cust_contact.grid(row=0,column=0,sticky=W)

        entry_contact=ttk.Entry(label_frame_left,width=17,textvariable=self.var_contact,font=("arial",13,"bold"))
        entry_contact.grid(row=0,column=1,sticky=W)

        ## fetch data button
        btn_fetch_data=Button(label_frame_left,text="Fetch Data",font=("arial",8,"bold"),bg="black",fg="gold",width=8,command=self.fetch_contact)
        btn_fetch_data.place(x=310,y=4)

        #check in date
        check_in_date=Label(label_frame_left,text="Chect In Date:",font=("arial",12,"bold"),padx=2,pady=6)
        check_in_date.grid(row=1,column=0,sticky=W)

        self.check_in_date=DateEntry(label_frame_left,width=20,font=("arial",12,"bold"),date_pattern="yyyy/mm/dd",state="readonly")
        self.check_in_date.grid(row=1,column=1)

        #check out date
        check_out_date=Label(label_frame_left,text="Check Out Date:",font=("arial",12,"bold"),padx=2,pady=6)
        check_out_date.grid(row=2,column=0,sticky=W)

        self.check_out_date=DateEntry(label_frame_left,width=20,font=("arial",12,"bold"),date_pattern="yyyy/mm/dd",state="readonly")
        self.check_out_date.grid(row=2,column=1)

        #room type
        lbl_room_type=Label(label_frame_left,text="Room Type:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_room_type.grid(row=3,column=0,sticky=W)

        connection=get_connection()
        my_cursor=connection.cursor()
        my_cursor.execute("select distinct `Room Type` from details")
        ide=[r[0] for r in my_cursor.fetchall()]
        connection.close()

        self.combo_room_type=ttk.Combobox(label_frame_left,font=("arial",12,"bold"),textvariable=self.var_roomtype,width=20,state="readonly")
        self.combo_room_type["value"]=ide if ide else ("Single","Double","Luxury")
        self.combo_room_type.current(0)
        self.combo_room_type.grid(row=3,column=1,padx=2)
        self.combo_room_type.bind("<<ComboboxSelected>>",lambda e:self.refresh_available_rooms())

        #available room
        lbl_available_room=Label(label_frame_left,text="Available Room:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_available_room.grid(row=4,column=0,sticky=W)

        self.combo_room_no=ttk.Combobox(label_frame_left,font=("arial",12,"bold"),textvariable=self.var_roomavailable,width=20,state="readonly")
        self.combo_room_no.grid(row=4,column=1,padx=2)

        btn_check_avail=Button(label_frame_left,text="Check Availability",font=("arial",9,"bold"),bg="black",fg="gold",command=self.refresh_available_rooms)
        btn_check_avail.grid(row=4,column=1,sticky=E,padx=2)

        #meal
        lbl_meal=Label(label_frame_left,text="Meal:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_meal.grid(row=5,column=0,sticky=W)

        combo_meal=ttk.Combobox(label_frame_left,font=("arial",12,"bold"),textvariable=self.var_meal,width=20,state="readonly")
        combo_meal["value"]=("Breakfast","Lunch","Dinner")
        combo_meal.current(0)
        combo_meal.grid(row=5,column=1,padx=2)

        #no of days
        lbl_no_of_days=Label(label_frame_left,text="No Of Days:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_no_of_days.grid(row=6,column=0,sticky=W)

        entry_no_of_days=ttk.Entry(label_frame_left,width=22,textvariable=self.var_no_of_day,font=("arial",13,"bold"))
        entry_no_of_days.grid(row=6,column=1)

        #sub total
        lbl_sub_total=Label(label_frame_left,text="Sub Total:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_sub_total.grid(row=7,column=0,sticky=W)

        entry_sub_total=ttk.Entry(label_frame_left,width=22,textvariable=self.var_actualtotal,font=("arial",13,"bold"))
        entry_sub_total.grid(row=7,column=1)

        #paid tax
        lbl_paid_tax=Label(label_frame_left,text="Paid Tax:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_paid_tax.grid(row=8,column=0,sticky=W)

        entry_paid_tax=ttk.Entry(label_frame_left,width=22,textvariable=self.var_paidtax,font=("arial",13,"bold"))
        entry_paid_tax.grid(row=8,column=1)


        #total cost
        lbl_total_cost=Label(label_frame_left,text="Total Cost:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_total_cost.grid(row=9,column=0,sticky=W)

        entry_total_cost=ttk.Entry(label_frame_left,width=22,textvariable=self.var_total,font=("arial",13,"bold"))
        entry_total_cost.grid(row=9,column=1)

        #status
        lbl_status=Label(label_frame_left,text="Status:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_status.grid(row=10,column=0,sticky=W)

        combo_status=ttk.Combobox(label_frame_left,font=("arial",12,"bold"),textvariable=self.var_status,width=20,state="readonly")
        combo_status["value"]=("Checked-in","Checked-out","Cancelled")
        combo_status.current(0)
        combo_status.grid(row=10,column=1,padx=2)

        # bill button
        btn_bill=Button(label_frame_left,text="Bill",font=("arial",11,"bold"),bg="black",fg="gold",width=8,command=self.total)
        btn_bill.grid(row=11,column=0,padx=1,sticky=W)

        # invoice button
        btn_invoice=Button(label_frame_left,text="Print Invoice",font=("arial",11,"bold"),bg="black",fg="gold",width=12,command=self.generate_invoice)
        btn_invoice.grid(row=11,column=1,padx=1,sticky=W)

        #===============Buttons==================
        btn_frame=Frame(label_frame_left,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=400,width=412,height=40)

        btn_add=Button(btn_frame,text="Add",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.add_button)
        btn_add.grid(row=0,column=0,padx=1)

        btn_update=Button(btn_frame,text="Update",command=self.update,font=("arial",12,"bold"),bg="black",fg="gold",width=9)
        btn_update.grid(row=0,column=1,padx=1)

        btn_delete=Button(btn_frame,text="Delete",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.deleted)
        btn_delete.grid(row=0,column=2,padx=1)

        btn_reset=Button(btn_frame,text="Reset",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.reset)
        btn_reset.grid(row=0,column=3,padx=1)

        #==============right side image===========================
        imgs=Image.open(r"D:\hotel management system\hotel images\bedroom.jpg")
        imgs=imgs.resize((400,300),Image.Resampling.LANCZOS)
        self.photoimgs=ImageTk.PhotoImage(imgs)

        lblimgs=Label(self.root,image=self.photoimgs,bd=0,relief=RIDGE)
        lblimgs.place(x=580,y=55,width=880,height=300)

        #===============table frame search system==================

        table_frame=LabelFrame(self.root,bd=2,relief=RIDGE,text="View Details And Search System",padx=2,font=("times new roman",12,"bold"))
        table_frame.place(x=435,y=280,width=860,height=260)

        lbl_searchby=Label(table_frame,text="Search By:",font=("arial",12,"bold"),bg="pink",fg="green")
        lbl_searchby.grid(row=0,column=0,sticky=W,padx=2)

        self.search_var=StringVar()

        combo_search=ttk.Combobox(table_frame,textvariable=self.search_var,font=("arial",12,"bold"),width=20,state="readonly")
        combo_search["value"]=("Customer Contact","Room No")
        combo_search.current(0)
        combo_search.grid(row=0,column=1,padx=2)

        self.txt_search=StringVar()

        txt_search=ttk.Entry(table_frame,width=22,text=self.txt_search,font=("arial",13,"bold"))
        txt_search.grid(row=0,column=2,padx=2)

        btn_search=Button(table_frame,text="Search",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.search)
        btn_search.grid(row=0,column=3,padx=1)

        btn_show_all=Button(table_frame,text="Show All",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.fetch_data)
        btn_show_all.grid(row=0,column=4,padx=1)

#===============Show data table==================
        details_table=Frame(table_frame,bd=2,relief=RIDGE)
        details_table.place(x=0,y=50,width=860,height=180)

        scrollbar_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        scrollbar_y=ttk.Scrollbar(details_table,orient=VERTICAL)

        self.room_table=ttk.Treeview(details_table,column=("Customer Contact","Checkin date","Checkout date","Room Type","Room No","Meal","No of Days","Status"),xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)

        scrollbar_x.pack(side=BOTTOM,fill=X)
        scrollbar_y.pack(side=RIGHT,fill=Y)
        scrollbar_x.config(command=self.room_table.xview)
        scrollbar_y.config(command=self.room_table.yview)
        self.room_table.heading("Customer Contact",text="Customer Contact")
        self.room_table.heading("Checkin date",text="Checkin date")
        self.room_table.heading("Checkout date",text="Checkout date")
        self.room_table.heading("Room Type",text="Room Type")
        self.room_table.heading("Room No",text="Room No")
        self.room_table.heading("Meal",text="Meal")
        self.room_table.heading("No of Days",text="No of Days")
        self.room_table.heading("Status",text="Status")

        self.room_table["show"]="headings"

        self.room_table.column("Customer Contact",width=100)
        self.room_table.column("Checkin date",width=100)
        self.room_table.column("Checkout date",width=100)
        self.room_table.column("Room Type",width=100)
        self.room_table.column("Room No",width=100)
        self.room_table.column("Meal",width=100)
        self.room_table.column("No of Days",width=100)
        self.room_table.column("Status",width=100)
        self.room_table.pack(fill=BOTH,expand=1)

        self.room_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
        self.refresh_available_rooms()

    # -------------------- date helpers --------------------
    def _checkin_str(self):
        return self.check_in_date.get_date().strftime("%Y/%m/%d")

    def _checkout_str(self):
        return self.check_out_date.get_date().strftime("%Y/%m/%d")

    def refresh_available_rooms(self):
        """Populate the available-room combobox with rooms of the selected type
        that are NOT already booked for the chosen date range."""
        try:
            checkin=self._checkin_str()
            checkout=self._checkout_str()
            connection=get_connection()
            my_cursor=connection.cursor()
            # Rooms of the chosen type, excluding rooms with an active booking
            # whose dates overlap the requested range.
            query=(
                "SELECT `Room No.` FROM details WHERE `Room Type`=%s "
                "AND `Room No.` NOT IN ("
                "  SELECT `Room No` FROM room "
                "  WHERE Status='Checked-in' "
                "  AND `Checkin date` < %s AND `Checkout date` > %s"
                ")"
            )
            my_cursor.execute(query,(self.var_roomtype.get(),checkout,checkin))
            rooms=[r[0] for r in my_cursor.fetchall()]
            connection.close()

            self.combo_room_no["value"]=rooms
            if rooms:
                self.combo_room_no.current(0)
            else:
                self.var_roomavailable.set("")
        except Exception as es:
            messagebox.showwarning("Warning",f"Could not load availability:{str(es)}",parent=self.root)

    def _is_room_booked(self,room_no,checkin,checkout,exclude_contact=None):
        """Return True if room_no has an overlapping active booking."""
        connection=get_connection()
        my_cursor=connection.cursor()
        query=(
            "SELECT COUNT(*) FROM room WHERE `Room No`=%s AND Status='Checked-in' "
            "AND `Checkin date` < %s AND `Checkout date` > %s"
        )
        params=[room_no,checkout,checkin]
        if exclude_contact is not None:
            query+=" AND `Customer Contact`<>%s"
            params.append(exclude_contact)
        my_cursor.execute(query,tuple(params))
        count=my_cursor.fetchone()[0]
        connection.close()
        return count>0

    def add_button(self):
        if self.var_contact.get()=="" or self.var_roomavailable.get()=="":
            messagebox.showerror("Error","Customer contact and an available room must be selected.",parent=self.root)
            return

        checkin=self.check_in_date.get_date()
        checkout=self.check_out_date.get_date()
        if checkout<=checkin:
            messagebox.showerror("Error","Check-out date must be after the check-in date.",parent=self.root)
            return

        checkin_s=self._checkin_str()
        checkout_s=self._checkout_str()

        if self._is_room_booked(self.var_roomavailable.get(),checkin_s,checkout_s):
            messagebox.showerror("Error","This room is already booked for the selected dates.",parent=self.root)
            self.refresh_available_rooms()
            return

        try:
            connection=get_connection()
            my_cursor=connection.cursor()
            my_cursor.execute("insert into room values(%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                            self.var_contact.get(),
                                                                            checkin_s,
                                                                            checkout_s,
                                                                            self.var_roomtype.get(),
                                                                            self.var_roomavailable.get(),
                                                                            self.var_meal.get(),
                                                                            self.var_no_of_day.get(),
                                                                            self.var_status.get() or "Checked-in"
                                                                                            ))
            connection.commit()
            self.fetch_data()
            connection.close()
            self.refresh_available_rooms()
            messagebox.showinfo("Success","Room has been booked",parent=self.root)
        except Exception as es:
            messagebox.showwarning("Warning",f"Something went wrong:{str(es)}",parent=self.root)

    def fetch_data(self):
                connection=get_connection()
                my_cursor=connection.cursor()
                my_cursor.execute("select * from room")
                rows=my_cursor.fetchall()
                if len(rows)!=0:
                    # Clear any existing rows in the treeview widget
                    self.room_table.delete(*self.room_table.get_children())
                    for i in rows:
                        self.room_table.insert("",END,values=i)
                    connection.commit()
                connection.close()

    def get_cursor(self,event=""):
        cursor_row=self.room_table.focus()
        content=self.room_table.item(cursor_row)
        row=content["values"]
        if not row:
            return

        self.var_contact.set(row[0])
        try:
            self.check_in_date.set_date(datetime.strptime(str(row[1]),"%Y/%m/%d"))
            self.check_out_date.set_date(datetime.strptime(str(row[2]),"%Y/%m/%d"))
        except Exception:
            pass
        self.var_roomtype.set(row[3])
        self.var_roomavailable.set(row[4])
        self.combo_room_no["value"]=(row[4],)
        self.var_meal.set(row[5])
        self.var_no_of_day.set(row[6])
        if len(row)>7:
            self.var_status.set(row[7])

    def update(self):
        if self.var_contact.get()=="":
            messagebox.showerror("Error","Please enter contact number.",parent=self.root)
            return

        checkin=self.check_in_date.get_date()
        checkout=self.check_out_date.get_date()
        if checkout<=checkin:
            messagebox.showerror("Error","Check-out date must be after the check-in date.",parent=self.root)
            return

        checkin_s=self._checkin_str()
        checkout_s=self._checkout_str()

        if self.var_status.get()=="Checked-in" and self._is_room_booked(
            self.var_roomavailable.get(),checkin_s,checkout_s,exclude_contact=self.var_contact.get()):
            messagebox.showerror("Error","This room is already booked for the selected dates.",parent=self.root)
            return

        connection=get_connection()
        my_cursor=connection.cursor()
        my_cursor.execute("update room set `Checkin date`=%s,`Checkout date`=%s,`Room Type`=%s,`Room No`=%s,Meal=%s,`No Of Days`=%s,Status=%s where `Customer Contact`=%s",(
                                                                        checkin_s,
                                                                        checkout_s,
                                                                        self.var_roomtype.get(),
                                                                        self.var_roomavailable.get(),
                                                                        self.var_meal.get(),
                                                                        self.var_no_of_day.get(),
                                                                        self.var_status.get() or "Checked-in",
                                                                        self.var_contact.get()
                                                                    ))
        connection.commit()
        self.fetch_data()
        connection.close()
        self.refresh_available_rooms()
        messagebox.showinfo("Update","Room details has been successfully updated..",parent=self.root)

    def deleted(self):
        deleted=messagebox.askyesno("Hotel Management System","Do you want to delete this customer?",parent=self.root)
        if deleted>0:
            connection=get_connection()
            my_cursor=connection.cursor()
            query="delete from room where `Customer Contact`=%s"
            value=(self.var_contact.get(),)
            my_cursor.execute(query,value)
        else:
            if not deleted:
                return
        connection.commit()
        self.fetch_data()
        connection.close()
        self.refresh_available_rooms()

    def reset(self):
        self.var_contact.set("")
        self.var_roomavailable.set("")
        self.var_no_of_day.set("")
        self.var_actualtotal.set("")
        self.var_paidtax.set("")
        self.var_total.set("")
        self.var_status.set("Checked-in")

    def search(self):
        # Whitelist the column to avoid SQL injection from the combobox value.
        allowed={"Customer Contact":"`Customer Contact`","Room No":"`Room No`"}
        column=allowed.get(self.search_var.get())
        if not column:
            messagebox.showerror("Error","Invalid search column.",parent=self.root)
            return

        connection=get_connection()
        my_cursor=connection.cursor()
        query="SELECT * FROM room WHERE "+column+" LIKE %s"
        value=('%'+self.txt_search.get()+'%',)
        my_cursor.execute(query,value)
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.room_table.delete(*self.room_table.get_children())
            for i in rows:
                self.room_table.insert("",END,values=i)
            connection.commit()
        connection.close()

    #===============All Data fetch=======================
    def fetch_contact(self):
        if self.var_contact.get()=="":
            messagebox.showerror("Error","Please enter the contact number.",parent=self.root)
            return

        connection=get_connection()
        my_cursor=connection.cursor()
        my_cursor.execute(
            "select Name,Gender,Email,Nationality,Address from customer where Mobile=%s",
            (self.var_contact.get(),))
        row=my_cursor.fetchone()
        connection.close()

        if row==None:
            messagebox.showerror("Error","This number not found.",parent=self.root)
            return

        name,gender,email,nationality,address=row
        show_data_frame=Frame(self.root,bd=4,relief=RIDGE,padx=2)
        show_data_frame.place(x=455,y=55,width=300,height=180)

        fields=[("Name:",name),("Gender:",gender),("Email:",email),
                ("Nationality:",nationality),("Address:",address)]
        for idx,(label_text,value) in enumerate(fields):
            Label(show_data_frame,text=label_text,font=("arial",12,"bold")).place(x=0,y=idx*30)
            Label(show_data_frame,text=value,font=("arial",12,"bold")).place(x=90,y=idx*30)

    def total(self):
        in_date=self.check_in_date.get_date()
        out_date=self.check_out_date.get_date()
        no_of_days=(out_date-in_date).days
        if no_of_days<=0:
            messagebox.showerror("Error","Check-out date must be after the check-in date.",parent=self.root)
            return
        self.var_no_of_day.set(no_of_days)

        price=0
        if (self.var_meal.get()=="Breakfast"):price=150
        elif (self.var_meal.get()=="Lunch"):price=500
        elif (self.var_meal.get()=="Dinner"):price=800

        if (self.var_roomtype.get()=="Single"):price=price+1500
        elif (self.var_roomtype.get()=="Double"):price=price+1000
        elif (self.var_roomtype.get()=="Luxury"):price=price+3000

        net_price=price*no_of_days
        # paid tax
        self.var_paidtax.set(round(0.04*net_price,2))
        self.var_total.set(round(net_price+(0.04*net_price),2))
        self.var_actualtotal.set(net_price)

    #===============PDF invoice=======================
    def generate_invoice(self):
        if self.var_contact.get()=="":
            messagebox.showerror("Error","Please select a booking and click Bill first.",parent=self.root)
            return
        if self.var_total.get()=="":
            messagebox.showerror("Error","Please click Bill to calculate the total first.",parent=self.root)
            return

        # Look up the customer name for a nicer invoice.
        customer_name=""
        try:
            connection=get_connection()
            my_cursor=connection.cursor()
            my_cursor.execute("select Name from customer where Mobile=%s",(self.var_contact.get(),))
            r=my_cursor.fetchone()
            connection.close()
            if r:
                customer_name=r[0]
        except Exception:
            pass

        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica","B",18)
        pdf.cell(0,12,"Hotel Management System",ln=True,align="C")
        pdf.set_font("Helvetica","",12)
        pdf.cell(0,8,"Booking Invoice",ln=True,align="C")
        pdf.ln(4)
        pdf.cell(0,8,f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",ln=True)
        pdf.line(10,pdf.get_y(),200,pdf.get_y())
        pdf.ln(4)

        rows=[
            ("Customer Name",customer_name),
            ("Customer Contact",self.var_contact.get()),
            ("Check-in Date",self._checkin_str()),
            ("Check-out Date",self._checkout_str()),
            ("Room Type",self.var_roomtype.get()),
            ("Room No",self.var_roomavailable.get()),
            ("Meal",self.var_meal.get()),
            ("No. of Days",str(self.var_no_of_day.get())),
            ("Status",self.var_status.get()),
        ]
        pdf.set_font("Helvetica","",12)
        for label,value in rows:
            pdf.cell(70,9,str(label),border=0)
            pdf.cell(0,9,str(value),border=0,ln=True)

        pdf.ln(4)
        pdf.line(10,pdf.get_y(),200,pdf.get_y())
        pdf.ln(2)
        pdf.set_font("Helvetica","",12)
        pdf.cell(70,9,"Sub Total",0)
        pdf.cell(0,9,str(self.var_actualtotal.get()),0,ln=True)
        pdf.cell(70,9,"Tax (4%)",0)
        pdf.cell(0,9,str(self.var_paidtax.get()),0,ln=True)
        pdf.set_font("Helvetica","B",13)
        pdf.cell(70,10,"Total Cost",0)
        pdf.cell(0,10,str(self.var_total.get()),0,ln=True)

        pdf.ln(10)
        pdf.set_font("Helvetica","I",11)
        pdf.cell(0,8,"Thank you for choosing our hotel!",ln=True,align="C")

        filename=f"invoice_{self.var_contact.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath=os.path.join(INVOICE_DIR,filename)
        try:
            pdf.output(filepath)
        except Exception as es:
            messagebox.showwarning("Warning",f"Could not save invoice:{str(es)}",parent=self.root)
            return

        messagebox.showinfo("Invoice",f"Invoice saved to:\n{filepath}",parent=self.root)
        try:
            os.startfile(filepath)  # opens the PDF on Windows
        except Exception:
            pass


if __name__=="__main__":
    root=Tk()
    obj=Room_Booking(root)
    root.mainloop()
