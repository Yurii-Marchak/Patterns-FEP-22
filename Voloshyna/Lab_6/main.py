
from fastapi import FastAPI, HTTPException
from Modified_Inventory_Subsystem import Stock
from Modified_Order_Process_Subsystem import ShoppingCart, Order
from Modified_Payment_Subsystem import Payment
from Modified_Shipment_Subsystem import Shipment
from Modified_OrderFacade import OrderFacade

app = FastAPI()

inventory = Stock()
order_process = ShoppingCart()
payment_system = Payment()
shipment_system = Shipment()

order_facade = OrderFacade(inventory, order_process, payment_system, shipment_system)

@app.post("/process_order")
def process_order(customer_id: str, order_details: dict):
    try:
        result = order_facade.process_order(customer_id, order_details)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
