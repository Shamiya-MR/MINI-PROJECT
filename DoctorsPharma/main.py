import fileinput
from sqlite3 import DatabaseError
from flask import Flask, render_template, request, session
from DBConnection import Db
import datetime
import time

app=Flask(__name__)
app.secret_key="hello"

staticpath = "E:\\DoctorsPharma1\\DoctorsPharma\\static\\"

@app.route('/')
def hello():
    return render_template('Admin/index.html')

@app.route('/login')
def login():
    return render_template('login_index.html')

@app.route('/login_post', methods=['post'])
def login_post():
    username = request.form['textfield']
    password = request.form['textfield2']
    a = Db()
    qry = "SELECT * FROM `login` WHERE user_name='"+username+"' AND `password`='"+password+"'"
    res = a.selectOne(qry)
    if res!=None:
        session['lid'] = res['login_id']
        if res['type']=='admin':
            return '''<script>alert('Login Success');window.location='/ad_home'</script>'''
        elif res['type']=='dealer':
            return '''<script>alert('Login Success');window.location='/dealer_home'</script>'''
        elif res['type']=='user':
            return '''<script>alert('Login Success');window.location='/home'</script>'''
        else:
            return '''<script>alert('Invalid user');window.location='/login'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/login'</script>'''


@app.route('/adm_home')
def adm_home():
    return render_template('Admin/inner-page.html')
@app.route('/ad_home')
def ad_home():
    return render_template('Admin/Home.html')

@app.route('/changePassword')
def changePassword():
    return render_template('Admin/Change_password.html')

@app.route('/changePassword_post', methods=['post'])
def changePassword_post():
    current = request.form['textfield']
    new = request.form['textfield2']
    confirm = request.form['textfield3']
    a = Db()
    qry = "SELECT * FROM login WHERE `password`='"+current+"'"
    res = a.selectOne(qry)
    if res!=None:
        if new==confirm:
            qry ="update login set password ='"+confirm+"' where login_id='"+str(session['lid'])+"'"
            res = a.update(qry)
            return '''<script>alert('Password created');window.location='/login'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/changePassword'</script>'''
    else:
        return '''<script>alert('Current password must be valid');window.location='/changePassword'</script>'''


@app.route('/viewComplaint')
def view_complaint():
    a = Db()
    qry = "SELECT `complaint`.*, `user`.`user_name`,`user`.`email` FROM `user` INNER JOIN `complaint` ON `complaint`.`user_id`=`user`.`login_id`"
    res = a.select(qry)
    return render_template('Admin/View_complaint.html', data=res)

@app.route('/viewComplaint_post', methods=['post'])
def viewcomplaint_post():
    a = Db()
    frm = request.form['textfield']
    to = request.form['textfield2']
    qry = "SELECT `complaint`.*, `user`.`user_name`,`user`.`email` FROM `user` INNER JOIN `complaint` ON `complaint`.`user_id`=`user`.`login_id` where date between '"+frm+"' and '"+to+"' "
    res = a.select(qry)
    return render_template('Admin/View_complaint.html', data=res)


@app.route('/sendRply/<cid>')
def SendReply(cid):
    a = Db()
    qry = "SELECT * FROM `complaint` WHERE `complaint_id`='"+cid+"'"
    res = a.selectOne(qry)
    return render_template('Admin/Send_reply.html', data=res)

@app.route('/sendrply_post', methods=['post'])
def sendrply_post():
    c_id = request.form['com_id']
    rply = request.form['textarea']
    a = Db()
    qry = "UPDATE complaint SET reply='"+rply+"',STATUS='replied' WHERE `complaint_id`='"+c_id+"'"
    res = a.update(qry)
    return '''<script>alert('Replied');window.location='/viewComplaint'</script>'''

@app.route('/view_user')
def viewUser():
    a = Db()
    qry = "SELECT * FROM `user`"
    res = a.select(qry)
    return render_template('Admin/View_users.html', data=res)
#
# @app.route('/search_user', methods=['post'])
# def searchUser():
#     search = request.form['textfield']
#     return render_template('Admin/View_users.html')

