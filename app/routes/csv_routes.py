import os
import secrets
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
from app import db, app
from app.models.Importsalesdata import Sales, ImportSalesData

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@app.route('/')
def index():
    """Serve CSV upload form"""
    return render_template('upload.html')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def secure_upload_file(file):
    """Securely save an uploaded file"""
    if not file or file.filename == '':
        raise ValueError("No file selected")
    
    if not allowed_file(file.filename):
        raise ValueError("Only CSV files are allowed")
    
    original_filename = secure_filename(file.filename)
    unique_filename = f"{secrets.token_hex(8)}_{original_filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)
    
    return unique_filename, original_filename


@upload_bp.route('/csv', methods=['POST'])
def upload_csv():
    """Handle CSV file upload and import sales data"""
    try:
        if 'csv' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400
        
        file = request.files['csv']
        
        try:
            unique_filename, original_filename = secure_upload_file(file)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            importer = ImportSalesData(filepath)
            result = importer.import_and_save_to_db()
            
            if not result['success']:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify(result), 400
            
            return jsonify({
                'success': True,
                'message': result['message'],
                'count': result['count'],
                'filename': original_filename
            }), 201
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Import failed: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@upload_bp.route('/sales', methods=['GET'])
def get_sales():
    """Retrieve all imported sales records with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)
        
        pagination = Sales.query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'data': [sale.to_dict() for sale in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve sales: {str(e)}'}), 500


@upload_bp.route('/sales/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    """Retrieve a specific sales record"""
    try:
        sale = Sales.query.get_or_404(sale_id)
        return jsonify(sale.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Sale not found'}), 404


@upload_bp.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    """Delete a sales record"""
    try:
        sale = Sales.query.get_or_404(sale_id)
        db.session.delete(sale)
        db.session.commit()
        return jsonify({'message': 'Sales record deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete: {str(e)}'}), 500


@upload_bp.route('/sales/stats', methods=['GET'])
def get_sales_stats():
    """Get sales statistics"""
    try:
        from sqlalchemy import func
        
        stats = db.session.query(
            func.count(Sales.id).label('total_records'),
            func.sum(Sales.quantity).label('total_quantity'),
            func.sum(Sales.price * Sales.quantity).label('total_revenue'),
            func.avg(Sales.price).label('avg_price')
        ).first()
        
        return jsonify({
            'total_records': stats.total_records or 0,
            'total_quantity': stats.total_quantity or 0,
            'total_revenue': float(stats.total_revenue or 0),
            'avg_price': float(stats.avg_price or 0)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve stats: {str(e)}'}), 500

@app.route('/api')
def api_info():
    """API information endpoint"""
    return {
        'status': 'ok',
        'message': 'Book Express API is running',
        'endpoints': {
            'upload_csv': 'POST /upload/csv',
            'get_sales': 'GET /upload/sales',
            'get_sales_stats': 'GET /upload/sales/stats',
            'get_single_sale': 'GET /upload/sales/<id>',
            'delete_sale': 'DELETE /upload/sales/<id>'
        }
    }, 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {'error': 'Endpoint not found'}, 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return {'error': 'Internal server error'}, 500
