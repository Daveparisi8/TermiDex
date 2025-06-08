import os, hashlib

class LoginData:
    def __init__(self, username: str, password: str, pin: str):
        self.username = username
        self._password_hash = self._hash_password(password)
        if not (pin.isdigit() and len(pin)==4):
            raise ValueError("PIN must be 4 digits")
        self.pin = pin
        self.login_attempts = 0

    @staticmethod
    def _hash_password(raw: str) -> bytes:
        salt = os.urandom(16)
        key  = hashlib.pbkdf2_hmac('sha256', raw.encode(), salt, 100_000)
        return salt + key

    def check_password(self, raw: str) -> bool:
        salt, key = self._password_hash[:16], self._password_hash[16:]
        test = hashlib.pbkdf2_hmac('sha256', raw.encode(), salt, 100_000)
        return test == key

    @property
    def is_locked(self) -> bool:
        return self.login_attempts >= 3

    def increment_attempts(self):
        self.login_attempts += 1

    def reset_attempts(self):
        self.login_attempts = 0

    def to_dict(self) -> dict:

        return {
            "username": self.username,
            "password_hash": self._password_hash.hex(),
            "pin": self.pin
        }

    @classmethod
    def from_dict(cls, data: dict):
        inst = cls.__new__(cls)
        inst.username = data["username"]
        inst._password_hash = bytes.fromhex(data["password_hash"])
        inst.pin = data["pin"]
        inst.login_attempts = 0
        return inst

    def __repr__(self):
        return (f"<LoginData {self.username!r} locked={self.is_locked}>")

class Pokemon:
    def __init__(self, name, types, evolves_to, caught=False):
        self.name = name
        self.types = types
        self.evolves_to = evolves_to
        self.caught = caught

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.types,
            "evolves_to": self.evolves_to,
            "caught": self.caught
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            types=data["type"],
            evolves_to=data.get("evolves_to", []),
            caught=data.get("caught", False)
        )
    
    def __repr__(self):
        status = "✓" if self.caught else "✗"
        return f"<Pokemon {self.name} ({'/'.join(self.types)}) {status}>"
    
    def catch(self):
        if not self.caught:
            self.caught = True
        else:
            raise RuntimeError(f"{self.name} already caught!")
            
    def release(self):
        self.caught = False