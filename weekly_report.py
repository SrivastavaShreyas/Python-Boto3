import boto3
import json
import pandas as pd
from datetime import date
from datetime import timedelta


today = date.today()

recentMonday = today - timedelta(days = today.weekday())

Prev_Week_Monday = recentMonday - timedelta(days = 7)

Prev_Prev_Week_Monday = Prev_Week_Monday - timedelta(days = 7)

recent_Sunday = recentMonday - timedelta(days = 1)

prev_week_Sunday = Prev_Week_Monday - timedelta(days = 1)

''' 
Assigning Previous two weeks' 

Mondays and Sundays for weekly reports
'''


pd.set_option("display.max.rows", None)


ce = boto3.client('ce') 
ses = boto3.client('ses')

'''
Creating Client Connections with AWS Cost Explorer and AWS-SES respectively
'''


def CostNUsageReport(Start, End, granularity, metrics, teamNames, tag_Key_value):
	'''
	Function to call Get Cost And Usage API with respect to AWS-TAGs.
	'''
	response = ce.get_cost_and_usage(
		TimePeriod={
			'Start': Start.isoformat(),
			'End': End.isoformat()
		},
		Granularity=granularity,
		Filter = {
			'Tags': {
				'Key': tag_Key_value,
				'Values': [
					teamNames,
				],
				'MatchOptions': [
					'EQUALS',
				]
			},
			
		},
		Metrics=[
			metrics,
		],
	)
	return response

def Cost_Handler():

	'''
	Team lists from AWS[Tags -> Teams] and AWS[Tags -> Members]

	Fetch cost usage team wise from Cost Explorer on "Granularity = Daily" 

	Add the amounts for previous week and previous to previous week.

	'''

	Team_CostUsage_Dict1 = {}
	Team_CostUsage_Dict2 = {}
	Final_CostUsage_Dict = {}



	Teams = [] # Add the list of team names as present in the Tags
	Members = [] # Add the list of member names as present in Tags
	

	for teamNames in Teams:
		costNusage = CostNUsageReport(Prev_Prev_Week_Monday, Prev_Week_Monday, 'DAILY', 'UnblendedCost', teamNames, 'Teams')
		Total_Cost_Usage = 0.00

		for results in costNusage['ResultsByTime']:
			Total_Cost_Usage = Total_Cost_Usage + float(results['Total']['UnblendedCost']['Amount'])
		Team_CostUsage_Dict1[teamNames]=Total_Cost_Usage

	for teamNames in Members:
		costNusage = CostNUsageReport(Prev_Prev_Week_Monday, Prev_Week_Monday, 'DAILY', 'UnblendedCost', teamNames, 'Members')
		Total_Cost_Usage = 0.00

		for results in costNusage['ResultsByTime']:
			Total_Cost_Usage = Total_Cost_Usage + float(results['Total']['UnblendedCost']['Amount'])
		Team_CostUsage_Dict1[teamNames]=Total_Cost_Usage


	dfWeek1 = pd.DataFrame([Team_CostUsage_Dict1])
	dfWeek1 = dfWeek1.fillna(' ').T
	dfWeek1 = dfWeek1.rename(columns = {0 : Prev_Prev_Week_Monday.isoformat() +' to ' + prev_week_Sunday.isoformat()})


	for teamNames in Teams:
		costNusage = CostNUsageReport(Prev_Week_Monday, recentMonday, 'DAILY', 'UnblendedCost', teamNames, 'Teams')
		Total_Cost_Usage = 0.00

		for results in costNusage['ResultsByTime']:
			Total_Cost_Usage = Total_Cost_Usage + float(results['Total']['UnblendedCost']['Amount'])
		Team_CostUsage_Dict2[teamNames]=Total_Cost_Usage

	for teamNames in Members:
		costNusage = CostNUsageReport(Prev_Week_Monday, recentMonday, 'DAILY', 'UnblendedCost', teamNames, 'Members')
		Total_Cost_Usage = 0.00

		for results in costNusage['ResultsByTime']:
			Total_Cost_Usage = Total_Cost_Usage + float(results['Total']['UnblendedCost']['Amount'])
		Team_CostUsage_Dict2[teamNames]=Total_Cost_Usage

	
	dfWeek2 = pd.DataFrame([Team_CostUsage_Dict2])
	dfWeek2 = dfWeek2.fillna(' ').T
	dfWeek2 = dfWeek2.rename(columns = {0 : Prev_Week_Monday.isoformat() + ' to ' + recent_Sunday.isoformat()})


	'''
	Create a single dictionary for each team's previous two week's costs.
	'''

	for team in Teams:
		Final_CostUsage_Dict[team] = [Team_CostUsage_Dict1[team], Team_CostUsage_Dict2[team]]
	
	for team in Members:
		Final_CostUsage_Dict[team] = [Team_CostUsage_Dict1[team], Team_CostUsage_Dict2[team]]
	
	Teams_CostComparedValue_List = {}

	'''
	Calculate the team wise delta for previous two weeks.

	Add the data team wise to a dictionary.
	'''

	for team in Final_CostUsage_Dict:
		team_value_list = Final_CostUsage_Dict[team]
		length = len(team_value_list)
		arbit = team_value_list[length-1] - team_value_list[length-2]
		Teams_CostComparedValue_List[team]=arbit


	'''
	Creating Data Frame for Team wise cost delta dictionary.

	Convert the data frames to HTML format for SES-send_email API

	Concat the Cost Savers and Cost Contributors Tables in HTML Format
	'''

	dfWeekDifference = pd.DataFrame([Teams_CostComparedValue_List])
	dfWeekDifference = dfWeekDifference.fillna(' ').T
	dfWeekDifference = dfWeekDifference.rename(columns = {0 : 'Difference'})

	dfInitial = pd.concat([dfWeek1, dfWeek2, dfWeekDifference], axis = 1)
	dfInitial = dfInitial.sort_values(by = 'Difference')
	dfInitial['Difference']=dfInitial['Difference'].apply(lambda x:round(x,2))

	dfCostSavers = dfInitial.head(7)
	dfCostSavers.columns.values[2]='Cost Savers : Difference of 2 Consecutive Weeks'
	dfCostSavers_html = dfCostSavers.to_html()


	dfCostContributors =dfInitial.tail(7)
	dfCostContributors = dfCostContributors.sort_values(['Difference'], ascending=False)
	dfCostContributors.columns.values[2]='Cost Contributors : Difference of 2 Consecutive Weeks'
	dfCostContributors_html = dfCostContributors.to_html()

	df_final_table = dfCostSavers_html + dfCostContributors_html

	def Email(Table1):

		'''
		AWS-SES 'send_email' API is used for sending email

		The source email ID needs to be verified with AWS-SES
		'''
		response = ses.send_email(
				Source = 'Sender Email Address',
				Destination = {
					'ToAddresses' : ['Receivers Email Address']  
                	# 'CcAddresses' : []
				},
				Message = {
					'Subject' : {
						'Data':'ENTER TEXT HERE',
					},
					'Body':{
						'Html':{
							'Data' : Table1,
							'Charset': 'UTF-8',
						}
					}
				},
			)



	Email(df_final_table)

if __name__ == '__main__':
	Cost_Handler()
