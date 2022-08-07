import requests
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


def data_load():
    # api authentication
    url = '####'
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    jsonobj = {'appId': ####, 'password': '####'}
    resp = requests.post(url=url, headers=headers, json=jsonobj)
    data = resp.json()
    token = data.get("access_token")

    # request getting data from working hours summary api
    url4 = '#####'
    headers['Authorization'] = f"Bearer {token}"
    resp = requests.get(url=url4, headers=headers)
    # converting api response to normalized dataframe
    data = resp.json()
    df = pd.json_normalize(data)

    # clearing the data, drop data without user id
    df.dropna(subset=["ProjectUser.User.id"], inplace=True)

    # adding column date2 cope of data for indexing date
    df['date2'] = df['date']

    # adding new column user
    df['user name'] = df['ProjectUser.User.firstName'] + ' ' + df['ProjectUser.User.lastName']

    # slicing column for needed columns for transformation
    df = df[['date', 'date2', 'user name', 'FTE', 'allWorkingHours', 'allUsedWorkingHours', 'allPlannedHours',
             'allUsedPlannedHours', 'ProjectUser.Project.isBillable', 'ProjectUser.Project.name',
             'ProjectUser.Project.customer.name', 'notWorkingHours', 'isOverhours', 'ProjectUser.Project.isProductive']]
    # rounding values of columns
    df['allWorkingHours'] = round(df['allWorkingHours'], 2)
    df['allUsedWorkingHours'] = round(df['allUsedWorkingHours'], 2)
    df['allPlannedHours'] = round(df['allPlannedHours'], 2)
    df['allUsedPlannedHours'] = round(df['allUsedPlannedHours'], 2)

    # renaming columns for display version
    df.rename(columns={'ProjectUser.Project.name': 'Project name', 'allWorkingHours': 'Work',
                       'allUsedWorkingHours': 'UsedWork', 'allPlannedHours': 'Plan',
                       'ProjectUser.Project.customer.name': 'Customer Name', 'allUsedPlannedHours': 'UsedPlan',
                       'ProjectUser.Project.isBillable': 'isBillable'}, inplace=True)

    # sorting table on project name in primary starting display version
    df = df.sort_values(by='Project name', ascending=True)

    # adding hours calculation rounded columns
    df['UsedWork/Work'] = round(df.UsedWork.div(df.Work), 2)
    df['UsedPlan/Plan'] = round(df.UsedPlan.div(df.Plan), 2)
    df['UsedWork/UsedPlan'] = round(df.UsedWork.div(df.UsedPlan), 2)

    # for billable hours fill na values to avoid zero div error or dividing nan error
    df['isBillable'] = df['isBillable'].fillna(0)
    df['isBillable'] = df['isBillable'].astype(int)
    df['allBillable'] = (df['isBillable']) * (df['UsedWork'])
    df['allBillable'] = round(df['allBillable'], 2)
    df['allBillable/UsedWork'] = round(df.allBillable.div(df.UsedWork), 2)

    # copy of dataframe to df2 witch will not be displayed but will be base for future plots
    df2 = df

    # final rename of columns for customer display needs
    df.rename(columns={'UsedWork': 'Used Work', 'UsedPlan': 'Used Plan', 'allBillable/UsedWork': 'Billable/Used Work',
                       'UsedWork/Work': 'Used Work/Work', 'UsedPlan/Plan': 'Used Plan/Plan',
                       'UsedWork/UsedPlan': 'Used Work/Used Plan', 'allBillable': 'Billable', }, inplace=True)

    # final slice of columns for customer display needs
    df = df[['date', 'date2', 'FTE', 'user name', 'Customer Name', 'Project name', 'Work', 'Used Work', 'Plan',
             'Used Plan', 'Billable', 'Used Work/Work', 'Used Plan/Plan', 'Used Work/Used Plan', 'Billable/Used Work',
             'notWorkingHours', 'isOverhours', 'ProjectUser.Project.isProductive']]

    # change of date format to format possible for indexing, indexing date for calendar data range picker
    pd.options.mode.chained_assignment = None
    df['date2'] = pd.to_datetime(df['date2'].astype(str), format='%Y/%m', )
    df.set_index('date2', inplace=True)

    # set graphs from fig0 to fig4
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", x=df['user name']))
    df3 = pd.DataFrame({"Hours": ["Used Work", "Work"], "Amount": [df2['Used Work'].sum(), df2['Work'].sum()]})

    fig1 = px.bar(df3, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")
    df4 = pd.DataFrame({"Hours": ["Used Planed", "Planed"], "Amount": [df2['Used Plan'].sum(), df2['Plan'].sum()]})

    fig2 = px.bar(df4, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")
    df5 = pd.DataFrame({"Hours": ["Used Work", "Used Plan"], "Amount": [df2['Used Work'].sum(),
                                                                        df2['Used Plan'].sum()]})

    fig3 = px.bar(df5, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")
    df7 = pd.DataFrame({"Hours": ['Billable', "Used Work"], "Amount": [df2['Billable'].sum(), df2['Used Work'].sum()]})

    fig4 = px.bar(df7, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")

    return df, fig, fig1, fig2, fig3, fig4
