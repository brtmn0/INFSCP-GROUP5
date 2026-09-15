import socketserver
import http.server
import json

from providers import auth_provider
from providers import data_provider

from processors import notification_processor

class ApiRequestHandler(http.server.BaseHTTPRequestHandler):

    def handle_get_version_1(self, paths, user):
        if not auth_provider.has_access(user, paths, "get"):
            self.send_response(403)
            self.end_headers()
            return
        if paths[0] == "warehouses":
            parts = len(paths)
            match parts:
                case 1:
                    warehouses = data_provider.fetch_warehouse_pool().get_warehouses()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(warehouses).encode("utf-8"))
                case 2:
                    warehouse_id = int(paths[1])
                    warehouse = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(warehouse).encode("utf-8"))
                case 3:
                    if paths[2] == "locations":
                        warehouse_id = int(paths[1])
                        locations = data_provider.fetch_location_pool().get_locations_in_warehouse(warehouse_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(locations).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "locations":
            parts = len(paths)
            match parts:
                case 1:
                    locations = data_provider.fetch_location_pool().get_locations()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(locations).encode("utf-8"))
                case 2:
                    location_id = int(paths[1])
                    location = data_provider.fetch_location_pool().get_location(location_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(location).encode("utf-8"))
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "transfers":
            parts = len(paths)
            match parts:
                case 1:
                    transfers = data_provider.fetch_transfer_pool().get_transfers()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(transfers).encode("utf-8"))
                case 2:
                    transfer_id = int(paths[1])
                    transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(transfer).encode("utf-8"))
                case 3:
                    if paths[2] == "items":
                        transfer_id = int(paths[1])
                        items = data_provider.fetch_transfer_pool().get_items_in_transfer(transfer_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(items).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "items":
            parts = len(paths)
            match parts:
                case 1:
                    items = data_provider.fetch_item_pool().get_items()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(items).encode("utf-8"))
                case 2:
                    item_id = int(paths[1])
                    item = data_provider.fetch_item_pool().get_item(item_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item).encode("utf-8"))
                case 3:
                    if paths[2] == "inventory":
                        item_id = int(paths[1])
                        inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(item_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(inventories).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 4:
                    if paths[2] == "inventory" and paths[3] == "totals":
                        item_id = int(paths[1])
                        totals = data_provider.fetch_inventory_pool().get_inventory_totals_for_item(item_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(totals).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "item_lines":
            parts = len(paths)
            match parts:
                case 1:
                    item_lines = data_provider.fetch_item_line_pool().get_item_lines()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_lines).encode("utf-8"))
                case 2:
                    item_line_id = int(paths[1])
                    item_line = data_provider.fetch_item_line_pool().get_item_line(item_line_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_line).encode("utf-8"))
                case 3:
                    if paths[2] == "items":
                        item_line_id = int(paths[1])
                        items = data_provider.fetch_item_pool().get_items_for_item_line(item_line_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(items).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "item_groups":
            parts = len(paths)
            match parts:
                case 1:
                    item_groups = data_provider.fetch_item_group_pool().get_item_groups()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_groups).encode("utf-8"))
                case 2:
                    item_group_id = int(paths[1])
                    item_group = data_provider.fetch_item_group_pool().get_item_group(item_group_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_group).encode("utf-8"))
                case 3:
                    if paths[2] == "items":
                        item_group_id = int(paths[1])
                        items = data_provider.fetch_item_pool().get_items_for_item_group(item_group_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(items).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "item_types":
            parts = len(paths)
            match parts:
                case 1:
                    item_types = data_provider.fetch_item_type_pool().get_item_types()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_types).encode("utf-8"))
                case 2:
                    item_type_id = int(paths[1])
                    item_type = data_provider.fetch_item_type_pool().get_item_type(item_type_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_type).encode("utf-8"))
                case 3:
                    if paths[2] == "items":
                        item_type_id = int(paths[1])
                        items = data_provider.fetch_item_pool().get_items_for_item_type(item_type_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(items).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "inventories":
            parts = len(paths)
            match parts:
                case 1:
                    inventories = data_provider.fetch_inventory_pool().get_inventories()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(inventories).encode("utf-8"))
                case 2:
                    # Inventory rows are keyed on a composite (item_id, location_id)
                    # in the new schema, so a single surrogate id has no meaning.
                    self.send_response(404)
                    self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "suppliers":
            parts = len(paths)
            match parts:
                case 1:
                    suppliers = data_provider.fetch_supplier_pool().get_suppliers()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(suppliers).encode("utf-8"))
                case 2:
                    supplier_id = int(paths[1])
                    supplier = data_provider.fetch_supplier_pool().get_supplier(supplier_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(supplier).encode("utf-8"))
                case 3:
                    if paths[2] == "items":
                        supplier_id = int(paths[1])
                        items = data_provider.fetch_item_pool().get_items_for_supplier(supplier_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(items).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers() 
        elif paths[0] == "orders":
            parts = len(paths)
            match parts:
                case 1:
                    orders = data_provider.fetch_order_pool().get_orders()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(orders).encode("utf-8"))
                case 2:
                    order_id = int(paths[1])
                    order = data_provider.fetch_order_pool().get_order(order_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(order).encode("utf-8"))
                case 3:
                    if paths[2] == "items":
                        order_id = int(paths[1])
                        items = data_provider.fetch_order_pool().get_items_in_order(order_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(items).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "clients":
            parts = len(paths)
            match parts:
                case 1:
                    clients = data_provider.fetch_client_pool().get_clients()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(clients).encode("utf-8"))
                case 2:
                    client_id = int(paths[1])
                    client = data_provider.fetch_client_pool().get_client(client_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(client).encode("utf-8"))     
                case 3:
                    if paths[2] == "orders":
                        client_id = int(paths[1])
                        orders = data_provider.fetch_order_pool().get_orders_for_client(client_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(orders).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers() 
        elif paths[0] == "shipments":
            parts = len(paths)
            match parts:
                case 1:
                    shipments = data_provider.fetch_shipment_pool().get_shipments()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(shipments).encode("utf-8"))
                case 2:
                    shipment_id = int(paths[1])
                    shipment = data_provider.fetch_shipment_pool().get_shipment(shipment_id)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(shipment).encode("utf-8"))
                case 3:
                    if paths[2] == "orders":
                        shipment_id = int(paths[1])
                        orders = data_provider.fetch_shipment_pool().get_order_ids_in_shipment(shipment_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(orders).encode("utf-8"))
                    elif paths[2] == "items":
                        shipment_id = int(paths[1])
                        items = data_provider.fetch_shipment_pool().get_items_in_shipment(shipment_id)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(items).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        if user == None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                paths = self.path.split("/")
                if len(paths) > 3 and paths[1] == "api" and paths[2] == "v1":
                    self.handle_get_version_1(paths[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()

    def handle_post_version_1(self, paths, user):
        if not auth_provider.has_access(user, paths, "post"):
            self.send_response(403)
            self.end_headers()
            return
        if paths[0] == "warehouses":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_warehouse = json.loads(post_data.decode())
            data_provider.fetch_warehouse_pool().add_warehouse(new_warehouse)
            data_provider.fetch_warehouse_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "locations":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_location = json.loads(post_data.decode())
            data_provider.fetch_location_pool().add_location(new_location)
            data_provider.fetch_location_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "transfers":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_transfer = json.loads(post_data.decode())
            data_provider.fetch_transfer_pool().add_transfer(new_transfer)
            data_provider.fetch_transfer_pool().save()
            notification_processor.push(f"Scheduled batch transfer {new_transfer['id']}")
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "items":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item = json.loads(post_data.decode())
            data_provider.fetch_item_pool().add_item(new_item)
            data_provider.fetch_item_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "item_lines":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item_line = json.loads(post_data.decode())
            data_provider.fetch_item_line_pool().add_item_line(new_item_line)
            data_provider.fetch_item_line_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "item_groups":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item_group = json.loads(post_data.decode())
            data_provider.fetch_item_group_pool().add_item_group(new_item_group)
            data_provider.fetch_item_group_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "item_types":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item_type = json.loads(post_data.decode())
            data_provider.fetch_item_type_pool().add_item_type(new_item_type)
            data_provider.fetch_item_type_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "inventories":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_inventory = json.loads(post_data.decode())
            data_provider.fetch_inventory_pool().add_inventory(new_inventory)
            data_provider.fetch_inventory_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "suppliers":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_supplier = json.loads(post_data.decode())
            data_provider.fetch_supplier_pool().add_supplier(new_supplier)
            data_provider.fetch_supplier_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "orders":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_order = json.loads(post_data.decode())
            data_provider.fetch_order_pool().add_order(new_order)
            data_provider.fetch_order_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "clients":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_client = json.loads(post_data.decode())
            data_provider.fetch_client_pool().add_client(new_client)
            data_provider.fetch_client_pool().save()
            self.send_response(201)
            self.end_headers()
        elif paths[0] == "shipments":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_shipment = json.loads(post_data.decode())
            data_provider.fetch_shipment_pool().add_shipment(new_shipment)
            data_provider.fetch_shipment_pool().save()
            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        if user == None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                paths = self.path.split("/")
                if len(paths) > 3 and paths[1] == "api" and paths[2] == "v1":
                    self.handle_post_version_1(paths[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()

    def handle_put_version_1(self, paths, user):
        if not auth_provider.has_access(user, paths, "put"):
            self.send_response(403)
            self.end_headers()
            return
        if paths[0] == "warehouses":
            warehouse_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_warehouse = json.loads(post_data.decode())
            data_provider.fetch_warehouse_pool().update_warehouse(warehouse_id, updated_warehouse)
            data_provider.fetch_warehouse_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "locations":
            location_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_location = json.loads(post_data.decode())
            data_provider.fetch_location_pool().update_location(location_id, updated_location)
            data_provider.fetch_location_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "transfers":
            parts = len(paths)
            match parts:
                case 2:
                    transfer_id = int(paths[1])
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_transfer = json.loads(post_data.decode())
                    data_provider.fetch_transfer_pool().update_transfer(transfer_id, updated_transfer)
                    data_provider.fetch_transfer_pool().save()
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if paths[2] == "commit":
                        transfer_id = int(paths[1])
                        transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
                        from_location_id = transfer["from_location_id"]
                        to_location_id = transfer["to_location_id"]
                        inventory_pool = data_provider.fetch_inventory_pool()
                        for x in transfer["items"]:
                            item_id = x["item_id"]
                            amount = x["amount"]
                            # decrease on-hand at the source location
                            src = inventory_pool.get_inventory(item_id, from_location_id)
                            if src is not None:
                                src["quantity_on_hand"] -= amount
                                inventory_pool.update_inventory(item_id, from_location_id, src)
                            # increase (or create) on-hand at the destination location
                            dst = inventory_pool.get_inventory(item_id, to_location_id)
                            if dst is not None:
                                dst["quantity_on_hand"] += amount
                                inventory_pool.update_inventory(item_id, to_location_id, dst)
                            else:
                                inventory_pool.add_inventory({
                                    "item_id": item_id,
                                    "location_id": to_location_id,
                                    "quantity_on_hand": amount,
                                    "quantity_expected": 0,
                                    "quantity_ordered": 0,
                                    "quantity_allocated": 0,
                                })
                        transfer["transfer_status"] = "Processed"
                        transfer.pop("items", None)
                        data_provider.fetch_transfer_pool().update_transfer(transfer_id, transfer)
                        notification_processor.push(f"Processed batch transfer with id:{transfer['id']}")
                        data_provider.fetch_transfer_pool().save()
                        data_provider.fetch_inventory_pool().save()
                        self.send_response(200)
                        self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "items":
            item_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item = json.loads(post_data.decode())
            data_provider.fetch_item_pool().update_item(item_id, updated_item)
            data_provider.fetch_item_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "item_lines":
            item_line_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_line = json.loads(post_data.decode())
            data_provider.fetch_item_line_pool().update_item_line(item_line_id, updated_item_line)
            data_provider.fetch_item_line_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "item_groups":
            item_group_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_group = json.loads(post_data.decode())
            data_provider.fetch_item_group_pool().update_item_group(item_group_id, updated_item_group)
            data_provider.fetch_item_group_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "item_types":
            item_type_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_type = json.loads(post_data.decode())
            data_provider.fetch_item_type_pool().update_item_type(item_type_id, updated_item_type)
            data_provider.fetch_item_type_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "inventories":
            # Inventory rows are keyed on a composite (item_id, location_id); a
            # single surrogate id is not meaningful in the new schema.
            self.send_response(404)
            self.end_headers()
        elif paths[0] == "suppliers":
            supplier_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_supplier = json.loads(post_data.decode())
            data_provider.fetch_supplier_pool().update_supplier(supplier_id, updated_supplier)
            data_provider.fetch_supplier_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "orders":
            parts = len(paths)
            match parts:
                case 2:
                    order_id = int(paths[1])
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_order = json.loads(post_data.decode())
                    data_provider.fetch_order_pool().update_order(order_id, updated_order)
                    data_provider.fetch_order_pool().save()
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if paths[2] == "items":
                        order_id = int(paths[1])
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_items = json.loads(post_data.decode())
                        data_provider.fetch_order_pool().update_items_in_order(order_id, updated_items)
                        data_provider.fetch_order_pool().save()
                        self.send_response(200)
                        self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif paths[0] == "clients":
            client_id = int(paths[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_client = json.loads(post_data.decode())
            data_provider.fetch_client_pool().update_client(client_id, updated_client)
            data_provider.fetch_client_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "shipments":
            parts = len(paths)
            match parts:
                case 2:
                    shipment_id = int(paths[1])
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_shipment = json.loads(post_data.decode())
                    data_provider.fetch_shipment_pool().update_shipment(shipment_id, updated_shipment)
                    data_provider.fetch_shipment_pool().save()
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if paths[2] == "orders":
                        shipment_id = int(paths[1])
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_orders = json.loads(post_data.decode())
                        data_provider.fetch_shipment_pool().update_orders_in_shipment(shipment_id, updated_orders)
                        data_provider.fetch_shipment_pool().save()
                        self.send_response(200)
                        self.end_headers()
                    elif paths[2] == "items":
                        shipment_id = int(paths[1])
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_items = json.loads(post_data.decode())
                        data_provider.fetch_shipment_pool().update_items_in_shipment(shipment_id, updated_items)
                        data_provider.fetch_shipment_pool().save()
                        self.send_response(200)
                        self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        if user == None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                paths = self.path.split("/")
                if len(paths) > 3 and paths[1] == "api" and paths[2] == "v1":
                    self.handle_put_version_1(paths[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()

    def handle_delete_version_1(self, paths, user):
        if not auth_provider.has_access(user, paths, "delete"):
            self.send_response(403)
            self.end_headers()
            return
        if paths[0] == "warehouses":
            warehouse_id = int(paths[1])
            data_provider.fetch_warehouse_pool().remove_warehouse(warehouse_id)
            data_provider.fetch_warehouse_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "locations":
            location_id = int(paths[1])
            data_provider.fetch_location_pool().remove_location(location_id)
            data_provider.fetch_location_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "transfers":
            transfer_id = int(paths[1])
            data_provider.fetch_transfer_pool().remove_transfer(transfer_id)
            data_provider.fetch_transfer_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "items":
            item_id = int(paths[1])
            data_provider.fetch_item_pool().remove_item(item_id)
            data_provider.fetch_item_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "item_lines":
            item_line_id = int(paths[1])
            data_provider.fetch_item_line_pool().remove_item_line(item_line_id)
            data_provider.fetch_item_line_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "item_groups":
            item_group_id = int(paths[1])
            data_provider.fetch_item_group_pool().remove_item_group(item_group_id)
            data_provider.fetch_item_group_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "item_types":
            item_type_id = int(paths[1])
            data_provider.fetch_item_type_pool().remove_item_type(item_type_id)
            data_provider.fetch_item_type_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "inventories":
            self.send_response(404)
            self.end_headers()
        elif paths[0] == "suppliers":
            supplier_id = int(paths[1])
            data_provider.fetch_supplier_pool().remove_supplier(supplier_id)
            data_provider.fetch_supplier_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "orders":
            order_id = int(paths[1])
            data_provider.fetch_order_pool().remove_order(order_id)
            data_provider.fetch_order_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "clients":
            client_id = int(paths[1])
            data_provider.fetch_client_pool().remove_client(client_id)
            data_provider.fetch_client_pool().save()
            self.send_response(200)
            self.end_headers()
        elif paths[0] == "shipments":
            shipment_id = int(paths[1])
            data_provider.fetch_shipment_pool().remove_shipment(shipment_id)
            data_provider.fetch_shipment_pool().save()
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        if user == None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                paths = self.path.split("/")
                if len(paths) > 3 and paths[1] == "api" and paths[2] == "v1":
                    self.handle_delete_version_1(paths[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()

if __name__ == "__main__":
    PORT = 3000
    with socketserver.TCPServer(("", PORT), ApiRequestHandler) as httpd:
        notification_processor.start()
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()