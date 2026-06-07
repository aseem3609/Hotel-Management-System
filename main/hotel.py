from tkinter import *
from PIL import Image,ImageTk
from customer import Cust_win
from room import Room_Booking
from details import Details_Room
from staffdetails import Details_Staff
from dashboard import Dashboard
from reviews import Reviews
from customer_segmentation import Customer_Segmentation


class Hotel_Management_System:
    def __init__(self, root):
        self.root=root
        self.root.title("Hotel Management System")
        self.root.geometry("1550x800+0+0")
 
        # ======================first image=====================
        img1=Image.open(r"D:/hotel management system/hotel images/photo1.webp")
        img1=img1.resize((1550,140),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        lblimg1=Label(self.root,image=self.photoimg1,bd=4,relief=RIDGE)
        lblimg1.place(x=0,y=0,width=1550,height=140)

        # ======================logo=====================
        img2=Image.open(r"D:\hotel management system\hotel images\hotel logo.webp")
        img2=img2.resize((230,140),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg2=Label(self.root,image=self.photoimg2,bd=4,relief=RIDGE)
        lblimg2.place(x=0,y=0,width=230,height=140)


        # ======================title=====================
        lbl_title=Label(self.root,text="HOTEL MANAGEMENT SYSTEM",font=("times new roman",40,"bold italic"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=140,width=1550,height=50)

        # ======================Main frame=====================
        main_frame=Frame(self.root,bd=4,relief=RIDGE)
        main_frame.place(x=0,y=190,width=1550,height=620)

        # ======================Menu=====================
        lbl_menu=Label(main_frame,text="MENU",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_menu.place(x=0,y=0,width=230)

        # ======================button frame=====================
        btn_frame=Frame(main_frame,bd=4,relief=RIDGE)
        btn_frame.place(x=0,y=35,width=228,height=270)

        cust_btn=Button(btn_frame,text="CUSTOMER",command=self.cust_details,width=22,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1")
        cust_btn.grid(row=0,column=0,pady=1)

        room_btn=Button(btn_frame,text="ROOM",width=22,command=self.booking_details,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1")
        room_btn.grid(row=1,column=0,pady=1)

        details_btn=Button(btn_frame,text="DETAILS",width=22,command=self.details_room,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1")
        details_btn.grid(row=2,column=0,pady=1)

        report_btn=Button(btn_frame,text="STAFF REPORT",width=22,command=self.staff_details,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1")
        report_btn.grid(row=3,column=0,pady=1)

        dashboard_btn=Button(btn_frame,text="DASHBOARD",width=22,command=self.dashboard,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1")
        dashboard_btn.grid(row=4,column=0,pady=1)

        reviews_btn=Button(btn_frame,text="REVIEWS",width=22,command=self.reviews,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1")
        reviews_btn.grid(row=5,column=0,pady=1)

        segments_btn=Button(btn_frame,text="SEGMENTS",width=22,command=self.segments,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1")
        segments_btn.grid(row=6,column=0,pady=1)

        logout_btn=Button(btn_frame,text="LOG OUT",width=22,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=0,cursor="hand1",command=self.logout)
        logout_btn.grid(row=7,column=0,pady=1)

        # ======================right side img===================== 
        img3=Image.open(r"D:\hotel management system\hotel images\photo3.webp")
        img3=img3.resize((1310,590),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        lblimg3=Label(main_frame,image=self.photoimg3,bd=4,relief=RIDGE)
        lblimg3.place(x=225,y=0,width=1310,height=590) 

        # ======================down images=====================
        img4=Image.open(r"D:\hotel management system\hotel images\myh.jpg")
        img4=img4.resize((230,210),Image.Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(img4)

        lblimg4=Label(main_frame,image=self.photoimg4,bd=4,relief=RIDGE)
        lblimg4.place(x=0,y=225,width=230,height=210)

        img5=Image.open(r"D:\hotel management system\hotel images\khana.jpg")
        img5=img5.resize((230,190),Image.Resampling.LANCZOS)
        self.photoimg5=ImageTk.PhotoImage(img5)

        lblimg5=Label(main_frame,image=self.photoimg5,bd=4,relief=RIDGE)
        lblimg5.place(x=0,y=420,width=230,height=190)

    def cust_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Cust_win(self.new_window)

    def booking_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Room_Booking(self.new_window)

    def details_room(self):
        self.new_window=Toplevel(self.root)
        self.app=Details_Room(self.new_window)

    def staff_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Details_Staff(self.new_window)

    def dashboard(self):
        self.new_window=Toplevel(self.root)
        self.app=Dashboard(self.new_window)

    def reviews(self):
        self.new_window=Toplevel(self.root)
        self.app=Reviews(self.new_window)

    def segments(self):
        self.new_window=Toplevel(self.root)
        self.app=Customer_Segmentation(self.new_window)

    def logout(self):
        self.root.destroy()



if __name__=="__main__":
    root=Tk()
    obj=Hotel_Management_System(root)
    root.mainloop()