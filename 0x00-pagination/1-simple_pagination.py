#!/usr/bin/env python3
"""
Simple Pagination
"""

import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    return a tuple of size two containing a start index and an
    end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters.
    :param page:
    :param page_size:
    :return:
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a specific page of data from the dataset.

        Args:
        page(int): The page number to retrieve (default: 1)
        page_size(int): The number of items per page (default:10)

        Returns:
        List[List]: A list of rorws for the specified page
        """
        # Verify that both page and page_size are integers greater than 0
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        # Find the correct start and end indexes for the current page
        start_index, end_index = index_range(page, page_size)
        # Retrieve the dataset
        dataset = self.dataset()
        # Check if the end_index is greater than the length of dataset
        # Return an empty list if it is
        if end_index > len(dataset):
            return []
        # Return the appropriate page of the dataset
        return dataset[start_index:end_index]