@app.route('/dealer_home')
def dealer_home():
    return render_template('Dealer/inner-page.html')

@app.route('/dealer_changePassword')
def dealer_changePassword():
    return render_template('Dealer/Change_password.html')

@app.route('/dealer_changePassword_post', methods=['post'])
def dealer_changePassword_post():
    current = request.form['textfield']
    new = request.form['textfield2']
    confirm = request.form['textfield3']
    a = Db()
    qry = "SELECT * FROM login WHERE `password`='"+current+"'"
    res = a.selectOne(qry)
    if res!=None:
        if new==confirm:
            qry ="update login set password ='"+confirm+"' where login_id='"+str(session['lid'])+"'"
            res = a.update(qry)
            return '''<script>alert('Password created');window.location='/login'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/dealer_changePassword'</script>'''
    else:
        return '''<script>alert('Current password must be valid');window.location='/dealer_changePassword'</script>'''

@app.route('/dealer_addmedicines')
def dealer_addmedicines():
    return render_template('Dealer/add_product.html')

@app.route('/dealer_addmedicines_post',methods=['POST'])
def dealer_addmedicines_post():
    name=request.form["textfield"]
    brand=request.form["textfield2"]
    dose=request.form["textfield3"]
    Prescription=request.form["textfield4"]
    side=request.form["side"]
    cost=request.form["textfield33"]
    db=Db()
    qry="insert into medicine(name,brand,dose,prescription,side_effect,cost)values('"+name+"','"+brand+"','"+dose+"','"+Prescription+"','"+side+"','"+cost+"')"
    mid=db.insert(qry)
    qrr="insert into stock(medicine_id,quantity,date)values('"+str(mid)+"','10',curdate())"
    db.insert(qrr)
    return '''<script>alert('Success');window.location='/dealer_addmedicines'</script>'''

@app.route('/dealer_viewmedicines')
def dealer_viewmedicines():
    db=Db()
    qry="select * from medicine"
    dres=db.select(qry)
    return render_template('Dealer/view_product.html',data=dres)

@app.route('/dealer_viewmedicines_post',methods=['POST'])
def dealer_viewmedicines_post():
    name=request.form["name"]
    db=Db()
    qry="select * from medicine where name like '%"+name+"%'"
    dres=db.select(qry)
    return render_template('Dealer/view_product.html',data=dres)

@app.route('/dealer_deletemedicines/<id>')
def dealer_deletemedicines(id):
    db=Db()
    qry="delete from medicine where medicine_id='"+id+"'"
    dres=db.delete(qry)
    return dealer_viewmedicines()

@app.route('/dealer_editmedicines/<id>')
def dealer_editmedicines(id):
    db=Db()
    qry="select * from medicine where medicine_id='"+id+"'"
    dres=db.selectOne(qry)
    return render_template('Dealer/edit_product.html',data=dres)

@app.route('/dealer_updatemedicines_post',methods=['POST'])
def dealer_updatemedicines_post():
    name=request.form["textfield"]
    brand=request.form["textfield2"]
    dose=request.form["textfield3"]
    Prescription=request.form["textfield4"]
    side=request.form["side"]
    cost=request.form["textfield33"]
    id=request.form["ii"]
    db=Db()
    qry="update medicine set name='"+name+"',brand='"+brand+"',prescription='"+Prescription+"',side_effect='"+side+"',dose='"+dose+"',cost='"+cost+"' where medicine_id ='"+id+"'"
    db.update(qry)
    return '''<script>alert('Success');window.location='/dealer_viewmedicines'</script>'''

@app.route('/dealer_view_order_and_payment_details')
def store_view_order_and_payment_details():
    c=Db()
    qry="select order_main.*,user.* from user inner join order_main on order_main.user_id=user.login_id"
    r=c.select(qry)
    ##print(r)
    return render_template("Dealer/view_order_and_payment_details.html",data=r)

