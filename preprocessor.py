import re
import pandas as pd


def preprocess(data) :
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}'
    message = re.split(pattern, data)[1 :]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message' : message, 'message_date' : dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(':\s', message, maxsplit=1)
        if len(entry) >= 2:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages

    # extract additional date/time columns
    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    # reordering columns
    df = df[['period','only_date','message_date', 'year', 'month','month_num', 'day','day_name', 'hour', 'minute', 'user', 'message']]

    return df




