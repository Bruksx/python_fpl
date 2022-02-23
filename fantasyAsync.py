import json
import time
import httpx
import datetime
import asyncio

class fantasySpider:
	time= datetime.datetime.now
	def __init__(self):
		self.overall_league_id="314"
		self.general_info="https://fantasy.premierleague.com/api/bootstrap-static/"
		self.overall_league_data= "https://fantasy.premierleague.com/api/leagues-classic/{}/standings".format(self.overall_league_id)
		self.manager_history="https://fantasy.premierleague.com/api/entry/{}/history/"
		self.manager_details="https://fantasy.premierleague.com/api/entry/{}/"
		
	async def get_total_managers(self):
		async with httpx.AsyncClient() as client:
			r = await client.get(self.general_info).text["total_players"]
			return r.text
	
	async def get_history(self, manager):
		async with httpx.AsyncClient() as client:
			r = await client.get(self.manager_history.format(manager))
			return json.loads(r.text)
	
	async def get_current_rank(self, manager):
		try:
			history = await self.get_history(manager)
			return int(history["current"][-1]["overall_rank"])
		except:
			return 0

	async def get_previous_rank(self, manager):#
		try:
			history = await self.get_history(manager)
			return int(history["current"][-2]["overall_rank"])
		except:
			return 0
		

	
	async def get_change_in_rank(self, manager):
		change= await self.get_current_rank(manager) - await self.get_previous_rank(manager)
		print(manager, change)
		return change
	
	async def get_manager_details(self, manager):
		updated= datetime.datetime.now()
		data= json.loads(httpx.get(self.manager_details.format(manager)).text)
		first_name= data["player_first_name"]
		last_name= data["player_last_name"]
		current_rank= data["summary_overall_rank"]
		previous_rank= await self.get_previous_rank(manager)
		
		manager_data={
			"updated": updated,
			"first name": first_name,
			"last name": last_name,
			"current rank": current_rank,
			"previous_rank": previous_rank
		}
		return manager_data		
		
	
	async def get_max_mover_and_faller(self, start, stop):
		updated= datetime.datetime.now()
		"""
		def yield_managers_change_in_rank():
			for manager in range(start, stop):
				yield self.get_change_in_rank(str(manager))
		"""
		change_in_ranks= await asyncio.gather(*map(self.get_change_in_rank, range(start, stop+1)))
		
		change_in_rank_list= [ change_in_rank for change_in_rank in  change_in_ranks  ]
		max_rise= min(change_in_rank_list)
		max_riser_id=(change_in_rank_list.index(max_rise)) + start
		min_rise= max(change_in_rank_list)
		min_riser_id= (change_in_rank_list.index(min_rise)) + start
		
		max_mover_data= await self.get_manager_details(max_riser_id)
		max_faller_data= await self.get_manager_details(min_riser_id)
		
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
		with open("mover.json", "w") as file:
			file.write(str(data))
			file.close()
		return data
	
	




spider= fantasySpider()

async def main():
	start=time.time()
	result = await spider.get_max_mover_and_faller(1,10000)
	print(result)

	stop= time.time()- start
	print(stop)


asyncio.run(main())