# database connectivity file
import pymysql as pm

class Connection:
    def __init__(self):
        self.con = pm.connect(host='localhost',user='root',password='te31259',database='mybank')
        self.cursor = self.con.cursor()

    def storeUser(self,email,pass1):
        sql="insert into users values ('%s','%s')" % (email,pass1)
        self.cursor.execute(sql)
        try:
            self.con.commit()
            self.status=True
        except:
            self.con.rollback()
            self.status=False
        return self.status

    def checkUser(self,email,pass1):
        sql="select * from users where emailid = '%s' and password = '%s'" % (email,pass1)
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.status=True
        else:
            self.status=False
        return self.status

    def storeAccount(self,email, acno, amt):
        exp=0
        sql = "insert into account values ('%s','%d','%f','%f')" % (email, acno, amt, exp)
        self.cursor.execute(sql)
        try:
            self.con.commit()
            self.status = True
        except:
            self.con.rollback()
            self.status = False
        return self.status

    def storeTrans(self,email, accno, amt, type):
        self.cursor.execute("select * from account where emailid = '%s' and acno = '%d'" % (
        email, accno))
        if(self.cursor.rowcount<1):
            self.status=0
        else:
            if type == 'Deposit':
                sql = "update account set balance = balance + '%d' where emailid ='%s' and acno = '%d'" % (
                    amt, email, accno)
                self.cursor.execute(sql)
                self.con.commit()
                self.status=1
                sql = "insert into transaction values ('%s','%d','%d','%s')" % (email, accno, amt,type)
                self.cursor.execute(sql)
                self.con.commit()
            else:
                self.cursor.execute("select * from account where emailid = '%s' and acno = '%d'" % (
                email, accno))
                data=self.cursor.fetchone()
                x=data[2]
                if(x<amt):
                    self.status=2
                else:
                    # print(x)
                    sql = "update account set balance = '%d' where emailid ='%s' and acno = '%d'" % ((x-amt), email, accno)
                    self.cursor.execute(sql)
                    try:
                        self.con.commit()
                        self.status = 3
                    except:
                        self.con.rollback()
                        self.status = 4
                    sql = "update account set expenditure = '%d' where emailid ='%s' and acno = '%d'" % ((data[3]+amt), email, accno)
                    self.cursor.execute(sql)
                    try:
                        self.con.commit()
                        self.status = 3
                    except:
                        self.con.rollback()
                        self.status = 4
        return self.status

    def storeRecharge(self,email, acno, amt, type):
        sql = "update account set balance = balance - '%f' where emailid ='%s' and acno = '%d'" % (amt, email, acno)
        self.cursor.execute(sql)
        try:
            self.con.commit()
            self.status = True
        except:
            self.con.rollback()
            self.status = False
        return self.status
    def storemobilerecharge(self,email, acno, amt, type):
        sql="insert into mobile values('%s','%d','%f','%s')"%(email,acno,amt,type)
        self.cursor.execute(sql)
        self.con.commit()

    def storeFundTranser(self,email, acno1, acno2, amt):
        sql = "update account set balance = balance - '%f' where emailid ='%s' and acno = '%d'" % (amt, email, acno1)
        self.cursor.execute(sql)
        try:
            self.con.commit()
            sql = "update account set balance = balance + '%f' where emailid ='%s' and acno = '%d'" % (
            amt, email, acno2)
            self.cursor.execute(sql)
            self.con.commit()
            self.status = True
        except:
            self.con.rollback()
            self.status = False
        return self.status

    def checkAccount(self, email, acno):
        sql = "select * from account where emailid = '%s' and acno = '%d'" % (email, acno)
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            data = self.cursor.fetchone()
            balance = data[2]
        else:
            balance = -1
        return balance

    def checkPassword(self, email, pass1):
        sql = "select * from users where emailid = '%s' and password = '%s'" % (email, pass1)
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            status = True
        else:
            status = False
        return status
    def info(self,email):
        sql="select * from "

    def updatePassword(self,email, oldp, newp):
        sql = "update users set password = '%s' where emailid ='%s' and password = '%s'" % (newp, email, oldp)
        self.cursor.execute(sql)
        try:
            self.con.commit()
            self.status = True
        except:
            self.con.rollback()
            self.status = False
        return self.status
    def acno(self,email):
        sql="select acno from account where emailid='%s'"%(email)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
