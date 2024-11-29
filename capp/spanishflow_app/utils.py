from .. import db
from ..models import Sentence, UserProgress, Section
from flask_login import current_user

def calculate_section_progress(section, user):
    total_sentences = Sentence.query.filter_by(section_id=section.id).count()
    if total_sentences == 0:
        return 0
    
    learned_sentences = db.session.query(UserProgress).join(Sentence).filter(
        UserProgress.user_id == user.id,
        Sentence.section_id == section.id,
        UserProgress.learned == True
    ).count()

    return (learned_sentences / total_sentences) * 100

def calculate_category_progress(category, user):
    sections = Section.query.filter_by(category_id=category.id).all()
    total_sections = len(sections)
    if total_sections == 0:
        return 0

    fully_learned_sections = sum(1 for section in sections if calculate_section_progress(section, user) == 100)

    return (fully_learned_sections / total_sections) * 100

def update_user_progress(sentence_id, learned=False):
    """
    Updates the user's progress for a sentence.
    - Marks the sentence as viewed.
    - Optionally marks the sentence as learned if `learned=True`.
    """
    if sentence_id is None:
        raise ValueError("Sentence ID cannot be None")

    try:
        # Try to find an existing progress entry for the sentence and user
        user_progress = UserProgress.query.filter_by(user_id=current_user.id, sentence_id=sentence_id).first()
        
        # If no existing progress, create a new one
        if user_progress:
            if learned:
                user_progress.learned = True
        else:
            # Create new UserProgress entry
            user_progress = UserProgress(
                user_id=current_user.id,
                sentence_id=sentence_id,
                learned=learned
            )
            db.session.add(user_progress)

        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback transaction if an error occurs
        raise RuntimeError(f"Error updating user progress: {str(e)}")

