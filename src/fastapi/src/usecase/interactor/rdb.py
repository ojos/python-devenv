from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional, TypedDict

from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.sql.schema import Table


class KeyValueTable(TypedDict):
    key: str
    value: Optional[Table]


class SqlAlchemyInteractor(object):
    def __init__(self, engine: Engine, base: DeclarativeMeta, *args, **kwargs):
        self._engine: Engine = engine
        self._base: DeclarativeMeta = base


class ITableInteractor(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, table_names: Optional[List[str]] = None, *args, **kwargs) -> Any:
        raise NotImplementedError(
            "Not Implemented {}: {}".format(self.__class__.__name__, "execute")
        )


class TableInteractor(SqlAlchemyInteractor):
    @property
    def managed_tables(self) -> List[str]:
        return list(self._base.metadata.tables.keys())

    def _contains_foreign_key(self, table: Table) -> int:
        n: int = 0
        for clm in table.columns:
            n += len(clm.foreign_keys)
        return n

    def _find_tables(
        self, table_names: Optional[List[str]], reflect: bool, sort_reverse: bool
    ) -> List[KeyValueTable]:
        _table_names = self.managed_tables if table_names is None else table_names
        _metadata: MetaData
        if reflect:
            _metadata = MetaData()
            _metadata.reflect(self._engine)
        else:
            _metadata = self._base.metadata
        tables = [
            KeyValueTable(key=tn, value=_metadata.tables.get(tn)) for tn in _table_names
        ]
        return sorted(
            tables,
            key=lambda x: self._contains_foreign_key(x["value"]),
            reverse=sort_reverse,
        )


class CreateTableInteractor(ITableInteractor, TableInteractor):
    def execute(self, table_names: Optional[List[str]] = None, *args, **kwargs) -> Any:
        tables: List[KeyValueTable] = self._find_tables(
            table_names, reflect=False, sort_reverse=False
        )
        for kv_table in tables:
            if kv_table["value"] is None:
                print("Not Found Table: {}".format(kv_table["key"]))
            else:
                self._base.metadata.create_all(
                    bind=self._engine,
                    tables=[kv_table["value"]],
                    checkfirst=True,
                )
                print("Create Table: {}".format(kv_table["key"]))


class DropTableInteractor(ITableInteractor, TableInteractor):
    def execute(self, table_names: Optional[List[str]] = None, *args, **kwargs) -> Any:
        tables: List[KeyValueTable] = self._find_tables(
            table_names, reflect=False, sort_reverse=True
        )
        for kv_table in tables:
            if kv_table["value"] is None:
                print("Not Found Table: {}".format(kv_table["key"]))
            else:
                self._base.metadata.drop_all(
                    bind=self._engine,
                    tables=[kv_table["value"]],
                    checkfirst=True,
                )
                print("Drop Table: {}".format(kv_table["key"]))
