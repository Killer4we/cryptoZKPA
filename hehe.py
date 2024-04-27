import hashlib

class ShortenString:
    def shorten(self, original):
        # Generate a shortened string using SHA-256 hash
        hashed = hashlib.sha256(original.encode()).hexdigest()[:6]  # Taking first 6 characters for brevity
        return hashed

    def retrieve_original_from_hash(self, shortened):
        # Retrieve the original string from the hash without using a map
        # Brute force approach to find the original string
        original = ""
        found = False
        for i in range(1000000):  # Assuming the original string length is less than 1,000,000 characters
            test_string = str(i)
            test_hashed = hashlib.sha256(test_string.encode()).hexdigest()[:6]
            if test_hashed == shortened:
                original = test_string
                found = True
                break

        if found:
            return original
        else:
            return "Original string not found for this shortened string."

# Create an instance of ShortenString
shortener = ShortenString()

# Take input for the shortened string
shortened_string = input("Enter the shortened string to retrieve the original: ")

# Retrieve the original string using the shortened string without using a map
retrieved_original = shortener.retrieve_original_from_hash(shortened_string)
print("Retrieved string without map:", retrieved_original)
