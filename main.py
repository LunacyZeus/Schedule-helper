from datetime import datetime, timedelta


# 定义班次类型及规则
class ScheduleHelper:
    def __init__(self, schedules):
        """
        schedules: 字典，表示每个人的班次初始状态
        {
            '张三': {'type': '日勤', 'start_date': '2024-12-10'},
            '李四': {'type': '白夜休休', 'start_date': '2024-12-10'},
        }
        """
        self.schedules = {}
        for person, data in schedules.items():
            self.schedules[person] = {
                'type': data['type'],
                'start_date': datetime.strptime(data['start_date'], '%Y-%m-%d')
            }

    def get_shift(self, person, query_date):
        """
        查询某人在指定日期的班次
        person: 姓名
        query_date: 查询日期，字符串格式 'YYYY-MM-DD'
        返回: 班次字符串
        """
        if person not in self.schedules:
            return f"{person} 不在排班表中。"

        person_schedule = self.schedules[person]
        schedule_type = person_schedule['type']
        start_date = person_schedule['start_date']
        query_date = datetime.strptime(query_date, '%Y-%m-%d')

        if schedule_type == '日勤':
            return '日勤'
        elif schedule_type == '白夜休休':
            delta_days = (query_date - start_date).days % 4
            if delta_days == 0:
                return '白班'
            elif delta_days == 1:
                return '夜班'
            else:
                return '休息'
        else:
            return '未知班次类型'

    def get_schedule_in_range(self, start_date, end_date):
        """
        查询所有人在指定日期范围内的班次
        start_date: 起始日期，字符串格式 'YYYY-MM-DD'
        end_date: 结束日期，字符串格式 'YYYY-MM-DD'
        返回: 字典，表示每个人在日期范围内的班次表
        {
            '张三': {'2024-12-10': '日勤', '2024-12-11': '日勤', ...},
            '李四': {'2024-12-10': '白班', '2024-12-11': '夜班', ...},
        }
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        result = {}
        for person in self.schedules:
            result[person] = {}
            current_date = start_date
            while current_date <= end_date:
                result[person][current_date.strftime('%Y-%m-%d')] = self.get_shift(person,
                                                                                   current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

        return result

    def get_schedule_for_day(self, query_date):
        """
        查询指定日期所有人的班次
        query_date: 查询日期，字符串格式 'YYYY-MM-DD'
        返回: 字典，表示每个人的班次
        {
            '张三': '日勤',
            '李四': '白班',
        }
        """
        query_date = datetime.strptime(query_date, '%Y-%m-%d')
        result = {}
        for person in self.schedules:
            result[person] = self.get_shift(person, query_date.strftime('%Y-%m-%d'))
        return result


# 示例使用
if __name__ == "__main__":
    initial_schedules = {
        '张三': {'type': '日勤', 'start_date': '2024-12-10'},
        '李四': {'type': '白夜休休', 'start_date': '2024-12-10'},
        '王五': {'type': '日勤', 'start_date': '2024-12-10'},
        '钟六': {'type': '白夜休休', 'start_date': '2024-12-10'},
    }

    helper = ScheduleHelper(initial_schedules)

    # 查询指定日期某人的班次
    query_date = '2024-12-12'
    print(helper.get_shift('李四', query_date))  # 输出: 休息

    # 查询指定日期范围内的所有班次
    schedule_range = helper.get_schedule_in_range('2024-12-10', '2024-12-13')
    for person, schedule in schedule_range.items():
        print(f"{person}:")
        for date, shift in schedule.items():
            print(f"  {date}: {shift}")

    date = '2024-12-19'
    # 查询指定日期所有人的班次
    daily_schedule = helper.get_schedule_for_day(date)
    print(f"\n指定日期{date}的所有人班次:")
    for person, shift in daily_schedule.items():
        print(f"{person}: {shift}")
