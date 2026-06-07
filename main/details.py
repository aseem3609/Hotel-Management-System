from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import random
from time import strptime
from datetime import datetime
import mysql.connector
from tkinter import messagebox

class Details_Room:
    def __init__(self, root):
        self.root=root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")

       #=======================variables=================
        self.var_floor=StringVar()
        self.var_room_no=StringVar()
        self.var_room_type=StringVar()

        # ======================title=====================
        lbl_title=Label(self.root,text="NEW ROOM BOOKING DETAILS",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=0,width=1295,height=50)

        # ======================logo=====================
        img2=Image.open(r"D:\hotel management system\hotel images\hotel logo.webp")
        img2=img2.resize((100,40),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg2=Label(self.root,image=self.photoimg2,bd=0,relief=RIDGE)
        lblimg2.place(x=5,y=2,width=100,height=40)

        # ======================background image=====================
        bg_img = Image.open(r"D:\hotel management system\hotel images\background.jpg")  
        bg_img = bg_img.resize((1295, 500), Image.Resampling.LANCZOS)  
        self.photo_bg_img = ImageTk.PhotoImage(bg_img)

        lbl_bg = Label(self.root, image=self.photo_bg_img, bd=0, relief=RIDGE)
        lbl_bg.place(x=0, y=50, width=1295, height=500)


        # ======================label_frame=====================
        label_frame_left=LabelFrame(self.root,bd=2,relief=RIDGE,text="Adding New Room ",padx=2,font=("times new roman",12,"bold"))
        label_frame_left.place(x=5,y=50,width=540,height=350)

        # ======================labels and entries=====================
        #Room no
        lbl_floor=Label(label_frame_left,text="Room No.",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_floor.grid(row=0,column=0,sticky=W,padx=20)

        entry_floorw=ttk.Entry(label_frame_left,width=17,font=("arial",13,"bold"),textvariable=self.var_room_no)
        entry_floorw.grid(row=0,column=1,sticky=W)

        #floor
        lbl_room_no=Label(label_frame_left,text="Floor:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_room_no.grid(row=1,column=0,sticky=W,padx=20)

        entry_room_no=ttk.Entry(label_frame_left,width=17,font=("arial",13,"bold"),textvariable=self.var_floor)
        entry_room_no.grid(row=1,column=1,sticky=W)

        #room type
        lbl_room_types=Label(label_frame_left,text="Room Type:",font=("arial",12,"bold"),padx=2,pady=6)
        lbl_room_types.grid(row=2,column=0,sticky=W,padx=20)

        combo_room_type=ttk.Combobox(label_frame_left,font=("arial",12,"bold"),textvariable=self.var_room_type,width=15,state="readonly")
        combo_room_type["value"]=("Single","Double","Luxury")
        combo_room_type.current(0)
        combo_room_type.grid(row=2,column=1)

        #===============Buttons==================
        btn_frame=Frame(label_frame_left,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=200,width=412,height=40)

        btn_add=Button(btn_frame,text="Add",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.add_button)
        btn_add.grid(row=0,column=0,padx=1)

        btn_update=Button(btn_frame,text="Update",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.updated)
        btn_update.grid(row=0,column=1,padx=1)

        btn_delete=Button(btn_frame,text="Delete",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.deleted)
        btn_delete.grid(row=0,column=2,padx=1)

        btn_reset=Button(btn_frame,text="Reset",font=("arial",12,"bold"),bg="black",fg="gold",width=9,command=self.reset)
        btn_reset.grid(row=0,column=3,padx=1)

        #===============table frame search system==================

        details_table=LabelFrame(self.root,bd=2,relief=RIDGE,text="Room Details",padx=2,font=("times new roman",12,"bold"))
        details_table.place(x=600,y=55,width=600,height=350)

        scrollbar_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        scrollbar_y=ttk.Scrollbar(details_table,orient=VERTICAL)

        self.room_table=ttk.Treeview(details_table,column=("Room No.","Floor","Room Type"),xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)

        scrollbar_x.pack(side=BOTTOM,fill=X)
        scrollbar_y.pack(side=RIGHT,fill=Y)
        scrollbar_x.config(command=self.room_table.xview)
        scrollbar_y.config(command=self.room_table.yview)

        self.room_table.heading("Room No.",text="Room No.")
        self.room_table.heading("Floor",text="Floor")
        self.room_table.heading("Room Type",text="Room Type")


        self.room_table["show"]="headings"

        self.room_table.column("Room No.",width=100)
        self.room_table.column("Floor",width=100)
        self.room_table.column("Room Type",width=100)

        self.room_table.pack(fill=BOTH,expand=1)
        self.room_table.bind("<ButtonRelease-1>",self.get_cursor) 
        self.fetch_data()

    def add_button(self):
        if self.var_room_no.get() == "" or self.var_room_type.get() == "" or self.var_floor.get() == "":
            messagebox.showerror("Error", "All fields must be filled.", parent=self.root)
        else:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="AshimtiW@07",
                    database="hotel_management_system",
                )
                my_cursor = connection.cursor()

                # Check for duplicate room number
                my_cursor.execute("SELECT * FROM details WHERE `Room No.` = %s", (self.var_room_no.get(),))
                room_exists = my_cursor.fetchone()

                if room_exists:
                    messagebox.showerror("Error", "Room Number already exists!", parent=self.root)
                else:
                    # Insert new room details
                    my_cursor.execute(
                        "INSERT INTO details (`Room No.`, `Floor`, `Room Type`) VALUES (%s, %s, %s)",
                        (self.var_room_no.get(), self.var_floor.get(), self.var_room_type.get()),
                    )
                    connection.commit()
                    self.fetch_data()
                    messagebox.showinfo("Success", "New Room Added Successfully.", parent=self.root)

                connection.close()
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def fetch_data(self):
                connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
                my_cursor=connection.cursor()
                my_cursor.execute("select * from details")
                rows=my_cursor.fetchall()
                if len(rows)!=0:
                    self.room_table.delete(*self.room_table.get_children())
                    for i in rows:
                        self.room_table.insert("",END,values=i)
                    connection.commit()
                connection.close()

    def get_cursor(self,event=""):
        cursor_row=self.room_table.focus()
        content=self.room_table.item(cursor_row)
        row=content["values"]

        self.var_room_no.set(row[0])
        self.var_floor.set(row[1])
        self.var_room_type.set(row[2])

    def updated(self):
        if self.var_floor.get()=="":
            messagebox.error("Error","Please enter floor number.",parent=self.root)
        else:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor()
            my_cursor.execute("update details set `Floor`=%s,`Room Type`=%s where `Room No.`=%s",(
                                                                            self.var_floor.get(),
                                                                            self.var_room_type.get(),
                                                                            self.var_room_no.get()
                                                                        ))
            connection.commit()
            self.fetch_data()
            connection.close()
            messagebox.showinfo("Update","New Room details has been successfully updated..",parent=self.root)

    def deleted(self):
        deleted=messagebox.askyesno("Hotel Management System","Do you want to delete this room details?",parent=self.root)
        if deleted>0:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor() 
            query="delete from details where `Room No.`=%s"
            value=(self.var_room_no.get(),)  
            my_cursor.execute(query,value)           
        else:
            if not deleted:
                return
        connection.commit()
        self.fetch_data()
        connection.close()

    def reset(self):
        self.var_floor.set("")
        self.var_room_no.set("")
if __name__=="__main__":
    root=Tk()
    obj=Details_Room(root)
    root.mainloop()