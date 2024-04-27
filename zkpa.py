import sys
import hashlib
import base64
import pymongo
import smtplib
import ssl
from email.message import EmailMessage
from cryptography.fernet import Fernet, InvalidToken
def shorten(self, original):
        # Generate a shortened string using SHA-256 hash
        hashed = hashlib.sha256(original.encode()).hexdigest()[:6]  # Taking first 6 characters for brevity

        # Store mapping
        self.shortened_strings[hashed] = original

        return hashed

def generate_key(aadhar_number):
    return hashlib.sha256(aadhar_number.encode()).digest()

def encrypt_key(key, password):
    cipher_suite = Fernet(base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()))
    return cipher_suite.encrypt(key)

def decrypt_key(encrypted_key, password):
    cipher_suite = Fernet(base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()))
    return cipher_suite.decrypt(encrypted_key)

def verify_identity(original_key, decrypted_key):
    original_hash = hashlib.sha256(original_key).hexdigest()
    decrypted_hash = hashlib.sha256(decrypted_key).hexdigest()
    
    return original_hash == decrypted_hash


user_aadhar_number = sys.argv[1]
password = sys.argv[2]

unique_key = generate_key(user_aadhar_number)
client = pymongo.MongoClient("mongodb+srv://abhinavajay20:ijdDhmzGxB3uBeJg@cluster0.r9abfzl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['test']
collection = db['users']
unique_identifier = {'aadhaar':user_aadhar_number}
encrypted_unique_key = encrypt_key(unique_key, password)
hash_object = hashlib.sha256(encrypted_unique_key)
hash_hex = hash_object.hexdigest()
unique_code = hash_hex[:8]
collection.update_one(
    unique_identifier,
    { '$set' : { 'Key': unique_code } }
)




email_sender = 'cryptographyproject123@gmail.com'
email_password = 'itinobtdwqrsehwt'
email_receiver = sys.argv[3]
key = unique_code
subject = 'UNIQUE CODE'
body = f"""Hello,
Here is your unique token: {key}
Thank you for using our service.
Best regards,
INDIAN GOVT"""
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender,email_receiver,em.as_string())

print('Email Sent Successfully')