#1.	Write a hash_password() and verify_password() utility using passlib. Test them in isolation before wiring into routes.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    print("Security Test in Isolation")
    
    test_password = "usman123"
    print(f"1. User's typed password: '{test_password}'")
    
    # Test the hash
    hashed_result = hash_password(test_password)
    print(f"2. Hashed Password: {hashed_result}")
    
    # Test a successful login
    success_check = verify_password(test_password, hashed_result)
    print(f"3. Verify with 'usman123' -> {success_check}")
    
    # Test a failed login
    fail_check = verify_password("usman321", hashed_result)
    print(f"4. Verify with 'usman321' -> {fail_check}")