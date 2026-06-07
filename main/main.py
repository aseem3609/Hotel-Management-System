from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import mysql.connector
from hotel import Hotel_Management_System
from register import Register

def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()



class Login_Window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1530x800+0+0")

        self.bg=ImageTk.PhotoImage(file=r"D:\hotel management system\hotel images\bg.jpg")
        lbl_img=Label(self.root,image=self.bg)
        lbl_img.place(x=0,y=0,relwidth=1,relheight=1)

        frame=Frame(self.root,bg="black")
        frame.place(x=610,y=170,width=340,height=450)

        img1=Image.open(r"D:\hotel management system\hotel images\LoginIconAppl.png")
        img1=img1.resize((100,100),Image.Resampling.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lbl_img1=Label(image=self.photoimage1,bg="black",borderwidth=0)
        lbl_img1.place(x=730,y=175,width=100,height=100)

        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="white",bg="black")
        get_str.place(x=95,y=100)

        #label
        username_lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        username_lbl.place(x=70,y=155)

        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)


        passowrd_lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        passowrd_lbl.place(x=70,y=225)

        self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"),show="*")
        self.txtpass.place(x=40,y=250,width=270)


        #=======icon images===============

        img2=Image.open(r"D:\hotel management system\hotel images\LoginIconAppl.png")
        img2=img2.resize((25,25),Image.Resampling.LANCZOS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lbl_img2=Label(image=self.photoimage2,bg="black",borderwidth=0)
        lbl_img2.place(x=650,y=323,width=25,height=25)

        img3=Image.open(r"D:\hotel management system\hotel images\kir.png")
        img3=img3.resize((25,25),Image.Resampling.LANCZOS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lbl_img3=Label(image=self.photoimage3,bg="black",borderwidth=0)
        lbl_img3.place(x=650,y=394,width=25,height=25)

        #login button
        loginbtn=Button(frame,text="Login",font=("times new roman",15,"bold"),bd=3,command=self.login,relief=RIDGE,fg="white",bg="red",activeforeground="white",activebackground="red")
        loginbtn.place(x=110,y=300,width=120,height=35)

        #register button
        registerbtn=Button(frame,text="New User Register",command=self.register_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        registerbtn.place(x=15,y=350,width=160)

        #forgot password button
        forgotbtn=Button(frame,text="Forget Passoword",command=self.forgot_password_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        forgotbtn.place(x=10,y=370,width=160)
    

    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)

    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error","All fields required")
        else:
                    connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
                    my_cursor=connection.cursor()
                    my_cursor.execute("select * from register where Email=%s and Password=%s",(self.txtuser.get(),self.txtpass.get(),))
                    rows=my_cursor.fetchone()
                    if rows==None:
                        messagebox.showerror("Error","Invalid Username and Pasword.")
                    else:
                        open_main=messagebox.askyesno("YesNo","Access only admin.")
                        if open_main>0:
                            self.new_window=Toplevel(self.root)
                            self.app=Hotel_Management_System(self.new_window)
                        else:
                            if not open_main:
                                return
                    connection.commit()
                    connection.close()


    #======================reset password=================================
    def reset_pass(self):
        if self.combo_security_q.get()=="Select":
            messagebox.showerror("Error","Please select security question.",parent=self.root2)
        elif self.txtsecurity_a.get()=="":
            messagebox.showerror("Error","Please enter the answer.",parent=self.root2)
        elif self.txtnew_pass.get()=="":
            messagebox.showerror("Error","Please enter the new password.",parent=self.root2)
        else:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor()
            my_cursor.execute("select * from register where Email=%s and SecurityQ=%s and SecurityA=%s",(self.txtuser.get(),self.combo_security_q.get(),self.txtsecurity_a.get(),))
            rows=my_cursor.fetchone()
            if rows==None:
                messagebox.showerror("Error","Please enter the correct answer.",parent=self.root2)
            else:
                my_cursor.execute("update register set password=%s where email=%s",(self.txtnew_pass.get(),self.txtuser.get(),))
                connection.commit()
                connection.close()
                messagebox.showinfo("Info","Your password has been reset,you can login with new password.",parent=self.root2)
                self.root2.destroy()

    #======================forgot password window===========================
    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter the email address to reset the password")
        else:
            connection=mysql.connector.connect(host="localhost",username="root",password="AshimtiW@07",database="hotel_management_system")
            my_cursor=connection.cursor()
            my_cursor.execute("select * from register where Email=%s",(self.txtuser.get(),))
            rows=my_cursor.fetchone()
            #print(rows)
            if rows==None:
                messagebox.showerror("Error","Email you entered isn't registered..Enter the registered email.")
            else:
                connection.close()
                self.root2=Toplevel()
                self.root2.title("Forgot Password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forgot Password.",font=("times new roman",10,"bold"),fg="red")
                l.place(x=0,y=10,relwidth=1)

                security_q=Label(self.root2,text="Select Security Questions",font=("times new roman",15,"bold"),fg="black")
                security_q.place(x=50,y=80)
                self.combo_security_q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_q["values"]=("Select","Your Birth Place","Your Father's Name","Your Grandfather's Name")
                self.combo_security_q.current(0)
                self.combo_security_q.place(x=50,y=110,width=250)

                security_a=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),fg="black")
                security_a.place(x=50,y=150)
                self.txtsecurity_a=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txtsecurity_a.place(x=50,y=180,width=250)

                new_pass=Label(self.root2,text="New Password",font=("times new roman",15,"bold"))
                new_pass.place(x=50,y=220)
                self.txtnew_pass=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txtnew_pass.place(x=50,y=250,width=250)

                btn=Button(self.root2,text="Reset",font=("times new roman",15,"bold"),fg="white",bg="green",command=self.reset_pass)
                btn.place(x=140,y=290)




if __name__=="__main__":
    main()
