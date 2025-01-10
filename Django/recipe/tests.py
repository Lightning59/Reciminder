from django.test import TestCase
from .views import *


#models
# create a recipe with all fields - Then check it's string repr
# create a recipe with only a title - check string repr

# Test paginate function somehow

# Test query function somehow.

#forms
# try to submit a form with all fields proper
# Try to sumit a form with only title
# try to submit blank
# try to submit all fields except title
# try to submit non-numeric to numeric.
# Try float vs decimal
# Try a negative number

#views
# have a db with a valid recipe, deleted recipe, Then also generate a valid UUID at random
# Scrub function should return a recipe object, Raise Error, Raise Error respectively

#attempt to access add-recipe while logged out
#attemp to access add-recipe while logged in
#attempt to post a valid form
#attempt to post an invalid form

#attempt to access view-recipe while logged out valid recipe
#attemp to access view-recipe while logged in valid recipe
#attempt to delete recip while logged out invalid recipe
#attemp to delete recipe while logged in invalid recipe

#attempt to access edit recipe while logged out valid recipe
#attempt to access edit recipe while logged in valid recipe
#attempt to access recipe while logged out invalid recipe
#attempt to access recipe while logged in invalid recipe
#attempt to post update to recipe while logged in valid recipe
#attempt to post update to recipe while logged out valid recipe
#attempt to post update to recipe blank title while logged out valid recipe
#attempt to post update to recipe blank title while logged in valid recipe

#attempt to delete recipe while logged out valid recipe
#attemp to delete recipe while logged in valid recipe
#attempt to delete recipe while logged out invalid recipe
#attemp to delete recipe while logged in invalid recipe

#attempt to view home logged in
#attempt to view home logged out