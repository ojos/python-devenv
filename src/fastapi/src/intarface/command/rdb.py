from typing import List, Optional

from usecase.interactor import ITableInteractor


class RdbCommand(object):
    def __init__(
        self,
        create_table_interactor: ITableInteractor,
        drop_table_interactor: ITableInteractor,
    ):
        self._create_table_interactor: ITableInteractor = create_table_interactor
        self._drop_table_interactor: ITableInteractor = drop_table_interactor

    @property
    def managed_tables(self) -> List[str]:
        return self._create_table_interactor.managed_tables

    def create_tables(
        self, table_names: Optional[List[str]] = None, *args, **kwargs
    ) -> None:
        self._create_table_interactor.execute(table_names)

    def drop_tables(
        self, table_names: Optional[List[str]] = None, *args, **kwargs
    ) -> None:
        self._drop_table_interactor.execute(table_names)

    def reset_tables(
        self, table_names: Optional[List[str]] = None, *args, **kwargs
    ) -> None:
        self.drop_tables(table_names)
        self.create_tables(table_names)
