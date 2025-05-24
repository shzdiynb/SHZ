from werkzeug.security import generate_password_hash
print(generate_password_hash("admin", method='pbkdf2:sha256'))
