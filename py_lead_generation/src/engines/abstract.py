from abc import ABC
#have to work on this code which uses yelp.com to extract the info.This will not affect the main code for extracting the code from Google Maps

class AbstractEngine(ABC):
    BASE_URL = ''
    FIELD_NAMES = []
    FILENAME = 'leads.csv'
    async def _get_search_results_urls(self, *args, **kwargs) -> list[str]:
        pass

    def _parse_data_with_soup(self, html: str) -> list[dict]:
        pass
