import unittest.mock

from contacts import app


class EntryPointTests(unittest.TestCase):
    def test_that_entry_point_calls_run(self):
        with unittest.mock.patch('contacts.app.sprockets.http.run') as run:
            app.entry_point()
            run.assert_called_once_with(app.Application,
                                        log_config=unittest.mock.ANY)
