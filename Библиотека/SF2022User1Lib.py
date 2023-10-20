from datetime import timedelta, time


class Calculations:
    @staticmethod
    def available_periods(start_times: list, durations: list, begin_working_time: time,
                          end_working_time: time, consultation_time: int):
        resp = []
        consultation_tm = timedelta(minutes=consultation_time)
        check_fun = lambda start, now, end: start <= now < end or start < now + consultation_tm <= end or now < start < now + consultation_tm or now < end < now + consultation_tm
        len_workday = timedelta(hours=end_working_time.hour, minutes=end_working_time.minute) - timedelta(
            hours=begin_working_time.hour, minutes=begin_working_time.minute)
        if len_workday < timedelta(hours=0, minutes=0):
            raise Exception
        now_time = timedelta(hours=begin_working_time.hour, minutes=begin_working_time.minute)
        for tm in range(len_workday // consultation_tm):
            if now_time + timedelta(minutes=1) > timedelta(hours=end_working_time.hour,
                                                           minutes=end_working_time.minute) \
                    or now_time + consultation_tm > timedelta(hours=end_working_time.hour,
                                                              minutes=end_working_time.minute):
                break
            check = True
            h = 0
            for check_time in start_times:
                start = timedelta(hours=check_time.hour, minutes=check_time.minute)
                end = timedelta(hours=check_time.hour, minutes=check_time.minute) + timedelta(minutes=durations[h])
                h += 1
                if check_fun(start, now_time, end):
                    check = False
                    break
            if check:
                resp.append(f'{now_time}-{now_time + consultation_tm}\n')
                now_time += consultation_tm
                continue
            while not check:
                now_time += timedelta(minutes=1)
                h = 0
                check = True
                for check_time in start_times:
                    start = timedelta(hours=check_time.hour, minutes=check_time.minute)
                    end = timedelta(hours=check_time.hour, minutes=check_time.minute) + timedelta(minutes=durations[h])
                    h += 1
                    if check_fun(start, now_time, end):
                        check = False
        return ''.join(resp)


list_cansel = [time(hour=10, minute=0), time(hour=11, minute=0), time(hour=15, minute=0), time(hour=15, minute=30),
               time(hour=16, minute=50)]
list_len_cansel = [60, 30, 10, 10, 40]
time_begin = time(hour=8, minute=0)
time_end = time(hour=18, minute=0)
consultation = 30
cl = Calculations()
print(cl.available_periods(list_cansel, list_len_cansel, time_begin, time_end, consultation))
