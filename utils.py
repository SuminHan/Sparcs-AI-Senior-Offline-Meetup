
import hashlib

def hash_string(string, algorithm='sha256'):
    hash_object = hashlib.new(algorithm)
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()