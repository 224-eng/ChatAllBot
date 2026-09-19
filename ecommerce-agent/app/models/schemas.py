"""数据模型定义"""
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    JSON,
    BigInteger,
    func,
)
from sqlalchemy.orm import relationship

from app.models.database import Base


# ============================================================
# 枚举类型
# ============================================================

class UserRole(str, enum.Enum):
    """用户角色"""
    SELLER = "seller"              # 卖家/运营
    CUSTOMER_SERVICE = "customer_service"  # 客服
    BUYER = "buyer"                # 买家
    ADMIN = "admin"                # 管理员


class ShopStatus(str, enum.Enum):
    """店铺状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class ProductStatus(str, enum.Enum):
    """商品状态"""
    ON_SALE = "on_sale"
    OFF_SALE = "off_sale"
    SOLD_OUT = "sold_out"


class OrderStatus(str, enum.Enum):
    """订单状态"""
    PENDING = "pending"          # 待支付
    PAID = "paid"                # 已支付
    SHIPPED = "shipped"          # 已发货
    COMPLETED = "completed"      # 已完成
    REFUNDED = "refunded"        # 已退款


class MessageType(str, enum.Enum):
    """消息类型"""
    USER = "user"                # 买家消息
    AGENT = "agent"              # AI回复
    HUMAN = "human"              # 人工客服


# ============================================================
# 用户表
# ============================================================

class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.BUYER)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    shop = relationship("Shop", back_populates="owner", foreign_keys=[shop_id])
    orders = relationship("Order", back_populates="buyer")


# ============================================================
# 店铺表
# ============================================================

class Shop(Base):
    """店铺表"""
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=True)  # shopify/taobao/self_built
    api_key = Column(String(255), nullable=True)
    status = Column(Enum(ShopStatus), default=ShopStatus.ACTIVE)
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    owner = relationship("User", back_populates="shop", foreign_keys=[owner_id])
    products = relationship("Product", back_populates="shop")
    orders = relationship("Order", back_populates="shop")
    chat_messages = relationship("ChatMessage", back_populates="shop")


# ============================================================
# 商品表
# ============================================================

class Product(Base):
    """商品表"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    product_name = Column(String(200), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    cost = Column(Numeric(10, 2), nullable=True)
    stock = Column(Integer, default=0)
    status = Column(Enum(ProductStatus), default=ProductStatus.ON_SALE)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    shop = relationship("Shop", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


# ============================================================
# 订单表
# ============================================================

class Order(Base):
    """订单表"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_no = Column(String(50), unique=True, nullable=False, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, server_default=func.now())
    paid_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)

    # 关系
    shop = relationship("Shop", back_populates="orders")
    buyer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


# ============================================================
# 订单明细表
# ============================================================

class OrderItem(Base):
    """订单明细表"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # 关系
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


# ============================================================
# 客服聊天表
# ============================================================

class ChatMessage(Base):
    """客服聊天表"""
    __tablename__ = "chat_messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String(50), nullable=False, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)  # 意图、情绪、工具调用等
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    shop = relationship("Shop", back_populates="chat_messages")
