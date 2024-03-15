# Permissions

## AUTH SERVICE

### AUTH

**POST /register**
- all

**POST /token**
- all

**POST /token/refresh**
- token required (already implemented)

### USER

**GET /**
- all, BUT only usernames zurückgeben!  # TODO: /user/ only usernames


## RECIPE SERVICE

### CART

**GET /**
- filter by owner or can access


### COLLECTION

**GET /**
- filter by owner_user_id or has access


### PLANNER

**GET /**
- filter by owner_user_id or has access
