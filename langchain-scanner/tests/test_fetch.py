from unittest.mock import MagicMock, patch

from scanner.nodes.fetch import _parse_api_results, fetch_listings, load_fixture_listings


def test_load_fixture_listings_shape():
    listings = load_fixture_listings()
    assert len(listings) >= 1
    first = listings[0]
    assert "listing_id" in first
    assert "zip" in first
    assert "listing_price" in first


def test_parse_api_results():
    api_data = {
        "data": {
            "home_search": {
                "results": [
                    {
                        "property_id": "prop-1",
                        "list_price": 450000,
                        "description": {"beds": 3, "baths": 2, "sqft": 1500},
                        "location": {
                            "address": {
                                "line": "123 Main St",
                                "city": "Phoenix",
                                "state_code": "AZ",
                                "postal_code": "85018",
                            }
                        },
                    }
                ]
            }
        }
    }
    listings = _parse_api_results(api_data)
    assert len(listings) == 1
    assert listings[0]["listing_id"] == "prop-1"
    assert listings[0]["zip"] == 85018
    assert listings[0]["sqft"] == 1500


@patch("scanner.nodes.fetch.httpx.post")
def test_fetch_listings_uses_api(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "home_search": {
                "results": [
                    {
                        "property_id": "api-1",
                        "list_price": 400000,
                        "description": {"beds": 2, "baths": 1, "sqft": 1000},
                        "location": {
                            "address": {
                                "line": "1 Test Ave",
                                "city": "Phoenix",
                                "state_code": "AZ",
                                "postal_code": "85004",
                            }
                        },
                    }
                ]
            }
        }
    }
    mock_post.return_value = mock_response

    result = fetch_listings({"location": "Phoenix, AZ", "max_results": 10})
    assert len(result["raw_listings"]) == 1
    assert result["raw_listings"][0]["listing_id"] == "api-1"
    mock_post.assert_called_once()


@patch("scanner.nodes.fetch.httpx.post", side_effect=Exception("network error"))
def test_fetch_listings_falls_back_to_fixture(mock_post):
    result = fetch_listings({"location": "Phoenix, AZ", "max_results": 5})
    assert len(result["raw_listings"]) >= 1
    mock_post.assert_called_once()
