#!/usr/bin/env python3
"""
Defines the app_views Blueprint for organizing the API routes.
"""
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Blueprint for API version 1 routes with a URL prefix of /api/v1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Load users from file storage upon initialization
User.load_from_file()
