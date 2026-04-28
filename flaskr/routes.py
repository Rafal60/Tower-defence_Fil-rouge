from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return {'status': 'ok', 'message': 'Tower Defense API'}


@main_bp.route('/health')
def health():
    return {'status': 'healthy'}
