import re
import tkinter
import customtkinter
import random
import string
from tkinter import messagebox
from PIL import Image, ImageTk
import imageio
import smtplib
import os

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class LoadingScreen(customtkinter.CTk):
    def __init__(self, video_path, next_screen_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video_path = video_path
        self.next_screen_callback = next_screen_callback
        self.geometry("1920x1080")
        self.attributes("-fullscreen", True)
        self.label = customtkinter.CTkLabel(self)
        self.label.pack(fill=tkinter.BOTH, expand=True)
        self.frames = []
        self.load_frames()
        self.current_frame_index = 0
        self.animate()

    def load_frames(self):
        video = imageio.get_reader(self.video_path, 'ffmpeg')
        for frame in video:
            image = Image.fromarray(frame).resize((1920, 1080), Image.Resampling.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(image))

    def animate(self):
        if self.current_frame_index < len(self.frames):
            self.label.configure(image=self.frames[self.current_frame_index])
            self.current_frame_index += 1
            self.after(20, self.animate)  # Adjust the delay as needed
        else:
            self.destroy()
            self.next_screen_callback()

def main_screen():
    root = customtkinter.CTk()
    root.geometry("1920x1080")
    root.destroy()
    root.mainloop()

def start_loading_screen():
    loading_screen = LoadingScreen("WizzBank loading....mp4", main_screen)
    loading_screen.geometry("1920x1080")
    loading_screen.mainloop()

# Start the loading screen
start_loading_screen()

app = customtkinter.CTk()
app.attributes("-fullscreen", True)
app.title('Welcome to Wizzbank')

def generate_random_password():
    entry_password.delete(0, 'end')  # Clear the entry field
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(characters) for i in range(12))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            return password

# Text File Generation to store user details:
def save_user_details(username, email, password, pin, phone_number, initial_amount):
    account_number = ''.join(random.choice(string.digits) for i in range(10))
    initial_amount = round(float(initial_amount), 2)
    with open("BankData.txt", "a") as file:
        file.write(f"Username: {username}, Email: {email}, Password: {password}, Pin: {pin}, Phone Number: {phone_number}, Account Number: {account_number}, Available Balance: {initial_amount}\n")
    return account_number

def load_user_details(username):
    try:
        with open("BankData.txt", "r") as file:
            for line in file:
                details = line.strip().split(', ')
                user_data = {item.split(': ')[0]: item.split(': ')[1] for item in details}
                if user_data.get("Username") == username:
                    return {
                        "Username": user_data.get("Username"),
                        "Email": user_data.get("Email"),
                        "Password": user_data.get("Password"),
                        "Pin": user_data.get("Pin"),
                        "Phone Number": user_data.get("Phone Number"),
                        "Account Number": user_data.get("Account Number"),
                        "Balance": user_data.get("Available Balance")
                    }
        return None
    except FileNotFoundError:
        return None
    
# Email Function
def send_email(user_email, subject, message):
    sender_email = "adlerkramer08@gmail.com"  # Replace with your email
    sender_password = "xkor pfep ppho wtdx"  # Replace with your email password

    text = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, user_email, text)
    server.quit()

