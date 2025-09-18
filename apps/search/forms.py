from oscar.apps.search.forms import SearchForm


class BrowseBrandForm(SearchForm):
    """
    Variant of SearchForm that returns all products (instead of none) if no
    query is specified.
    """

    def no_query_found(self):
        """
        Return Queryset of all the results.
        """
        return self.searchqueryset