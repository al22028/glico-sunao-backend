# Standard Library
from datetime import datetime
from unittest.mock import MagicMock, patch

# Third Party Library
import pytest
from database.base import Hba1cModel
from repositories.hba1c_repository import Hba1cRepository
from schemas.hba1c import Hba1cCreateRequestSchema, Hba1cSchema, Hba1cUpdateRequestSchema

test_user_id = "test_user_id"
test_id = "test_id"
test_record_time = datetime.now()
test_data = Hba1cSchema(
    id="1qazxxsw23edc",
    user_id=test_user_id,
    value=4.0,
    event_timing="食後",
    record_time=test_record_time,
    sunao_food="パスタ",
    is_deleted=False,
    created_at="2022-01-01T00:00:00.000000+00:00",
    updated_at="2022-01-01T00:00:00.000000+00:00",
)
test_data_create = Hba1cCreateRequestSchema(
    user_id=test_user_id,
    value=5.5,
    event_timing="食後",
    record_time=test_record_time,
    sunao_food=None,
)
test_data_update = Hba1cUpdateRequestSchema(
    value=6.0, event_timing="空腹時", record_time=test_record_time, sunao_food="パスタ"
)


@pytest.fixture
def hba1c_repository() -> Hba1cRepository:
    return Hba1cRepository()


@patch("database.base.Hba1cModel.scan")
def test_find_all(mock_scan: MagicMock, hba1c_repository: Hba1cRepository) -> None:
    mock_scan.return_value = [
        Hba1cModel(
            id=test_data.id,
            user_id=test_data.user_id,
            value=test_data.value,
            event_timing=test_data.event_timing,
            record_time=test_data.record_time,
            sunao_food=None,
        )
    ]
    items = hba1c_repository.find_all()
    assert len(items) == 1
    assert items[0].value == 4.0
    assert items[0].event_timing == "食後"
    assert items[0].sunao_food is None


@patch("database.base.Hba1cModel.save")
def test_create_one(
    mock_save: MagicMock,
    hba1c_repository: Hba1cRepository,
) -> None:
    item = hba1c_repository.create_one(test_data_create)
    mock_save.assert_called_once()
    assert item is not None
    assert item.value == test_data_create.value
    assert item.event_timing == test_data_create.event_timing
    assert item.record_time == test_data_create.record_time
    assert item.user_id == test_data_create.user_id


@patch("database.base.Hba1cModel.scan")
def test_is_exist(mock_scan: MagicMock, hba1c_repository: Hba1cRepository) -> None:
    scan_iterator_mock = MagicMock()
    scan_iterator_mock.next.return_value = Hba1cModel(test_data)
    mock_scan.return_value = scan_iterator_mock

    assert hba1c_repository.is_exist(test_id) is True

    scan_iterator_mock.next.side_effect = StopIteration
    mock_scan.return_value = scan_iterator_mock
    assert hba1c_repository.is_exist(test_id) is False


@patch("database.base.Hba1cModel.scan")
def test_find_one(mock_scan: MagicMock, hba1c_repository: Hba1cRepository) -> None:
    scan_iterator_mock = MagicMock()
    scan_iterator_mock.next.return_value = Hba1cModel(**test_data.dict())
    mock_scan.return_value = scan_iterator_mock

    item = hba1c_repository.find_one(test_id)

    assert item is not None
    assert item.id == test_data.id
    assert item.user_id == test_data.user_id
    assert item.value == test_data.value
    assert item.event_timing == test_data.event_timing
    assert item.record_time == test_data.record_time
    assert item.sunao_food == test_data.sunao_food


@patch("database.base.Hba1cModel.save")
@patch("database.base.Hba1cModel.delete")
@patch("database.base.Hba1cModel.scan")
def test_update_one(
    mock_scan: MagicMock,
    mock_delete: MagicMock,
    mock_save: MagicMock,
    hba1c_repository: Hba1cRepository,
) -> None:
    scan_iterator_mock = MagicMock()
    scan_iterator_mock.next.return_value = Hba1cModel(test_data)
    mock_scan.return_value = scan_iterator_mock

    new_item = hba1c_repository.update_one(test_data.id, test_data_update)

    mock_delete.assert_called_once()
    mock_save.assert_called()

    assert new_item is not None
    assert new_item.value == test_data_update.value
    assert new_item.event_timing == test_data_update.event_timing
    assert new_item.record_time == test_data_update.record_time
    assert new_item.sunao_food == test_data_update.sunao_food


@patch("database.base.Hba1cModel.scan")
@patch("database.base.Hba1cModel.save")
def test_delete_one(
    mock_save: MagicMock, mock_scan: MagicMock, hba1c_repository: Hba1cRepository
) -> None:
    scan_iterator_mock = MagicMock()
    scan_iterator_mock.next.return_value = Hba1cModel(**test_data.dict())
    mock_scan.return_value = scan_iterator_mock

    item = hba1c_repository.delete_one(test_id)

    mock_save.assert_called_once()
    assert item is not None
    assert item.id == test_data.id
    assert item.user_id == test_data.user_id
    assert item.value == test_data.value
    assert item.event_timing == test_data.event_timing
    assert item.record_time == test_data.record_time
    assert item.sunao_food == test_data.sunao_food
    assert item.is_deleted is True


@patch("database.base.Hba1cModel.query")
def test_find_many_by_user_id(mock_query: MagicMock, hba1c_repository: Hba1cRepository) -> None:
    test_data_active = Hba1cModel(test_data)
    test_data_deleted = Hba1cModel(test_data)
    test_data_deleted.is_deleted = True

    mock_query.return_value = [test_data_active, test_data_deleted]

    items = hba1c_repository.find_many_by_user_id(test_user_id, datetime.now(), datetime.now())

    assert len(items) == 1
    assert not items[0].is_deleted
