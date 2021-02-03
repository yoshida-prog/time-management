# 残業時間を分析するプログラム
import matplotlib.pyplot as plt
import os
import pandas as pd

# 名前を入力
input_name = input('write your name:')
over_time_file = input_name + '_engraving.csv'

# 入力者の勤怠記録データを読み込む
os.chdir('./engraving_files')
df = pd.read_csv(over_time_file, sep=",")
df.columns = ["Day", "AttendanceTime", "RetirementTime", "OverTime(min)"]


# 月毎の残業時間の合計を計算
def monthly_over_time():
    # ある月の各日残業時間を格納するリスト
    total_overtime_tmp = []
    # ある月の合計残業時間を{年/月: 合計残業時間}で格納するディクショナリ
    total_overtime = {}
    # 年/月を代入する為の変数を定義
    df_tmp = ""
    # 月毎の合計残業時間を計算する際に用いる変数を定義
    n = 0
    for (i, x) in enumerate(df["Day"]):
        if i == 0:
            # 年/月をスライス
            df_tmp = x[0:7]
            # 各日の残業時間を格納
            total_overtime_tmp.append(df["OverTime(min)"][i])
        # 前日と年/月が同じであれば繰り返す
        elif x[0:7] == df_tmp:
            df_tmp = x[0:7]
            total_overtime_tmp.append(df["OverTime(min)"][i])
        # 前日と年/月が異なる場合はそれまでの合計残業時間をtotal_overtimeに格納
        elif x[0:7] != df_tmp:
            # 月初から月末までの合計残業時間をtotal_overtimeディクショナリに格納
            total_overtime.setdefault(df_tmp, sum(total_overtime_tmp[n:]))
            # 次月頭の残業時間と年/月
            total_overtime_tmp.append(df["OverTime(min)"][i])
            df_tmp = x[0:7]
            # 月初のインデックスナンバーを記憶
            n = i
    # for文を抜けたら集計最後の月のデータをtotal_overtimeディクショナリに格納
    else:
        total_overtime.setdefault(df_tmp, sum(total_overtime_tmp[n:]))
    return total_overtime


# x軸が年/月、y軸が月毎の合計残業時間の棒グラフを描写
plt.bar(range(len(monthly_over_time())), monthly_over_time().values(), align='center')
# xticks()関数で目盛りラベルを描写
plt.xticks(range(len(monthly_over_time())), monthly_over_time().keys())
plt.show()