@app.route('/store_view_order_and_payment_details_more/<nn>')
def seller_view_order_and_payment_details_more(nn):
    c=Db()
    qry2="select order_main.*,user.* from user inner join order_main on order_main.user_id=user.login_id where  `order_main`.order_id='"+nn+"'"
    res2=c.selectOne(qry2)
    qry2="select * from delivery_address where order_id='"+nn+"'"
    res5=c.selectOne(qry2)
    qry3="select order_sub.sub_id as os_id,order_sub.medicine_id,order_sub.count as qqty,medicine.*,medicine.cost*order_sub.count as price from order_sub inner join medicine on medicine.medicine_id=order_sub.medicine_id where order_sub.order_main_id='"+nn+"'"
    res3=c.select(qry3)
    session["order_id"]=nn
    ##print(qry3)
    total = 0
    for nn in res3:
        total = total + float(nn['price'])
        ##print("-----------", total)
    # qry4="update order_main set total='"+str(totalamou)+"' where o_id='"+nn+"'"
    # res4=c.update(qry4)
    ##print(res3)
    return  render_template("Dealer/more_option_assign_order.html",data2=res2,data3=res3,tot=total,data5=res5)

@app.route('/update_status',methods=["post"])
def update_status():
    db=Db()
    qry="update delivery_address set status='Order Shipped',date=curdate() where order_id='"+str(session["order_id"])+"'"
    dres=db.update(qry)
    return store_view_order_and_payment_details()

@app.route('/dealer_viewstock')
def dealer_viewstock():
    db=Db()
    qry="select * from medicine inner join stock on stock.medicine_id=medicine.medicine_id"
    dres=db.select(qry)
    return render_template('Dealer/viewstock.html',data=dres)

@app.route('/dealer_viewstock_post',methods=["post"])
def dealer_viewstock_post():
    db=Db()
    name=request.form["name"]
    qry="select * from medicine inner join stock on stock.medicine_id=medicine.medicine_id where name like '%"+name+"%'"

    dres=db.select(qry)
    return render_template('Dealer/viewstock.html',data=dres)

@app.route('/update_stock/<id>')
def update_stock(id):
    db=Db()
    qry="select * from medicine where medicine_id='"+id+"'"
    dres=db.selectOne(qry)
    return render_template('Dealer/update_stock.html',data=dres)

@app.route('/dealer_updatestock_post',methods=["POST"])
def dealer_updatestock_post():
    db=Db()
    medicine_id=request.form["mid"]
    count=request.form["textfield33"]
    qry="update stock set quantity=quantity+'"+count+"' ,date=curdate() where medicine_id='"+medicine_id+"'"
    dres=db.update(qry)
    return dealer_viewstock()

@app.route('/dealer_viewoutstock')
def dealer_viewoutstock():
    db=Db()
    qry="select * from medicine inner join stock on stock.medicine_id=medicine.medicine_id where stock.quantity<20"
    dres=db.select(qry)
    return render_template('Dealer/view out of stock.html',data=dres)

@app.route('/signup')
def signup():
    return render_template('user/signup_index.html')

@app.route('/signup_post', methods=['post'])
def signup_post():
    img = request.files['filefield']
    # dt = time.strftime("Y%m%d-%H%M%S%")
    # img.save(staticpath+"user_img\\"+dt+".jpg")
    # path = "/static/user_img/"+dt+".jpg"
    img.save(staticpath + "user_img\\" + img.filename)
    path = "/static/user_img/" + img.filename
    name = request.form['n1']
    email = request.form['n2']
    phone = request.form['n3']
    dob = request.form['n4']
    gender = request.form['n5']
    place = request.form['n6']
    post = request.form['n7']
    district = request.form['n8']
    pin = request.form['n9']
    pswrd = request.form['n10']
    cnf_pswrd = request.form['n11']

    d = Db()
    if pswrd==cnf_pswrd:
        qry = "insert into login(user_name,password,type) values('"+email+"','"+pswrd+"','user')"
        res = d.insert(qry)
        qry1 = "insert into user(user_name,email,phone,dob,gender,place,post,district,pin,photo,login_id) values('"+name+"','"+email+"','"+phone+"','"+dob+"','"+gender+"','"+place+"','"+post+"','"+district+"','"+pin+"','"+path+"','"+str(res)+"')"
        res1 = d.insert(qry1)
        return '''<script>alert('Sign Up Successfully');window.location='/login'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/signup'</script>'''

