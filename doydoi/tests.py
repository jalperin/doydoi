import unittest
import transaction

from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound

from .models import DBSession


class TestNewDoiQuery(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            Query,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_missing_data_returns_400(self):
        from .views import new_doi_query
        request = testing.DummyRequest()

        self.assertRaises(HTTPBadRequest, lambda: new_doi_query(request))

    def test_new_doi_query(self):
        from .views import new_doi_query
        request = testing.DummyRequest()
        request.POST = {'callback': 'http://foo.com/bar?id=1234',
                        'data': '{"foo": "baz"}'}

        self.assertIsInstance(new_doi_query(request), HTTPFound)
        import pdb; pdb.set_trace()
        self.assertEquals(DBSession.query(Query).one())

