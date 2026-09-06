import json
import os
import tempfile
import csv

# 1. Product Model (Data Architecture Evolution - Week 9)
class Product:
    def __init__(self, product_id, name, quantity, price, barcode="", reorder_point=5):
        self.id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.barcode = barcode
        self.reorder_point = reorder_point

    def is_low_stock(self) -> bool:
        return self.quantity <= self.reorder_point

# 2. Inventory Repository (Data Access Layer - Week 8, 10, 11)
class InventoryRepository:
    def __init__(self, filename='data.json'):
        self.filename = filename

    def load_all(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                products = {}
                for pid, pdata in data.items():
                    # RCA: ใช้ .get() เพื่อรองรับ Legacy Schema ป้องกัน KeyError (Week 10)
                    products[pid] = Product(
                        product_id=pid,
                        name=pdata.get('name', ''),
                        quantity=pdata.get('quantity', 0),
                        price=pdata.get('price', 0.0),
                        barcode=pdata.get('barcode', ''),
                        reorder_point=pdata.get('reorder_point', 5)
                    )
                return products
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_all(self, products):
        data = {
            pid: {
                'name': p.name,
                'quantity': p.quantity,
                'price': p.price,
                'barcode': p.barcode,
                'reorder_point': p.reorder_point
            } for pid, p in products.items()
        }
        
        # Atomic File Writing ป้องกัน Data Corruption (Week 11)
        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(self.filename) or '.')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            os.replace(temp_path, self.filename)
        except Exception as e:
            os.remove(temp_path)
            raise e

# 3. Csv Exporter (Emergency CR-02 - Week 10)
class CsvExporter:
    @staticmethod
    def export_low_stock(filename, low_stock_products):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Quantity', 'Price', 'Barcode', 'Reorder Point'])
            for p in low_stock_products:
                writer.writerow([p.id, p.name, p.quantity, p.price, p.barcode, p.reorder_point])

# 4. Inventory Service (Business Logic Layer - Week 8, 9)
class InventoryService:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository
        self.products = self.repository.load_all()

    def add_product(self, product_id, name, quantity, price, barcode="", reorder_point=5):
        self.products[product_id] = Product(product_id, name, quantity, price, barcode, reorder_point)
        self.repository.save_all(self.products)

    def update_quantity(self, product_id, amount):
        if product_id in self.products:
            self.products[product_id].quantity += amount
            self.repository.save_all(self.products)
            return True
        return False

    def calculate_total_inventory_value(self):
        return sum(p.quantity * p.price for p in self.products.values())

    def get_low_stock_alerts(self) -> list:
        return [p for p in self.products.values() if p.is_low_stock()]

# --- ตัวอย่างการใช้งานโปรแกรมหลัก (Main Execution) ---
def main():
    repo = InventoryRepository('data.json')
    service = InventoryService(repo)

    while True:
        print("\n--- Mini Inventory System v2.0.0 ---")
        print("1. เพิ่มสินค้าใหม่ (รองรับ Barcode)")
        print("2. ปรับปรุงจำนวนสต็อก")
        print("3. ตรวจสอบสินค้าสต็อกต่ำ")
        print("4. ส่งออกรายงานสินค้าสต็อกต่ำ (CSV)")
        print("5. ออกจากระบบ")
        
        choice = input("เลือกเมนู: ")
        
        if choice == '1':
            pid = input("รหัสสินค้า: ")
            name = input("ชื่อสินค้า: ")
            qty = int(input("จำนวน: "))
            price = float(input("ราคา: "))
            barcode = input("บาร์โค้ด (เว้นว่างได้): ")
            reorder = input("จุดสั่งซื้อขั้นต่ำ (ค่าเริ่มต้น 5): ")
            reorder = int(reorder) if reorder else 5
            
            service.add_product(pid, name, qty, price, barcode, reorder)
            print("เพิ่มสินค้าสำเร็จ!")
            
        elif choice == '2':
            pid = input("รหัสสินค้า: ")
            amount = int(input("จำนวนที่เพิ่ม/ลด (ใส่ค่าติดลบเพื่อลด): "))
            if service.update_quantity(pid, amount):
                print("ปรับปรุงสต็อกสำเร็จ!")
                # เช็ค Alert ทันทีหลังตัดสต็อก (UAT Scenario)
                alerts = service.get_low_stock_alerts()
                if any(p.id == pid for p in alerts):
                    print("⚠️ แจ้งเตือน: สินค้ารายการนี้สต็อกต่ำกว่าเกณฑ์แล้ว!")
            else:
                print("ไม่พบสินค้ารหัสนี้")
                
        elif choice == '3':
            alerts = service.get_low_stock_alerts()
            print("\n--- รายการสินค้าสต็อกต่ำ ---")
            for p in alerts:
                print(f"[{p.id}] {p.name} - คงเหลือ: {p.quantity} (จุดสั่งซื้อ: {p.reorder_point})")
                
        elif choice == '4':
            alerts = service.get_low_stock_alerts()
            CsvExporter.export_low_stock('low_stock_report.csv', alerts)
            print("ส่งออกไฟล์ low_stock_report.csv สำเร็จ!")
            
        elif choice == '5':
            break

if __name__ == "__main__":
    main()
