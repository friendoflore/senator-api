import webapp2

app = webapp2.WSGIApplication([], debug=True)
app.router.add(webapp2.Route(r'/senator', 'senator.Senator'))
app.router.add(webapp2.Route(r'/senator/<id:[0-9]+><:/?>', 'senator.Senator'))
app.router.add(webapp2.Route(r'/state', 'state.State'))
app.router.add(webapp2.Route(r'/state/<id:[0-9]+><:/?>', 'state.State'))
app.router.add(webapp2.Route(r'/state/<sid:[0-9]+>/senator/<oid:[0-9]+><:/?>', 'state.StateSenators'))
app.router.add(webapp2.Route(r'/state/search', 'state.StateSearch'))