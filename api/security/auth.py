import os

import boto3
from flask import Blueprint, jsonify, make_response, request



auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/status", methods=["POST"]) 
def login():
    pass
def sign_up():
    pass