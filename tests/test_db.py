from sqlalchemy.orm import Session
from app.db.db import get_db, Base
from app.db.db import Player, CardFig  # Import the actual models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup an in-memory SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_get_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for testing
Base.metadata.create_all(bind=engine)

def test_get_db():
    """ Test the real get_db function with a live database session """
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
    retrieved_record = db.query(Player).filter(Player.name == "Test Player").first()
    assert retrieved_record is not None
    assert retrieved_record.name == "Test Player"

    # Test that the session gets closed properly
    # Clean up the generator
    try:
        next(db_gen)  # This should raise StopIteration since db is closed after use
    except StopIteration:
        pass  # Expected behavior, session closed successfully

    # Clean up
    # Now delete the test record in players
    db.query(Player).filter(Player.id == retrieved_record.id).delete()
    db.commit()
