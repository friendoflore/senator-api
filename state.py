import webapp2
from google.appengine.ext import ndb
import db_models
import json
import senator

class State(webapp2.RequestHandler):
	def post(self):
		""" Creates a State entity

		name - Required. State name
		population - Required. Population
		cost_of_living - Required. Cost of living index
		median_income - Required. Median income per capita
		largest_employer - Required. State's largest employer
		"""

		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return

		# Create a new state entity
		new_state = db_models.State()

		# Get all of the attribute values passed with the request
		name = self.request.get('name')
		population = int(self.request.get('population'))
		cost_of_living = float(self.request.get('cost_of_living'))
		median_income = float(self.request.get('median_income'))
		largest_employer = self.request.get('largest_employer')

		# All attributes for a state are required except for a state's senators
		# The senators will be added to a state with a PUT request
		if name and population and cost_of_living and median_income and \
			largest_employer:
			new_state.name = name
			new_state.population = population
			new_state.cost_of_living = cost_of_living
			new_state.median_income = median_income
			new_state.largest_employer = largest_employer
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
			self.response.write(self.response.status_message)
			return
		
		# Store the new state entity
		key = new_state.put()

		# Output the new state that was stored in JSON
		out = new_state.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.state = 406
			self.response.status_message = "API only supports JSON"
			self.response.write(self.response.status_message)
			return
		
		# If an ID was provided in the request, get that single entity
		if 'id' in kwargs:
			
			# Get the state entity and store it in a variable as a JSON object
			out = ndb.Key(db_models.State, int(kwargs['id'])).get().to_dict()
			
			# Write the state entity identited by the ID
			self.response.write(json.dumps(out))
		
		# Else get all of the state entities and display their keys
		else:
			
			# Get all state entities
			q = db_models.State.query()
			
			# Store all of their keys as a list
			keys = q.fetch(keys_only=True)

			# Store all of the key IDs as a dictionary
			results = { 'keys' : [x.id() for x in keys]}

			# Write the list of keys
			self.response.write(json.dumps(results))

	def delete(self, **kwargs):
		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.state = 406
			self.response.status_message = "API only supports JSON"
			self.response.write(self.response.status_message)
			return
		
		# An ID is required in order to delete an entity
		if 'id' in kwargs:

			# Get the state entities by the the ID provided
			del_state = ndb.Key(db_models.State, int(kwargs['id'])).get()
			
			# Delete the state entity; there are no other references to this state
			del_state.key.delete()


class StateSenators(webapp2.RequestHandler):
	def put(self, **kwargs):
		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			self.response.write(self.response.status_message)
			return
		
		# A state ID must be provided to store a senator as a state's senator
		if 'sid' in kwargs:
			
			# Get the state by the ID provided
			state = ndb.Key(db_models.State, int(kwargs['sid'])).get()
			
			# If the state is NULL, then the state was not found in the DB
			if not state:
				self.response.status = 404
				self.response.status_message = "State not found"
				self.response.write(self.response.status_message)
				return
		
		# A senator ID must be provided to store a senator as a state's senator
		if 'oid' in kwargs:
			
			# Get the state by the ID provided
			senator = ndb.Key(db_models.Senator, int(kwargs['oid']))
			
			# If the senator is NULL, then the senator was not found in the DB
			if not senator:
				self.response.status = 404
				self.response.status_message = "Senator not found"
				self.response.write(self.response.status_message)
				return
		
		# If the senator has not already been added to the state
		if senator not in state.senators:
			
			# Add this senator to the state
			state.senators.append(senator)
			
			# Save the updated state
			state.put()
		
		# Write the updated state as a JSON object
		self.response.write(json.dumps(state.to_dict()))
		return
