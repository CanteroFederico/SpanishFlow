from flask import render_template, Blueprint, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from capp import db
from capp.models import Sentence, Category, Section, UserProgress
from .utils import calculate_section_progress, calculate_category_progress, update_user_progress
from sqlalchemy.sql.expression import func

# Define the Blueprint
spanishflow_app = Blueprint('spanishflow_app', __name__)

# Home route
@spanishflow_app.route('/spanishflow_app')
@login_required
def spanishflow_app_home():
    return render_template(
        '/app/spanishflow_app.html',
        title='SpanishFlow App',
        username=current_user.username
    )


# View a category's sections
@spanishflow_app.route('/section_app')
@login_required
def section_app():
    category_name = request.args.get('category')
    if not category_name:
        flash("No category selected. Redirecting to home.")
        return redirect(url_for('spanishflow_app.spanishflow_app_home'))

    category = Category.query.filter_by(name=category_name).first_or_404()
    sections = Section.query.filter_by(category_id=category.id).all()

    if not sections:
        flash("No sections found for this category.")
        return redirect(url_for('spanishflow_app.spanishflow_app_home'))

    total_sentences = Sentence.query.filter_by(category_id=category.id).count()
    learned_sentences = {
        progress.sentence_id
        for progress in UserProgress.query.filter_by(user_id=current_user.id).filter_by(learned=True)
    }

    learned_in_category = len([s for s in Sentence.query.filter_by(category_id=category.id) if s.id in learned_sentences])
    progress_percentage_category = (learned_in_category / total_sentences * 100) if total_sentences else 0

    sections_data = []
    for section in sections:
        total_section_sentences = Sentence.query.filter_by(section_id=section.id).count()
        learned_in_section = len([s for s in Sentence.query.filter_by(section_id=section.id) if s.id in learned_sentences])
        section_progress_percentage = (learned_in_section / total_section_sentences * 100) if total_section_sentences else 0
        sections_data.append({
            'section': section,
            'icon': section.icon,  # Add the icon here
            'progress_percentage': section_progress_percentage,
            'progress_learned': learned_in_section,
            'progress_total': total_section_sentences
        })

    return render_template(
        'app/section_app.html',
        title=f'Section - {category.name}',
        username=current_user.username,
        category=category,
        section=section,
        sections_data=sections_data,
        progress_percentage_category=progress_percentage_category
    )

@spanishflow_app.route('/carbon_app/<int:section_id>/<int:sentence_id>')
@login_required
def carbon_app(section_id, sentence_id):
    # Fetch all sentences for the section, order them randomly
    sentences = Sentence.query.filter_by(section_id=section_id).order_by(func.random()).all()

    # Find the sentence with the given sentence_id in the randomized list
    sentence = next((s for s in sentences if s.id == sentence_id), None)

    if not sentence:
        flash("Sentence not found.", "info")
        return redirect(url_for('spanishflow_app.section_app', section_id=section_id))

    # Ensure that sentence_id is passed to the update function
    update_user_progress(sentence.id)  # Make sure sentence.id is passed here.

    # Calculate section and category progress
    section_progress = calculate_section_progress(sentence.section, current_user)
    category_progress = calculate_category_progress(sentence.category, current_user)

    return render_template(
        '/app/carbon_app.html',
        title=f"{sentence.category.name} | {sentence.section.name}",
        sentence=sentence,
        section_progress=section_progress,
        category_progress=category_progress,
        username=current_user.username,
        sentences=sentences,  # Pass the list of randomized sentences to the template
        image_path=sentence.image_path  # Pass the image path to the template
    )




@spanishflow_app.route('/sentence/<int:sentence_id>/learned', methods=['POST'])
@login_required
def mark_sentence_as_learned(sentence_id):
    try:
        # Mark the sentence as learned by calling the update function
        update_user_progress(sentence_id, learned=True)
        return jsonify({"status": "success", "message": "Sentence marked as learned."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500



# Next sentence (randomized order)
@spanishflow_app.route('/next_sentence/<int:section_id>/<int:sentence_id>')
@login_required
def next_sentence(section_id, sentence_id):
    # Fetch all sentences for the section, order them randomly
    sentences = Sentence.query.filter_by(section_id=section_id).order_by(func.random()).all()
    
    # Find the index of the current sentence
    sentence_idx = next((i for i, s in enumerate(sentences) if s.id == sentence_id), None)
    
    if sentence_idx is None or sentence_idx == len(sentences) - 1:
        return redirect(url_for('spanishflow_app.carbon_app', section_id=section_id, sentence_id=sentence_id))

    # Get the next sentence in the randomized list
    next_sentence = sentences[sentence_idx + 1]
    return redirect(url_for('spanishflow_app.carbon_app', section_id=section_id, sentence_id=next_sentence.id))

# Previous sentence (randomized order)
@spanishflow_app.route('/previous_sentence/<int:section_id>/<int:sentence_id>')
@login_required
def previous_sentence(section_id, sentence_id):
    # Fetch all sentences for the section, order them randomly
    sentences = Sentence.query.filter_by(section_id=section_id).order_by(func.random()).all()
    
    # Find the index of the current sentence
    sentence_idx = next((i for i, s in enumerate(sentences) if s.id == sentence_id), None)
    
    if sentence_idx is None or sentence_idx == 0:
        return redirect(url_for('spanishflow_app.carbon_app', section_id=section_id, sentence_id=sentence_id))

    # Get the previous sentence in the randomized list
    previous_sentence = sentences[sentence_idx - 1]
    return redirect(url_for('spanishflow_app.carbon_app', section_id=section_id, sentence_id=previous_sentence.id))


# Shuffle a random sentence
@spanishflow_app.route('/shuffle_sentence/<int:section_id>')
@login_required
def shuffle_sentence(section_id):
    sentence = Sentence.query.filter_by(section_id=section_id).order_by(func.random()).first()
    if not sentence:
        flash("No sentences found for this section.", "info")
        return redirect(url_for('spanishflow_app.section_app', section_id=section_id))

    update_user_progress(sentence.id)
    return redirect(url_for('spanishflow_app.carbon_app', section_id=section_id, sentence_id=sentence.id))



# Exit the carbon app
@spanishflow_app.route('/exit_carbon_app/<int:section_id>/<int:sentence_id>')
@login_required
def exit_carbon_app(section_id, sentence_id):
    update_user_progress(sentence_id)  # Ensure progress is updated before exit
    return redirect(url_for('spanishflow_app.section_app', section_id=section_id))


# Clear learned status for all sentences in a category
@spanishflow_app.route('/clear_learned_status/<int:category_id>', methods=['POST'])
@login_required
def clear_learned_status(category_id):
    # Your logic to clear learned status for the category
    try:
        # Find all sentences in the category
        sentences = Sentence.query.filter_by(category_id=category_id).all()

        # Reset learned status for all sentences
        for sentence in sentences:
            progress = UserProgress.query.filter_by(user_id=current_user.id, sentence_id=sentence.id).first()
            if progress:
                progress.learned = False

        db.session.commit()
        flash("Learned status cleared for all sentences in this category.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "error")

    return redirect(url_for('spanishflow_app.section_app', category=Category.query.get(category_id).name))