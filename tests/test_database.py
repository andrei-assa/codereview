import datetime

import pytest
from codereview.database import Database, initialize_database
import os

# Fixture to set up and tear down a test database
@pytest.fixture
def test_database():

    test_db_path = 'test_database.db'
    initialize_database(test_db_path)

    # Initialize test database
    db = Database(test_db_path)
    yield db
    # Teardown test database
    os.remove(test_db_path)

def test_insert_and_get_run(test_database):
    run_id = test_database.insert_run('2023-01-01 10:00:00', 'file1.py, file2.py')
    assert run_id is not None

    run = test_database.get_run(run_id)
    assert run is not None
    assert run['timestamp'] == datetime.datetime.strptime('2023-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
    assert run['files_analyzed'] == ['file1.py', 'file2.py']


def test_insert_and_get_snapshot(test_database):
    snapshot = test_database.insert_snapshot(snapshot_id='snapshot123', timestamp='2023-01-01 11:00:00', summary='Snapshot summary', module_id=1)
    assert snapshot is not None

    snapshot_id = snapshot.snapshot_id
    snapshot = test_database.get_snapshot_by_snapshot_id(snapshot_id)
    assert snapshot is not None
    assert snapshot['snapshot_id'] == 'snapshot123'
    assert snapshot['summary'] == 'Snapshot summary'
    assert snapshot['module_id'] == 1

def test_insert_and_get_message(test_database):
    message_id = test_database.insert_message('2023-01-01 12:00:00', 'This is a test message.')
    assert message_id is not None

    message = test_database.get_message(message_id)
    assert message is not None
    assert message['content'] == 'This is a test message.'

def test_insert_and_get_review(test_database):
    review_id = test_database.insert_review(timestamp='2023-01-01 13:00:00', content='This is a test review.')
    assert review_id is not None

    review = test_database.get_review(review_id)
    assert review is not None
    assert review['content'] == 'This is a test review.'
