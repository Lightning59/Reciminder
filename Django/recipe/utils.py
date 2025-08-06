

def minutes_to_user_text(minutes: int, long: bool=False) -> str:
    if long:
        minutes_str = ' minutes'
        hours_str = ' hours'
        days_str = ' days'
    else:
        minutes_str = 'm'
        hours_str = 'h'
        days_str = 'd'
    if minutes < 0:
        raise ValueError("minutes cannot be negative")
    elif minutes == 0:
        return ""
    elif minutes <=59:
        return str(minutes)+minutes_str
    elif minutes <= (24*60)-1:
        if minutes % 60 == 0:
            return str(minutes//60)+hours_str
        else:
            return str(minutes//60)+hours_str +' ' +str(minutes%60)+minutes_str
    else:
        if minutes % (24*60) == 0: # exact number of days
            return str(minutes//(24*60))+days_str
        elif minutes % (24*60) <= 59: # a few minutes over a day but less than 1 hour
            return str(minutes//(24*60))+days_str + ' ' + str(minutes%(24*60))+minutes_str
        elif minutes % 60 == 0: # some number of days plus hours no remaining minutes
            days=minutes//(24*60)
            hours = (minutes %(24*60))//60
            return str(days)+days_str+' '+str(hours) + hours_str
        else:
            days = minutes // (24 * 60)
            hours = (minutes % (24 * 60)) // 60
            minutes_final=minutes -(24*60*days) -(60*hours)
            return str(days)+days_str+' '+str(hours) + hours_str+' '+str(minutes_final)+minutes_str


