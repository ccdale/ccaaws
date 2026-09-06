from unittest.mock import MagicMock

from ccaaws.session import paginate


def testPaginateYieldsItemsAcrossPages() -> None:
    mockClient = MagicMock()
    mockPaginator = mockClient.get_paginator.return_value
    mockPaginator.paginate.return_value = [
        {"Items": [1, 2]},
        {"Items": [3]},
    ]

    result = list(paginate(mockClient, "list_things", "Items", Bucket="mybucket"))

    mockClient.get_paginator.assert_called_once_with("list_things")
    mockPaginator.paginate.assert_called_once_with(Bucket="mybucket")
    assert result == [1, 2, 3]


def testPaginateSkipsPagesMissingResultKey() -> None:
    mockClient = MagicMock()
    mockClient.get_paginator.return_value.paginate.return_value = [{}, {"Items": [1]}]

    result = list(paginate(mockClient, "list_things", "Items"))

    assert result == [1]
