import csv
import datetime
import os
import pandas as pd
import shutil

# 打刻する人の名前を入力して打刻処理を始める
input_name = input('write your name:')
tmp_file = input_name + '_tmp.csv'
engraving_file = input_name + '_engraving.csv'


# 打刻した日付(year/month/day)を取得
def engraving_day():
    now = datetime.datetime.now()
    day = now.strftime('%Y/%m/%d')
    return day


def attendance_time():
    now = datetime.datetime.now()
    attendance = now.time()
    return attendance.strftime('%H:%M')


# 打刻した時間(hour:min)を取得して
# 17:01~17:05であれば乖離時間として扱い、17:00にする
def retirement_time():
    now = datetime.datetime.now()
    engraving = now.time()
    on_time = datetime.time(hour=17, minute=0)
    deviation = datetime.time(hour=17, minute=5)
    if on_time <= engraving <= deviation:
        return on_time.strftime('%H:%M')
    else:
        return engraving.strftime('%H:%M')


# 17:05を超えた時間を残業時間として分単位で取得する
def over_time():
    attendance_tmp_hour = int(attendance_tmp[0:2]) * 60
    attendance_tmp_minute = int(attendance_tmp[3:5])
    attendance_tmp_count = attendance_tmp_hour + attendance_tmp_minute
    now = datetime.datetime.now()
    now_hour = now.hour * 60
    now_minute = now.minute
    now_count = now_hour + now_minute
    if day_tmp == engraving_day():
        if now_count - attendance_tmp_count > 530:
            over_time_count = now_count - (17 * 60 + 5)
            return over_time_count
        else:
            over_time_count = 0
            return over_time_count
    else:
        over_time_count = now_count + 415
        return over_time_count


# 出勤打刻をテンポラリファイルに一時保存する
if not os.path.exists(tmp_file) and not os.path.exists('tmp_files/'+tmp_file):
    with open(tmp_file, 'w') as csv_file:
        fieldnames = ['Day', 'AttendanceTime']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {'Day': engraving_day(),
             'AttendanceTime': attendance_time(),
             }
        )
    shutil.move(tmp_file, 'tmp_files/'+tmp_file)

# 出勤打刻のテンポラリファイルがあれば、出退勤打刻と残業時間を記憶する
else:
    os.chdir('./tmp_files')
    df = pd.read_csv(tmp_file)
    day_tmp = df.iat[0, 0]
    attendance_tmp = df.iat[0, 1]
    os.chdir('../engraving_files')
    with open(engraving_file, 'a') as csv_file:
        fieldnames = ['Day', 'AttendanceTime', 'RetirementTime', 'OverTime(min)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        try:
            pd.read_csv(engraving_file)
        except Exception:
            writer.writeheader()
        if day_tmp == engraving_day():
            if retirement_time() == '17:00':
                writer.writerow(
                    {'Day': day_tmp,
                     'AttendanceTime': attendance_tmp,
                     'RetirementTime': retirement_time()
                     }
                )
            else:
                writer.writerow(
                    {'Day': day_tmp,
                     'AttendanceTime': attendance_tmp,
                     'RetirementTime': retirement_time(),
                     'OverTime(min)': over_time()
                     }
                )
        else:
            writer.writerow(
                {'Day': str(day_tmp) + '~' + str(engraving_day()),
                 'AttendanceTime': attendance_tmp,
                 'RetirementTime': retirement_time(),
                 'OverTime(min)': over_time()
                 }
            )
    os.chdir('../tmp_files')
    os.remove(tmp_file)


# with open(engraving_file, 'r') as csv_file:
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         print(row['Day'], row['AttendanceTime'], row['RetirementTime'], row['OverTime(min)'])