def update_balance(username, new_balance):
            new_lines = []
            with open("BankData.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    details = line.strip().split(', ')
                    user_data = {item.split(': ')[0]: item.split(': ')[1] for item in details}
                    if user_data.get("Username") == username:
                        user_data["Available Balance"] = f"{new_balance:.2f}"
                        new_line = ", ".join([f"{key}: {value}" for key, value in user_data.items()])
                        new_lines.append(new_line + "\n")
                    else:
                        new_lines.append(line)
            
            with open("BankData.txt", "w") as file:
                file.writelines(new_lines)

def update_transactions(username, transaction_details):
    with open("Transactions.txt", "a") as file:
        file.write(f"Username: {username}, {transaction_details}\n")

def show_frame(frame):
    frame.tkraise()

#Handle Signup
def signup_function():
    for widget in app.winfo_children():
        widget.destroy()

    original_image = Image.open("wizzbank-bg.png")
    ctk_image = customtkinter.CTkImage(dark_image=original_image, size=original_image.size)

    l1 = customtkinter.CTkLabel(master=app, image=ctk_image)
    l1.pack(fill=tkinter.BOTH, expand=True)

    # Load images with transparency
    eye_open_img = Image.open("visible.png").resize((20, 20)).convert("RGBA")
    eye_closed_img = Image.open("hide.png").resize((20, 20)).convert("RGBA")

    eye_open_img_tk = ImageTk.PhotoImage(eye_open_img)
    eye_closed_img_tk = ImageTk.PhotoImage(eye_closed_img)


    def handle_signup():
        username = entry_username.get()
        email = entry_email.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()
        pin = entry_pin.get()
        phone_number = entry_phone_number.get()
        initial_amount = entry_initial_amount.get()

        username = entry_username.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()
        confirm_password = entry_confirm_password.get().strip()
        pin = entry_pin.get().strip()
        phone_number = entry_phone_number.get().strip()
        initial_amount = entry_initial_amount.get().strip()

        user_data = load_user_details(username)

        #Check that Entries have information in them
        if not username:
            messagebox.showerror("Error", "The username field does not contain any information!")
        if not username:
            messagebox.showerror("Error", "The email field does not contain any information!")
        if not password:
            messagebox.showerror("Error", "The password field does not contain any information!")
        if not confirm_password:
            messagebox.showerror("Error", "The confirm password field does not contain any information!")
        if not pin:
            messagebox.showerror("Error", "The pin field does not contain any information!")
        if not phone_number:
            messagebox.showerror("Error", "The phone number field does not contain any information!")
        if not initial_amount:
            messagebox.showerror("Error", "The initial amount field does not contain any information!")

        def validate_email(email):
            # Check if email ends with "@gmail.com"
            if email.endswith("@gmail.com"):
                # Extract the username part
                username = email.split("@")[0]
                # Check if the username has at least 3 characters
                if len(username) >= 3 and re.match("^[a-zA-Z0-9_.+-]+$", username):
                    return True
            return False

        # Username validation
        if not re.match(r"^[a-zA-Z]{3,20}[a-zA-Z0-9@#$%^&+=]*$", username):
            messagebox.showerror("Error", "Username must begin with at least 3 letters and can contain special characters or digits after.")
            return
        if load_user_details(username) is not None:
            messagebox.showerror("Error", "Username already exists. Please choose another one.")
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email address. Please use a valid @gmail.com address with at least 3 characters before the @ symbol.")
            return

        # Password Matching validation
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        # Pin validation
        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "Pin must be exactly 4 digits long and contain only numbers!")
            return
        
         # Phone Number validation
        if not phone_number.isdigit() or len(phone_number) != 10 or not phone_number.startswith('0'):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits long, start with 0, and contain only numbers!")
            return

        # Save user details
        account_number = save_user_details(username, email, password, pin, phone_number, initial_amount)

        # Send email after successful sign-up
        subject = "Account Creation Notification"
        message = f"Dear {username},\n\nWelcome to WizzBank! Your account has been successfully created.\n\nBelow are your banking details-\nUsername: {username}\nEmail: {email}\nPhone Number: {phone_number}\nPassword: {password}\nPin Number: {pin}\nAccount Number: {account_number}\nBalance: {initial_amount}\n\nThank You For Choosing Us\nRegards,\nThe WizzBank Team"
        send_email(email, subject, message)

        messagebox.showinfo("Signup Successful", f"Account created! Your account number is {account_number}")
        messagebox.showinfo("Welcome to WizzBank!",f"You have been sent an email containing your banking details.")
        login_screen()


    show_password_var = tkinter.BooleanVar(value=False)

    def toggle_password_visibility():
        if show_password_var.get():
            entry_password.configure(show='*')
            entry_confirm_password.configure(show='*')
            eye_button.configure(image=eye_closed_img_tk)
        else:
            entry_password.configure(show='')
            entry_confirm_password.configure(show='')
            eye_button.configure(image=eye_open_img_tk)
        show_password_var.set(not show_password_var.get())

    show_pin_var = tkinter.BooleanVar(value=False)    
    
    def toggle_pin_visibility():
        if show_pin_var.get():
            entry_pin.configure(show='')
            pin_eye_button.configure(image=eye_open_img_tk)
        else:
            entry_pin.configure(show='*')
            pin_eye_button.configure(image=eye_closed_img_tk)
        show_pin_var.set(not show_pin_var.get())


    global entry_username
    entry_username = customtkinter.CTkEntry(master=l1, width=350, placeholder_text='Username', font=('Century Gothic', 20))
    entry_username.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

    global entry_email
    entry_email = customtkinter.CTkEntry(master=l1, width=350, placeholder_text='Email', font=('Century Gothic', 20))
    entry_email.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    global entry_password
    entry_password = customtkinter.CTkEntry(master=l1, width=350, placeholder_text='Password', font=('Century Gothic', 20), show="*")
    entry_password.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

    global entry_confirm_password
    entry_confirm_password = customtkinter.CTkEntry(master=l1, width=300, placeholder_text='Confirm Password', font=('Century Gothic', 20), show="*")
    entry_confirm_password.place(relx=0.484, rely=0.5, anchor=tkinter.CENTER)

    # Eye button setup for password
    eye_button = customtkinter.CTkButton(master=l1, image=eye_closed_img_tk, text="", fg_color="transparent", bg_color="transparent", hover_color=None, width=30, command=toggle_password_visibility)
    eye_button.place(relx=0.6, rely=0.5, anchor=tkinter.W)

    global entry_pin
    entry_pin = customtkinter.CTkEntry(master=l1, width=300, placeholder_text='Pin', font=('Century Gothic', 20), show="*")
    entry_pin.place(relx=0.484, rely=0.55, anchor=tkinter.CENTER)

    # Eye button setup for pin
    pin_eye_button = customtkinter.CTkButton(master=l1, image=eye_closed_img_tk, text="", fg_color="transparent", hover_color=None,  width=30, command=toggle_pin_visibility)
    pin_eye_button.place(relx=0.6, rely=0.55, anchor=tkinter.W)

    global entry_phone_number
    entry_phone_number = customtkinter.CTkEntry(master=l1, width=350, placeholder_text='Phone Number', font=('Century Gothic', 20))
    entry_phone_number.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

    global entry_initial_amount
    entry_initial_amount = customtkinter.CTkEntry(master=l1, width=350, placeholder_text='Initial Amount (R)', font=('Century Gothic', 20))
    entry_initial_amount.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

    signup_button = customtkinter.CTkButton(
        master=l1,
        width=350,
        text="Sign Up",
        command=handle_signup,
        fg_color=None,
        font=('Century Gothic', 20),
        corner_radius=10
    )
    signup_button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

    generate_password_button = customtkinter.CTkButton(
        master=l1,
        width=350,
        text="Generate Password",
        command=lambda: entry_password.insert(0, generate_random_password()),
        fg_color=None,
        font=('Century Gothic', 20),
        corner_radius=10
    )
    generate_password_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

    back_button = customtkinter.CTkButton(
        master=l1,
        width=350,
        text="Back to Login",
        command=lambda: app.after(500, login_screen),# Transition effect
        fg_color=None,
        font=('Century Gothic', 20),
        corner_radius=10
    )
    back_button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        ctk_resized_image = customtkinter.CTkImage(dark_image=resized_image, size=(new_width, new_height))
        l1.configure(image=ctk_resized_image)
        l1.image = ctk_resized_image

    app.bind('<Configure>', resize_image)
    