@app.route('/home')
def home():
    return render_template('user/inner-page.html')
@app.route('/view_profile')
def view_profile():
    d = Db()
    qry = "select * from user where login_id='"+str(session['lid'])+"'"
    res = d.selectOne(qry)
    print(res)
    return render_template('user/view_profile.html', data=res)

@app.route('/edit_profile/<id>')
def edit_profile(id):
    d = Db()
    qry = "select * from user where login_id='"+id+"'"
    res = d.selectOne(qry)
    return render_template('user/edit_profile.html', data=res)

@app.route('/edit_profile_post', methods=['post'])
def edit_profile_post():
    id = request.form['uslid']
    name = request.form['n1']
    email = request.form['n2']
    phone = request.form['n3']
    dob = request.form['n4']
    gender = request.form['n5']
    place = request.form['n6']
    post = request.form['n7']
    district = request.form['n8']
    pin = request.form['n9']
    d = Db()
    if 'fileField' in request.files:
        img = request.files['filefield']
        if img.filename !="":
            dt = time.strftime("Y%m%d-%H%M%S")
            img.save(staticpath + "user_img\\" + dt + ".jpg")
            path = "/static/user_img/" + dt + ".jpg"
            qry ="update user set user_name='"+name+"', email='"+email+"', phone='"+phone+"', dob='"+dob+"', gender='"+gender+"', place='"+place+"', post='"+post+"',district='"+district+"', pin='"+pin+"', photo='"+path+"' where login_id='"+id+"'"
            res = d.update(qry)
            print("1",res)

            return '''<script>alert('Profile updated');window.location='/view_profile'</script>'''
        else:
            qry = "update user set user_name='" + name + "', email='" + email + "', phone='" + phone + "', dob='" + dob + "', gender='" + gender + "', place='" + place + "', post='" + post + "',district='" + district + "', pin='" + pin + "' where login_id='" + id + "'"
            res = d.update(qry)
            print("2",res)
            return '''<script>alert('Profile updated');window.location='/view_profile'</script>'''
    else:
        qry = "update user set user_name='" + name + "', email='" + email + "', phone='" + phone + "', dob='" + dob + "', gender='" + gender + "', place='" + place + "', post='" + post + "',district='" + district + "', pin='" + pin + "' where login_id='" + id + "'"
        res = d.update(qry)
        print("3",res)
        return '''<script>alert('Profile updated');window.location='/view_profile'</script>'''

@app.route('/user_changePassword')
def user_changePassword():
    return render_template('user/Change_password.html')

@app.route('/user_changePassword_post', methods=['post'])
def user_changePassword_post():
    cp =request.form['textfield']
    np = request.dform['textfield2']
    cnp = request.form['textfield3']
    d = Db()
    qry = "select * from login where password='"+cp+"'"
    res = d.selectOne(qry)
    if res!=None:
        if np==cnp:
            qry = "Update login set password='"+cnp+"' where login_id='"+str(session['lid'])+"'"
            res = d.update(qry)
            return '''<script>alert('Password Changed');window.location='/login'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/user_changePassword'</script>'''
    else:
        return '''<script>alert('Password mismatch');window.location='/user_changePassword'</script>'''

@app.route('/view_med')
def view_med():
    d = Db()
    qry = "SELECT * FROM medicine"
    res = d.select(qry)
    return render_template('user/view_medicine.html', data=res)

@app.route('/user_viewmedicines_post', methods=['post'])
def user_viewmedicines_post():
    search = request.form['name']
    d = Db()
    qry = "SELECT * FROM medicine where name like '%"+search+"%'"
    res = d.select(qry)
    return render_template('user/view_medicine.html', data=res)

