from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from matplotlib import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import sqlite3
import matplotlib.pyplot as plt


global apl_type
global apl_values
global apl_cost


def mainmenu():
    apl_type = []
    apl_values = []
    apl_cost = []

    def clean_mainmenu():
        # Enlarge the window
        appwidth = 400
        appheight = 400
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width / 2) - (appwidth / 2)
        y = (screen_height / 2) - (appheight / 2)
        new_win.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
        new_win.maxsize("400", "400")
        new_win.minsize("400", "400")
        #new_win.iconbitmap('audit_energy.ico')
        # Clear window
        list = new_win.place_slaves()
        for widget in list:
            widget.destroy()
    def hide_mainmenu():
        # Hide the widget
        list = new_win.place_slaves()
        for widget in list:
            widget.place_forget()

    def back_page():
        clean_mainmenu()
        appwidth = 400
        appheight = 250
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width / 2) - (appwidth / 2)
        y = (screen_height / 2) - (appheight / 2)
        new_win.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
        new_win.maxsize("400", "250")
        new_win.minsize("400", "250")
        new_win.iconbitmap('audit_energy.ico')
        mmenu_title = Label(mmenu_frame, text="Welcome to Audit Energy v1.0", font=('arial', '12', 'bold')).place(relx=0.5, rely=0.1, anchor="center")
        mmenu_lframe = LabelFrame(mmenu_frame, text="Main Menu").place(relx=0.5, rely=0.58, relheight=0.7, relwidth=0.7, anchor='center')
        desc = Label(mmenu_frame, text="Which one do you want to calculate?").place(relx=0.5, rely=0.41, anchor="center")
        lamp_btn = Button(mmenu_frame, text="Lamp", relief='groove', command=lamp).place(relx=0.5, rely=0.56, relwidth=0.35, anchor="center")
        elecaps_btn = Button(mmenu_frame, text="Electronic Appliances", relief='groove', command=elaps).place(relx=0.5, rely=0.68, relwidth=0.35, anchor="center")
        graph_btn = Button(mmenu_frame, text="Graph", relief="groove", command=graph).place(relx=0.5, rely=0.8, relwidth=0.35, anchor="center")

    def graph():
        def backpage_fromgraph():
            back_page()
            sb.pack_forget()
        def graphit():
            root = Tk()
            root.wm_title("Energy Usage Chart")
            fig = Figure(figsize=(12, 7), dpi=80)
            fig.add_subplot().bar(apl_type, apl_cost)
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
            toolbar.update()
            canvas.mpl_connect(
                "key_press_event", lambda event: print(f"you pressed {event.key}"))
            canvas.mpl_connect("key_press_event", key_press_handler)
            toolbar.pack(side=BOTTOM, fill=X)
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            root.mainloop()

        def delete_list():
            selected = treev.focus()
            temp = treev.item(selected, 'values')
            print(temp)
            apl_type.remove(temp[0])
            apl_values.remove(float(temp[1]))
            apl_cost.remove(float(temp[2]))
            treev.delete(treev.selection())

        clean_mainmenu()
        appwidth = 400
        appheight = 400
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width / 2) - (appwidth / 2)
        y = (screen_height / 2) - (appheight / 2)
        new_win.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
        new_win.maxsize("400", "400")
        new_win.minsize("400", "400")
        new_win.iconbitmap('audit_energy.ico')
        back_btn = Button(mmenu_frame, text='Back', relief='groove', command=backpage_fromgraph).place(relx=0.06, rely=0.08, relwidth=0.1, anchor='w')
        graph_label = Label(mmenu_frame, text="Electronics Appliances", font=('arial', '12', 'bold')).place(relx=0.5, rely=0.08, anchor="center")
        graph_lframe = LabelFrame(mmenu_frame).place(relx=0.5, rely=0.95, relheight=0.75, relwidth=0.91, anchor='s')
        elaps_label2 = Label(mmenu_frame, text="Usage Chart", font=('arial', '12', 'bold')).place(relx=0.5, rely=0.13, anchor="center")
        treev = ttk.Treeview(mmenu_frame, selectmode='browse')
        treev['column'] = ('Appliance', 'Total Energy', 'Total Cost')
        treev.column('#0', width=0, stretch=NO)
        treev.column('Appliance', width=150, anchor=W)
        treev.column('Total Energy', width=90, anchor=W)
        treev.column('Total Cost', width=90, anchor=W)
        treev.heading('#0', text='', anchor=CENTER)
        treev.heading('Appliance', text='Appliance', anchor=CENTER)
        treev.heading('Total Energy', text='Total Energy', anchor=CENTER)
        treev.heading('Total Cost', text='Total Cost', anchor=CENTER)
        for j in range(len(apl_type)):
            aptype = apl_type[j]
            apenergy = apl_values[j]
            apcost = apl_cost[j]
            treev.insert(parent='', index=j, iid=j, text='', values=(str(aptype), float(apenergy), float(apcost)))
        treev.place(relx=0.5, rely=0.52, anchor='center')
        if len(apl_type)>=10:
            sb = Scrollbar(mmenu_frame, orient=VERTICAL)
            sb.pack(side=RIGHT, fill=Y)
            treev.config(yscrollcommand=sb.set)
            sb.config(command=treev.yview)

        del_button = Button(mmenu_frame, text='Delete', relief='groove', command=delete_list).place(relx=0.37, rely=0.88, relwidth=0.25, anchor='center')
        graph_button = Button(mmenu_frame, text='Graph it!', relief='groove', command=graphit).place(relx=0.62, rely=0.88, relwidth=0.25, anchor='center')

    def lamp():
        def save_item():
            lamp_type = str(entry_pow.get())
            title = 'Lamp ' + lamp_type + ' W'
            apl_type.append(title)
            apl_cost.append(float(cost))
            apl_values.append(float(values))
            print(apl_type)
            print(apl_cost)
            print(apl_values)
        def calculate_lamp():
            try:
                # Deleting result space
                tc_result.configure(mmenu_frame, state='normal')
                tc_result.delete(1.0, END)
                tc_result.configure(mmenu_frame, state='disabled')
                te_result.configure(mmenu_frame, state='normal')
                te_result.delete(1.0, END)
                te_result.configure(mmenu_frame, state='disabled')
                # Carrying value
                quantity=float(spin_qty.get())
                hours=float(spin_use.get())
                power=float(entry_pow.get())
                cosperkwh=float(entry_cost.get(1.0, END))
                # Calculating
                te=str(((quantity*(power*hours))/1000.0))
                tc=str((((quantity*(power*hours))/1000.0)*cosperkwh))
                # Displaying result
                tc_result.configure(mmenu_frame, state='normal')
                tc_result.insert(1.0, tc)
                tc_result.configure(mmenu_frame, state='disabled')
                te_result.configure(mmenu_frame, state='normal')
                te_result.insert(1.0, te)
                te_result.configure(mmenu_frame, state='disabled')
                global values
                global cost
                values = te
                cost = tc

            except:
                # Display information dialog
                messagebox.showinfo("Information", "Please fill the blank field!")
            return
        def reset():
            # Deleting all value
            spin_qty.delete(0, END)
            spin_use.delete(0, END)
            entry_pow.delete(0, END)

            tc_result.configure(mmenu_frame, state='normal')
            tc_result.delete(1.0, END)
            tc_result.configure(mmenu_frame, state='disabled')

            te_result.configure(mmenu_frame, state='normal')
            te_result.delete(1.0, END)
            te_result.configure(mmenu_frame, state='disabled')
            return

        # Clear widget
        clean_mainmenu()
        # Title
        lamp_title = Label(mmenu_frame, text="Lamp Energy Calculation", font=('arial', '12', 'bold')).place(relx=0.5, rely=0.08, anchor="center")
        # Back Button
        back_btn = Button(mmenu_frame, text='Back', relief='groove', command=back_page).place(relx=0.06, rely=0.08, relwidth=0.1, anchor='w')
        # Make labelframe
        lamp_lframe = LabelFrame(mmenu_frame).place(relx=0.5, rely=0.55, relheight=0.8, relwidth=0.88, anchor='center')
        # Quantity
        qty_label = Label(mmenu_frame, text='Quantity', font=('arial', '10')).place(relx=0.13, rely=0.24, anchor='w')
        spin_qty = Spinbox(mmenu_frame, from_=0, to=1000000, relief='flat')
        spin_qty.place(relx=0.85, rely=0.24, relwidth=0.15, anchor='e')
        # Power
        pwr_label = Label(mmenu_frame, text='Power Consumption (Watt)', font=('arial', '10')).place(relx=0.13, rely=0.34, anchor='w')
        entry_pow = Entry(mmenu_frame, relief='flat')
        entry_pow.place(relx=0.85, rely=0.34, relwidth=0.15, anchor='e')
        # Use
        uselbl = Label(mmenu_frame, text='Use per day (Hours)', font=('arial', '10')).place(relx=0.13, rely=0.44, anchor='w')
        spin_use = Spinbox(mmenu_frame, from_=0, to=24, relief='flat')
        spin_use.place(relx=0.85, rely=0.44, relwidth=0.15, anchor='e')
        # Cost
        label_cost = Label(mmenu_frame, text='Cost per kWh (Rupiah)', font=('arial', '10')).place(relx=0.13, rely=0.54, anchor='w')
        entry_cost = Text(mmenu_frame, state='normal', relief='flat')
        entry_cost.place(relx=0.85, rely=0.54, relwidth=0.15, relheight=0.05, anchor='e')
        entry_cost.insert(1.0, '1500')
        entry_cost.configure(state='disabled')
        # Calculate and Reset button
        cal_button = Button(mmenu_frame, text='Calculate', relief='groove', command=calculate_lamp).place(relx=0.25, rely=0.64, relwidth=0.25, anchor='center')
        sav_button = Button(mmenu_frame, text='Save All', relief='groove', command=save_item).place(relx=0.5, rely=0.64, relwidth=0.25, anchor='center')
        res_button = Button(mmenu_frame, text='Reset', relief='groove', command=reset).place(relx=0.75, rely=0.64, relwidth=0.25, anchor='center')
        # Result section
        tc_label = Label(mmenu_frame, text='Total Cost (Rupiah)', font=('arial', '10')).place(relx=0.15, rely=0.74, anchor='w')
        tc_result = Text(mmenu_frame, state='disabled', relief='flat')
        tc_result.place(relx=0.82, rely=0.74, relwidth=0.26, relheight=0.05, anchor='e')
        te_label = Label(mmenu_frame, text='Total Energy (kWh)', font=('arial', '10')).place(relx=0.15, rely=0.84, anchor='w')
        te_result = Text(mmenu_frame, state='disabled', relief='flat')
        te_result.place(relx=0.82, rely=0.84, relwidth=0.26, relheight=0.05, anchor='e')

    def elaps():
        def save():
            apl_type.append(appliance)
            apl_cost.append(float(cost))
            apl_values.append(float(values))
            print(apl_type)
            print(apl_cost)
            print(apl_values)
        def calculate_elaps():
            try:
                # Deleting result space
                tc_result.configure(mmenu_frame, state='normal')
                tc_result.delete(1.0, END)
                tc_result.configure(mmenu_frame, state='disabled')
                te_result.configure(mmenu_frame, state='normal')
                te_result.delete(1.0, END)
                te_result.configure(mmenu_frame, state='disabled')
                # Carrying value
                quantity=float(spin_qty.get())
                hours=float(spin_use.get())
                power=float(apl_pow.get(1.0, END))
                cosperkwh=float(entry_cost.get(1.0, END))
                # Calculating
                te=str(((quantity*(power*hours))/1000.0))
                tc=str((((quantity*(power*hours))/1000.0)*cosperkwh))
                # Displaying result
                tc_result.configure(mmenu_frame, state='normal')
                tc_result.insert(1.0, tc)
                tc_result.configure(mmenu_frame, state='disabled')
                te_result.configure(mmenu_frame, state='normal')
                te_result.insert(1.0, te)
                te_result.configure(mmenu_frame, state='disabled')
                global values
                global cost
                values = te
                cost = tc
            except:
                # Display information dialog
                messagebox.showinfo("Information", "Please fill the blank field!")
            return
        def reset_elaps():
            # Deleting all value
            spin_qty.delete(0, END)
            spin_use.delete(0, END)
            apl_pow.configure(mmenu_frame, state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.configure(mmenu_frame, state='disabled')
            tc_result.configure(mmenu_frame, state='normal')
            tc_result.delete(1.0, END)
            tc_result.configure(mmenu_frame, state='disabled')
            te_result.configure(mmenu_frame, state='normal')
            te_result.delete(1.0, END)
            te_result.configure(mmenu_frame, state='disabled')
            return
        def refr():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '150')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Refrigerator'
        def washm():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '350')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Washing Machine'
        def watrp():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '300')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Water Pump'
        def airc():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '700')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'AC'
        def fan():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '60')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Fan'
        def telev():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '50')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'TV'
        def microw():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '800')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Microwave'
        def ricook():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '380')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Rice Cooker'
        def blend():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '250')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Blender'
        def watheat():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '1200')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Water Heater'
        def estove():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '600')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Stove'
        def deskcom():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '200')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'PC'
        def iron():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '350')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Iron'
        def vacclean():
            apl_pow.configure(state='normal')
            apl_pow.delete(1.0, END)
            apl_pow.insert(1.0, '1200')
            apl_pow.configure(state='disabled')
            global appliance
            appliance = 'Vacuum'
        def cust1():
            global appliance
            apl_pow.configure(state='normal')
            appliance = 'Custom 1'
        def cust2():
            global appliance
            apl_pow.configure(state='normal')
            appliance = 'Custom 2'

        # Clear widget
        clean_mainmenu()
        # Title
        elaps_label = Label(mmenu_frame, text="Electronic Appliances", font=('arial', '12', 'bold')).place(relx=0.5, rely=0.08, anchor="center")
        elaps_label2 = Label(mmenu_frame, text="Energy Calculation", font=('arial', '12', 'bold')).place(relx=0.5, rely=0.13, anchor="center")
        # Back Button
        back_btn = Button(mmenu_frame, text='Back', relief='groove', command=back_page).place(relx=0.06, rely=0.08, relwidth=0.1, anchor='w')
        # Labelframe
        elaps_lframe = LabelFrame(mmenu_frame).place(relx=0.5, rely=0.95, relheight=0.75, relwidth=0.9, anchor='s')
        # Type of appliance
        apl_label = Label(mmenu_frame, text='Appliance Type', font=('arial', '10')).place(relx=0.13, rely=0.28, anchor='w')
        apl_choice = Menubutton(mmenu_frame, text='Choose', relief='raised')
        apl_choice.place(relx=0.85, rely=0.28, relwidth=0.15, anchor='e')
        apl_choice.menu = Menu(apl_choice, tearoff=0)
        apl_choice['menu'] = apl_choice.menu
        apl_choice.menu.add_command(label='Refrigerator', command=refr)
        apl_choice.menu.add_command(label='Washing Machine', command=washm)
        apl_choice.menu.add_command(label='Water Pump', command=watrp)
        apl_choice.menu.add_command(label='Air Conditioner', command=airc)
        apl_choice.menu.add_command(label='Fan', command=fan)
        apl_choice.menu.add_command(label='Television', command=telev)
        apl_choice.menu.add_command(label='Microwave', command=microw)
        apl_choice.menu.add_command(label='Rice Cooker', command=ricook)
        apl_choice.menu.add_command(label='Blender', command=blend)
        apl_choice.menu.add_command(label='Water Heater', command=watheat)
        apl_choice.menu.add_command(label='Electric Stove', command=estove)
        apl_choice.menu.add_command(label='Desktop Computer', command=deskcom)
        apl_choice.menu.add_command(label='Iron', command=iron)
        apl_choice.menu.add_command(label='Vacuum Cleaner', command=vacclean)
        apl_choice.menu.add_separator()
        apl_choice.menu.add_command(label='Custom 1', command=cust1)
        apl_choice.menu.add_command(label='Custom 2', command=cust2)
        # Quantity
        qty_label = Label(mmenu_frame, text='Quantity', font=('arial', '10')).place(relx=0.13, rely=0.36, anchor='w')
        spin_qty = Spinbox(mmenu_frame, from_=0, to=1000000, relief='flat')
        spin_qty.place(relx=0.85, rely=0.36, relwidth=0.15, anchor='e')
        # Power
        pwr_label = Label(mmenu_frame, text='Power Consumption (Watt)', font=('arial', '10')).place(relx=0.13, rely=0.44, anchor='w')
        apl_pow = Text(mmenu_frame, state='disabled', relief='flat')
        apl_pow.place(relx=0.85, rely=0.44, relwidth=0.15, relheight=0.05, anchor='e')
        # Use
        uselbl = Label(mmenu_frame, text='Use per day (Hours)', font=('arial', '10')).place(relx=0.13, rely=0.52, anchor='w')
        spin_use = Spinbox(mmenu_frame, from_=0, to=24, relief='flat')
        spin_use.place(relx=0.85, rely=0.52, relwidth=0.15, anchor='e')
        # Cost
        label_cost = Label(mmenu_frame, text='Cost per kWh (Rupiah)', font=('arial', '10')).place(relx=0.13, rely=0.6, anchor='w')
        entry_cost = Text(mmenu_frame, state='normal', relief='flat')
        entry_cost.place(relx=0.85, rely=0.6, relwidth=0.15, relheight=0.05, anchor='e')
        entry_cost.insert(1.0, '1500')
        entry_cost.configure(state='disabled')
        # Calculate and Reset button
        cal_button = Button(mmenu_frame, text='Calculate', relief='groove', command=calculate_elaps).place(relx=0.25, rely=0.7, relwidth=0.25, anchor='center')
        sav_button = Button(mmenu_frame, text='Save', relief='groove', command=save).place(relx=0.5, rely=0.7, relwidth=0.25, anchor='center')
        res_button = Button(mmenu_frame, text='Reset', relief='groove', command=reset_elaps).place(relx=0.75, rely=0.7, relwidth=0.25, anchor='center')
        # Result section
        tc_label = Label(mmenu_frame, text='Total Cost (Rupiah)', font=('arial', '10')).place(relx=0.15, rely=0.8, anchor='w')
        tc_result = Text(mmenu_frame, state='disabled', relief='flat')
        tc_result.place(relx=0.82, rely=0.8, relwidth=0.26, relheight=0.05, anchor='e')
        te_label = Label(mmenu_frame, text='Total Energy (kWh)', font=('arial', '10')).place(relx=0.15, rely=0.88, anchor='w')
        te_result = Text(mmenu_frame, state='disabled', relief='flat')
        te_result.place(relx=0.82, rely=0.88, relwidth=0.26, relheight=0.05, anchor='e')

    # Make new window
    new_win = Tk()
    appwidth = 400
    appheight = 250
    screen_width = new_win.winfo_screenwidth()
    screen_height = new_win.winfo_screenheight()
    x = (screen_width / 2) - (appwidth / 2)
    y = (screen_height / 2) - (appheight / 2)
    new_win.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
    new_win.maxsize("400", "250")
    new_win.minsize("400", "250")
    new_win.title("Audit Energy v1.0")
    #new_win.iconbitmap('audit_energy.ico')
    mmenu_frame = Frame(new_win).pack(expand='yes', fill='both')
    mmenu_title = Label(mmenu_frame, text="Welcome to Audit Energy v1.0", font=('arial', '12', 'bold')).place(relx=0.5, rely=0.1, anchor="center")
    mmenu_lframe = LabelFrame(mmenu_frame, text="Main Menu").place(relx=0.5, rely=0.58, relheight=0.7, relwidth=0.7, anchor='center')
    desc = Label(mmenu_frame, text="Which one do you want to calculate?").place(relx=0.5, rely=0.41, anchor="center")
    lamp_btn = Button(mmenu_frame, text="Lamp", relief='groove', command=lamp).place(relx=0.5, rely=0.56, relwidth=0.35, anchor="center")
    elecaps_btn = Button(mmenu_frame, text="Electronic Appliances", relief='groove', command=elaps).place(relx=0.5, rely=0.68, relwidth=0.35, anchor="center")
    graph_btn = Button(mmenu_frame, text="Graph", relief="groove", command=graph).place(relx=0.5, rely=0.8, relwidth=0.35, anchor="center")


