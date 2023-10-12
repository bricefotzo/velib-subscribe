import requests

BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets"


def get_dataset_info(dataset_id, **kwargs):
    """

    Args:
        dataset_id:
        **kwargs:

    Returns:

    """
    url = f"{BASE_URL}/{dataset_id}/records?"
    response = requests.get(url, params=kwargs)
    if response.status_code == 200:
        return response.json().get("results")
    else:
        print(f"Erreur: {response.status_code}")
        return None
