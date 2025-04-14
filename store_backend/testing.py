def clock(time):
    dt='AM'
    hrs,mins=time.split(':')
    hrs=int(hrs)
    mins=int(mins)
    if hrs>=12:
        de='PM'
    hrs=hrs%12
    print(f"0{hrs}:{mins} {dt}")


clo="12:12"
clock(clo)