def signup_btn():
    def clean_loguppage():
        # Clear window
        list = win.place_slaves()
        for widget in list:
            widget.destroy()
    def hide_loguppage():
        # Hide the widget
        list = win.place_slaves()
        for widget in list:
            widget.place_forget()
    def add_new_account():
        if uname.get()=='' and passw.get()=='':
            messagebox.showinfo("Information", "Please fill the username and password")
        else:
            audit_db = sqlite3.connect('audit_account.db')
            adb = audit_db.cursor()
            adb.execute("INSERT INTO ACCOUNT(username, password) VALUES(?,?)",(uname.get(), passw.get()))
            audit_db.commit()
            audit_db.close()
            messagebox.showinfo("Information", "Account Created!")
            clean_loguppage()
            login_page()

    hide_loguppage()
    login_frame = Frame(win).pack(expand='yes', fill='both')
    logup_title = Label(login_frame, text="Audit Energy v1.0", font=("arial", "12", "bold")).place(relx=0.5, rely=0.1, anchor="center")
    logup_lframe = LabelFrame(login_frame, text="Sign Up").place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.6, anchor='center')
    nname = Label(logup_lframe, text='New Username').place(relx=0.23, rely=0.4, anchor='w')
    nentry_name = Entry(logup_lframe, relief='flat', textvariable=uname).place(relx=0.6, rely=0.4, anchor='center')
    npasw = Label(logup_lframe, text='New Password').place(relx=0.23, rely=0.53, anchor='w')
    nentry_pasw = Entry(logup_lframe, relief='flat', textvariable=passw, show='*').place(relx=0.6, rely=0.53, anchor='center')
    siup_btn = Button(logup_lframe, text='Sign Up', padx=15, relief='groove', command=add_new_account).place(relx=0.66, rely=0.68, anchor='center')


