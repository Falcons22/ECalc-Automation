#fileName= 'D:\dash-das\\automate\\results\A60-7XS V4 28-Pole_LiPo 6000mAh - 80-120C_22_10.csv'
import pandas as pd

def thrust_at_750(df):
    #print(df)
    thrust=df['Thrust'].tolist()
    power=df['el. Power'].tolist()
    x1=0
    y1=0
    x2=0
    y2=0
    for i in range(len(thrust)):
        if float(power[i])<750:
            y1=float(thrust[i])
            x1=float(power[i])
            y2=float(thrust[i+1])
            x2=float(power[i+1])
    #print(x1,x2,y1,y2)
    thrust_750=-((y2-y1)/(x2-x1)*(750-x1)-y1)
    return thrust_750


