import webapp2
from google.appengine.ext import ndb
import db_models
import json
import state

class Senator(webapp2.RequestHandler):
	def post(self):
		"""
		Creates a Senator entity

		POST variables:
		name - Required. State name
		largest_ind_contributor - Required. Largest campaign contribution industry
		net_worth - Required. Net worth of senator
		years - Required. Years in office
		"""

		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return
		
		# Create a new senator entity
		new_senator = db_models.Senator()

		# Get all of the attribute values passed with the request
		name = self.request.get('name')
		largest_ind_contributor = self.request.get('largest_ind_contributor')
		net_worth = int(self.request.get('net_worth'))
		years = int(self.request.get('years'))

		# All attributes for a senator are required
		# Store the attribute values in the new entity
		if name and largest_ind_contributor and net_worth and years:
			new_senator.name = name
			new_senator.largest_ind_contributor = largest_ind_contributor
			new_senator.net_worth = net_worth
			new_senator.years = years
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
			self.response.write(self.response.status_message)
			return

		# Store the new senator entity
		key = new_senator.put()

		# Output the new senator that was stored in JSON
		out = new_senator.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.state = 406
			self.response.status_message = "API only supports JSON"
			return

		# If an ID was provided in the request, get that single entity
		if 'id' in kwargs:

			# Get the senator entity and store it in a variable as a JSON object
			out = ndb.Key(db_models.Senator, int(kwargs['id'])).get().to_dict()
			
			# Write the senator entity identified by the ID
			self.response.write(json.dumps(out))
		
		# Else get all of the senator entities and display their keys
		else:

			# Get all senator entities
			q = db_models.Senator.query()

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
			return

		# An ID is required in order to delete an entity
		if 'id' in kwargs:
			
			# Get the senator entities by the ID provided
			del_key = ndb.Key(db_models.Senator, int(kwargs['id'])).get()
			
			# Delete the senator entity
			del_key.key.delete()
			
			# Delete references to this senator entity in the state entity
			# Query the DB for the state that has this senator
			q = db_models.State.query(db_models.State.senators.IN([del_key.key]))
			
			# Returns a list of states
			update_state = q.fetch()
			
			# Remove the senator's key from the state
			for x in update_state:
				x.senators.remove(del_key.key)

				# Update the state
				x.put()
			return
		else:
			self.response.state = 400
			self.response.status_message = "Invalid request"
			return
