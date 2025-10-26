class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(128), unique=True, nullable=False, index=True)  # external OrderID, e.g., for BTCPay metadata
    user_id = Column(Integer, nullable=True)
    status = Column(String(32), default="created")
    created_at = Column(DateTime(timezone=True), server_default=func.now())