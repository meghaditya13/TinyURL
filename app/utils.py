import secrets
import string

characters = string.ascii_letters + string.digits #base 62

#help(secrets)

def short_code_generator():
	return ''.join(secrets.choice(characters) for i in range(6))