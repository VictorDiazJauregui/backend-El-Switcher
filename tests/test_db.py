import pytest

from sqlalchemy.orm import Session

from app.db.db import get_db, Player


# Skipped by default to not trigger prod database operations
@pytest.mark.skip(reason="Contextual test")
def test_get_db():
    """Test the real get_db function with a live database session"""
    # Use get_db to get a session
    db_gen = get_db()
    db = next(db_gen)  # Get the session object

    # Check if the session is a valid Session object
    assert isinstance(db, Session)

    # Perform some database operations to check session works
    # Assuming Player is a model in your app you can insert into the database
    new_record = Player(name="Test Player")
    db.add(new_record)
    db.commit()

    # Retrieve the same record to verify session functionality
    retrieved_record = (
        db.query(Player).filter(Player.name == "Test Player").first()
    )
    assert retrieved_record is not None
    assert retrieved_record.name == "Test Player"

    # Test that the session gets closed properly
    # Clean up the generator
    try:
        next(
            db_gen
        )  # This should raise StopIteration since db is closed after use
    except StopIteration:
        pass  # Expected behavior, session closed successfully

    # Clean up
    # Now delete the test record in players
    db.query(Player).filter(Player.id == retrieved_record.id).delete()
    db.commit()
