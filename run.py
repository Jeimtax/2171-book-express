"""
Main Flask application entry point
"""
import os
from app import app, db
from flask import render_template


@app.shell_context_processor
def make_shell_context():
    """Add database to shell context"""
    return {'db': db}


@app.route('/')
def index():
    """Serve CSV upload form"""
    return render_template('upload.html')


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
