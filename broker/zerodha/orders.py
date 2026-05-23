from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL = "SL"
    SL_MARKET = "SL-M"


@dataclass(frozen=True)
class OrderRequest:
    exchange: str
    tradingsymbol: str
    side: OrderSide
    quantity: int
    order_type: OrderType = OrderType.MARKET
    product: str = "MIS"
    variety: str = "regular"
    price: Optional[float] = None
    trigger_price: Optional[float] = None
    tag: str = "quant-os"


class PaperOrderBook:
    def __init__(self):
        self.orders = {}

    def place_order(self, request: OrderRequest):
        order_id = f"PAPER-{uuid4().hex[:12].upper()}"
        self.orders[order_id] = {
            "order_id": order_id,
            "status": "COMPLETE",
            "mode": "paper",
            "exchange": request.exchange,
            "tradingsymbol": request.tradingsymbol,
            "transaction_type": request.side.value,
            "quantity": request.quantity,
            "order_type": request.order_type.value,
            "product": request.product,
            "price": request.price,
            "trigger_price": request.trigger_price,
            "tag": request.tag,
            "created_at": datetime.now().isoformat()
        }
        return order_id

    def get_order(self, order_id: str):
        return self.orders.get(order_id)

    def cancel_order(self, order_id: str):
        order = self.orders.get(order_id)
        if not order:
            return None

        order["status"] = "CANCELLED"
        order["cancelled_at"] = datetime.now().isoformat()
        return order_id


class ZerodhaOrderManager:
    def __init__(
        self,
        kite=None,
        paper_mode: bool = True,
        allow_live_orders: bool = False
    ):
        self.kite = kite
        self.paper_mode = paper_mode
        self.allow_live_orders = allow_live_orders
        self.paper_orders = PaperOrderBook()

    def place_order(self, request: OrderRequest):
        self._validate_request(request)

        if self.paper_mode:
            return self.paper_orders.place_order(request)

        if not self.allow_live_orders:
            raise PermissionError(
                "Live orders are blocked unless allow_live_orders=True"
            )

        if self.kite is None:
            raise RuntimeError(
                "Kite client is required for live order placement"
            )

        return self.kite.place_order(
            variety=request.variety,
            exchange=request.exchange,
            tradingsymbol=request.tradingsymbol,
            transaction_type=request.side.value,
            quantity=request.quantity,
            product=request.product,
            order_type=request.order_type.value,
            price=request.price,
            trigger_price=request.trigger_price,
            tag=request.tag
        )

    def cancel_order(
        self,
        order_id: str,
        variety: str = "regular"
    ):
        if self.paper_mode:
            return self.paper_orders.cancel_order(order_id)

        if not self.allow_live_orders:
            raise PermissionError(
                "Live order cancellation is blocked unless allow_live_orders=True"
            )

        return self.kite.cancel_order(
            variety=variety,
            order_id=order_id
        )

    def get_order(self, order_id: str):
        if self.paper_mode:
            return self.paper_orders.get_order(order_id)

        if self.kite is None:
            raise RuntimeError(
                "Kite client is required for live order lookup"
            )

        for order in self.kite.orders():
            if str(order.get("order_id")) == str(order_id):
                return order

        return None

    @staticmethod
    def _validate_request(request: OrderRequest):
        if request.quantity <= 0:
            raise ValueError(
                "Order quantity must be positive"
            )

        if request.order_type in {OrderType.LIMIT, OrderType.SL} and request.price is None:
            raise ValueError(
                "Limit and SL orders require price"
            )

        if request.order_type in {OrderType.SL, OrderType.SL_MARKET} and request.trigger_price is None:
            raise ValueError(
                "SL orders require trigger_price"
            )
