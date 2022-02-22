import json
import time
from requests_futures.sessions import FuturesSession
import datetime

session = FuturesSession(max_workers=100)


class fantasySpider:
	time= datetime.datetime.now
	def __init__(self):
		self.overall_league_id="314"
		self.test_id="8800004"
		self.general_info="https://fantasy.premierleague.com/api/bootstrap-static/"
		self.overall_league_data= "https://fantasy.premierleague.com/api/leagues-classic/{}/standings".format(self.overall_league_id)
		self.manager_history="https://fantasy.premierleague.com/api/entry/{}/history/"
		self.manager_details="https://fantasy.premierleague.com/api/entry/{}/"

	def get_total_managers(self):
		return int(json.loads(session.get(self.general_info).result().content)["total_players"])

	def get_history(self, manager):
		 return json.loads(session.get(self.manager_history.format(manager)).result().content)

	def get_current_rank(self, manager):
		if self.get_history(manager)["current"][-1]["overall_rank"] == None:
			return 0
		else:
			return int(self.get_history(manager)["current"][-1]["overall_rank"])

	def get_previous_rank(self, manager):
		if (self.get_history(manager)["current"][-2]["overall_rank"]) == None:
			return 0
		else:
			return self.get_history(manager)["current"][-2]["overall_rank"]



	def get_change_in_rank(self, manager):
		change= self.get_current_rank(manager) - self.get_previous_rank(manager)
		print(manager, change)
		return change

	def get_manager_details(self, manager):
		updated= datetime.datetime.now()
		data= json.loads(session.get(self.manager_details.format(manager)).result().content)
		first_name= data["player_first_name"]
		last_name= data["player_last_name"]
		current_rank= data["summary_overall_rank"]
		previous_rank= self.get_previous_rank(manager)

		manager_data={
			"updated": updated,
			"first name": first_name,
			"last name": last_name,
			"current rank": current_rank,
			"previous_rank": previous_rank
		}
		return manager_data


	def get_max_mover_and_faller(self, start, stop):
		updated= datetime.datetime.now()
		def yield_managers_change_in_rank():
			for manager in range(start, stop):
				yield self.get_change_in_rank(str(manager))

		change_in_rank_list= [ change_in_rank for change_in_rank in  yield_managers_change_in_rank()  ]
		max_rise= min(change_in_rank_list)
		max_riser_id=(change_in_rank_list.index(max_rise)) + start
		min_rise= max(change_in_rank_list)
		min_riser_id= (change_in_rank_list.index(min_rise)) + start

		max_mover_data= self.get_manager_details(max_riser_id)
		max_faller_data= self.get_manager_details(min_riser_id)

		data= {
			"updated": updated,
			"start": start,
			"stop": stop,
			"max mover": max_riser_id,
			"max rise": max_rise,
			"max faller": min_riser_id,
			"min rise": min_rise,
			"max mover data": max_mover_data,
			"max faller data": max_faller_data
		}
		with open("start({}) stop({})mover.json".format(start,stop), "w") as file:
			file.write(str(data))
			file.close()
		return data






spider= fantasySpider()

start=time.time()
print(spider.get_max_mover_and_faller(10001,100000))
stop= time.time()- start
print(stop)