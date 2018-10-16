from datetime import datetime, timedelta
from decimal import Decimal, ROUND_CEILING
import sqlite3
from config import *


class Subject:
    def __init__(self, sub):
        self.number = sub[0]
        self.name = sub[1]
        self.teacher = sub[2]
        self.audit = sub[3]

    def __str__(self):
        return '*' + str(self.number) + ' пара* ' + RINGSCHEDULE[self.number] + '\n_' + self.name + '_  *' + self.teacher + '* _' + str(
            self.audit) + '_\n'


def get_user(uid):
    try:
        db = sqlite3.connect(DBNAME, check_same_thread=False)
        cursor = db.cursor()
        cursor.execute("SELECT fac FROM user WHERE id = :uid", {"uid": uid})
        fac = cursor.fetchone()[0]
        db.close()
        return fac
    except sqlite3.Error as err:
        print(err)


def create_user(uid, fac):
    global db
    try:
        db = sqlite3.connect(DBNAME, check_same_thread=False)
        cursor = db.cursor()
        cursor.execute("INSERT INTO user VALUES (:uid, :fac)", {"uid": uid, "fac": fac})
        db.commit()
    except sqlite3.Error as err:
        print(err)
        return False
    except Exception as esc:
        print(esc)
    finally:
        db.close()
    return True


def update_user(uid, fac):
    global db
    try:
        db = sqlite3.connect(DBNAME, check_same_thread=False)
        cursor = db.cursor()
        cursor.execute("UPDATE user SET fac = :fac WHERE id = :uid", {"uid": uid, "fac": fac})
        db.commit()
    except sqlite3.Error as err:
        print(err)
        return False
    except Exception as esc:
        print(esc)
    finally:
        db.close()
    return True


def get_schedule(uid, is_tomorrow):
    fac = get_user(uid)
    day = datetime.now().isoweekday()
    is_num = is_numeral(datetime.now())
    if is_tomorrow:
        day += 1
    return select_schedule(fac, day, is_num)


def select_schedule(gr, day, is_num):
    try:
        db = sqlite3.connect(DBNAME, check_same_thread=False)
        cursor = db.cursor()
        if is_num:
            cursor.execute(
                "SELECT number, name, teacher, audit FROM scheduler WHERE fac = :fac AND day = :day AND chys = 1 ORDER BY number",
                {"fac": gr, "day": day})
        else:
            cursor.execute(
                "SELECT number, name, teacher, audit FROM scheduler WHERE fac = :fac AND day = :day AND znam = 1 ORDER BY number",
                {"fac": gr, "day": day})
        query = cursor.fetchall()
        schedule = []
        for sub in query:
            schedule.append(Subject(sub))
        db.close()
        return schedule
    except Exception as esc:
        print(esc)


def get_all_groups():
    groups = []
    try:
        db = sqlite3.connect(DBNAME, check_same_thread=False)
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT fac FROM scheduler ORDER BY fac")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            groups.append(row[0])
        db.close()
    except Exception as err:
        print(err)
    return groups


def is_numeral(date):
    return Decimal((date - datetime(2018, 9, 2)).days / 7).quantize(0, ROUND_CEILING) % 2