# Login screen function
def login_screen():
    for widget in app.winfo_children():
        widget.destroy()

    original_image = Image.open("wizzbank-bg.png")
    ctk_image = customtkinter.CTkImage(dark_image=original_image, size=original_image.size)

    l1 = customtkinter.CTkLabel(master=app, image=ctk_image)
    l1.pack(fill=tkinter.BOTH, expand=True)

    global entry_username
    entry_username = customtkinter.CTkEntry(
        master=l1, 
        width=300, 
        height=40,
        placeholder_text='Username',
        font=('Century Gothic', 20) 
        )
    entry_username.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    global entry_password
    entry_password = customtkinter.CTkEntry(
        master=l1,
        width=300,
        height=40,
        placeholder_text='Password',
        font=('Century Gothic', 20), 
        show="*"
        )
    entry_password.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    login_button = customtkinter.CTkButton(
        master=l1,
        width=300,
        height=40,
        text="Login",
        command=login_function,
        fg_color=None,
        font=('Century Gothic', 20),
        )
    login_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

    signup_button = customtkinter.CTkButton(
        master=l1,
        width=300,
        height=40,
        text="Sign Up",
        command=signup_function,
        font=('Century Gothic', 20), 
        corner_radius=10
        )
    signup_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        ctk_resized_image = customtkinter.CTkImage(dark_image=resized_image, size=(new_width, new_height))
        l1.configure(image=ctk_resized_image)
        l1.image = ctk_resized_image

    app.bind('<Configure>', resize_image)

