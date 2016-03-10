from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class State(Model):
	name = ndb.StringProperty(required=True)
	population = ndb.IntegerProperty(required=True)
	cost_of_living = ndb.FloatProperty(required=True)
	median_income = ndb.FloatProperty(required=True)
	largest_employer = ndb.StringProperty(required=True)
	senators = ndb.KeyProperty(repeated=True)

	def to_dict(self):
		d = super(Model, self).to_dict()
		d['senators'] = [s.id() for s in d['senators']]
		return d

class Senator(Model):
	name = ndb.StringProperty(required=True)
	largest_ind_contributor = ndb.StringProperty(required=True)
	net_worth = ndb.IntegerProperty(required=True)
	years = ndb.IntegerProperty(required=True)

