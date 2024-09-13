#!/usr/bin/env python3
"""
Setting up the routes for the admin Blueprint to
handle admin specific tasks.
"""

from .__init__ import admin
from flask_login import login_required, current_user
from flask import request, redirect, url_for
from flask import render_template, flash
from app.models import User
from app.forms import ManageUsersForm
from app.extensions import db


@login_required
@admin.route('/admin/manage_users', methods=['GET', 'POST'])
def manage_users():
    """
    Querying the database for all the users. Managing user
    accounts, including activating, deactivating, or
    deleting users.
    """
    if not current_user.is_admin:
        flash("You do not have permission to this page.")
        return redirect(url_for('main.homepage'))

    all_users = User.query.all()
    form = ManageUsersForm()
    # Populating the choices dynamically
    form.user.choices = [(user.id, user.username) for user in all_users]
    
    if request.method == 'POST':
        # Validating the form and collecting its data
        if form.validate_on_submit():
            user_id = form.user.data
            action = form.action.data
            user = User.query.get(user_id)
            if user is None:
                flash("Invalid user id, please try again with a user id that exists.")
                return redirect(url_for('admin.manage_users'))
            username = user.username

            if action == 'activate':
                user.is_active = True
            elif action == 'deactivate':
                user.is_active = False
            elif action == 'delete':
                # Check if user is trying to delete themselves
                if user.id == current_user.id:
                    flash("You cannot delete your own account.")
                    return redirect(url_for('admin.manage_users'))
                # Check if the deletion confirmation checkbox is checked in the UI
                if not form.confirm_delete.data:
                    flash("Please confirm deletion by checking the checkbox.")
                    return redirect(url_for('admin.manage_users'))
                db.session.delete(user)

            db.session.commit()
            flash(f"User {username} {action}d successfully.")
            return redirect(url_for('admin.manage_users'))
    return render_template('manage_users.html', form=form)
