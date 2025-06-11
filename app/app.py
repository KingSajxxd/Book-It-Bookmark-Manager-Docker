from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
import validators
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# MongoDB connection with authentication from environment variable
try:
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection on a request as a check

    db = client['bookmarkdb'] # Explicitly choose bookmarkdb
    bookmarks = db['bookmarks']

    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

@app.route('/')
def index():
    """Display all bookmarks with search functionality"""
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 10
    
    try:
        if search_query:
            query = {
                '$or': [
                    {'name': {'$regex': search_query, '$options': 'i'}},
                    {'url': {'$regex': search_query, '$options': 'i'}}
                ]
            }
            total_bookmarks = bookmarks.count_documents(query)
            all_bookmarks = bookmarks.find(query).sort('created_at', -1).skip((page-1)*per_page).limit(per_page)
        else:
            total_bookmarks = bookmarks.count_documents({})
            all_bookmarks = bookmarks.find().sort('created_at', -1).skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total_bookmarks + per_page - 1) // per_page
        
        return render_template('index.html', 
                             bookmarks=all_bookmarks, 
                             search_query=search_query,
                             current_page=page,
                             total_pages=total_pages,
                             total_bookmarks=total_bookmarks)
    except Exception as e:
        logger.error(f"Error fetching bookmarks: {e}")
        flash('Error loading bookmarks', 'error')
        return render_template('index.html', bookmarks=[], search_query='', current_page=1, total_pages=1, total_bookmarks=0)

@app.route('/add', methods=['POST'])
def add_bookmark():
    """Add a new bookmark with validation"""
    try:
        url = request.form.get('url', '').strip()
        name = request.form.get('name', '').strip()
        category = request.form.get('category', 'General').strip()
        description = request.form.get('description', '').strip()
        
        # Validation
        if not url or not name:
            flash('Name and URL are required', 'error')
            return redirect(url_for('index'))
        
        if not validators.url(url):
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('index'))
        
        # Check for duplicates
        existing = bookmarks.find_one({'url': url})
        if existing:
            flash('This URL is already bookmarked', 'warning')
            return redirect(url_for('index'))
        
        # Create bookmark document
        bookmark_doc = {
            'name': name,
            'url': url,
            'category': category,
            'description': description,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        bookmarks.insert_one(bookmark_doc)
        flash(f'Bookmark "{name}" added successfully', 'success')
        logger.info(f"Added bookmark: {name} - {url}")
        
    except Exception as e:
        logger.error(f"Error adding bookmark: {e}")
        flash('Error adding bookmark', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_bookmark(id):
    """Edit an existing bookmark"""
    try:
        bookmark = bookmarks.find_one({'_id': ObjectId(id)})
        if not bookmark:
            flash('Bookmark not found', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            url = request.form.get('url', '').strip()
            name = request.form.get('name', '').strip()
            category = request.form.get('category', 'General').strip()
            description = request.form.get('description', '').strip()
            
            # Validation
            if not url or not name:
                flash('Name and URL are required', 'error')
                return render_template('edit.html', bookmark=bookmark)
            
            if not validators.url(url):
                flash('Please enter a valid URL', 'error')
                return render_template('edit.html', bookmark=bookmark)
            
            # Update bookmark
            bookmarks.update_one(
                {'_id': ObjectId(id)},
                {
                    '$set': {
                        'name': name,
                        'url': url,
                        'category': category,
                        'description': description,
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            flash(f'Bookmark "{name}" updated successfully', 'success')
            logger.info(f"Updated bookmark: {name} - {url}")
            return redirect(url_for('index'))
        
        return render_template('edit.html', bookmark=bookmark)
        
    except Exception as e:
        logger.error(f"Error editing bookmark {id}: {e}")
        flash('Error editing bookmark', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_bookmark(id):
    """Delete a bookmark with confirmation"""
    try:
        result = bookmarks.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            flash('Bookmark deleted successfully', 'success')
            logger.info(f"Deleted bookmark with id: {id}")
        else:
            flash('Bookmark not found', 'error')
    except Exception as e:
        logger.error(f"Error deleting bookmark {id}: {e}")
        flash('Error deleting bookmark', 'error')
    
    return redirect(url_for('index'))

@app.route('/categories')
def get_categories():
    """Get all unique categories"""
    try:
        categories = bookmarks.distinct('category')
        return jsonify(categories)
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify([])

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