@app.route('/add_cart/<id>')
def add_cart(id):
    d = Db()
    qry = "select * from medicine where medicine_id='"+id+"'"
    res = d.selectOne(qry)
    return render_template('user/add_cart.html', data=res)

@app.route('/add_cart_post', methods=['post'])
def add_Cart_post():
    medid = request.form['pid']
    quantity = request.form['textfield']
    d = Db()
    qry = "insert into cart(medicine_id,quantity,ul_id) values('"+medid+"','"+quantity+"','"+str(session['lid'])+"')"
    res = d.insert(qry)
    return '''<script>alert('Added');window.location='/view_med'</script>'''

@app.route('/view_cart')
def view_cart():
    d = Db()
    qry = "select medicine.medicine_id,medicine.name,cart.quantity, cart.cart_id, cart.quantity * medicine.cost as total_amnt from medicine inner join cart on cart.medicine_id=medicine.medicine_id where cart.ul_id='"+str(session['lid'])+"'"
    res = d.select(qry)
    print(res)
    total=0
    for i in res:
            medid=print(i['medicine_id'])
            total+=i["total_amnt"]
            # qry22="select * from medicine where medicine_id='"+medid+"'"
            # print(qry22)
            # res22 = d.select(qry22)
            # print(res)
            # qry = "select * from medicine where medicine_id='"+str(i['medicine_id'])+"'"
            # res = d.select(qry)
            # print(res['price'])
    session["total"]=total
    return render_template('user/view_cart.html', data=res,total=total)

# @app.route('/view_cart_post', methods=['post'])
# def view_cart_post():
#
#     # qry = "select * from cart where ul_id='"+str(session['lid'])+"'"
#     # res = d.select(qry)
#     # a = len(res)
#     # if a>0:
#     #     for i in range(a):
#     #         print(res)
#     #         # qry = "select * from medicine where medicine_id='"+str(i['medicine_id'])+"'"
#     #         # res = d.select(qry)
#     #         # print(res['price'])
#     # print(a)
#     return render_template('user/add_prescription.html')

@app.route('/add_prescription',methods=['post'])
def add_prescription():
    d=Db()
    qq="insert into order_main(user_id,total_amount,prescription,date)values('"+str(session["lid"])+"','"+str(session["total"])+"','',curdate())"
    oid=str(d.insert(qq))
    qry = "select medicine.medicine_id,medicine.name,cart.quantity, cart.cart_id, cart.quantity * medicine.cost as total_amnt from medicine inner join cart on cart.medicine_id=medicine.medicine_id where cart.ul_id='" + str(
        session['lid']) + "'"
    res = d.select(qry)
    print(res)
    for i in res:
        print(i)
        qqr="insert into order_sub(order_main_id,medicine_id,count)values('"+str(oid)+"','"+str(i['medicine_id'])+"','"+str(i["quantity"])+"')"
        d.insert(qqr)
    session["oid"]=oid

    return render_template('user/add_prescription.html',oid=oid)

@app.route('/prescription_post', methods=['post'])
def prescription_post():
    prescription=request.files['presc']
    lat = request.form['l1']
    long = request.form['l2']
    prescription.save(staticpath+"prescription\\"+prescription.filename)
    url = "/static/prescription/"+prescription.filename
    d=Db()
    qq="update order_main set prescription='"+url+"' where order_id='"+str(session["oid"])+"'"
    print(qq)
    res = d.update(qq)
    print(res)
    return render_template('user/payment.html')

@app.route('/purchase')
def purchase():
    return render_template('user/payment.html')

@app.route('/purchase_post',methods=['POST'])
def purchase_post():
    h1 = request.form['t1']
    b1 = request.form['t2']
    p1 = request.form['t3']
    c1 = request.form['t4']
    d1 = request.form['t5']
    s1 = request.form['t6']
    acc=request.form["textfield"]
    pin=request.form["textfield2"]
    d = Db()
    qry="insert into payment (payment_type,amount,account_no,order_main_id)values('Online','"+str(session["total"])+"','"+acc+"','"+str(session["lid"])+"')"
    res = d.insert(qry)
    qry1 = "insert into delivery_address(order_id, house_name,building_no,place,city,district,state,status,date) values('"+str(session['oid'])+"','"+h1+"','"+b1+"','"+p1+"','"+c1+"','"+d1+"','"+s1+"','pending',curdate())"
    res = d.insert(qry1)
    return render_template('user/payment.html')

