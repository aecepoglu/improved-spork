from behave import given, when, then
from assertpy import assert_that as ensure
from json import loads as load_json
from jsonschema import validate as validate_jsonschema
from jsonpath_rw import parse as parse_jsonpath


def make_request(fun, context, *args, **kwargs):
    context.response = fun(*args, **kwargs)


def expand_variables(context, text):
    for key, val in context.variables.items():
        text = text.replace("$<{}>".format(key), val)

    return text


def parse_json_or_cry(data, msg):
    try:
        return load_json(data)
    except ValueError:
        print(data)
        raise AssertionError(msg + ". " + str(data))


@given(u"the server is setup")
def setup(context):
    assert context.client


@given(u"I made a GET request to \"{url}\"")
@when(u"I make a GET request to \"{url}\"")
def make_get_request(context, url):
    make_request(context.client.get, context, url)


@when(u"I made a POST request to \"{url}\"")
@when(u"I make a POST request to \"{url}\"")
def make_post_request(context, url):
    make_request(context.client.post, context, url)


@given(u"I made a GET request to \"{url}\" expanding variables")
@when(u"I make a GET request to \"{url}\" expanding variables")
def make_get_request_with_vars(context, url):
    make_request(context.client.get, context, expand_variables(context, url))


@given(u"I made a POST request to \"{url}\" expanding variables")
@when(u"I make a POST request to \"{url}\" expanding variables")
def make_get_request_with_vars(context, url):
    make_request(context.client.post, context, expand_variables(context, url))


@given(u"I saved the response at path \"{path}\" to variable \"{name}\"")
def save_variable(context, path, name):
    data = parse_json_or_cry(context.response.data, "resp wasn't json")
    val = parse_jsonpath(path).find(data)
    ensure(val).is_length(1)

    if "variables" not in context:
        context.variables = {}

    context.variables[name] = val[0].value


@then(u"the response status should be {status_code:d}")
def check_resp_status(context, status_code):
    ensure(context.response.status_code).is_type_of(int)
    ensure(status_code).is_type_of(int)
    ensure(context.response.status_code).is_equal_to(status_code)


@then(u"the response text should be \"{text}\"")
def check_resp_equals(context, text):
    ensure(str(context.response.data, "utf-8")).is_equal_to(text)


@then(u"the response json should be")
def check_resp_json_equals(context):
    ensure(str(context.response.data, "utf-8")).is_equal_to(
        parse_json_or_cry(context.text, "resp wasn't json"))


@then(u"the response at path \"{path}\" should be {value:g}")
@then(u"the response at path \"{path}\" should be \"{value}\"")
def check_response_jsonpath(context, path, value):
    data = parse_json_or_cry(context.response.data, "resp wasn't json")
    matches = parse_jsonpath(path).find(data)

    ensure(matches).is_length(1)
    ensure(matches[0].value).is_equal_to(value)


@then(u"the response at path \"{path}\" should have {count:d} items")
def check_array_len_jsonpath(context, path, count):
    data = parse_json_or_cry(context.response.data, "resp wasn't json")
    matches = parse_jsonpath(path).find(data)

    ensure(matches).is_length(1)
    ensure(matches[0].value).is_length(count)


@then(u"the response json schema should be")
def check_jsonschema(context):
    validate_jsonschema(
        instance=parse_json_or_cry(context.response.data, "resp wasn't json"),
        schema=parse_json_or_cry(context.text, "schema isn't json"))
