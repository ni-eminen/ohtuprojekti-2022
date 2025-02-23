import unittest
from database_connection import get_database_connection
from repositories import ReferenceRepository
from entities import Reference


class ReferenceRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reference_repository = ReferenceRepository(
            get_database_connection())
        self.reference_repository.delete_all()
        self.mock_reference = Reference(
            reference_id="1",
            authors=["author1", "author2"],
            title="Test",
            year=2020,
            publisher="Test"
        )
        self.reference_repository.post(self.mock_reference)

    def test_id_exists(self) -> None:
        self.assertTrue(self.reference_repository.id_exists("1"))

    def test_id_does_not_exist(self) -> None:
        self.assertFalse(self.reference_repository.id_exists("2"))

    def test_get_all(self) -> None:
        references = self.reference_repository.get_all()
        references = references[0]["reference_id"]
        self.assertEqual(len(references), 1)
        self.assertEqual(
            references, self.mock_reference.to_dict()["reference_id"])

    def test_get_all_empty(self) -> None:
        self.reference_repository.delete("1")
        self.assertEqual(self.reference_repository.get_all(), [])

    def test_post(self) -> None:
        self.reference_repository.delete("1")
        self.reference_repository.post(self.mock_reference)
        references = self.reference_repository.get_all()
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0]["reference_id"],
                         self.mock_reference.to_dict()["reference_id"])

    def test_post_duplicate_error(self) -> None:
        with self.assertRaises(Exception):
            self.reference_repository.post(self.mock_reference)

    def test_put(self) -> None:
        self.reference_repository.put(self.mock_reference)
        references = self.reference_repository.get_all()
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0]["reference_id"],
                         self.mock_reference.to_dict()["reference_id"])

    def test_put_non_existing(self) -> None:
        self.reference_repository.delete("1")
        self.reference_repository.put(self.mock_reference)
        self.assertEqual(self.reference_repository.get_all(), [])

    def test_delete(self) -> None:
        self.reference_repository.delete("1")
        self.assertEqual(self.reference_repository.get_all(), [])

    def test_delete_non_existing(self) -> None:
        self.reference_repository.delete("2")
        references = self.reference_repository.get_all()
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0]["reference_id"],
                         self.mock_reference.to_dict()["reference_id"])

    def test_delete_all(self) -> None:
        self.reference_repository.delete_all()
        self.assertEqual(self.reference_repository.get_all(), [])