# Login function
def login_function():
    username = entry_username.get()
    password = entry_password.get()

    username = entry_username.get().strip()
    password = entry_password.get().strip()
    
    if not username:
        messagebox.showerror("Error", "The username field does not contain any information.")
    if not password:
        messagebox.showerror("Error", "The password field does not contain any information.")

    user_info = load_user_details(username)
    if user_info and user_info["Password"] == password:
        main_screen(username, user_info)
    else:
        messagebox.showerror("Error", "Invalid username or password")

def main_screen(username, user_info):
    for widget in app.winfo_children():
        widget.destroy()

    app.geometry("1280x720")
    app.title('Welcome To WizzBank')

    original_image = Image.open("wizzbank-bg2.png")
    ctk_image = customtkinter.CTkImage(dark_image=original_image, size=original_image.size)

    l1 = customtkinter.CTkLabel(master=app, image=ctk_image)
    l1.pack(fill=tkinter.BOTH, expand=True)

    label_username=customtkinter.CTkLabel(
        master=l1,
        text=f"Welcome, {username}",
        font=('Century Gothic', 20)
        )
    label_username.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
    
    label_account=customtkinter.CTkLabel(
        master=l1, 
        text=f"Account Number: {user_info['Account Number']}",
        font=('Century Gothic', 20)
        )
    label_account.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    
    label_balance=customtkinter.CTkLabel(
        master=l1,
        text=f"Balance: R{float(user_info['Balance']):.2f}",
        font=('Century Gothic', 20)
        )
    label_balance.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    def withdraw_function():
        for widget in app.winfo_children():
            widget.destroy()

        app.geometry("1280x720")
        app.title('Welcome To WizzBank')

        original_image = Image.open("wizzbank-bg2.png")
        ctk_image = customtkinter.CTkImage(dark_image=original_image, size=original_image.size)

        l1 = customtkinter.CTkLabel(master=app, image=ctk_image)
        l1.pack(fill=tkinter.BOTH, expand=True)

        global entry_withdrawal_amount, entry_pin

        def handle_withdraw():
            pin = entry_pin.get().strip()
            user_data = load_user_details(username)
            withdraw=entry_withdrawal_amount.get().strip()
            

            if not withdraw:
                messagebox.showerror("Error", "Please enter an amount to withdraw.")
                return
            if not pin:
                messagebox.showerror("Error", "Please enter your pin.")
                return
            
            # Convert to integer for further checks
            amount = int(withdraw)

            # Check if the input is an integer
            if not withdraw.isdigit():
                messagebox.showerror("Error", "Please enter a valid integer amount without decimals, commas, special characters, or letters.")
                return

            # Check if the amount is a multiple of ten
            if amount % 10 != 0:
                messagebox.showerror("Error", "The withdrawal amount must be in multiples of ten.")
                return

            amount = float(entry_withdrawal_amount.get())
            if amount <= 10:
                messagebox.showerror("Error", "Minimum withdrawal amount is R10.00.")
                return
 
            if pin != user_data["Pin"]:
                messagebox.showerror("Error", "Incorrect Pin")
                return

            user_info = load_user_details(username)
            if user_info:
                current_balance = float(user_info['Balance'])
            if amount > current_balance:
                messagebox.showerror("Error", "Insufficient funds.")
                return
            if messagebox.askyesno("Confirm", "Are you sure you want to make this withdrawal?"):
                new_balance = current_balance - amount
                update_balance(username, new_balance)
                update_transactions(username, f"Withdrawn: R{amount:.2f}")
                messagebox.showinfo("Success", f"Withdrawn: R{amount:.2f}")
                user_info['Balance'] = str(new_balance)
                main_screen(username, user_info)

        label_withdrawal_username=customtkinter.CTkLabel(
            master=l1,
            text=f"Hi {username}!,Withdraw Now.",
            font=('Century Gothic', 25)
            )
        label_withdrawal_username.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        label_withdrawal_balance=customtkinter.CTkLabel(
            master=l1,
            text=f"Current Balance: R{float(user_info['Balance']):.2f}",
            font=('Century Gothic', 25)
            )
        label_withdrawal_balance.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        entry_withdrawal_amount = customtkinter.CTkEntry(
            master=l1,
            width=330,
            height=40,
            placeholder_text='Withdrawal Amount(R)',
            font=('Century Gothic', 20),
            )
        entry_withdrawal_amount.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        entry_pin = customtkinter.CTkEntry(
            master=l1,
            width=330,
            height=40,
            placeholder_text='Please Enter Your Pin',
            font=('Century Gothic', 20),
            show='*'
            )
        entry_pin.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        withdrawal_button=customtkinter.CTkButton(
            master=l1,
            text="Withdraw",
            width=330,
            height=40,
            command=handle_withdraw,
            font=('Century Gothic', 20),
            )
        withdrawal_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        
        withdrawal_back=customtkinter.CTkButton(
            master=l1,
            text="Back to Banking",
            width=330,
            height=40,
            command=lambda: main_screen(username, user_info),
            font=('Century Gothic', 20),
            )
        withdrawal_back.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

    def transfer_function():
        for widget in app.winfo_children():
            widget.destroy()

        app.geometry("1280x720")
        app.title('Welcome To WizzBank')

        original_image = Image.open("wizzbank-bg2.png")
        ctk_image = customtkinter.CTkImage(dark_image=original_image, size=original_image.size)

        l1 = customtkinter.CTkLabel(master=app, image=ctk_image)
        l1.pack(fill=tkinter.BOTH, expand=True)

        global entry_transfer_pin

        def handle_transfer():
            pin = entry_transfer_pin.get().strip()
            recipient_username = entry_transfer_recipient.get().strip()
            recipient_account_number = entry_transfer_recipient_account_number.get().strip()
            transfermoney = entry_transfer_amount.get().strip()

            user_info = load_user_details(username)
            recipient_info = load_user_details(recipient_username)

            if not recipient_username:
                messagebox.showerror("Error", "Please specify who you would like to transfer money to.")
                return
            if not pin:
                messagebox.showerror("Error", "Please enter your pin.")
                return
            if not recipient_account_number:
                messagebox.showerror("Error", "Please specify the account number of who you would like to transfer money to.")
                return
            if not transfermoney:
                messagebox.showerror("Error", "Please specify an amount to proceed to transfer.")
                return

            # Check if the input is an integer
            if not transfermoney.isdigit():
                messagebox.showerror("Error", "Please enter a valid integer amount without decimals, commas, special characters, or letters.")
                return
            
            # Check if pin is valid
            if pin != user_info["Pin"]:
                messagebox.showerror("Error", "Incorrect Pin")
                return

            # Convert to integer for further checks
            amount = int(transfermoney)
            current_balance = float(user_info['Balance'])

            # Check if the amount is a multiple of ten
            if amount % 10 != 0:
                messagebox.showerror("Error", "The withdrawal amount must be in multiples of ten.")
                return

            recipient_info = load_user_details(recipient_username)
            if not recipient_info or recipient_info['Account Number'] != recipient_account_number:
                messagebox.showerror("Error", "Recipient not found.")
                return

            # Validate sender is not the same as receiver
            if recipient_username == username:
                messagebox.showerror("Error", "You cannot transfer money to yourself.")
                return

            if amount > current_balance:
                messagebox.showerror("Error", "Insufficient balance for this transfer.")
                return
            if amount < 10:
                messagebox.showerror("Error", "Minimum transfer amount is R10.00.")
                return

            if user_info and recipient_info:
                current_balance = float(user_info['Balance'])
                if amount > current_balance:
                    messagebox.showerror("Error", "Insufficient funds.")
                    return
                if messagebox.askyesno("Confirm", "Are you sure you want to make this transfer?"):
                    new_balance = current_balance - amount
                    update_balance(username, new_balance)
                    update_transactions(username, f"Transferred: R{amount:.2f} to {recipient_username}")

                    recipient_new_balance = float(recipient_info['Balance']) + amount
                    update_balance(recipient_username, recipient_new_balance)
                    update_transactions(recipient_username, f"Received: R{amount:.2f} from {username}")

                    messagebox.showinfo("Success", "Transfer Successful")
                    user_info['Balance'] = str(new_balance)
                    main_screen(username, user_info)

        label_transfer_username = customtkinter.CTkLabel(
            master=l1,
            text=f"Hi {username}!, Transfer Now.",
            font=('Century Gothic', 25)
        )
        label_transfer_username.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
                            
        label_transfer_balance = customtkinter.CTkLabel(
            master=l1,
            text=f"Current Balance: R{float(user_info['Balance']):.2f}",
            font=('Century Gothic', 25)
        )
        label_transfer_balance.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        entry_transfer_recipient = customtkinter.CTkEntry(
            master=l1,
            width=350,
            height=40,
            placeholder_text='Enter Recipient Username',     
            font=('Century Gothic', 20)
        )
        entry_transfer_recipient.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        entry_transfer_recipient_account_number = customtkinter.CTkEntry(
            master=l1,
            width=350,
            height=40,
            placeholder_text='Enter Recipient Account Number',     
            font=('Century Gothic', 20)
        )
        entry_transfer_recipient_account_number.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        entry_transfer_pin = customtkinter.CTkEntry(
            master=l1,
            width=350,
            height=40,
            placeholder_text='Please Enter Your Pin',     
            font=('Century Gothic', 20),
            show='*'
        )
        entry_transfer_pin.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        entry_transfer_amount = customtkinter.CTkEntry(
            master=l1,
            width=350,
            height=40,
            placeholder_text='Transfer Amount (R)',     
            font=('Century Gothic', 20)
        )
        entry_transfer_amount.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        transfer_button = customtkinter.CTkButton(
            master=l1,
            width=350,
            height=40,
            text="Transfer",
            command=handle_transfer,
            font=('Century Gothic', 20)
        )
        transfer_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        back_transfer_button = customtkinter.CTkButton(
            master=l1,
            width=350,
            height=40,
            text="Back to Banking",
            command=lambda: main_screen(username, user_info),
            font=('Century Gothic', 20)
        )
        back_transfer_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        
    def view_statement_function():
        for widget in app.winfo_children():
            widget.destroy()

        app.geometry("1280x720")
        app.title('Welcome To WizzBank')

        original_image = Image.open("wizzbank-bg2.png")
        ctk_image = customtkinter.CTkImage(dark_image=original_image, size=original_image.size)

        l1 = customtkinter.CTkLabel(master=app, image=ctk_image)
        l1.pack(fill=tkinter.BOTH, expand=True)

        statement_welcome_label = customtkinter.CTkLabel(
            master=l1,
            text=f"Hi {username}!, Please View Statement Below.",
            font=('Century Gothic', 25)
            )
        statement_welcome_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        statement_available_balance= customtkinter.CTkLabel(
            master=l1,
            text=f"Your Available Balance is: R{float(user_info['Balance']):.2f}",
            font=('Century Gothic', 25)
            )
        statement_available_balance.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        statement_text = customtkinter.CTkTextbox(
            master=l1,
            width=400,
            height=400
            )
        statement_text.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        def send_statement_via_email(username, user_info, user_email):
            transactions = format_transactions(username)
            subject = "Your WizzBank Account Statement"
            message = f"Dear {username},\n\nHere is your account statement:\n\nTransactions:\n{transactions}\n\nAvailable Balance: R{float(user_info['Balance']):.2f}\n\nThank you for using WizzBank.\n\nRegards,\nThe WizzBank Team"
            send_email(user_email, subject, message)
            messagebox.showinfo("Email Sent", "Your statement has been sent to your email.")

        def format_transactions(username):
            try:
                with open("Transactions.txt", "r") as file:
                    transactions = [line.strip() for line in file if line.strip().startswith(f"Username: {username}")]
                    return "\n".join(transactions) if transactions else "No transactions found"
            except FileNotFoundError:
                return "No transactions found"

        def load_transactions():
            try:
                with open("Transactions.txt", "r") as file:
                    transactions = [line.strip() for line in file if line.strip().startswith(f"Username: {username}")]
                
                if transactions:
                    statement_text.insert(tkinter.END, "\n".join(transactions))
                else:
                    statement_text.insert(tkinter.END, "No transactions found")
            except FileNotFoundError:
                statement_text.insert(tkinter.END, "No transactions found")
                # Make the textbox read-only
                statement_text.configure(state='disabled')
        
        # Load transactions on startup
        load_transactions()

        email_statement_button = customtkinter.CTkButton(
        master=l1,
        width=350,
        height=40,
        text="Email Statement",
        command=lambda: send_statement_via_email(username, user_info, user_info['Email']),
        font=('Century Gothic', 20)
        )
        email_statement_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        back_statement_button=customtkinter.CTkButton(
            master=l1,  
            width=350,
            height=40,
            text="Back to Banking",
            command=lambda: main_screen(username, user_info),
            font=('Century Gothic', 20)
            )
        back_statement_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    withdraw_button=customtkinter.CTkButton(
        master=l1,
        width=220,
        height=40,
        text="Withdraw",
        command=withdraw_function,
        font=('Century Gothic', 20),
        )
    withdraw_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    
    transfer_button=customtkinter.CTkButton(
        master=l1,
        width=220,
        height=40,
        text="Transfer",
        command=transfer_function,
        font=('Century Gothic', 20),
        )
    transfer_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    
    statement_button=customtkinter.CTkButton(
        master=l1,
        width=220,
        height=40,
        text="View Statement",
        command=view_statement_function,
        font=('Century Gothic', 20)
        )
    statement_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    
    login_button=customtkinter.CTkButton(
        master=l1,
        width=220,
        height=40,
        text="Logout",
        command=login_screen,
        font=('Century Gothic', 20),
        )
    login_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        ctk_resized_image = customtkinter.CTkImage(dark_image=resized_image, size=(new_width, new_height))
        l1.configure(image=ctk_resized_image)
        l1.image = ctk_resized_image

    app.bind('<Configure>', resize_image)

login_screen()

def toggle_fullscreen(event=None):
    is_fullscreen = app.attributes("-fullscreen")
    if is_fullscreen:
        app.attributes("-fullscreen", False)
        app.geometry("1280x720")
    else:
        app.attributes("-fullscreen", True)

app.bind("<Escape>", toggle_fullscreen)
app.bind("<F11>", toggle_fullscreen)
app.mainloop()
