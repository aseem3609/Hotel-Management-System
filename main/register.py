from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import mysql.connector

class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1530x900+0+0")

        #===========variables================
        self.var_first_name=StringVar()
        self.var_last_name=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityq=StringVar()
        self.var_securitya=StringVar()
        self.var_pass=StringVar()
        self.var_confirmpass=StringVar()
        self.var_check=IntVar()

        

        #===========bg image===================
        self.bg=ImageTk.PhotoImage(file=r"D:\hotel management system\hotel images\0-3450_3d-nature-wallpaper-hd-1080p-free-download-new.jpg")
        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relheight=1,relwidth=1)

        #===========left1 image===================
        img23 = Image.open(r"D:\hotel management system\hotel images\quote.webp")
        img23 = img23.resize((470, 550), Image.Resampling.LANCZOS)
        self.photoimage23 = ImageTk.PhotoImage(img23)
        lbl_img23 = Label(self.root, image=self.photoimage23, borderwidth=0)
        lbl_img23.place(x=50, y=100, width=470, height=550)

        #==========main frame==================
        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="darkgreen",bg="white")
        register_lbl.place(x=20,y=20)

        #==========label and entry==================
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)
        self.txtfname=ttk.Entry(frame,textvariable=self.var_first_name,font=("times new roman",15,"bold"))
        self.txtfname.place(x=50,y=130,width=250)

        lname=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white")
        lname.place(x=370,y=100)
        self.txtlname=ttk.Entry(frame,textvariable=self.var_last_name,font=("times new roman",15,"bold"))
        self.txtlname.place(x=370,y=130,width=250)

        #row2
        contact=Label(frame,text="Contact No",font=("times new roman",15,"bold"),bg="white")
        contact.place(x=50,y=170)
        self.txtcontact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15,"bold"))
        self.txtcontact.place(x=50,y=200,width=250)

        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white")
        email.place(x=370,y=170)
        self.txtemail=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15,"bold"))
        self.txtemail.place(x=370,y=200,width=250)

        #row3
        security_q=Label(frame,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white")
        security_q.place(x=50,y=240)
        self.combo_security_q=ttk.Combobox(frame,font=("times new roman",15,"bold"),textvariable=self.var_securityq,state="readonly")
        self.combo_security_q["values"]=("Select","Your Birth Place","Your Father's Name","Your Grandfather's Name")
        self.combo_security_q.current(0)
        self.combo_security_q.place(x=50,y=270,width=250)

        security_a=Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="white")
        security_a.place(x=370,y=240)
        self.txtsecurity_a=ttk.Entry(frame,textvariable=self.var_securitya,font=("times new roman",15,"bold"))
        self.txtsecurity_a.place(x=370,y=270,width=250)

        #row4
        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white")
        pswd.place(x=50,y=310)
        self.txtpswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15,"bold"))
        self.txtpswd.place(x=50,y=340,width=250)

        confirm_pswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white")
        confirm_pswd.place(x=370,y=310)
        self.txtconfirm_pswd=ttk.Entry(frame,textvariable=self.var_confirmpass,font=("times new roman",15,"bold"))
        self.txtconfirm_pswd.place(x=370,y=340,width=250)

        #============check button============
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I Agree The Terms And Conditions.",font=("times new roman",12,"bold"),onvalue=1,offvalue=0,bg="white",activebackground="white")
        checkbtn.place(x=50,y=380)

        #============buttons============
        img=Image.open(r"D:\hotel management system\hotel images\register-now-button1.jpg")
        img=img.resize((200,50),Image.Resampling.LANCZOS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame,image=self.photoimage,borderwidth=0,cursor="hand2",bg="white",activebackground="white",command=self.register_data)
        b1.place(x=10,y=420,width=200)

        imgs=Image.open(r"D:\hotel management system\hotel images\unnamed.png")
        imgs=imgs.resize((200,40),Image.Resampling.LANCZOS)
        self.photoimages=ImageTk.PhotoImage(imgs)
        b1=Button(frame,image=self.photoimages,borderwidth=0,cursor="hand2",bg="white",activebackground="white",command=self.return_login)
        b1.place(x=330,y=425,width=200)

        #==========function declaration=========
    def register_data(self):
        if self.var_first_name.get()=="" or self.var_email.get()=="" or self.var_securityq.get()=="Select":
            messagebox.showerror("Error","All fields are required.")
        elif self.var_confirmpass.get()!=self.var_pass.get():
            messagebox.showerror("Error","Password and Confirm password must be same.")
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Terms and Conditions must be agreed.")
        else:
                connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
                my_cursor=connection.cursor()
                my_cursor.execute("select * from register where email=%s",(self.var_email.get(),))
                rows=my_cursor.fetchone()
                if rows!=None:
                     messagebox.showerror("Error","User already exists..Please try another email")
                else:
                     my_cursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                                self.var_first_name.get(),
                                                                                self.var_last_name.get(),
                                                                                self.var_contact.get(),
                                                                                self.var_email.get(),
                                                                                self.var_securityq.get(),
                                                                                self.var_securitya.get(),
                                                                                self.var_pass.get(),
                                                                                             ))
                connection.commit()
                connection.close()
                messagebox.showinfo("Success","Register Successfull !!!")

    def return_login(self):
         self.root.destroy()
    
    def get_email(self):
        return self.var_email.get()
    def get_password(self):
        return self.var_pass.get()




if __name__=="__main__":
    root=Tk()
    app=Register(root)
    root.mainloop()
        