@app.route('/delete_cart/<id>')
def delete_cart(id):
    d = Db()
    qry = "delete from cart where cart_id='"+id+"'"
    res = d.delete(qry)
    return '''<script>alert('Removed');window.location='/view_cart'</script>'''

@app.route('/edit_cart/<id>')
def edit_cart(id):
    d = Db()
    qry = "select medicine.name,cart.quantity, cart.cart_id, cart.quantity * medicine.cost as total_amnt from medicine inner join cart on cart.medicine_id=medicine.medicine_id where cart.cart_id='"+id+"'"
    res = d.selectOne(qry)
    return render_template('user/edit_Cart.html', data=res)

@app.route('/edit_cart_post', methods=['post'])
def edit_cart_post():
    cid = request.form['cid']
    quantity = request.form['textfield']
    d = Db()
    qry = "update cart set quantity='"+quantity+"' where cart_id='"+cid+"'"
    res = d.update(qry)
    return '''<script>alert('Updated');window.location='/view_cart'</script>'''

@app.route('/view_orderd_product')
def view_orderd_product():
    d = Db()
    qry = "select order_main.*, order_sub.*, delivery_address.*, medicine.* from order_main inner join order_sub on order_sub.order_main_id=order_main.order_id inner join delivery_address on delivery_address.order_id=order_main.order_id inner join medicine on medicine.medicine_id=order_sub.medicine_id where order_main.user_id= '"+str(session['lid'])+"' and delivery_address.status='Order Shipped'"
    res = d.select(qry)
    return render_template('user/view_orderd_products.html', data=res)


@app.route('/return_product/<id>')
def return_product(id):
    d = Db()
    qry = "update delivery_address set status='return' where delivery_id='"+id+"' "
    res = d.update(qry)
    return '''<script>alert('Removed from your order');window.location='/view_orderd_product'</script>'''

@app.route('/view_returned_product')
def view_returned_product():
    d = Db()
    qry = "select order_main.*, order_sub.*, delivery_address.*, medicine.* from order_main inner join order_sub on order_sub.order_main_id=order_main.order_id inner join delivery_address on delivery_address.order_id=order_main.order_id inner join medicine on medicine.medicine_id=order_sub.medicine_id where order_main.user_id= '"+str(session['lid'])+"' and delivery_address.status='return'"
    res = d.select(qry)
    return render_template('user/return_product.html', data=res)



@app.route('/send_complaint')
def send_complaint():
    return render_template('user/send_complaint.html')

@app.route('/send_complaint_post', methods=['post'])
def send_complaint_post():
    complaint = request.form['txtarea']
    d = Db()
    qry = "insert into complaint(user_id,date,complaint,reply,status) values('"+str(session['lid'])+"',curdate(),'"+complaint+"','None','pending')"
    res = d.insert(qry)
    return '''<script>alert('Send');window.location='/send_complaint'</script>'''

@app.route('/view_reply')
def view_reply():
    d = Db()
    qry = "select * from complaint where user_id='"+str(session['lid'])+"'"
    res = d.select(qry)
    print(res)
    return render_template('user/view_reply.html', data=res)

@app.route('/view_reply_post', methods=['post'])
def view_reply_post():
    frm = request.form['d1']
    to = request.form['d2']
    d = Db()
    qry = "select * from complaint where user_id='"+str(session['lid'])+"' and date between '"+frm+"' and '"+to+"'"
    res = d.select(qry)
    return render_template('user/view_reply.html', data=res)




@app.route('/user_home')
def user_home():
    return render_template('user/index.html')

if __name__ == '__main__':
    app.run(debug=True,port=3000)