from flask import Flask, render_template, request,session,make_response
from database import Connection

app = Flask(__name__)
app.secret_key="abcdef"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userhome')
def userhome():
    x=session.get("myemail")
    # y=request.cookies['yourpass']
    # y=session.get("myacno")
    cnn = Connection()
    l=cnn.acno(x)
    l1=[]
    ac=''
    for i in l:
        l1.append(str(i[0]))
        ac=",\n".join(l1)
    return render_template('userhome.html',email=x,ac=ac)

@app.route('/myaccount')
def myaccount():
    return render_template('myaccount.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/funds')
def funds():
    return render_template('funds.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/createAccount',methods=['POST','GET'])
def createAccount():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])
        amt = float(request.form['tamt'])

        cnn = Connection()
        if cnn.storeAccount(email, acno, amt) == True:
            msg = "Account created Successfully !!!"
        else:
            msg = "Account creation Failed !!!"
        return render_template('usermessage.html', message=msg)

@app.route('/viewAccount',methods=['POST','GET'])
def viewAccount():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])

        cnn = Connection()
        balance = cnn.checkAccount(email, acno)
        if balance >= 0:
            msg = "Balance in your account = " + str(balance)
        else:
            msg = "Account number is incorrect !!"

        return render_template('usermessage.html', message=msg)

@app.route('/performTrans',methods=['POST','GET'])
def performTrans():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])
        amt = int(request.form['tamt'])
        type = request.form['type']

        cnn = Connection()
        stat=cnn.storeTrans(email,acno,amt,type)
        if stat == 0:
            msg = "Email Id or Account Number invalid !!"
        elif stat == 1:
            msg = "Amount deposited successfully !!"
        elif stat == 2:
            msg = "Insufficient Balance !!"
        elif stat == 3:
            msg = "Withdrawl successful !!"
        elif stat == 4:
            msg = "Withdrawl Unsuccessful !!"
        return render_template('usermessage.html', message=msg)

@app.route('/mobileRecharge',methods=['POST','GET'])
def mobileRecharge():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])
        amt = float(request.form['tamt'])
        type = request.form['type']

        cnn = Connection()
        if cnn.storeRecharge(email,acno,amt,type):
            cnn.storemobilerecharge(email,acno,amt,type)
            msg = "Mobile Recharge Successful !!"
        else:
            msg = "Mobile Recharge Failed !!"

        return render_template('usermessage.html', message=msg)

@app.route('/transferFund',methods=['POST','GET'])
def transferFund():
    if request.method=='POST':
        email = request.form['temail']
        acno1 = int(request.form['tacno1'])
        acno2 = int(request.form['tacno2'])
        amt = int(request.form['tamt'])

        cnn = Connection()
        if cnn.storeFundTranser(email,acno1,acno2,amt):
            msg = "Fund Transfer Successful !!"
        else:
            msg = "Fund Transfer Failed !!"

        return render_template('usermessage.html', message=msg)

@app.route('/changePassword',methods=['POST','GET'])
def changePassword():
    if request.method=='POST':
        email = request.form['temail']
        oldp = request.form['toldp']
        newp1 = request.form['tnewp1']
        newp2 = request.form['tnewp2']

        cnn = Connection()
        if cnn.checkPassword(email,oldp) == False:
            msg="Your password is incorrect !!"
        else:
            if newp1 != newp2:
                msg = "Passowrd not matched !!!"
            else:
                if cnn.updatePassword(email,oldp,newp1) == True:
                    msg = "Password Update Successful !!"
                else:
                    msg = "Password Update Failed !!"

        return render_template('usermessage.html', message=msg)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupUser',methods=['GET','POST'])
def signupUser():
    if request.method=='POST':
        email = request.form['uemail']
        pass1 = request.form['upass1']
        pass2 = request.form['upass2']

        # store data into database
        cnn = Connection()
        if cnn.storeUser(email,pass1) == True:
            if(pass1==pass2):
                msg="Signup Successful !!!"
                return render_template('index.html')
            msg="* Password and confirm password must be same ! *"
            return render_template('signupwrong.html',message=msg)
        else:
            msg="Signup Failed !!!"
            return render_template('fail.html',message=msg)

@app.route('/loginUser',methods=['GET','POST'])
def loginUser():
    if request.method=='POST':
        email = request.form['uemail']
        pass1 = request.form['upass']

        # check the email and pass in the database
        cnn = Connection()
        if cnn.checkUser(email,pass1) == True:
            l=cnn.acno(email)
            l1=[]
            for i in l:
                l1.append(str(i[0]))
            ac=",".join(l1)
            session["myemail"]=email
            session["myacno"]=ac
            # resp = make_response(render_template('userhome.html',email=email))
            # resp.set_cookie('yourpass',pass1,max_age=10*5)
            # return resp
            return render_template('userhome.html',email=email,ac=ac)
        else:
            msg="Invalid Credentials !!!"
            return render_template('wrongsignin.html',message=msg)
@app.route('/logout')
def logout():
    # session["myemail"]=None
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)