import unittest
from datetime import datetime, timedelta

class TestSSLValidation(unittest.TestCase):
    
    # test valid certificate 
    def test_valid_ssl(self):
        domain = "fearless.com"    # domain name
        port = 443                # demain port
        now = datetime.utcnow()     #curresnt time 
        expiration_date = (now + timedelta(days=30)).strftime('%b %d %H:%M:%S %Y %Z') #the expiration time is set at 30 day in the future

        result = check_ssl_expiration({'queryStringParameters': {'host': domain}}, {}) # call check_ssl_expiration fucntion and parsed the domain name as query parameter
        self.assertEqual(result['statusCode'], 200)    # assert the status to success
        self.assertEqual(result['body']['domain_name'], domain) # assert that the domain in the body is correct
        self.assertEqual(result['body']['is_valid'], True)  # assert that SSL is valid
        self.assertGreaterEqual(result['body']['days_until_expiration'], 0) # assert that the remaining day is between 0 and 30
        self.assertLessEqual(result['body']['days_until_expiration'], 30)

# test for invalid certificate
    def test_expired_ssl(self):
        domain = "efearless.com"
        port = 443
        now = datetime.utcnow()
        expiration_date = (now - timedelta(days=30)).strftime('%b %d %H:%M:%S %Y %Z')
        result = check_ssl_expiration({'queryStringParameters': {'host': domain}}, {})
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['body']['domain_name'], domain)
        self.assertEqual(result['body']['is_valid'], False)
        self.assertLess(result['body']['days_until_expiration'], 0)

# test in case domain does not exist
    def test_invalid_domain(self):
    
        domain = "invalid.fearless.com"
        port = 443
        result = check_ssl_expiration({'queryStringParameters': {'host': domain}}, {})
        self.assertEqual(result['statusCode'], 500)  
        self.assertEqual
