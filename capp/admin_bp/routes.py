from flask import Blueprint, jsonify, render_template, redirect, flash, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from capp import db, bcrypt
from capp.admin_bp.forms import AdminLoginForm, CategoryForm, AddSectionForm, AddSentenceForm
from capp.models import User, Category, Section, Sentence
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Unauthorized access", "danger")
        return redirect(url_for('users.login'))

    # Fetch stats or recent activities for the dashboard
    categories_count = Category.query.count()
    sections_count = Section.query.count()
    sentences_count = Sentence.query.count()
    sections = Section.query.all()  # Fetch all sections
    sentences = Sentence.query.all()  # Fetch all sentences

    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard',
        username=current_user.username,
        categories_count=categories_count,
        sections_count=sections_count,
        sentences_count=sentences_count,
        sections=sections,  # Pass sections to the template
        sentences=sentences  # Pass sentences to the template
    )



@admin_bp.route('/manage_users', methods=['GET'])
@login_required
def manage_users():
    if not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('admin_bp.admin_dashboard'))

    users = User.query.all()  # Retrieve all users
    return render_template('admin/promote_user.html', users=users)

@admin_bp.route('/promote_user/<int:user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('admin_bp.admin_dashboard'))

    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash(f"User {user.username} is already an admin.", "info")
    else:
        user.is_admin = True
        db.session.commit()
        flash(f"User {user.username} has been promoted to admin.", "success")

    return redirect(url_for('admin_bp.manage_users'))


# Admin Logout Route
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home.home_home'))

# Add Category Route
@admin_bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category_name = form.name.data
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash(f'Category "{category_name}" added successfully!', 'success')
        return redirect(url_for('admin_bp.add_category'))  # Redirect to the same page to add more categories
    return render_template('admin/add_category.html', form=form)

# View Categories Route
@admin_bp.route('/categories')
@login_required
def categories():
    all_categories = Category.query.all()  # Get all categories from the database
    return render_template('admin/view_categories.html', categories=all_categories)

# Add Section Route
@admin_bp.route('/add_section', methods=['GET', 'POST'])
@login_required
def add_section():
    form = AddSectionForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        # Retrieve the selected category by ID
        category = Category.query.get(form.category.data)
        if category:  # Check if the category exists
            # Create new section including the icon class
            section = Section(
                name=form.section_name.data, 
                category_id=category.id, 
                icon=form.icon.data  # Save the icon class
            )
            db.session.add(section)
            db.session.commit()
            flash(f'Section "{form.section_name.data}" added to category "{category.name}" with icon "{form.icon.data}"', 'success')
            return redirect(url_for('admin_bp.add_section'))  # Redirect to add another section
        else:
            flash('Invalid category selected.', 'danger')
    return render_template('admin/add_section.html', form=form)


# View Sections Route
@admin_bp.route('/view_sections', methods=['GET'])
@login_required
def view_sections():
    selected_category_id = request.args.get('category_id')  # Get the selected category ID from URL args

    # Fetch sections if a category is selected
    if selected_category_id:
        selected_category_id = int(selected_category_id)
        categories = Category.query.filter_by(id=selected_category_id).all()
    else:
        categories = Category.query.all()

    return render_template('admin/view_sections.html', categories=categories, selected_category_id=selected_category_id)


# Edit Section Route
@admin_bp.route('/edit_section/<int:section_id>', methods=['GET', 'POST'])
@login_required
def edit_section(section_id):
    section = Section.query.options(joinedload(Section.category)).get_or_404(section_id)  # Eager load the category
    form = AddSectionForm()

    # Populate categories for the dropdown
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        section.name = form.section_name.data
        section.category_id = form.category.data
        section.icon = form.icon.data  # Save the icon link
        db.session.commit()
        flash(f'Section "{section.name}" updated successfully!', 'success')
        return redirect(url_for('admin_bp.view_sections'))

    # Prefill the form with existing data
    form.section_name.data = section.name
    form.category.data = section.category_id  # Set the category field with the category ID
    form.icon.data = section.icon  # Prefill the icon link

    return render_template('admin/edit_section.html', form=form, section=section)


# Delete Section Route with handling dependent sentences
@admin_bp.route('/delete_section/<int:section_id>', methods=['POST'])
@login_required
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)  # Find the section by ID

    # Check if the section has dependent sentences
    dependent_sentences = Sentence.query.filter_by(section_id=section_id).all()
    
    if dependent_sentences:
        # If there are dependent sentences, show a warning and prevent deletion
        flash(f'Cannot delete section "{section.name}" because it has dependent sentences.', 'danger')
        return redirect(url_for('admin_bp.view_sections'))

    # Now delete the section if there are no dependent sentences
    db.session.delete(section)  # Delete the section
    db.session.commit()  # Commit the change
    
    flash(f'Section "{section.name}" has been deleted!', 'success')
    return redirect(url_for('admin_bp.view_sections'))  # Redirect to the view sections page



