from behave import given, when, then
from assertpy import assert_that as ensure


def make_request(fun, context, *args, **kwargs):
    context.response = fun(*args, **kwargs)


@given(u"the server is setup")
def setup(context):
    assert context.client


@when(u"I make a GET request to \"{url}\"")
def make_get_request(context, url):
    make_request(context.client.get, context, url)


@when(u"I make a POST request to \"{url}\"")
def make_post_request(context, url):
    make_request(context.client.post, context, url)


@then(u"the response status should be {status_code:d}")
def check_resp_status(context, status_code):
    ensure(context.response.status_code).is_type_of(int)
    ensure(status_code).is_type_of(int)
    ensure(context.response.status_code).is_equal_to(status_code)


@then(u"the response should equal \"{text}\"")
def check_resp_equals(context, text):
    ensure(str(context.response.data, "utf-8")).is_equal_to(text)