def signin_btn():
    # Check username and password
    audit_db = sqlite3.connect('audit_account.db')
    adb = audit_db.cursor()
    adb.execute("SELECT * FROM ACCOUNT WHERE username=? AND password=?",(uname.get(), passw.get()))
    con = adb.fetchone()
    if con:
        messagebox.showinfo("Information", "Login Success")
        parent_id = con[0]
        # Remove login window
        win.destroy()
        # Main menu
        mainmenu()
    else:
        messagebox.showinfo("Information", "Login Failed")
    audit_db.commit()
    audit_db.close()
    #win.destroy()
    #mainmenu()


def login_page():
    login_frame = Frame(win).pack(expand='yes', fill='both')
    login_title = Label(login_frame, text="Audit Energy v1.0", font=("arial", "12","bold")).place(relx=0.5,rely=0.1,anchor="center")
    login_lframe = LabelFrame(login_frame, text="Login").place(relx=0.5,rely=0.5,relheight=0.6,relwidth=0.6,anchor='center')
    name = Label(login_lframe, text='Username').place(relx=0.23,rely=0.4,anchor='w')
    entry_name = Entry(login_lframe, relief='flat', textvariable=uname).place(relx=0.6,rely=0.4,anchor='center')
    pasw = Label(login_lframe, text='Password').place(relx=0.23,rely=0.53,anchor='w')
    entry_pasw = Entry(login_lframe, relief='flat', textvariable=passw, show='*').place(relx=0.6,rely=0.53,anchor='center')
    login_btn = Button(login_lframe, text='Sign in', padx=15, relief='groove', command=signin_btn).place(relx=0.66,rely=0.68,anchor='center')
    sigup_lbl = Label(login_frame, text='Don\'t have an account?').place(relx=0.42,rely=0.88,anchor='center')
    sigup_btn = Button(login_frame, text='Sign Up', relief='flat', fg='#2596be', command=signup_btn).place(relx=0.65,rely=0.88,anchor='center')

## Starting point ##
win = Tk()
appwidth = 400
appheight = 250
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
x = (screen_width/2)-(appwidth/2)
y = (screen_height/2)-(appheight/2)
win.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
win.maxsize("400","250")
win.minsize("400","250")
win.title("Audit Energy v1.0")
#win.iconbitmap('audit_energy.ico')
uname=StringVar()
passw=StringVar()
# Create SQLite database
audit_db = sqlite3.connect('audit_account.db')
adb = audit_db.cursor()
adb.execute("CREATE TABLE IF NOT EXISTS ACCOUNT(userid INTEGER PRIMARY KEY, username text, password text)")
adb.execute("SELECT * FROM ACCOUNT")
check = adb.fetchall()
if check == []:
    adb.execute("INSERT INTO ACCOUNT(username, password) VALUES(?,?)",('admin', 'admin'))
    # Login page
    login_page()
else:
    # Login page
    login_page()
audit_db.commit()
audit_db.close()

win.mainloop()
