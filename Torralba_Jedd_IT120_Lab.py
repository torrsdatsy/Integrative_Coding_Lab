from abc import ABC, abstractmethod

# STEP 1: Interface and Factory Method (Decoupling)
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

# Using GCash API
class GCashProcessor(PaymentProcessor):
    def pay(self, amount: float) -> None:
        print(f"Processing PHP {amount:.2f} via GCash API...")

# Using Credit Card for process.
class CreditCardProcessor(PaymentProcessor):
    def pay(self, amount: float) -> None:
        print(f"Processing PHP {amount:.2f} via Credit Card Gateway...")

# Add new payment transaction for Maya.
class MayaProcessor(PaymentProcessor):
    def pay(self, amount: float) -> None:
        print(f"Processing PHP {amount:.2f} via Maya API...")

# Build a PaymentFactory class that instantiates and returns the appropriate processor
class PaymentFactory:
    @staticmethod
    def create_processor(method: str) -> PaymentProcessor:
        processors = {
            "gcash": GCashProcessor,
            "creditcard": CreditCardProcessor,
            "maya": MayaProcessor
        }
        creator = processors.get(method.lower())
        if not creator:
            raise ValueError(f"Invalid Payment Method {method}")
        return creator()

# STEP 2: Decorator Pattern (Data Encryption)
class TransactionLogger(ABC):
    @abstractmethod
    def log(self, data: str) -> None:
        pass


class PlainTransactionLogger(TransactionLogger):
    def __init__(self):
        self.transaction_history = []

    def log(self, log_entry: str) -> None:
        print(f"[STORAGE] Saving: {log_entry}")
        self.transaction_history.append(log_entry)

class EncryptionDecorator(TransactionLogger):
    def __init__(self, wrap_logger: TransactionLogger):
        self._wrapped = wrap_logger

    def log(self, log_entry: str) -> None:
        log_entry_encrypted = f"ENC({log_entry[::-1]})"
        print("[DECORATOR] Encrypting sensitive transaction payload...")
        self._wrapped.log(log_entry_encrypted)

# STEP 3: Protection Proxy (Access Control)
class HistoryAccess(ABC):
    @abstractmethod
    def view_history(self) -> list:
        pass

class RealHistoryAccess(HistoryAccess):
    def __init__(self, logs: PlainTransactionLogger):
        self._logs = logs

    def view_history(self) -> list:
        return self._logs.transaction_history

class SecureHistoryProxy(HistoryAccess):
    def __init__(self, history_viewer: RealHistoryAccess, user_role: str):
        self._historyViewer = history_viewer
        self._user_role = user_role

    def view_history(self) -> list:
        if self._user_role != "admin":
            raise PermissionError(f"Access Denied: '{self._user_role}' cannot view historic logs")
        print("[PROXY] Admin verified. Fetching logs...")
        return self._historyViewer.view_history()


# Client Execution
raw_history_logs = PlainTransactionLogger()
secure_history = EncryptionDecorator(raw_history_logs)

payment_method = "maya"
processor = PaymentFactory.create_processor(payment_method)
amount = 1500.00
customer_ssn = "SSN-998-112"

processor.pay(amount)

log_entry = f"Method: {processor} | Amount: {amount} | SSN: {customer_ssn}"
secure_history.log(log_entry)

cashier_proxy = SecureHistoryProxy(RealHistoryAccess(raw_history_logs), user_role="cashier")
admin_proxy = SecureHistoryProxy(RealHistoryAccess(raw_history_logs), user_role="admin")

print("\n--- Testing Access Control ---")
try:
    print("Cashier History:", cashier_proxy.view_history())
except PermissionError as e:
    print(e)

print("Admin Logs:", admin_proxy.view_history())