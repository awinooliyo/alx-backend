#!/usr/bin/env python3
"""
Simple Pagination
"""

import csv
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Return a tuple of size two containing a start index and an
    end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters.

    :param page: The page number
    :param page_size: The number of items per page
    :return: A tuple (start_index, end_index)
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
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
            page (int): The page number to retrieve (default: 1)
            page_size (int): The number of items per page (default: 10)

        Returns:
            List[List]: A list of rows for the specified page
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Retrieves a specific page of the dataset of popular baby names
        along with pagination metadata.

        Args:
            page (int, optional): The number of the page to retrieve.
            Defaults to 1.
            page_size (int, optional): The number of items per page.
            Defaults to 10.

        Returns:
            Dict: A dictionary containing the following key-value pairs:
                  page_size: The length of the returned dataset page
                  page: The current page number
                  data: The dataset page (equivalent to
                  return from previous task)
                  next_page: Number of the next page,
                  None if no next page
                  prev_page: Number of the previous page,
                  None if no previous page
                  total_pages: The total number of pages in the
                  dataset as an integer

        Raises:
            AssertionError: If either of the input arguments is not
            an integer greater than 0.
        """
        data = self.get_page(page, page_size)

        if not data:
            return {
                'page_size': 0,
                'page': page,
                'data': [],
                'next_page': None,
                'prev_page': None,
                'total_pages': 0
            }

        dataset_len = len(self.dataset())
        total_pages = (dataset_len + page_size - 1) // page_size

        next_page = page + 1 if (page * page_size) < dataset_len else None
        prev_page = page - 1 if page > 1 else None

        return {
            'page_size': page_size,
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
