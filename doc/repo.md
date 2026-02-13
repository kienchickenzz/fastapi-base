
```python
class Repository(ABC, Generic[T]):
      # Core
      __init__(engine, db_model)
      _get_session() → AsyncSession

      # CRUD
      get_all() → Sequence[T]
      get_one(id) → Optional[T]
      get_multiple(skip, limit) → tuple[Sequence[T], int]
      create(values) → T
      update(id, values) → Optional[T]

      # Raw SQL
      fetch_sql(sql, params) → Sequence[RowMapping]
      execute_sql(sql, params) → int
```