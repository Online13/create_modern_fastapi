import grimp
from tests.utils import format_graph_error


def build_graph():
    return grimp.build_graph("src", cache_dir=None)


def assert_no_dependency(importer: str, imported: str):
    graph = build_graph()
    if graph.chain_exists(importer, imported, as_packages=True):
        chain = graph.find_shortest_chain(importer, imported, as_packages=True)
        raise AssertionError(format_graph_error(importer, imported, chain, graph))


# Test on domain


def test_domain_does_not_depend_on_application():
    assert_no_dependency("src.domain", imported="src.application")


def test_domain_does_not_depend_on_infrastructure():
    assert_no_dependency("src.domain", imported="src.infrastructure")


def test_domain_does_not_depend_on_presentation():
    assert_no_dependency("src.domain", imported="src.presentation")


# Test on application


def test_application_does_not_depend_on_infrastructure():
    assert_no_dependency("src.application", imported="src.infrastructure")


def test_application_does_not_depend_on_presentation():
    assert_no_dependency("src.application", imported="src.presentation")


# Test on infrastructure


def test_infrastructure_does_not_depend_on_presentation():
    assert_no_dependency("src.infrastructure", imported="src.presentation")