# Add Sentence Route
@admin_bp.route('/add_sentence', methods=['GET', 'POST'])
@login_required
def add_sentence():
    form = AddSentenceForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.category.data:
        form.section.choices = [(s.id, s.name) for s in Section.query.filter_by(category_id=form.category.data).all()]

    if form.validate_on_submit():
        sentence = Sentence(
            english_sentence=form.english_sentence.data,
            spanish_sentence=form.spanish_sentence.data,
            explanation_english=form.explanation_english.data,
            explanation_spanish=form.explanation_spanish.data,
            category_id=form.category.data,
            section_id=form.section.data if form.section.data else None,  # Ensure section_id is not None
            image_path=form.image_path.data,
        )
        db.session.add(sentence)
        db.session.commit()
        flash('Sentence added successfully!', 'success')
        return redirect(url_for('admin_bp.add_sentence'))

    return render_template('admin/add_sentence.html', form=form)



@admin_bp.route('/get_sections/<int:category_id>', methods=['GET'])
def get_sections(category_id):
    sections = Section.query.filter_by(category_id=category_id).all()
    sections_data = [{'id': section.id, 'name': section.name} for section in sections]
    return jsonify(sections_data)



# View Sentences Route with Category Filtering
@admin_bp.route('/view_sentences', methods=['GET', 'POST'])
@login_required
def view_sentences():
    categories = Category.query.all()  # Get all categories
    sections = None  # Initialize sections variable
    selected_category_id = request.args.get('category_id')  # Get the selected category ID from URL args
    selected_section_id = request.args.get('section_id')  # Get the selected section ID from URL args

    # Fetch sections if a category is selected
    if selected_category_id:
        selected_category_id = int(selected_category_id)
        sections = Section.query.filter_by(category_id=selected_category_id).all()
    else:
        selected_category_id = None

    # Filter sentences based on selected category and section
    query = Sentence.query
    if selected_category_id:
        query = query.filter_by(category_id=selected_category_id)
    if selected_section_id:
        query = query.filter_by(section_id=int(selected_section_id))

    sentences = query.all()

    return render_template(
        'admin/view_sentences.html',
        sentences=sentences,
        categories=categories,
        sections=sections,
        selected_category_id=selected_category_id,
        selected_section_id=int(selected_section_id) if selected_section_id else None
    )




# Delete Sentence Route
@admin_bp.route('/delete_sentence/<int:sentence_id>', methods=['GET', 'POST'])
@login_required
def delete_sentence(sentence_id):
    sentence = Sentence.query.get_or_404(sentence_id)  # Find the sentence by ID
    db.session.delete(sentence)  # Delete the sentence
    db.session.commit()  # Commit the change
    flash(f'Sentence has been deleted!', 'success')
    return redirect(url_for('admin_bp.view_sentences'))  # Redirect to the view sentences page





# Edit Sentence Route
@admin_bp.route('/edit_sentence/<int:sentence_id>', methods=['GET', 'POST'])
@login_required
def edit_sentence(sentence_id):
    sentence = Sentence.query.get_or_404(sentence_id)
    form = AddSentenceForm()

    # Populate category choices from the Category model
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if request.method == 'POST':
        selected_category_id = form.category.data

        # Dynamically populate section choices based on the selected category
        form.section.choices = [(s.id, s.name) for s in Section.query.filter_by(category_id=selected_category_id).all()]

        if form.validate_on_submit():
            sentence.english_sentence = form.english_sentence.data
            sentence.spanish_sentence = form.spanish_sentence.data
            sentence.explanation_english = form.explanation_english.data
            sentence.explanation_spanish = form.explanation_spanish.data
            sentence.category_id = form.category.data
            sentence.section_id = form.section.data if form.section.data else None  # Ensure section_id is not None
            sentence.image_path = form.image_path.data

            db.session.commit()
            flash('Sentence updated successfully!', 'success')
            return redirect(url_for('admin_bp.view_sentences'))

    # Pre-populate the form with the sentence's current data
    form.english_sentence.data = sentence.english_sentence
    form.spanish_sentence.data = sentence.spanish_sentence
    form.explanation_english.data = sentence.explanation_english
    form.explanation_spanish.data = sentence.explanation_spanish
    form.category.data = sentence.category_id
    form.section.data = sentence.section_id
    form.image_path.data = sentence.image_path

    # Populate sections based on the sentence's category
    form.section.choices = [(s.id, s.name) for s in Section.query.filter_by(category_id=sentence.category_id).all()]

    return render_template('admin/edit_sentence.html', form=form, sentence=sentence)
