import os, glob
from datetime import date, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def load_dataset(folder, which='last', activity_type='All'):

    dataset_files = glob.glob(os.path.join(folder,'my_dataset*.csv'))
    dataset_files.sort()
    if which=='last':
        activities = pd.read_csv(dataset_files[-1])

    if type != 'All':
        activities = activities[(activities.type==activity_type)]

    activities = activities.drop(
        [
            'resource_state', 'workout_type', 'upload_id', 'upload_id_str', 
            'map.id', 'map.summary_polyline', 'start_date_local',
            'map.resource_state', 'average_watts', 'kilojoules', 'device_watts', 'id',
            'external_id', 'from_accepted_tag', 'total_photo_count', 'athlete.id',
            'athlete.resource_state', 'heartrate_opt_out', 'display_hide_heartrate_option',
            'utc_offset', 'location_city', 'location_state', 'timezone', 'achievement_count',
            'flagged', 'photo_count', 'trainer', 'commute', 'manual', 'private',
            'visibility', 'from_accepted_tag', 'pr_count'
        ], 
        axis=1
    )

    return activities

def extract_marathons(marathon_dates, training_time, activities):
    marathons = {}

    for marathon_date in marathon_dates:

        print(marathon_date)
        
        marathon = activities[
            (activities.start_date > str(marathon_date - timedelta(training_time*7)))&
            (activities.start_date < str(marathon_date + timedelta(1)))&
            (activities.type=='Run')
        ].copy()
        marathon.loc[:,'date'] = [date(*[int(d) for d in day[:10].split('-')]) for day in marathon.start_date]
        marathon.loc[:,'days2race'] = marathon.date-marathon.date.max()
        marathon.loc[:,'year'] = str(marathon_date.year)
        marathon = marathon.reset_index()
        marathon = marathon.drop(['index'], axis=1)
        
        marathons[str(marathon_date.year)] = marathon

    marathons = pd.concat(marathons, ignore_index=True)

    return marathons
