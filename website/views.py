from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Wallet
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
	return render_template("home.html", user=current_user)

@views.route('/add_wallet', methods=['GET', 'POST'])
@login_required
def add_wallet():
	if request.method == 'GET':
		return render_template("add_wallet.html", user=current_user)
		
	if request.method == 'POST':
		wallet_name = request.form.get('wallet_name')

		if len(wallet_name) < 1:
			flash('Wallet name is too short!', category='error')
		else:
			new_wallet = Wallet(wallet_name=wallet_name, user_id=current_user.id)
			db.session.add(new_wallet)
			db.session.commit()
			flash('New wallet added!', category='success')

	return render_template("home.html", user=current_user)

@views.route('/delete-wallet', methods=['POST'])
def delete_wallet():
	wallet = json.loads(request.data)
	print(wallet)
	walletId = wallet['walletId']
	wallet = Wallet.query.get(walletId)
	if wallet:
		if wallet.user_id == current_user.id:
			db.session.delete(wallet)
			db.session.commit()

	return jsonify({})