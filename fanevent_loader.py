import pandas as pd


def fanevent_search(singer_name, region):
    #df = pd.concat([pd.read_csv('hero10.csv'), pd.read_csv('myagain10.csv')])
    #df = df[(df['가수'] == singer_name) & (df['지역'] == region)]#.to_dict(orient='records')
    from tinydb import TinyDB, Query
    db = TinyDB('DB/fanevent.json')
    Event = Query()
    df = pd.DataFrame(db.search((Event['가수'] == singer_name) & (Event['지역'] == region)))

    from datetime import datetime
    # Function to calculate days remaining for random future dates
    def calculate_random_days_remaining(future_date, current_date=datetime.now()):
        future_date = datetime.strptime(future_date, "%Y년 %m월 %d일")
        days_remaining = (future_date - current_date).days
        return f"{days_remaining}일 남음"
    
    df['DaysRemaining'] = [calculate_random_days_remaining(date) for date in df['Date']]
    return df.to_dict(orient='records')



def event_checkins(uid):
    #df = pd.concat([pd.read_csv('hero10.csv'), pd.read_csv('myagain10.csv')])
    #df = df[(df['가수'] == singer_name) & (df['지역'] == region)]#.to_dict(orient='records')
    from tinydb import TinyDB, Query
    cdb = TinyDB('DB/checkin.json')
    Checkin = Query()
    return cdb.search(Checkin.Event == uid)
