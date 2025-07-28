#!/usr/bin/env python3
"""
Web Server for Telegram Bot Status Dashboard

Provides a web interface to monitor bot status and webhook endpoint.
"""

import os
import json
import asyncio
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from threading import Thread
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Bot status tracking
bot_stats = {
    'status': 'online',
    'api_status': 'connected',
    'start_time': datetime.now(),
    'response_count': 0,
    'active_users': set(),
    'last_message_time': None,
    'average_response_time': 2.5
}

@app.route('/')
def dashboard():
    """Serve the status dashboard"""
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>Bot Status Dashboard</h1>
        <p>Dashboard file not found. Please ensure index.html exists.</p>
        <p><strong>Bot Status:</strong> Running</p>
        <p><strong>API Status:</strong> Connected</p>
        """

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    uptime = datetime.now() - bot_stats['start_time']
    uptime_hours = uptime.total_seconds() / 3600
    
    return jsonify({
        'bot_status': 'Online' if bot_stats['status'] == 'online' else 'Offline',
        'api_status': 'Connected' if bot_stats['api_status'] == 'connected' else 'Disconnected',
        'response_time': f"~{bot_stats['average_response_time']:.1f}s",
        'active_users': len(bot_stats['active_users']),
        'uptime_hours': f"{uptime_hours:.1f}h",
        'total_responses': bot_stats['response_count'],
        'last_message': bot_stats['last_message_time'].strftime('%H:%M:%S') if bot_stats['last_message_time'] else 'None',
        'start_time': bot_stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for Telegram bot"""
    try:
        update_data = request.get_json()
        
        if update_data and 'message' in update_data:
            # Update bot statistics
            user_id = update_data['message']['from']['id']
            bot_stats['active_users'].add(user_id)
            bot_stats['last_message_time'] = datetime.now()
            bot_stats['response_count'] += 1
            
            logger.info(f"Webhook received message from user {user_id}")
            
            # Here you would typically process the message
            # For now, we'll just acknowledge receipt
            return jsonify({'status': 'ok'}), 200
        
        return jsonify({'status': 'no_message'}), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'bot_running': bot_stats['status'] == 'online'
    })

def update_bot_stats(status=None, api_status=None, response_time=None, user_id=None):
    """Update bot statistics from external calls"""
    if status:
        bot_stats['status'] = status
    if api_status:
        bot_stats['api_status'] = api_status
    if response_time:
        bot_stats['average_response_time'] = response_time
    if user_id:
        bot_stats['active_users'].add(user_id)
        bot_stats['last_message_time'] = datetime.now()
        bot_stats['response_count'] += 1

def run_server():
    """Run the Flask server"""
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run_server()