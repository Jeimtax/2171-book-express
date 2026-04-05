import csv
import os
from datetime import datetime
from app import db


class Sales(db.Model):
    __tablename__ = "Sales"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, date, product_id, quantity, price):
        self.date = date
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Sales {self.id}: Product {self.product_id}, Qty: {self.quantity}, Price: ${self.price}>'


class ImportSalesData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.errors = []

    def import_data(self):
        """Import CSV data and return list of processed rows"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        sales_data = []
        self.errors = []
        
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            if csv_reader.fieldnames is None or not self._validate_headers(csv_reader.fieldnames):
                raise ValueError("CSV must contain columns: date, product_id, quantity, price")
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (header is 1)
                try:
                    processed = self.process_row(row)
                    sales_data.append(processed)
                except Exception as e:
                    self.errors.append(f"Row {row_num}: {str(e)}")
        
        return sales_data

    def import_and_save_to_db(self):
        """Import CSV data and save to database"""
        sales_data = self.import_data()
        
        if self.errors:
            return {
                'success': False,
                'message': f'Imported with {len(self.errors)} errors',
                'errors': self.errors,
                'count': 0
            }
        
        try:
            for data in sales_data:
                sale = Sales(
                    date=data['date'],
                    product_id=data['product_id'],
                    quantity=data['quantity'],
                    price=data['price']
                )
                db.session.add(sale)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Successfully imported {len(sales_data)} records',
                'count': len(sales_data),
                'errors': []
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Database error: {str(e)}',
                'count': 0,
                'errors': [str(e)]
            }

    def process_row(self, row):
        """Process and validate each row"""
        try:
            return {
                "date": datetime.strptime(row["date"].strip(), "%Y-%m-%d"),
                "product_id": int(row["product_id"].strip()),
                "quantity": int(row["quantity"].strip()),
                "price": float(row["price"].strip()),
            }
        except ValueError as e:
            raise ValueError(f"Invalid data format: {str(e)}")
        except KeyError as e:
            raise KeyError(f"Missing required column: {str(e)}")

    def _validate_headers(self, headers):
        """Validate CSV headers"""
        required_headers = {'date', 'product_id', 'quantity', 'price'}
        return required_headers.issubset(set(h.lower().strip() for h in headers))